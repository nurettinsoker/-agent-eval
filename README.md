# agent-eval

Open-source AI agent evaluation platform. Test your LLM agents across multiple test cases with pluggable graders and visualize results on a web dashboard.

## Features

- **CLI Engine**: Run evaluation suites from the command line
- **5 Grader Types**: exact_match, semantic_similarity, llm_judge, regex, code_execution
- **Agent Adapters**: OpenAI, Anthropic, custom HTTP endpoints, MockAgent for testing
- **Web Dashboard**: Next.js dashboard with tRPC API, dark mode, trace viewer
- **Push to Dashboard**: Send CLI results to dashboard with `--push` flag

## Prerequisites

- Python 3.12+
- Node.js 18+ and pnpm (for dashboard)

## Quick Start

### Python CLI

```bash
pip install -e .

# Initialize example project
agent-eval init my-project

# Run evaluation with mock agent (no API key needed)
agent-eval run my-project/suite.yaml --agent my-project/agent.yaml

# Run and push results to dashboard
agent-eval run my-project/suite.yaml --agent my-project/agent.yaml --push
```

### Dashboard

```bash
cd dashboard
pnpm install
npx prisma migrate dev
npx prisma db seed
pnpm dev
```

Open http://localhost:3000

## Configuration

### Agent Config (agent.yaml)

```yaml
name: my-agent
provider: openai          # openai | anthropic | http | mock
model: gpt-4o-mini
temperature: 0.0
max_tokens: 2000
system_prompt: "You are a helpful assistant."
```

### Test Cases (tests.yaml)

```yaml
test_cases:
  - name: basic_math
    input: "What is 2 + 2?"
    expected_output: "4"
    tags: [math, easy]
  - name: capital_france
    input: "What is the capital of France?"
    expected_output: "Paris"
    tags: [geography]
```

### Graders (graders.yaml)

```yaml
graders:
  - type: exact_match
    name: exact
    case_sensitive: false
  - type: semantic_similarity
    name: semantic
    threshold: 0.75
  - type: llm_judge
    name: judge
    model: gpt-4o-mini
```

### Suite (suite.yaml)

```yaml
name: basic_suite
agent: agent.yaml
test_cases: tests.yaml
graders: graders.yaml
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `agent-eval init [dir]` | Create example project |
| `agent-eval run <suite> --agent <agent>` | Run evaluation |
| `agent-eval version` | Show version |

### Run Options

| Flag | Description |
|------|-------------|
| `--agent, -a` | Agent config file |
| `--graders, -g` | Graders config file |
| `--output, -o` | Save results to JSON |
| `--concurrency, -c` | Max concurrent tests (default: 3) |
| `--verbose, -v` | Detailed output |
| `--push` | Push results to dashboard |
| `--project-id` | Dashboard project ID |
| `--api-url` | Dashboard API URL |

## Installation & Development

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/nurettinsoker/-agent-eval.git
cd -agent-eval

# Setup CLI
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .

# Setup Dashboard
cd dashboard
pnpm install
```

## Tech Stack

- **CLI**: Python 3.12+, Typer, Rich, Pydantic, httpx, asyncio
- **Dashboard**: Next.js 14, tRPC, Prisma, SQLite, Tailwind CSS v4
- **Agents**: OpenAI API, Anthropic API, custom HTTP

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
