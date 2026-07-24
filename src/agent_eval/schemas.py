"""Core Pydantic schemas for Agent Eval."""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from pydantic import BaseModel, Field, ConfigDict


class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    CUSTOM = "custom"
    MOCK = "mock"


class AgentConfig(BaseModel):
    """Configuration for an agent to be evaluated."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., description="Human-readable name")
    provider: ModelProvider = Field(default=ModelProvider.OPENAI)
    model: str = Field(default="gpt-4o-mini", description="Model identifier")
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1, le=128000)
    system_prompt: str | None = Field(default=None, description="System prompt for the agent")
    tools: list[dict[str, Any]] = Field(default_factory=list, description="Available tools/functions")
    custom_headers: dict[str, str] = Field(default_factory=dict)
    base_url: str | None = Field(default=None, description="Custom API base URL")
    api_key_env: str = Field(default="OPENAI_API_KEY", description="Environment variable for API key")


class TestCase(BaseModel):
    """A single test case for evaluation."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = Field(..., description="Test case name")
    input: str = Field(..., description="Input to the agent")
    expected_output: str | None = Field(default=None, description="Expected output (optional)")
    metadata: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    timeout_seconds: int = Field(default=60, ge=1, le=300)


class GraderType(str, Enum):
    LLM_JUDGE = "llm_judge"
    CODE_EXECUTION = "code_execution"
    REGEX = "regex"
    SEMANTIC_SIMILARITY = "semantic_similarity"
    EXACT_MATCH = "exact_match"
    CUSTOM = "custom"


class Grade(BaseModel):
    """Result of a single grader."""

    model_config = ConfigDict(extra="forbid")

    grader_name: str
    grader_type: GraderType
    score: float = Field(..., ge=0.0, le=1.0, description="Normalized score 0-1")
    passed: bool
    reasoning: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    """Response from an agent execution."""

    model_config = ConfigDict(extra="forbid")

    output: str
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    tokens_used: int = 0
    latency_ms: int = 0
    raw_response: dict[str, Any] | None = None
    error: str | None = None


class EvalResult(BaseModel):
    """Result of evaluating a single test case."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    test_case_id: str
    test_case_name: str
    agent_output: str
    grades: list[Grade]
    passed: bool
    latency_ms: int
    cost_usd: float = 0.0
    tokens: int = 0
    error: str | None = None

    @property
    def overall_score(self) -> float:
        if not self.grades:
            return 0.0
        return sum(g.score for g in self.grades) / len(self.grades)

    @property
    def all_passed(self) -> bool:
        return all(g.passed for g in self.grades)


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EvalRun(BaseModel):
    """An evaluation run containing multiple test cases."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    project_id: str = "default"
    agent_config: AgentConfig
    test_cases: list[TestCase]
    status: RunStatus = RunStatus.PENDING
    results: list[EvalResult] = Field(default_factory=list)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    total_latency_ms: int = 0
    total_cost_usd: float = 0.0
    total_tokens: int = 0
    pass_rate: float = 0.0

    def add_result(self, result: EvalResult) -> None:
        self.results.append(result)
        self.total_latency_ms += result.latency_ms
        self.total_cost_usd += result.cost_usd
        self.total_tokens += result.tokens
        if self.results:
            self.pass_rate = sum(1 for r in self.results if r.all_passed) / len(self.results)

    def to_summary(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "agent_name": self.agent_config.name,
            "model": self.agent_config.model,
            "status": self.status.value,
            "total_tests": len(self.test_cases),
            "completed_tests": len(self.results),
            "pass_rate": round(self.pass_rate * 100, 1),
            "avg_latency_ms": round(self.total_latency_ms / max(len(self.results), 1)),
            "total_cost_usd": round(self.total_cost_usd, 4),
            "total_tokens": self.total_tokens,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }