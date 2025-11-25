# Tests

This directory contains the test suite for the Analytics Tutorials project.

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_setup.py

# Run specific test function
pytest tests/test_setup.py::test_python_version
```

### Coverage Reports

```bash
# Run tests with coverage
pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser

# Generate XML coverage report (for CI)
pytest --cov=. --cov-report=xml
```

### Parallel Execution

```bash
# Run tests in parallel (faster)
pytest -n auto

# Run with specific number of workers
pytest -n 4
```

### Test Filtering

```bash
# Run only fast tests (skip slow ones)
pytest -m "not slow"

# Run only integration tests
pytest -m integration

# Run tests matching pattern
pytest -k "test_data"
```

## Test Structure

```
tests/
├── __init__.py
├── README.md (this file)
├── test_setup.py           # Basic setup and dependency tests
├── test_data_generators.py # Data generation utility tests
└── ...                     # Additional test files
```

## Writing Tests

### Test Naming Convention

- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_*`
- Test classes: `Test*`

### Example Test

```python
import pytest
import polars as pl


def test_example_function():
    """Test that example function works correctly."""
    result = example_function(input_data)
    
    assert result is not None
    assert isinstance(result, pl.DataFrame)
    assert len(result) > 0


@pytest.mark.slow
def test_slow_operation():
    """Test that takes significant time to run."""
    # This test will be skipped when running: pytest -m "not slow"
    pass


@pytest.mark.integration
def test_database_integration():
    """Test database integration."""
    # This test requires database setup
    pass
```

### Test Markers

Available markers:
- `@pytest.mark.slow` - For tests that take significant time
- `@pytest.mark.integration` - For integration tests requiring external resources

## Test Categories

### Unit Tests
- Test individual functions and classes
- Fast execution
- No external dependencies
- Example: `test_setup.py`

### Integration Tests
- Test interaction between components
- May require database or external services
- Marked with `@pytest.mark.integration`

### Data Generation Tests
- Verify data generation utilities work correctly
- Ensure generated data has expected structure
- Example: `test_data_generators.py`

## Continuous Integration

Tests are automatically run on GitHub Actions for:
- Multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)
- Multiple operating systems (Ubuntu, Windows, macOS)

See `.github/workflows/ci.yml` for CI configuration.

## Coverage Goals

- Aim for >80% code coverage
- Focus on critical paths and edge cases
- Don't sacrifice test quality for coverage percentage

## Troubleshooting

### Import Errors

If you get import errors, ensure the project is installed in editable mode:
```bash
uv pip install -e ".[dev]"
```

### Missing Test Data

Generate test data before running tests:
```bash
python setup_database.py
```

### Slow Test Execution

Use parallel execution:
```bash
pytest -n auto
```

Or skip slow tests:
```bash
pytest -m "not slow"
```

## Contributing Tests

When adding new features:
1. Write tests for new functionality
2. Ensure tests pass locally
3. Check coverage hasn't decreased significantly
4. Follow existing test patterns and naming conventions

See [CONTRIBUTING.md](../CONTRIBUTING.md) for more details.
