"""CLI entry point for agent-eval."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

import httpx
import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from .schemas import AgentConfig, ModelProvider, EvalRun, GraderType, TestCase
from .eval_runner import EvalRunner
from .graders_factory import GraderFactory

app = typer.Typer(
    name="agent-eval",
    help="Evaluate AI agents across test cases with multiple graders",
    add_completion=False,
)
console = Console()


def load_yaml_config(path: Path) -> dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f)


def load_test_cases(path: Path) -> list[TestCase]:
    data = load_yaml_config(path)
    if isinstance(data, list):
        return [TestCase(**tc) for tc in data]
    elif isinstance(data, dict) and "test_cases" in data:
        return [TestCase(**tc) for tc in data["test_cases"]]
    else:
        return [TestCase(**data)]


def load_agent_config(path: Path) -> AgentConfig:
    data = load_yaml_config(path)
    if "provider" in data and isinstance(data["provider"], str):
        data["provider"] = ModelProvider(data["provider"])
    return AgentConfig(**data)


def _snake_to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def _convert_keys(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {_snake_to_camel(k): _convert_keys(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_convert_keys(i) for i in obj]
    return obj


async def push_results_to_dashboard(run: EvalRun, project_id: str, api_url: str = "http://localhost:3000"):
    """Push evaluation results to dashboard API."""
    payload = {
        "projectId": project_id,
        "agentConfig": _convert_keys(run.agent_config.model_dump()) if run.agent_config else {},
        "testCases": [_convert_keys(tc.model_dump()) for tc in run.test_cases],
        "results": [_convert_keys(r.model_dump()) for r in run.results],
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(f"{api_url}/api/trpc/evalRun.create", json={"json": payload})
            response.raise_for_status()
            console.print("[green]Results pushed to dashboard[/green]")
        except httpx.HTTPError as e:
            console.print(f"[red]Failed to push to dashboard: {e}[/red]")
            console.print(f"[yellow]Make sure dashboard is running at {api_url}[/yellow]")


def load_graders(path: Path) -> list:
    data = load_yaml_config(path)
    graders = []
    for grader_config in data.get("graders", []):
        g = GraderFactory.create(grader_config)
        graders.append(g)
    return graders


@app.command()
def init(
    output_dir: Path = typer.Argument(Path("."), help="Directory to create example project"),
):
    """Initialize a new agent-eval project with example configs."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Agent config
    agent_config = AgentConfig(
        name="my-agent",
        provider=ModelProvider.OPENAI,
        model="gpt-4o-mini",
        temperature=0.0,
        max_tokens=2000,
        system_prompt="You are a helpful assistant.",
    )
    (output_dir / "agent.yaml").write_text(yaml.dump(agent_config.model_dump(mode='json'), sort_keys=False))

    # Test cases
    test_cases = [
        TestCase(
            name="basic_math",
            input="What is 2 + 2?",
            expected_output="4",
            tags=["math", "easy"],
        ),
        TestCase(
            name="capital_france",
            input="What is the capital of France?",
            expected_output="Paris",
            tags=["geography"],
        ),
        TestCase(
            name="python_fibonacci",
            input="Write a Python function to compute fibonacci(10)",
            expected_output="55",
            tags=["code"],
        ),
    ]
    (output_dir / "tests.yaml").write_text(yaml.dump({"test_cases": [tc.model_dump() for tc in test_cases]}, sort_keys=False))

    # Graders config
    graders_config = {
        "graders": [
            {"type": "exact_match", "name": "exact", "case_sensitive": False},
            {"type": "semantic_similarity", "name": "semantic", "threshold": 0.75},
            {"type": "llm_judge", "name": "llm_judge", "model": "gpt-4o-mini"},
        ]
    }
    (output_dir / "graders.yaml").write_text(yaml.dump(graders_config, sort_keys=False))

    # Example suite
    suite_config = {
        "name": "basic_suite",
        "agent": "agent.yaml",
        "test_cases": "tests.yaml",
        "graders": "graders.yaml",
    }
    (output_dir / "suite.yaml").write_text(yaml.dump(suite_config, sort_keys=False))

    console.print(Panel.fit(
        "[green]OK[/green] Created example project in [bold]{output_dir}[/bold]\n\n"
        "Files created:\n"
        "  * agent.yaml - Agent configuration\n"
        "  * tests.yaml - Test cases\n"
        "  * graders.yaml - Grader configuration\n"
        "  * suite.yaml - Suite definition\n\n"
        "Run: [cyan]agent-eval run suite.yaml[/cyan]",
        title="agent-eval init",
        border_style="green",
    ))


@app.command()
def run(
    suite_path: Path = typer.Argument(..., help="Path to suite.yaml or test cases YAML"),
    agent_path: Path | None = typer.Option(None, "--agent", "-a", help="Agent config (if not in suite)"),
    graders_path: Path | None = typer.Option(None, "--graders", "-g", help="Graders config (optional)"),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output JSON file"),
    concurrency: int = typer.Option(3, "--concurrency", "-c", help="Max concurrent evaluations"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    push: bool = typer.Option(False, "--push", help="Push results to dashboard"),
    project_id: str = typer.Option("default-project", "--project-id", help="Dashboard project ID"),
    api_url: str = typer.Option("http://localhost:3000", "--api-url", help="Dashboard API URL"),
):
    """Run evaluation suite."""
    if not suite_path.exists():
        console.print(f"[red]Suite file not found: {suite_path}[/red]")
        raise typer.Exit(1)

    # Load suite or test cases directly
    suite_data = load_yaml_config(suite_path)
    if "agent" in suite_data:  # It's a suite file
        agent_file = suite_path.parent / suite_data["agent"]
        test_file = suite_path.parent / suite_data["test_cases"]
        grader_file = suite_path.parent / suite_data.get("graders", "graders.yaml") if not graders_path else graders_path
    else:  # Direct test cases file
        if not agent_path:
            console.print("[red]--agent required when not using suite file[/red]")
            raise typer.Exit(1)
        agent_file = agent_path
        test_file = suite_path
        grader_file = graders_path

    try:
        agent_config = load_agent_config(agent_file)
        test_cases = load_test_cases(test_file)
        graders = load_graders(grader_file) if grader_file and grader_file.exists() else None
    except Exception as e:
        console.print(f"[red]Config error: {e}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Running eval:[/cyan] {agent_config.name} on {len(test_cases)} test cases")

    runner = EvalRunner(agent_config, test_cases, graders, concurrency)
    run = asyncio.run(runner.run_all())

    runner.print_results(verbose=verbose)

    if output:
        output.write_text(json.dumps(run.to_dict(), indent=2))
        console.print(f"\n[green]Results saved to {output}[/green]")

    if push:
        asyncio.run(push_results_to_dashboard(run, project_id=project_id, api_url=api_url))


@app.command()
def list_runs():
    """List recent evaluation runs (placeholder)."""
    console.print("[yellow]Not implemented yet - use dashboard for history[/yellow]")


@app.command()
def view(run_id: str):
    """View details of a specific run (placeholder)."""
    console.print(f"[yellow]Not implemented yet - run_id: {run_id}[/yellow]")


@app.command()
def version():
    """Show version."""
    console.print("agent-eval 0.1.0")


if __name__ == "__main__":
    app()