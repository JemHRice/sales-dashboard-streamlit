"""
Shared pytest fixtures for all tests
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch


@pytest.fixture
def sample_sales_df():
    """
    Minimal valid DataFrame for testing with all expected columns
    """
    return pd.DataFrame(
        {
            "Order Date": pd.date_range("2023-01-01", periods=10),
            "Sales": [
                100.0,
                150.0,
                200.0,
                120.0,
                180.0,
                220.0,
                190.0,
                160.0,
                210.0,
                175.0,
            ],
            "Category": [
                "Electronics",
                "Furniture",
                "Electronics",
                "Office Supplies",
                "Furniture",
                "Electronics",
                "Office Supplies",
                "Furniture",
                "Electronics",
                "Office Supplies",
            ],
            "Region": [
                "East",
                "West",
                "East",
                "South",
                "North",
                "East",
                "South",
                "West",
                "North",
                "East",
            ],
            "Product Name": [
                "Laptop",
                "Desk",
                "Monitor",
                "Pen Set",
                "Chair",
                "Keyboard",
                "Notebook",
                "Cabinet",
                "Mouse",
                "Stapler",
            ],
            "Customer Name": [
                "Alice",
                "Bob",
                "Charlie",
                "David",
                "Eve",
                "Frank",
                "Grace",
                "Henry",
                "Ivy",
                "Jack",
            ],
        }
    )


@pytest.fixture
def empty_df():
    """DataFrame with no rows but correct columns"""
    return pd.DataFrame(
        {
            "Order Date": pd.Series([], dtype="datetime64[ns]"),
            "Sales": pd.Series([], dtype="float64"),
        }
    )


@pytest.fixture
def missing_columns_df():
    """DataFrame missing required columns"""
    return pd.DataFrame(
        {
            "Product": ["A", "B", "C"],
            "Value": [100.0, 200.0, 300.0],
        }
    )


@pytest.fixture
def invalid_sales_df():
    """DataFrame with non-numeric Sales column"""
    return pd.DataFrame(
        {
            "Order Date": pd.date_range("2023-01-01", periods=3),
            "Sales": ["$100", "invalid", "$300"],
        }
    )


@pytest.fixture
def string_date_df():
    """DataFrame with dates as strings instead of datetime"""
    return pd.DataFrame(
        {
            "Order Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "Sales": [100.0, 150.0, 200.0],
        }
    )


@pytest.fixture
def multi_year_df():
    """DataFrame spanning multiple years for YoY calculations"""
    dates_2023 = pd.date_range("2023-01-01", "2023-12-31", freq="M")
    dates_2024 = pd.date_range("2024-01-01", "2024-12-31", freq="M")
    dates = pd.concat([pd.Series(dates_2023), pd.Series(dates_2024)]).reset_index(
        drop=True
    )

    return pd.DataFrame(
        {
            "Order Date": dates,
            "Sales": [100 + i * 10 for i in range(len(dates))],
        }
    )


@pytest.fixture
def large_sales_df():
    """Larger DataFrame for performance testing"""
    n_records = 10000
    return pd.DataFrame(
        {
            "Order Date": pd.date_range("2020-01-01", periods=n_records, freq="h"),
            "Sales": [100.0 + (i % 500) for i in range(n_records)],
            "Category": ["Electronics", "Furniture", "Office Supplies"]
            * (n_records // 3 + 1),
            "Region": ["East", "West", "North", "South"] * (n_records // 4 + 1),
            "Product Name": [f"Product_{i % 50}" for i in range(n_records)],
            "Customer Name": [f"Customer_{i % 100}" for i in range(n_records)],
        }
    )[:n_records]


@pytest.fixture
def mock_streamlit(monkeypatch):
    """
    Mock Streamlit functions to avoid UI side effects during testing
    """
    with patch("streamlit.write") as mock_write, patch(
        "streamlit.metric"
    ) as mock_metric, patch("streamlit.plotly_chart") as mock_plotly, patch(
        "streamlit.title"
    ) as mock_title, patch(
        "streamlit.markdown"
    ) as mock_markdown, patch(
        "streamlit.cache_data"
    ) as mock_cache:

        # Make cache_data a passthrough decorator
        mock_cache.side_effect = lambda f: f

        yield {
            "write": mock_write,
            "metric": mock_metric,
            "plotly_chart": mock_plotly,
            "title": mock_title,
            "markdown": mock_markdown,
            "cache_data": mock_cache,
        }


@pytest.fixture
def mock_file_system(tmp_path):
    """
    Create a temporary file system for testing file operations
    """
    csv_file = tmp_path / "test_data.csv"
    sample_data = pd.DataFrame(
        {
            "Order Date": pd.date_range("2023-01-01", periods=5),
            "Sales": [100.0, 150.0, 200.0, 120.0, 180.0],
        }
    )
    sample_data.to_csv(csv_file, index=False)

    return {
        "csv_file": csv_file,
        "tmp_path": tmp_path,
    }


@pytest.fixture
def mock_file_system_with_encoding(tmp_path):
    """
    Create test files with different encodings
    """
    # UTF-8 file
    utf8_file = tmp_path / "test_utf8.csv"
    df = pd.DataFrame(
        {
            "Order Date": pd.date_range("2023-01-01", periods=3),
            "Sales": [100.0, 150.0, 200.0],
        }
    )
    df.to_csv(utf8_file, index=False, encoding="utf-8")

    # File with BOM
    with_bom_file = tmp_path / "test_bom.csv"
    df.to_csv(with_bom_file, index=False, encoding="utf-8-sig")

    return {
        "utf8": utf8_file,
        "with_bom": with_bom_file,
        "tmp_path": tmp_path,
    }


@pytest.fixture
def mock_session_state(monkeypatch):
    """Mock Streamlit session state"""
    mock_state = {}

    def setitem(key, value):
        mock_state[key] = value

    def getitem(key):
        return mock_state.get(key)

    def contains(key):
        return key in mock_state

    mock_session = MagicMock()
    mock_session.__setitem__ = setitem
    mock_session.__getitem__ = getitem
    mock_session.__contains__ = contains

    monkeypatch.setattr("streamlit.session_state", mock_session)
    return mock_session
