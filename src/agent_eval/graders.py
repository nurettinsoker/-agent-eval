"""Grader system for evaluating agent outputs."""

from __future__ import annotations

import re
import subprocess
import tempfile
import time
from abc import ABC, abstractmethod
from typing import Any

import httpx
from pydantic import BaseModel, Field

from .schemas import AgentConfig, AgentResponse, Grade, GraderType, TestCase


class BaseGrader(ABC):
    """Abstract base class for all graders."""

    def __init__(self, name: str, config: dict[str, Any] | None = None):
        self.name = name
        self.config = config or {}

    @abstractmethod
    async def grade(self, test_case: TestCase, response: AgentResponse) -> Grade:
        """Grade the agent response against the test case."""
        pass

    def _create_grade(
        self,
        score: float,
        passed: bool,
        reasoning: str | None = None,
        metadata: dict[str, Any] | None = None,
        grader_type: GraderType = GraderType.CUSTOM,
    ) -> Grade:
        return Grade(
            grader_name=self.name,
            grader_type=grader_type,
            score=max(0.0, min(1.0, score)),
            passed=passed,
            reasoning=reasoning,
            metadata=metadata or {},
        )


class LLMJudgeGrader(BaseGrader):
    """LLM-as-a-judge grader using a separate LLM to evaluate responses."""

    DEFAULT_PROMPT = """You are an expert evaluator. Compare the agent's response to the expected output.

Test Case: {test_case_name}
Input: {input}
Expected: {expected_output}
Actual: {actual_output}

Evaluate on a scale of 0-1 where:
- 1.0 = Perfect match, fully correct
- 0.7 = Mostly correct, minor issues
- 0.5 = Partially correct, significant gaps
- 0.3 = Some relevant content but mostly wrong
- 0.0 = Completely incorrect or irrelevant

Provide your score and brief reasoning in JSON format:
{{"score": 0.8, "reasoning": "..."}}"""

    def __init__(
        self,
        name: str = "llm_judge",
        model: str = "gpt-4o-mini",
        prompt_template: str | None = None,
        api_key_env: str = "OPENAI_API_KEY",
        base_url: str | None = None,
        **kwargs,
    ):
        super().__init__(name, kwargs)
        self.model = model
        self.prompt_template = prompt_template or self.DEFAULT_PROMPT
        self.api_key_env = api_key_env
        self.base_url = base_url or "https://api.openai.com/v1"

    async def grade(self, test_case: TestCase, response: AgentResponse) -> Grade:
        import os

        api_key = os.getenv(self.api_key_env)
        if not api_key:
            return self._create_grade(0.0, False, "API key not found", grader_type=GraderType.LLM_JUDGE)

        prompt = self.prompt_template.format(
            test_case_name=test_case.name,
            input=test_case.input,
            expected_output=test_case.expected_output or "N/A",
            actual_output=response.output,
        )

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": "You are an expert evaluator. Output only valid JSON."},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.0,
                        "max_tokens": 500,
                        "response_format": {"type": "json_object"},
                    },
                )
                resp.raise_for_status()
                data = resp.json()

            result = data["choices"][0]["message"]["content"]
            import json
            parsed = json.loads(result)
            score = float(parsed.get("score", 0.0))
            reasoning = parsed.get("reasoning", "")
            passed = score >= 0.7

            return self._create_grade(score, passed, reasoning, grader_type=GraderType.LLM_JUDGE)
        except Exception as e:
            return self._create_grade(0.0, False, f"Grading error: {e}", grader_type=GraderType.LLM_JUDGE)


class CodeExecutionGrader(BaseGrader):
    """Grader that executes code and checks output."""

    def __init__(
        self,
        name: str = "code_execution",
        language: str = "python",
        timeout_seconds: int = 10,
        **kwargs,
    ):
        super().__init__(name, kwargs)
        self.language = language
        self.timeout_seconds = timeout_seconds

    async def grade(self, test_case: TestCase, response: AgentResponse) -> Grade:
        if self.language != "python":
            return self._create_grade(0.0, False, f"Unsupported language: {self.language}", grader_type=GraderType.CODE_EXECUTION)

        code = self._extract_python_code(response.output)
        if not code:
            return self._create_grade(0.0, False, "No Python code found in response", grader_type=GraderType.CODE_EXECUTION)

        expected = test_case.expected_output or ""
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(code)
                temp_path = f.name

            result = subprocess.run(
                ["python", temp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )

            output = result.stdout.strip()
            stderr = result.stderr.strip()
            passed = result.returncode == 0 and (not expected or output == expected.strip())

            score = 1.0 if passed else 0.0
            if result.returncode != 0:
                reasoning = f"Execution failed: {stderr}"
            elif expected and output != expected.strip():
                reasoning = f"Output mismatch. Expected: {expected}, Got: {output}"
            else:
                reasoning = "Code executed successfully"

            return self._create_grade(score, passed, reasoning, grader_type=GraderType.CODE_EXECUTION)
        except subprocess.TimeoutExpired:
            return self._create_grade(0.0, False, f"Timeout after {self.timeout_seconds}s", grader_type=GraderType.CODE_EXECUTION)
        except Exception as e:
            return self._create_grade(0.0, False, f"Execution error: {e}", grader_type=GraderType.CODE_EXECUTION)

    def _extract_python_code(self, text: str) -> str:
        # Try to extract code from markdown code blocks
        pattern = r"```(?:python)?\n(.*?)\n```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return matches[0].strip()
        # If no code blocks, assume the whole text is code
        return text.strip()


class RegexGrader(BaseGrader):
    """Grader that checks if output matches a regex pattern."""

    def __init__(
        self,
        name: str = "regex",
        pattern: str = "",
        flags: int = re.IGNORECASE,
        **kwargs,
    ):
        super().__init__(name, kwargs)
        self.pattern = pattern
        self.flags = flags
        self._compiled = re.compile(pattern, flags) if pattern else None

    async def grade(self, test_case: TestCase, response: AgentResponse) -> Grade:
        if not self._compiled:
            return self._create_grade(0.0, False, "No pattern configured", grader_type=GraderType.REGEX)

        match = self._compiled.search(response.output)
        passed = match is not None
        score = 1.0 if passed else 0.0
        reasoning = f"Pattern {'matched' if passed else 'not found'}: {self.pattern}"

        return self._create_grade(score, passed, reasoning, grader_type=GraderType.REGEX)


class ExactMatchGrader(BaseGrader):
    """Grader that checks for exact string match."""

    def __init__(
        self,
        name: str = "exact_match",
        case_sensitive: bool = False,
        strip_whitespace: bool = True,
        **kwargs,
    ):
        super().__init__(name, kwargs)
        self.case_sensitive = case_sensitive
        self.strip_whitespace = strip_whitespace

    async def grade(self, test_case: TestCase, response: AgentResponse) -> Grade:
        expected = test_case.expected_output or ""
        actual = response.output

        if self.strip_whitespace:
            expected = expected.strip()
            actual = actual.strip()

        if not self.case_sensitive:
            expected = expected.lower()
            actual = actual.lower()

        passed = actual == expected
        score = 1.0 if passed else 0.0
        reasoning = "Exact match" if passed else f"Mismatch. Expected: {expected[:100]}, Got: {actual[:100]}"

        return self._create_grade(score, passed, reasoning, grader_type=GraderType.EXACT_MATCH)


class SemanticSimilarityGrader(BaseGrader):
    """Grader using sentence embeddings for semantic similarity."""

    def __init__(
        self,
        name: str = "semantic_similarity",
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        threshold: float = 0.75,
        **kwargs,
    ):
        super().__init__(name, kwargs)
        self.model_name = model_name
        self.threshold = threshold
        self._model = None

    def _get_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
        return self._model

    async def grade(self, test_case: TestCase, response: AgentResponse) -> Grade:
        expected = test_case.expected_output or ""
        actual = response.output

        if not expected or not actual:
            return self._create_grade(0.0, False, "Empty expected or actual output", grader_type=GraderType.SEMANTIC_SIMILARITY)

        try:
            model = self._get_model()
            embeddings = model.encode([expected, actual])
            import numpy as np
            similarity = float(np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])))
            passed = similarity >= self.threshold
            reasoning = f"Semantic similarity: {similarity:.3f} (threshold: {self.threshold})"
            return self._create_grade(similarity, passed, reasoning, grader_type=GraderType.SEMANTIC_SIMILARITY)
        except Exception as e:
            return self._create_grade(0.0, False, f"Embedding error: {e}", grader_type=GraderType.SEMANTIC_SIMILARITY)


class GraderFactory:
    """Factory for creating grader instances."""

    _registry = {
        GraderType.LLM_JUDGE: LLMJudgeGrader,
        GraderType.CODE_EXECUTION: CodeExecutionGrader,
        GraderType.REGEX: RegexGrader,
        GraderType.SEMANTIC_SIMILARITY: SemanticSimilarityGrader,
        GraderType.EXACT_MATCH: ExactMatchGrader,
    }

    @classmethod
    def register(cls, grader_type: GraderType, grader_class: type[BaseGrader]):
        cls._registry[grader_type] = grader_class

    @classmethod
    def create(cls, grader_type: GraderType, name: str, **config) -> BaseGrader:
        grader_class = cls._registry.get(grader_type)
        if not grader_class:
            raise ValueError(f"Unknown grader type: {grader_type}")
        return grader_class(name=name, **config)

    @classmethod
    def create_from_config(cls, config: dict[str, Any]) -> BaseGrader:
        grader_type = GraderType(config.get("type", "custom"))
        name = config.get("name", "custom_grader")
        params = {k: v for k, v in config.items() if k not in ("type", "name")}
        return cls.create(grader_type, name, **params)