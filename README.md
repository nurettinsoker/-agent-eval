# Agent Eval

Open-source agent evaluation platform - CLI + Dashboard for testing AI agents.

## Quickstart

```bash
# Install
pip install -e .

# Set API key
export OPENAI_API_KEY="sk-..."

# Run evaluation
agent-eval run examples/suite.yaml --agent examples/agent.yaml
```

## Commands

```bash
agent-eval init                    # Create example project structure
agent-eval run suite.yaml          # Run evaluation suite
agent-eval run suite.yaml --agent agent.yaml --push  # Push to dashboard
agent-eval list                    # List recent runs
agent-eval view <run_id>           # View run details
agent-eval version                 # Show version
```

## Configuration

### Agent Config (`agent.yaml`)
```yaml
name: "my-agent"
provider: "openai"  # openai, anthropic, http
model: "gpt-4o-mini"
temperature: 0.0
max_tokens: 2000
system_prompt: "You are a helpful assistant."
tools: []
api_key_env: "OPENAI_API_KEY"
```

### Test Suite (`suite.yaml`)
```yaml
test_cases:
  - id: "test-001"
    name: "Test Name"
    input: "Your prompt here"
    expected_output: "Expected answer"
    tags: ["category"]
    metadata:
      difficulty: "easy"

graders:
  - type: "exact_match"
    name: "exact_match"
    case_sensitive: false
  - type: "llm_judge"
    name: "llm_judge"
    model: "gpt-4o-mini"
  - type: "regex"
    name: "contains_number"
    pattern: "\\d+"
```

### Grader Types
| Type | Description |
|------|-------------|
| `exact_match` | Exact string comparison |
| `regex` | Regex pattern matching |
| `llm_judge` | LLM evaluates correctness |
| `code_execution` | Executes Python code, checks output |
| `semantic_similarity` | Embedding-based similarity |

## Architecture

```
agent-eval/
├── src/agent_eval/
│   ├── __init__.py
│   ├── schemas.py         # Pydantic models
│   ├── agent.py           # Agent adapters (OpenAI, Anthropic, HTTP)
│   ├── graders.py         # Grader implementations
│   ├── graders_factory.py # Config-based grader loading
│   ├── eval_runner.py     # Orchestration
│   └── cli.py             # Typer CLI
├── examples/
│   ├── agent.yaml
│   └── suite.yaml
├── tests/
├── pyproject.toml
└── README.md
```

## Dashboard (Coming Soon)

- Next.js + tRPC + Prisma
- Visual trace viewer (React Flow)
- Failure clustering
- Regression detection
- GitHub Action for CI/CD

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .
mypy src/
```

## License

MIT