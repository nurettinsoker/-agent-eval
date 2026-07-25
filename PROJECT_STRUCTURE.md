# Project Structure

## Overview

```
-agent-eval/
├── src/                          # Source code
│   └── agent_eval/               # Main package
│       ├── __init__.py
│       ├── cli.py                # CLI entry point (Typer)
│       ├── core/
│       │   ├── __init__.py
│       │   ├── evaluator.py       # Main evaluation engine
│       │   ├── graders/           # Grader implementations
│       │   │   ├── __init__.py
│       │   │   ├── base.py        # Abstract base grader
│       │   │   ├── exact_match.py # String matching
│       │   │   ├── semantic.py    # Semantic similarity
│       │   │   ├── llm_judge.py   # LLM-based evaluation
│       │   │   ├── regex_grader.py# Regex patterns
│       │   │   └── code_exec.py   # Code execution
│       │   └── agents/            # Agent adapters
│       │       ├── __init__.py
│       │       ├── base.py        # Abstract base agent
│       │       ├── openai.py      # OpenAI adapter
│       │       ├── anthropic.py   # Anthropic adapter
│       │       ├── http.py        # Custom HTTP endpoint
│       │       └── mock.py        # Mock agent for testing
│       ├── models/
│       │   ├── __init__.py
│       │   ├── config.py          # Pydantic config models
│       │   └── results.py         # Result models
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── loader.py          # YAML/JSON file loading
│       │   ├── logger.py          # Logging setup
│       │   ├── validators.py      # Configuration validators
│       │   └── formatters.py      # Output formatting
│       └── api/
│           ├── __init__.py
│           └── server.py          # FastAPI server (optional)
├── dashboard/                    # Next.js web dashboard
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx         # Root layout
│   │   │   ├── page.tsx           # Home page
│   │   │   ├── projects/
│   │   │   │   ├── page.tsx       # Projects list
│   │   │   │   └── [id]/          # Project details
│   │   │   ├── results/
│   │   │   │   ├── page.tsx       # Results viewer
│   │   │   │   └── [id]/          # Result details
│   │   │   └── api/
│   │   │       └── trpc/          # tRPC API routes
│   │   ├── components/            # React components
│   │   │   ├── Header.tsx
│   │   │   ├── ResultsTable.tsx
│   │   │   ├── Charts.tsx
│   │   │   └── ...
│   │   ├── lib/
│   │   │   ├── trpc.ts            # tRPC client setup
│   │   │   ├── utils.ts           # Utilities
│   │   │   └── db.ts              # Database client
│   │   └── styles/
│   │       └── globals.css        # Tailwind CSS
│   ├── prisma/
│   │   ├── schema.prisma          # Database schema
│   │   ├── seed.ts                # Seed script
│   │   └── migrations/            # Database migrations
│   ├── public/                    # Static files
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── README.md
├── tests/
│   ├── unit/
│   │   ├── test_graders.py        # Grader tests
│   │   ├── test_agents.py         # Agent adapter tests
│   │   ├── test_config.py         # Configuration tests
│   │   └── test_utils.py          # Utility tests
│   ├── integration/
│   │   ├── test_evaluation.py     # End-to-end tests
│   │   ├── test_cli.py            # CLI tests
│   │   └── test_api.py            # API tests
│   └── fixtures/
│       ├── test_cases.yaml        # Test data
│       ├── agent_configs.yaml
│       ├── grader_configs.yaml
│       └── mock_responses.json
├── examples/
│   ├── basic/                     # Basic example
│   │   ├── agent.yaml
│   │   ├── tests.yaml
│   │   ├── graders.yaml
│   │   └── suite.yaml
│   ├── chatbot/                   # Chatbot evaluation
│   │   ├── agent.yaml
│   │   ├── tests.yaml
│   │   └── suite.yaml
│   ├── code-generator/            # Code generation testing
│   │   ├── agent.yaml
│   │   ├── tests.yaml
│   │   └── suite.yaml
│   └── translator/                # Translation testing
│       ├── agent.yaml
│       ├── tests.yaml
│       └── suite.yaml
├── docs/                          # Documentation
│   ├── api.md                     # API reference
│   ├── graders.md                 # Grader documentation
│   ├── agents.md                  # Agent adapter documentation
│   └── deployment.md              # Deployment guide
├── .github/
│   ├── workflows/
│   │   ├── tests.yml              # Test workflow
│   │   └── release.yml            # Release workflow
│   └── ISSUE_TEMPLATE/
├── .env.example                   # Environment template
├── .gitignore
├── .pre-commit-config.yaml        # Pre-commit hooks
├── pyproject.toml                 # Python project config
├── README.md                      # Main documentation
├── LANDING_PAGE.md                # Project overview
├── CONTRIBUTING.md                # Contributing guide
├── ARCHITECTURE.md                # Architecture overview
├── PROJECT_STRUCTURE.md           # This file
├── LICENSE                        # MIT License
└── .github/dependabot.yml         # Dependency updates
```

## Key Directories

### `/src/agent_eval`

Main Python package containing:

- **cli.py**: Command-line interface using Typer
- **core/**: Core evaluation logic
  - `evaluator.py`: Main evaluation engine that orchestrates tests
  - `graders/`: 5 different grading implementations
  - `agents/`: Adapters for different LLM providers
- **models/**: Pydantic models for configuration and results
- **utils/**: Helper functions for loading configs, logging, validation
- **api/**: Optional FastAPI server for remote evaluation

### `/dashboard`

Next.js web application for visualizing results:

- **src/app**: Next.js app router pages
- **src/components**: Reusable React components
- **src/lib**: Frontend utilities and tRPC setup
- **prisma**: Database schema and migrations

### `/tests`

Test suite with:

- **unit/**: Tests for individual components
- **integration/**: End-to-end tests
- **fixtures/**: Test data and mock responses

### `/examples`

Sample projects demonstrating different use cases:

- Basic evaluation
- Chatbot testing
- Code generation
- Translation

## File Naming Conventions

- **Python files**: `snake_case.py`
- **TypeScript/React files**: `PascalCase.tsx`
- **Configuration files**: `lowercase.yaml`
- **Test files**: `test_*.py`
- **Components**: `ComponentName.tsx`

## Architecture Patterns

### Grader System

```
BaseGrader (abstract)
├── ExactMatchGrader
├── SemanticSimilarityGrader
├── LLMJudgeGrader
├── RegexGrader
└── CodeExecutionGrader
```

All graders implement:
```python
class BaseGrader:
    def grade(self, expected: str, actual: str) -> dict:
        """Score the response (0-1)"""
```

### Agent System

```
BaseAgent (abstract)
├── OpenAIAgent
├── AnthropicAgent
├── HTTPAgent
└── MockAgent
```

All agents implement:
```python
class BaseAgent:
    async def evaluate(self, input_text: str) -> str:
        """Get response from agent"""
```

### Configuration Loading

```
YAML/JSON Files
    ↓
Pydantic Models (validation)
    ↓
Configuration Objects
    ↓
Evaluator / CLI
```

## Database Schema

Dashboard uses Prisma ORM with these main models:

```prisma
model Project {
  id        String     @id @default(cuid())
  name      String
  results   Result[]
  createdAt DateTime   @default(now())
}

model Result {
  id         String     @id @default(cuid())
  projectId  String
  project    Project    @relation(fields: [projectId], references: [id])
  testName   String
  status     String     # passed, failed, error
  score      Float      # 0-1
  details    Json
  createdAt  DateTime   @default(now())
}
```

## Development Workflow

1. **Make changes** to source code
2. **Run tests**: `pytest tests/`
3. **Format code**: `ruff format src/`
4. **Lint**: `ruff check src/`
5. **Type check**: `mypy src/`
6. **Commit**: `git commit -m "..."`

## Adding New Features

### Add a New Grader

1. Create `src/agent_eval/core/graders/my_grader.py`
2. Extend `BaseGrader`
3. Implement `grade()` method
4. Register in `graders/__init__.py`
5. Add tests in `tests/unit/test_graders.py`

### Add a New Agent Provider

1. Create `src/agent_eval/core/agents/my_agent.py`
2. Extend `BaseAgent`
3. Implement `evaluate()` method
4. Register in `agents/__init__.py`
5. Add tests in `tests/unit/test_agents.py`

### Add CLI Command

1. Add function in `src/agent_eval/cli.py`
2. Decorate with `@app.command()`
3. Document in CLI section
4. Add test in `tests/unit/test_cli.py`

## Dependency Graph

```
CLI (cli.py)
  ↓
Evaluator (core/evaluator.py)
  ├→ Agents (core/agents/)
  ├→ Graders (core/graders/)
  └→ Config Models (models/)
    ├→ Pydantic
    └→ Utils (utils/)
      ├→ YAML loader
      ├→ Logging
      └→ Validation

Dashboard
  ├→ tRPC API
  ├→ Prisma ORM
  ├→ SQLite Database
  └→ React Components
```

For more details, see [ARCHITECTURE.md](./ARCHITECTURE.md).
