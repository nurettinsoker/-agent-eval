"""Basic tests for agent-eval."""

import pytest
from agent_eval.schemas import AgentConfig, TestCase, ModelProvider, GraderType


def test_agent_config_creation():
    config = AgentConfig(
        name="test-agent",
        provider=ModelProvider.OPENAI,
        model="gpt-4o-mini",
        temperature=0.0,
    )
    assert config.name == "test-agent"
    assert config.provider == ModelProvider.OPENAI


def test_test_case_creation():
    tc = TestCase(
        name="Test Case",
        input="What is 2+2?",
        expected_output="4",
        tags=["math"],
    )
    assert tc.name == "Test Case"
    assert tc.input == "What is 2+2?"
    assert tc.expected_output == "4"
    assert "math" in tc.tags


def test_model_provider_enum():
    assert ModelProvider.OPENAI == "openai"
    assert ModelProvider.ANTHROPIC == "anthropic"
    assert ModelProvider.CUSTOM == "custom"


def test_grader_type_enum():
    assert GraderType.EXACT_MATCH == "exact_match"
    assert GraderType.LLM_JUDGE == "llm_judge"
    assert GraderType.CODE_EXECUTION == "code_execution"
    assert GraderType.REGEX == "regex"
    assert GraderType.SEMANTIC_SIMILARITY == "semantic_similarity"