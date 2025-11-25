# Contributing to Analytics Tutorials

Thank you for your interest in contributing to the Analytics Tutorials project! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites
- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Git

### Setting Up Your Development Environment

1. **Fork and clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/analytics_tutorials.git
cd analytics_tutorials
```

2. **Install uv (if not already installed)**
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Create a virtual environment and install dependencies**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[all]"
```

4. **Install pre-commit hooks**
```bash
pre-commit install
```

5. **Generate test data**
```bash
python setup_database.py
```

## Code Quality Standards

We use several tools to maintain code quality:

### Linting with Ruff

Ruff is our primary linter for catching errors and enforcing style:

```bash
# Check for issues
ruff check .

# Auto-fix issues where possible
ruff check . --fix

# Check formatting
ruff format --check .

# Apply formatting
ruff format .
```

### Formatting with Black

Black ensures consistent code formatting:

```bash
# Check formatting
black --check .

# Apply formatting
black .
```

### Running All Quality Checks

```bash
# Run all checks
ruff check . && ruff format --check . && black --check .
```

## Testing

### Running Tests

We use pytest for testing:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=term-missing

# Run specific test file
pytest tests/test_setup.py

# Run tests in parallel (faster)
pytest -n auto

# Run only fast tests (skip slow ones)
pytest -m "not slow"
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_*.py` or `*_test.py`
- Name test functions with `test_*`
- Use descriptive test names that explain what is being tested

Example test:
```python
def test_data_generation_creates_valid_dataframe():
    """Test that data generation produces a valid Polars DataFrame."""
    df = generate_insurance_claims(n_records=100)
    
    assert isinstance(df, pl.DataFrame)
    assert len(df) == 100
    assert "claim_id" in df.columns
```

### Test Markers

We use pytest markers to categorize tests:

- `@pytest.mark.slow` - For tests that take significant time
- `@pytest.mark.integration` - For integration tests

## Pre-commit Hooks

Pre-commit hooks automatically run quality checks before each commit:

```bash
# Install hooks (one-time setup)
pre-commit install

# Run hooks manually on all files
pre-commit run --all-files

# Update hooks to latest versions
pre-commit autoupdate
```

The hooks will:
- Check for trailing whitespace
- Ensure files end with newline
- Validate YAML, JSON, and TOML files
- Run Ruff linter and formatter
- Run Black formatter
- Run basic pytest checks

## Continuous Integration

All pull requests are automatically tested using GitHub Actions:

- **Linting and Formatting**: Checks code style with Ruff and Black
- **Tests**: Runs pytest on multiple Python versions (3.8-3.12) and OS platforms
- **Tutorial Validation**: Ensures tutorial scripts are syntactically correct

View the CI configuration in `.github/workflows/ci.yml`.

## Contributing Guidelines

### Creating a Pull Request

1. **Create a new branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
   - Write clear, concise code
   - Add tests for new functionality
   - Update documentation as needed

3. **Run quality checks**
```bash
ruff check . --fix
black .
pytest
```

4. **Commit your changes**
```bash
git add .
git commit -m "Add feature: description of your changes"
```

5. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

6. **Open a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template with details

### Pull Request Checklist

- [ ] Code follows project style guidelines (Ruff + Black)
- [ ] Tests pass locally (`pytest`)
- [ ] New tests added for new functionality
- [ ] Documentation updated (README, docstrings, etc.)
- [ ] Pre-commit hooks pass
- [ ] Commit messages are clear and descriptive

### Code Style Guidelines

- **Line length**: Maximum 100 characters
- **Imports**: Organized with `ruff` (stdlib, third-party, local)
- **Docstrings**: Use Google-style docstrings for functions and classes
- **Type hints**: Use type hints where appropriate
- **Naming**: 
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

### Tutorial Guidelines

When adding new tutorials:

1. Place Python scripts in appropriate difficulty folder:
   - `tutorials/01_beginner/`
   - `tutorials/02_intermediate/`
   - `tutorials/03_advanced/`

2. Include comprehensive comments explaining each step

3. Add corresponding entry to `TUTORIAL_INDEX.md`

4. Generate notebook version:
```bash
python convert_to_notebooks.py
```

5. Test the tutorial runs without errors:
```bash
python tutorials/path/to/your_tutorial.py
```

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)
- Relevant code snippets

## Questions?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Be respectful and constructive in discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Analytics Tutorials! 🎉
