"""Eval runner for executing test cases against agents."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from rich.console import Console
from rich.table import Table

from .agent import AgentFactory, BaseAgent
from .graders import BaseGrader, GraderFactory, ExactMatchGrader
from .schemas import AgentConfig, EvalResult, EvalRun, RunStatus, TestCase


class EvalRunner:
    """Runs evaluation suites against agents."""

    def __init__(
        self,
        agent_config: AgentConfig,
        test_cases: list[TestCase],
        graders: list[BaseGrader] | None = None,
        concurrency: int = 3,
    ):
        self.agent_config = agent_config
        self.test_cases = test_cases
        self.graders = graders or []
        self.concurrency = concurrency

        # Add default exact match grader if expected_output exists
        has_expected = any(tc.expected_output for tc in test_cases)
        if has_expected and not any(g.__class__.__name__ == "ExactMatchGrader" for g in self.graders):
            self.graders.append(ExactMatchGrader())

        self.console = Console()
        self.semaphore = asyncio.Semaphore(concurrency)

    async def run_all(self) -> EvalRun:
        """Run all test cases and return completed EvalRun."""
        run = EvalRun(
            agent_config=self.agent_config,
            test_cases=self.test_cases,
            status=RunStatus.RUNNING,
        )

        agent = AgentFactory.create(self.agent_config)
        run.started_at = datetime.now(timezone.utc)

        try:
            async with agent:
                tasks = [self._run_single(agent, tc, run) for tc in self.test_cases]
                await asyncio.gather(*tasks)

            run.status = RunStatus.COMPLETED
            run.completed_at = datetime.now(timezone.utc)
            self._calculate_stats(run)
        except Exception as e:
            run.status = RunStatus.FAILED
            run.completed_at = datetime.now(timezone.utc)
            self.console.print(f"[red]Eval run failed: {e}[/red]")
            raise
        finally:
            await agent.close()

        self.last_run = run
        return run

    async def _run_single(self, agent: BaseAgent, test_case: TestCase, run: EvalRun):
        async with self.semaphore:
            try:
                response = await agent.run(test_case.input)
                grades = await self._grade_response(test_case, response)

                passed = all(g.passed for g in grades)
                cost = self._estimate_cost(response.tokens_used)

                result = EvalResult(
                    run_id=run.id,
                    test_case_id=test_case.id,
                    test_case_name=test_case.name,
                    agent_output=response.output,
                    grades=grades,
                    passed=passed,
                    latency_ms=response.latency_ms,
                    cost_usd=cost,
                    tokens=response.tokens_used,
                    error=response.error,
                )
                run.add_result(result)

            except Exception as e:
                error_result = EvalResult(
                    run_id=run.id,
                    test_case_id=test_case.id,
                    test_case_name=test_case.name,
                    agent_output="",
                    grades=[],
                    passed=False,
                    latency_ms=0,
                    cost_usd=0.0,
                    tokens=0,
                    error=str(e),
                )
                run.add_result(error_result)

    async def _grade_response(self, test_case: TestCase, response) -> list:
        """Run all graders on the response."""
        grades = []
        for grader in self.graders:
            try:
                grade = await grader.grade(test_case, response)
                grades.append(grade)
            except Exception as e:
                from .schemas import Grade, GraderType
                grades.append(Grade(
                    grader_name=grader.name,
                    grader_type=GraderType.CUSTOM,
                    score=0.0,
                    passed=False,
                    reasoning=f"Grader error: {e}",
                ))
        return grades

    def _estimate_cost(self, tokens: int) -> float:
        """Rough cost estimation (GPT-4o-mini pricing)."""
        return (tokens / 1_000_000) * 0.15

    def _calculate_stats(self, run: EvalRun):
        """Calculate aggregate statistics."""
        if not run.results:
            return
        run.total_latency_ms = sum(r.latency_ms for r in run.results)
        run.total_cost_usd = sum(r.cost_usd for r in run.results)
        run.total_tokens = sum(r.tokens for r in run.results)
        run.pass_rate = sum(1 for r in run.results if r.passed) / len(run.results)

    def print_results(self, verbose: bool = False):
        """Print results table."""
        if not hasattr(self, 'last_run') or not self.last_run.results:
            return

        run = self.last_run

        table = Table(title=f"Eval Results: {run.agent_config.name}")
        table.add_column("Test Case", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Score", justify="right")
        table.add_column("Latency", justify="right")
        table.add_column("Cost", justify="right")
        table.add_column("Tokens", justify="right")

        for result in run.results:
            status = "[green]PASS[/green]" if result.passed else "[red]FAIL[/red]"
            score = f"{result.overall_score:.1%}"
            latency = f"{result.latency_ms}ms"
            cost = f"${result.cost_usd:.4f}"
            tokens = str(result.tokens)

            table.add_row(result.test_case_name, status, score, latency, cost, tokens)

        # Summary row
        table.add_row(
            "[bold]SUMMARY[/bold]",
            f"[bold]{run.pass_rate:.1%}[/bold]",
            f"[bold]{sum(r.overall_score for r in run.results)/len(run.results):.1%}[/bold]",
            f"[bold]{run.total_latency_ms}ms[/bold]",
            f"[bold]${run.total_cost_usd:.4f}[/bold]",
            f"[bold]{run.total_tokens}[/bold]",
        )

        self.console.print(table)

        if verbose:
            self._print_detailed_results(run)

    def _print_detailed_results(self, run: EvalRun):
        for result in run.results:
            self.console.print(f"\n[bold cyan]--- {result.test_case_name} ---[/bold cyan]")
            self.console.print(f"Input: {self._get_test_input(run, result.test_case_name)}")
            self.console.print(f"Output: {result.agent_output[:500]}..." if len(result.agent_output) > 500 else f"Output: {result.agent_output}")
            self.console.print(f"Expected: {self._get_expected(run, result.test_case_name)}")
            for grade in result.grades:
                status = "+" if grade.passed else "x"
                self.console.print(f"  {status} {grade.grader_name}: {grade.score:.1%} - {grade.reasoning}")

    def _get_test_input(self, run: EvalRun, name: str) -> str:
        tc = next((t for t in run.test_cases if t.name == name), None)
        return tc.input if tc else "N/A"

    def _get_expected(self, run: EvalRun, name: str) -> str:
        tc = next((t for t in run.test_cases if t.name == name), None)
        return tc.expected_output if tc else "N/A"