# Contributing to Agent-Eval

We love your input! We want to make contributing to Agent-Eval as easy and transparent as possible.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Commit Messages](#commit-messages)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [issue list](https://github.com/nurettinsoker/-agent-eval/issues) as you might find out that you don't need to create one.

When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs if possible**
- **Include your environment details** (OS, Python version, etc.)

**Example:**
```
Title: agent-eval crashes when running with OpenAI API key

Steps to reproduce:
1. Set OPENAI_API_KEY env variable
2. Run agent-eval run suite.yaml --agent agent.yaml
3. See error

Expected: Evaluation completes successfully
Actual: Program crashes with traceback...

Environment:
- OS: Ubuntu 22.04
- Python: 3.11.0
- agent-eval: 0.1.0
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Follow the Python and TypeScript styleguides
- Include appropriate test cases
- Update documentation accordingly
- End all files with a newline

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- pnpm
- Git

### Setup Steps

1. **Fork the repository**

```bash
git clone https://github.com/your-username/-agent-eval.git
cd -agent-eval
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies with dev tools**

```bash
# Install package with dev dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install
```

4. **Setup dashboard (optional)**

```bash
cd dashboard
pnpm install
npx prisma migrate dev
cd ..
```

5. **Create .env file**

```bash
cp .env.example .env
# Edit .env with your settings
```

## Making Changes

### Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming convention:
- `feature/feature-name` - New feature
- `fix/bug-description` - Bug fix
- `docs/what-to-document` - Documentation
- `test/what-to-test` - Tests
- `chore/what-to-improve` - Code cleanup, refactoring

### Make Your Changes

1. Make your code changes
2. Write or update tests
3. Run tests locally
4. Update documentation

## Pull Request Process

1. **Update tests**
   - Add tests for new features
   - Update existing tests if needed
   - Ensure all tests pass: `pytest`

2. **Update documentation**
   - Update README.md if needed
   - Add/update code comments
   - Document new CLI commands or configs

3. **Format and lint**
   ```bash
   # Format code
   ruff format src/ tests/
   
   # Run linter
   ruff check src/ tests/
   
   # Type check
   mypy src/
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "type: description"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Fill in the PR template
   - Reference any related issues
   - Wait for review

### Before Submitting

- [ ] Code follows the styleguides
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No new warnings are introduced
- [ ] Branch is up-to-date with `main`

## Coding Standards

### Python Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these tools:

- **Formatter**: `ruff format`
- **Linter**: `ruff check`
- **Type checker**: `mypy`

**Example:**

```python
"""Module docstring."""

from typing import Optional

from pydantic import BaseModel


class MyModel(BaseModel):
    """Model description."""
    
    name: str
    value: Optional[int] = None


def my_function(text: str) -> str:
    """Function description.
    
    Args:
        text: Input text.
        
    Returns:
        Processed text.
    """
    return text.strip().lower()
```

### TypeScript Code Style

We follow these conventions:

- Use TypeScript strict mode
- Use React functional components with hooks
- Use const/let (no var)
- Prefer interfaces over types
- Add JSDoc comments for public functions

**Example:**

```typescript
/**
 * Process user data.
 * @param data - User data
 * @returns Processed result
 */
export const processUserData = (data: UserData): Result => {
  return {
    ...data,
    processed: true,
  };
};
```

### Configuration File Format

Configuration files (agent.yaml, tests.yaml) should:
- Use 2-space indentation
- Include comments for complex sections
- Provide examples

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_graders.py

# Run with coverage
pytest --cov=src/agent_eval

# Run with verbose output
pytest -v
```

### Writing Tests

```python
import pytest
from agent_eval.core.graders import ExactMatchGrader


class TestExactMatchGrader:
    """Tests for ExactMatchGrader."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.grader = ExactMatchGrader(case_sensitive=False)
    
    def test_exact_match_success(self):
        """Test exact match with identical strings."""
        result = self.grader.grade("hello", "hello")
        assert result["passed"] is True
        assert result["score"] == 1.0
    
    def test_case_insensitive(self):
        """Test case-insensitive matching."""
        result = self.grader.grade("Hello", "hello")
        assert result["passed"] is True
```

### Test Structure

- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test components working together
- **Fixtures**: Share test data and setup

## Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

Optional body

Optional footer
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning
- `refactor`: Code change that neither fixes bugs nor adds features
- `perf`: Code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to build process, dependencies, etc.

### Examples

```
feat(graders): add regex grader implementation

Implement RegexGrader that validates responses against
regular expression patterns.

Closes #123
```

```
fix(cli): handle missing config files gracefully

Previously crashed with unhelpful error. Now provides
clear error message suggesting solution.
```

```
docs: update README with new examples
```

## Code Review Process

After you submit your pull request:

1. At least one maintainer will review your code
2. We may ask for changes, clarifications, or improvements
3. Address feedback and push new commits
4. Once approved, your PR will be merged

## Questions?

Feel free to:

- Open an [issue](https://github.com/nurettinsoker/-agent-eval/issues)
- Start a [discussion](https://github.com/nurettinsoker/-agent-eval/discussions)
- Email: nurettinsoker@gmail.com

## Additional Notes

### Issue and Pull Request Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested

### Community

We're building a great community! Feel free to:
- Ask questions in discussions
- Share your projects using Agent-Eval
- Report bugs and suggest features
- Help review pull requests

Thank you for contributing to Agent-Eval! 🎉
