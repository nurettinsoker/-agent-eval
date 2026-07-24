"""Grader factory for loading graders from config."""

from __future__ import annotations

from typing import Any

from .graders import (
    BaseGrader,
    LLMJudgeGrader,
    CodeExecutionGrader,
    RegexGrader,
    ExactMatchGrader,
    SemanticSimilarityGrader,
)


class GraderFactory:
    """Factory for creating graders from config dicts."""

    _registry = {
        "llm_judge": LLMJudgeGrader,
        "code_execution": CodeExecutionGrader,
        "regex": RegexGrader,
        "exact_match": ExactMatchGrader,
        "semantic_similarity": SemanticSimilarityGrader,
    }

    @classmethod
    def register(cls, name: str, grader_class: type[BaseGrader]):
        cls._registry[name] = grader_class

    @classmethod
    def create(cls, config: dict[str, Any]) -> BaseGrader:
        grader_type = config.pop("type", "exact_match")
        name = config.pop("name", grader_type)
        grader_class = cls._registry.get(grader_type)
        if not grader_class:
            raise ValueError(f"Unknown grader type: {grader_type}. Available: {list(cls._registry.keys())}")
        return grader_class(name=name, **config)

    @classmethod
    def create_from_list(cls, configs: list[dict[str, Any]]) -> list[BaseGrader]:
        return [cls.create(c) for c in configs]