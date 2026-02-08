# Testing Suite for Sales Dashboard

## Overview

This directory contains comprehensive unit, integration, and UI tests for the sales dashboard application. The test suite targets **80%+ code coverage** and follows Test-Driven Development (TDD) principles.

## Directory Structure

```
tests/
├── conftest.py           # Shared pytest fixtures and configuration
├── unit/                 # Pure function tests (no dependencies)
│   ├── test_metrics.py       - YoY and MoM growth calculations
│   ├── test_aggregations.py  - Data aggregation functions
│   ├── test_validators.py    - CSV validation logic
│   └── test_loader.py        - Data loading and parsing
├── integration/          # End-to-end data pipeline tests
│   └── test_data_pipeline.py
├── ui/                   # UI tests with mocked Streamlit
│   └── test_charts.py
└── fixtures/             # Reusable test data and helpers
    ├── sample_data.py
    └── mock_streamlit.py
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test categories
```bash
# Unit tests only
pytest tests/unit -v

# Integration tests
pytest tests/integration -v

# UI tests
pytest tests/ui -v

# Specific test file
pytest tests/unit/test_metrics.py
```

### Run with coverage report
```bash
pytest --cov=calculations --cov=data --cov=utils --cov=visualization --cov-report=html
# Open htmlcov/index.html to view coverage
```

### Run only failed tests (TDD workflow)
```bash
pytest --lf
```

### Show slowest tests
```bash
pytest --durations=10
```

## Test-Driven Development Workflow

### 1. Write the test first
```python
def test_calculate_yoy_growth_with_positive_growth():
    # Arrange
    df = pd.DataFrame({ ... })
    
    # Act
    result = calculate_yoy_growth(df, 2024, 2023)
    
    # Assert
    assert result == 50.0
```

### 2. Run it (watch it fail)
```bash
pytest tests/unit/test_metrics.py -v
# FAILED - function doesn't exist yet
```

### 3. Write minimal code to pass
```python
def calculate_yoy_growth(df, current_year, previous_year, metric_col="Sales"):
    current = df[df["Order Date"].dt.year == current_year][metric_col].sum()
    previous = df[df["Order Date"].dt.year == previous_year][metric_col].sum()
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100
```

### 4. Watch test pass
```bash
pytest tests/unit/test_metrics.py -v
# PASSED ✓
```

### 5. Refactor if needed (tests stay green)

## Test Coverage Goals

| Module | Target | Strategy |
|--------|--------|----------|
| `calculations/metrics.py` | 100% | Test all branches, edge cases |
| `calculations/aggregations.py` | 95% | Mock Streamlit cache, test branches |
| `data/validators.py` | 100% | Test all validation paths |
| `data/loader.py` | 90% | Mock file I/O, test encodings |
| `visualization/charts.py` | 85% | Mock Plotly, test with empty data |
| **Overall** | **80%+** | Coverage report enforced in CI/CD |

## Available Fixtures

Fixtures are defined in [conftest.py](conftest.py) and automatically available to all tests:

- `sample_sales_df` - Valid DataFrame with typical data
- `empty_df` - DataFrame with no rows
- `missing_columns_df` - Invalid DataFrame structure
- `multi_year_df` - Data spanning multiple years
- `large_sales_df` - 10,000+ rows for performance testing
- `mock_file_system` - Temporary files for I/O testing
- `mock_streamlit` - Mocked Streamlit functions
- `mock_session_state` - Mocked session state

## Key Testing Principles

| Principle | Example |
|-----------|---------|
| **AAA Pattern** | Arrange, Act, Assert |
| **One assertion per test** | Focus on single behavior |
| **Descriptive names** | `test_yoy_growth_with_zero_previous_year` |
| **DRY with fixtures** | Reuse `sample_sales_df` everywhere |
| **Isolation** | No test interdependencies |
| **Mock externals** | Mock Streamlit, file I/O |

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/tests.yml`) runs:

1. **Unit tests** - All pure function tests
2. **Integration tests** - End-to-end data flows
3. **UI tests** - Chart rendering with mocks
4. **Coverage check** - Enforces 80% minimum
5. **Lint checks** - Code quality (flake8, pylint)
6. **Security scan** - Vulnerability detection (bandit, safety)

Coverage reports are automatically uploaded to Codecov.

## Mocking Strategy

### Streamlit Components

```python
@pytest.fixture
def mock_streamlit(monkeypatch):
    """Mock all Streamlit functions"""
    with patch('streamlit.write') as mock_write, \
         patch('streamlit.metric') as mock_metric:
        yield {'write': mock_write, 'metric': mock_metric}

# Usage in tests
def test_chart_creation(mock_streamlit):
    result = create_chart(data)
    assert result is not None
```

### File I/O

```python
@pytest.fixture
def mock_file_system(tmp_path):
    """Create temporary CSV files"""
    csv_file = tmp_path / "test.csv"
    df.to_csv(csv_file)
    return {'csv_file': csv_file}

# Usage
def test_load_csv(mock_file_system):
    result = load_data(mock_file_system['csv_file'])
    assert result is not None
```

## Debugging Tests

### Show print statements
```bash
pytest -s tests/unit/test_metrics.py
```

### Stop at first failure
```bash
pytest -x
```

### Drop into debugger on failure
```bash
pytest --pdb tests/unit/test_metrics.py
```

### Verbose output with full tracebacks
```bash
pytest -vv --tb=long
```

## Common Test Issues

### Issue: Streamlit cache decorator breaks tests
**Solution**: Mock `streamlit.cache_data`
```python
@patch('streamlit.cache_data', lambda f: f)
def test_function(self):
    ...
```

### Issue: File not found in tests
**Solution**: Use `tmp_path` fixture for temporary files
```python
def test_with_temp_file(tmp_path):
    test_file = tmp_path / "test.csv"
    ...
```

### Issue: Tests pass locally but fail in CI/CD
**Solution**: Check datetime/timezone handling and file paths
```python
# Use tmp_path instead of absolute paths
# Handle timezone-aware datetimes consistently
```

## Contributing Tests

When contributing new features:

1. **Write tests first** (TDD approach)
2. **Ensure 80%+ coverage** on new code
3. **Use fixtures** for common test data
4. **Follow naming conventions**
5. **Mock external dependencies**
6. **Run full test suite** before committing

```bash
# Quick verification before commit
pytest tests/ --cov=calculations --cov=data --cov-report=term-missing
```

## Performance Benchmarks

Run performance tests with:
```bash
pytest tests/ --durations=0
```

Target response times:
- Unit tests: < 0.1s per test
- Integration tests: < 0.5s per test
- All tests: < 10s total

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Unittest Mock](https://docs.python.org/3/library/unittest.mock.html)
- [Pandas Testing](https://pandas.pydata.org/docs/reference/testing.html)
- [Test-Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
