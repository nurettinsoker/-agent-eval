# agent-eval

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/nurettinsoker/-agent-eval?style=social)](https://github.com/nurettinsoker/-agent-eval)

Open-source AI agent evaluation platform. Test your LLM agents across multiple test cases with pluggable graders and visualize results on a web dashboard.

> **[See full project documentation](./LANDING_PAGE.md)** | **[Architecture Overview](./ARCHITECTURE.md)** | **[Contributing](./CONTRIBUTING.md)**

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [CLI Commands](#cli-commands)
- [Environment Setup](#environment-setup)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **🚀 CLI Engine**: Run evaluation suites from the command line with async support
- **🎯 5 Grader Types**: 
  - Exact match
  - Semantic similarity
  - LLM Judge (AI-based evaluation)
  - Regex pattern matching
  - Code execution validation
- **🔌 Agent Adapters**: OpenAI, Anthropic, custom HTTP endpoints, MockAgent for testing
- **📊 Web Dashboard**: Next.js dashboard with tRPC API, dark mode, trace viewer
- **📤 Push to Dashboard**: Send CLI results to dashboard with `--push` flag
- **🔄 Concurrent Testing**: Run multiple tests in parallel (configurable)
- **💾 Export Results**: Save results to JSON for analysis
- **🧪 Mock Mode**: Test without API keys

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ and pnpm (for dashboard)
- Git

### 1. Install CLI

```bash
# Clone repository
git clone https://github.com/nurettinsoker/-agent-eval.git
cd -agent-eval

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install agent-eval
pip install -e .
```

### 2. Initialize Project

```bash
# Create example project
agent-eval init my-first-eval
cd my-first-eval
```

This creates:
- `agent.yaml` - AI agent configuration
- `tests.yaml` - Test cases
- `graders.yaml` - Evaluation methods
- `suite.yaml` - Test suite definition

### 3. Run Tests (No API Key Required)

```bash
# Run with mock agent (for testing)
agent-eval run suite.yaml --agent agent.yaml --verbose
```

### 4. View Dashboard (Optional)

```bash
# In another terminal, from project root
cd dashboard
pnpm install
npx prisma migrate dev
npx prisma db seed
pnpm dev

# Open http://localhost:3000
```

## 📦 Installation

### From Source

```bash
git clone https://github.com/nurettinsoker/-agent-eval.git
cd -agent-eval
pip install -e .
```

### With Optional Dependencies

```bash
# Development tools
pip install -e ".[dev]"

# CrewAI integration
pip install -e ".[crewai]"

# AutoGen integration
pip install -e ".[autogen]"
```

### Docker (Coming Soon)

```bash
docker pull agent-eval
docker run -v $(pwd):/workspace agent-eval run suite.yaml
```

## ⚙️ Configuration

### Environment Setup

Create a `.env` file in project root:

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Dashboard
DASHBOARD_API_URL=http://localhost:3000/api

# Optional
LOG_LEVEL=INFO
MAX_CONCURRENT_TESTS=5
```

See [.env.example](./.env.example) for all available options.

### Agent Config (agent.yaml)

```yaml
name: my-openai-agent
provider: openai              # openai | anthropic | http | mock
model: gpt-4o-mini
temperature: 0.7
max_tokens: 2000
system_prompt: |
  You are a helpful AI assistant.
  Answer questions accurately and concisely.
api_key: ${OPENAI_API_KEY}   # Use env variable or set directly
```

**Provider Options:**

```yaml
# OpenAI
provider: openai
model: gpt-4o-mini
api_key: ${OPENAI_API_KEY}

# Anthropic
provider: anthropic
model: claude-3-5-sonnet-20241022
api_key: ${ANTHROPIC_API_KEY}

# Custom HTTP Endpoint
provider: http
endpoint: http://localhost:8000/api/chat
headers:
  Authorization: Bearer YOUR_TOKEN

# Mock (for testing, no API key)
provider: mock
model: mock-gpt-4
```

### Test Cases (tests.yaml)

```yaml
test_cases:
  - name: math_addition
    input: "What is 2 + 2?"
    expected_output: "4"
    tags: [math, easy]
    
  - name: geography
    input: "What is the capital of France?"
    expected_output: "Paris"
    tags: [geography, knowledge]
    
  - name: code_generation
    input: "Write a Python function to reverse a string"
    expected_output: "def reverse_string(s):"
    tags: [coding, python]
```

### Graders (graders.yaml)

```yaml
graders:
  # Exact string match
  - type: exact_match
    name: exact
    case_sensitive: false
    
  # Semantic similarity (0-1 score)
  - type: semantic_similarity
    name: semantic
    threshold: 0.75
    model: all-MiniLM-L6-v2
    
  # LLM-based evaluation
  - type: llm_judge
    name: gpt_judge
    model: gpt-4o-mini
    api_key: ${OPENAI_API_KEY}
    criteria: "Is the answer helpful and accurate?"
    
  # Regex pattern matching
  - type: regex
    name: code_pattern
    pattern: "def \\w+\\(.*\\):"
    
  # Code execution validation
  - type: code_execution
    name: python_validator
    language: python
    timeout: 5
```

### Suite (suite.yaml)

```yaml
name: my_evaluation_suite
version: "1.0"
description: "Evaluate AI assistant performance"
agent: agent.yaml
test_cases: tests.yaml
graders: graders.yaml

# Optional
tags: [production, v1.0]
metadata:
  model: gpt-4o-mini
  date: 2024-01-15
```

## 🔧 Usage Examples

### Basic Evaluation

```bash
agent-eval run suite.yaml --agent agent.yaml
```

### With Verbose Output

```bash
agent-eval run suite.yaml --agent agent.yaml --verbose
```

### Save Results

```bash
agent-eval run suite.yaml --agent agent.yaml --output results.json
```

### Parallel Testing

```bash
agent-eval run suite.yaml --agent agent.yaml --concurrency 10
```

### Push to Dashboard

```bash
agent-eval run suite.yaml --agent agent.yaml --push --project-id my-project
```

### Custom Graders

```bash
agent-eval run suite.yaml --agent agent.yaml --graders custom-graders.yaml
```

### Compare Models

```bash
# Test OpenAI
agent-eval run suite.yaml --agent agent-openai.yaml --output openai-results.json

# Test Anthropic
agent-eval run suite.yaml --agent agent-anthropic.yaml --output anthropic-results.json

# Test Local Model
agent-eval run suite.yaml --agent agent-local.yaml --output local-results.json
```

## 📁 Project Structure

```
-agent-eval/
├── src/
│   └── agent_eval/
│       ├── __init__.py
│       ├── cli.py                 # CLI entry point
│       ├── core/
│       │   ├── evaluator.py       # Main evaluation engine
│       │   ├── graders/           # Grader implementations
│       │   │   ├── base.py
│       │   │   ├── exact_match.py
│       │   │   ├── semantic.py
│       │   │   ├── llm_judge.py
│       │   │   ├── regex_grader.py
│       │   │   └── code_exec.py
│       │   └── agents/            # Agent adapters
│       │       ├── base.py
│       │       ├── openai.py
│       │       ├── anthropic.py
│       │       ├── http.py
│       │       └── mock.py
│       ├── models/
│       │   ├── config.py          # Pydantic models
│       │   └── results.py
│       ├── utils/
│       │   ├── loader.py          # YAML/JSON loading
│       │   ├── logger.py
│       │   └── validators.py
│       └── api/
│           └── server.py          # FastAPI server (optional)
├── dashboard/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx           # Home page
│   │   │   ├── projects/          # Projects page
│   │   │   ├── results/           # Results viewer
│   │   │   └── api/               # tRPC routes
│   │   ├── components/            # React components
│   │   ├── lib/                   # Utilities
│   │   └── styles/                # Tailwind CSS
│   ├── prisma/
│   │   ├── schema.prisma          # Database schema
│   │   └── migrations/            # Database migrations
│   └── package.json
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/                  # Test data
├── examples/
│   ├── basic/
│   ├── chatbot/
│   ├── code-generator/
│   └── translator/
├── .env.example
├── pyproject.toml
├── README.md
├── LANDING_PAGE.md
├── CONTRIBUTING.md
└── LICENSE
```

See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for detailed structure.

## 🎮 CLI Commands

### Global Commands

| Command | Description | Example |
|---------|-------------|----------|
| `agent-eval init` | Initialize new project | `agent-eval init my-project` |
| `agent-eval run` | Run evaluation suite | `agent-eval run suite.yaml` |
| `agent-eval version` | Show version | `agent-eval version` |
| `agent-eval config` | Validate config files | `agent-eval config agent.yaml` |

### Run Command Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--agent, -a` | PATH | `agent.yaml` | Agent config file |
| `--graders, -g` | PATH | `graders.yaml` | Graders config file |
| `--output, -o` | PATH | None | Save results to JSON |
| `--concurrency, -c` | INT | 3 | Max concurrent tests |
| `--verbose, -v` | FLAG | False | Detailed output |
| `--push` | FLAG | False | Push to dashboard |
| `--project-id` | STR | None | Dashboard project ID |
| `--api-url` | URL | http://localhost:3000 | Dashboard API URL |
| `--timeout` | INT | 30 | Test timeout (seconds) |
| `--tags` | STR | None | Filter by tags (comma-separated) |

## 🌐 Environment Setup

### API Key Configuration

**OpenAI:**
```bash
export OPENAI_API_KEY=sk-...
# or add to .env file
OPENAI_API_KEY=sk-...
```

Get key: https://platform.openai.com/api-keys

**Anthropic:**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Get key: https://console.anthropic.com/

**Custom HTTP:**
No API key needed, provide endpoint URL in agent.yaml

**Mock (for testing):**
No API key needed

### Dashboard Setup

```bash
cd dashboard

# Install dependencies
pnpm install

# Setup database
npx prisma migrate dev

# Seed database (optional)
npx prisma db seed

# Run development server
pnpm dev
```

Open http://localhost:3000

## 🐛 Troubleshooting

### Common Issues

**Error: "API key not found"**
```bash
# Solution 1: Set environment variable
export OPENAI_API_KEY=sk-...

# Solution 2: Add to .env file
echo "OPENAI_API_KEY=sk-..." >> .env

# Solution 3: Add to agent.yaml
api_key: sk-...
```

**Error: "Module 'agent_eval' not found"**
```bash
# Solution: Reinstall package
pip install -e .
```

**Error: "Python version not supported"**
```bash
# Check Python version
python --version

# Solution: Use Python 3.11+
python3.11 -m venv venv
source venv/bin/activate
pip install -e .
```

**Dashboard connection fails**
```bash
# Check if dashboard is running
cd dashboard && pnpm dev

# Verify API URL
agent-eval run suite.yaml --push --api-url http://localhost:3000/api
```

**Grader failures**
```bash
# For llm_judge: Ensure API key is set
export OPENAI_API_KEY=sk-...

# For semantic_similarity: May need first-time model download
# (sentence-transformers will download automatically)

# For code_execution: Ensure code is valid
agent-eval run suite.yaml --verbose  # See detailed error
```

### Debug Mode

```bash
# Run with verbose logging
agent-eval run suite.yaml --verbose

# Save detailed output
agent-eval run suite.yaml --output debug.json --verbose

# Check configuration
agent-eval config agent.yaml
agent-eval config graders.yaml
```

### Performance Optimization

```bash
# Increase concurrency (default: 3)
agent-eval run suite.yaml --concurrency 10

# Set timeout
agent-eval run suite.yaml --timeout 60

# Run specific tests by tag
agent-eval run suite.yaml --tags math,easy
```

## 📊 Tech Stack

### Backend (CLI)
- **Python 3.11+**
- **Typer** - CLI framework
- **Pydantic** - Data validation
- **Rich** - Terminal UI
- **httpx** - Async HTTP client
- **asyncio** - Async support
- **sentence-transformers** - Semantic similarity
- **OpenAI SDK** - OpenAI API
- **Anthropic SDK** - Anthropic API
- **python-dotenv** - Environment management

### Frontend (Dashboard)
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **tRPC** - Type-safe API
- **Prisma** - ORM
- **SQLite** - Database
- **Tailwind CSS v4** - Styling
- **Dark mode** - Theme support

### Testing
- **pytest** - Testing framework
- **pytest-asyncio** - Async test support
- **pytest-cov** - Coverage reporting

## 📚 Examples

Check [examples/](./examples) directory for:
- Basic chatbot evaluation
- Code generator testing
- Translator validation
- Multi-model comparison

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## 📖 Documentation

- [Landing Page](./LANDING_PAGE.md) - Project overview (TR/EN)
- [Architecture](./ARCHITECTURE.md) - Technical details
- [Project Structure](./PROJECT_STRUCTURE.md) - Code organization
- [Contributing](./CONTRIBUTING.md) - How to contribute

## 📜 License

MIT License - See [LICENSE](./LICENSE) for details

## 🌟 Support

If you find this project helpful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting issues
- 💡 Suggesting features
- 🔗 Sharing with others

## 📞 Contact

- GitHub Issues: [Report bug or request feature](https://github.com/nurettinsoker/-agent-eval/issues)
- GitHub Discussions: [Ask questions](https://github.com/nurettinsoker/-agent-eval/discussions)

---

**Made with ❤️ by [Nurettin Soker](https://github.com/nurettinsoker)**
