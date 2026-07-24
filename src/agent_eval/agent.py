"""Agent protocol and adapters for different frameworks."""

from __future__ import annotations

import os
import time
from abc import ABC, abstractmethod
from typing import Any

import httpx
from pydantic import BaseModel

from .schemas import AgentConfig, AgentResponse


class BaseAgent(ABC):
    """Abstract base class for all agent adapters."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self._client: httpx.AsyncClient | None = None

    @abstractmethod
    async def run(self, input_text: str) -> AgentResponse:
        """Run the agent with input and return response."""
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None

    def _get_api_key(self) -> str:
        key = os.getenv(self.config.api_key_env)
        if not key:
            raise ValueError(f"API key not found in env var: {self.config.api_key_env}")
        return key

    def _get_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        headers.update(self.config.custom_headers)
        return headers


class OpenAIAgent(BaseAgent):
    """OpenAI ChatCompletion and Assistants API adapter."""

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.base_url = config.base_url or "https://api.openai.com/v1"

    async def run(self, input_text: str) -> AgentResponse:
        start = time.perf_counter()
        api_key = self._get_api_key()

        messages = []
        if self.config.system_prompt:
            messages.append({"role": "system", "content": self.config.system_prompt})
        messages.append({"role": "user", "content": input_text})

        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }

        if self.config.tools:
            payload["tools"] = self.config.tools
            payload["tool_choice"] = "auto"

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={**self._get_headers(), "Authorization": f"Bearer {api_key}"},
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        latency_ms = int((time.perf_counter() - start) * 1000)
        choice = data["choices"][0]
        message = choice["message"]

        tool_calls = []
        if message.get("tool_calls"):
            for tc in message["tool_calls"]:
                tool_calls.append({
                    "id": tc["id"],
                    "name": tc["function"]["name"],
                    "arguments": tc["function"]["arguments"],
                })

        usage = data.get("usage", {})
        tokens = usage.get("total_tokens", 0)

        return AgentResponse(
            output=message.get("content", ""),
            tool_calls=tool_calls,
            tokens_used=tokens,
            latency_ms=latency_ms,
            raw_response=data,
        )


class AnthropicAgent(BaseAgent):
    """Anthropic Messages API adapter."""

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.base_url = config.base_url or "https://api.anthropic.com/v1"

    async def run(self, input_text: str) -> AgentResponse:
        start = time.perf_counter()
        api_key = self._get_api_key()

        messages = []
        if self.config.system_prompt:
            messages.append({"role": "user", "content": self.config.system_prompt})
        messages.append({"role": "user", "content": input_text})

        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }

        if self.config.tools:
            payload["tools"] = self.config.tools

        headers = {
            **self._get_headers(),
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        latency_ms = int((time.perf_counter() - start) * 1000)

        content = ""
        tool_calls = []
        for block in data.get("content", []):
            if block["type"] == "text":
                content += block["text"]
            elif block["type"] == "tool_use":
                tool_calls.append({
                    "id": block["id"],
                    "name": block["name"],
                    "arguments": block["input"],
                })

        usage = data.get("usage", {})
        tokens = usage.get("input_tokens", 0) + usage.get("output_tokens", 0)

        return AgentResponse(
            output=content,
            tool_calls=tool_calls,
            tokens_used=tokens,
            latency_ms=latency_ms,
            raw_response=data,
        )


class HTTPAgent(BaseAgent):
    """Custom HTTP endpoint adapter for self-hosted/custom agents."""

    async def run(self, input_text: str) -> AgentResponse:
        start = time.perf_counter()

        if not self.config.base_url:
            raise ValueError("base_url required for HTTPAgent")

        payload = {
            "input": input_text,
            "config": {
                "model": self.config.model,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
            },
        }

        headers = self._get_headers()
        api_key = os.getenv(self.config.api_key_env)
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.config.base_url,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        latency_ms = int((time.perf_counter() - start) * 1000)

        # Expect standardized response format
        output = data.get("output", str(data))
        tool_calls = data.get("tool_calls", [])
        tokens = data.get("tokens_used", 0)

        return AgentResponse(
            output=output,
            tool_calls=tool_calls,
            tokens_used=tokens,
            latency_ms=latency_ms,
            raw_response=data,
        )


class MockAgent(BaseAgent):
    """Mock agent for testing without API keys."""
    
    async def run(self, input_text: str) -> AgentResponse:
        import time
        start = time.perf_counter()
        
        # Simple mock responses based on input
        input_lower = input_text.lower()
        
        if "2+2" in input_text or "2 + 2" in input_text:
            output = "4"
        elif "france" in input_lower:
            output = "Paris"
        elif "fibonacci" in input_lower:
            output = "55"
        elif "capital" in input_lower:
            output = "Paris"
        else:
            output = f"Mock response to: {input_text[:50]}"
        
        latency_ms = int((time.perf_counter() - start) * 1000)
        
        return AgentResponse(
            output=output,
            tool_calls=[],
            tokens_used=10,
            latency_ms=latency_ms,
            raw_response={"mock": True},
        )


class AgentFactory:
    """Factory for creating agent instances."""

    _registry = {
        "openai": OpenAIAgent,
        "anthropic": AnthropicAgent,
        "http": HTTPAgent,
        "mock": MockAgent,
    }

    @classmethod
    def register(cls, name: str, agent_class: type[BaseAgent]):
        cls._registry[name] = agent_class

    @classmethod
    def create(cls, config: AgentConfig) -> BaseAgent:
        provider = config.provider.value if hasattr(config.provider, "value") else str(config.provider)
        agent_class = cls._registry.get(provider.lower())
        if not agent_class:
            raise ValueError(f"Unknown agent provider: {provider}. Available: {list(cls._registry.keys())}")
        return agent_class(config)