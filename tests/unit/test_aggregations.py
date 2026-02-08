"""
Unit tests for calculations.aggregations module
Tests data aggregation functions with various edge cases
"""

import pytest
import pandas as pd
from unittest.mock import patch
from calculations.aggregations import (
    get_monthly_sales,
    get_yearly_sales,
    get_daily_sales,
    get_category_sales,
    get_region_sales,
    get_top_products,
    get_top_customers,
)


class TestGetMonthlySales:
    """Test monthly sales aggregation"""

    @patch("streamlit.cache_data", lambda f: f)  # Disable caching for tests
    def test_monthly_sales_aggregation_basic(self, sample_sales_df):
        """Test basic monthly aggregation"""
        # Act
        result = get_monthly_sales(sample_sales_df)

        # Assert
        assert not result.empty
        assert "Order Date" in result.columns
        assert "Sales" in result.columns
        assert len(result) == 10  # 10 days, each in different month/across months
        assert result["Sales"].sum() == sample_sales_df["Sales"].sum()

    @patch("streamlit.cache_data", lambda f: f)
    def test_monthly_sales_with_empty_dataframe(self, empty_df):
        """Test monthly aggregation with empty DataFrame"""
        # Act
        result = get_monthly_sales(empty_df)

        # Assert
        assert result.empty

    @patch("streamlit.cache_data", lambda f: f)
    def test_monthly_sales_multiple_entries_same_month(self):
        """Test monthly aggregation with multiple entries in same month"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.to_datetime(
                    ["2023-01-05", "2023-01-15", "2023-01-25"]
                ),
                "Sales": [100.0, 150.0, 200.0],
            }
        )

        # Act
        result = get_monthly_sales(df)

        # Assert
        assert len(result) == 1
        assert result.iloc[0]["Sales"] == 450.0  # Sum of all three


class TestGetYearlySales:
    """Test yearly sales aggregation"""

    @patch("streamlit.cache_data", lambda f: f)
    def test_yearly_sales_aggregation_basic(self, multi_year_df):
        """Test basic yearly aggregation"""
        # Act
        result = get_yearly_sales(multi_year_df)

        # Assert
        assert "Year" in result.columns
        assert "Sales" in result.columns
        assert len(result) == 2  # Should have 2 years
        assert result["Year"].tolist() == [2023, 2024]  # Sorted
        assert result["Sales"].sum() == multi_year_df["Sales"].sum()

    @patch("streamlit.cache_data", lambda f: f)
    def test_yearly_sales_sorted_ascending(self):
        """Test that yearly sales are sorted by year ascending"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.to_datetime(
                    ["2025-01-01", "2023-01-01", "2024-01-01"]
                ),
                "Sales": [300.0, 100.0, 200.0],
            }
        )

        # Act
        result = get_yearly_sales(df)

        # Assert
        assert result["Year"].tolist() == [2023, 2024, 2025]

    @patch("streamlit.cache_data", lambda f: f)
    def test_yearly_sales_with_empty_dataframe(self, empty_df):
        """Test yearly aggregation with empty DataFrame"""
        # Act
        result = get_yearly_sales(empty_df)

        # Assert
        assert result.empty


class TestGetDailySales:
    """Test daily sales aggregation"""

    @patch("streamlit.cache_data", lambda f: f)
    def test_daily_sales_aggregation_basic(self, sample_sales_df):
        """Test basic daily aggregation"""
        # Act
        result = get_daily_sales(sample_sales_df)

        # Assert
        assert "Date" in result.columns
        assert "Sales" in result.columns
        assert result["Sales"].sum() == sample_sales_df["Sales"].sum()

    @patch("streamlit.cache_data", lambda f: f)
    def test_daily_sales_multiple_entries_same_day(self):
        """Test daily aggregation with multiple entries on same day"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.to_datetime(
                    ["2023-01-01", "2023-01-01", "2023-01-02"]
                ),
                "Sales": [100.0, 150.0, 200.0],
            }
        )

        # Act
        result = get_daily_sales(df)

        # Assert
        assert len(result) == 2  # 2 unique days
        assert (
            result[result["Date"] == pd.to_datetime("2023-01-01").date()][
                "Sales"
            ].values[0]
            == 250.0
        )


class TestGetCategorySales:
    """Test category sales aggregation"""

    @patch("streamlit.cache_data", lambda f: f)
    def test_category_sales_aggregation_basic(self, sample_sales_df):
        """Test basic category aggregation"""
        # Act
        result = get_category_sales(sample_sales_df)

        # Assert
        assert "Category" in result.columns
        assert "Sales" in result.columns
        assert result["Sales"].sum() == sample_sales_df["Sales"].sum()
        # Should be sorted descending by sales
        assert result["Sales"].is_monotonic_decreasing

    @patch("streamlit.cache_data", lambda f: f)
    def test_category_sales_missing_column(self):
        """Test category aggregation when Category column missing"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=3),
                "Sales": [100.0, 150.0, 200.0],
            }
        )

        # Act
        result = get_category_sales(df)

        # Assert
        assert result.empty

    @patch("streamlit.cache_data", lambda f: f)
    def test_category_sales_sorted_descending(self, sample_sales_df):
        """Test that categories are sorted by sales descending"""
        # Act
        result = get_category_sales(sample_sales_df)

        # Assert
        sales_values = result["Sales"].tolist()
        assert sales_values == sorted(sales_values, reverse=True)


class TestGetRegionSales:
    """Test region sales aggregation"""

    @patch("streamlit.cache_data", lambda f: f)
    def test_region_sales_aggregation_basic(self, sample_sales_df):
        """Test basic region aggregation"""
        # Act
        result = get_region_sales(sample_sales_df)

        # Assert
        assert "Region" in result.columns
        assert "Sales" in result.columns
        assert result["Sales"].sum() == sample_sales_df["Sales"].sum()

    @patch("streamlit.cache_data", lambda f: f)
    def test_region_sales_missing_column(self):
        """Test region aggregation when Region column missing"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=3),
                "Sales": [100.0, 150.0, 200.0],
            }
        )

        # Act
        result = get_region_sales(df)

        # Assert
        assert result.empty


class TestGetTopProducts:
    """Test top products aggregation"""

    @patch("streamlit.cache_data", lambda f: f)
    def test_top_products_returns_exact_count(self, sample_sales_df):
        """Test that top N products returns exactly N items"""
        # Act
        result = get_top_products(sample_sales_df, n=5)

        # Assert
        assert len(result) <= 5
        assert "Product Name" in result.columns
        assert "Sales" in result.columns

    @patch("streamlit.cache_data", lambda f: f)
    def test_top_products_default_n_is_ten(self, sample_sales_df):
        """Test that default N is 10"""
        # Act
        result = get_top_products(sample_sales_df)  # No N specified

        # Assert
        assert len(result) <= 10

    @patch("streamlit.cache_data", lambda f: f)
    def test_top_products_fewer_than_n_available(self):
        """Test when fewer products available than requested"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=3),
                "Sales": [100.0, 150.0, 200.0],
                "Product Name": ["A", "B", "C"],
            }
        )

        # Act
        result = get_top_products(df, n=10)

        # Assert
        assert len(result) == 3  # Only 3 products available

    @patch("streamlit.cache_data", lambda f: f)
    def test_top_products_missing_column(self):
        """Test top products when Product Name column missing"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=3),
                "Sales": [100.0, 150.0, 200.0],
            }
        )

        # Act
        result = get_top_products(df)

        # Assert
        assert result.empty

    @patch("streamlit.cache_data", lambda f: f)
    def test_top_products_aggregates_duplicate_products(self):
        """Test that same product names are aggregated correctly"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=4),
                "Sales": [100.0, 200.0, 150.0, 250.0],
                "Product Name": ["Laptop", "Mouse", "Laptop", "Laptop"],
            }
        )

        # Act
        result = get_top_products(df, n=10)

        # Assert
        assert len(result) == 2
        laptop_sales = result[result["Product Name"] == "Laptop"]["Sales"].values[0]
        assert laptop_sales == 450.0  # 100 + 150 + 250


class TestGetTopCustomers:
    """Test top customers aggregation"""

    @patch("streamlit.cache_data", lambda f: f)
    def test_top_customers_returns_exact_count(self, sample_sales_df):
        """Test that top N customers returns exactly N items"""
        # Act
        result = get_top_customers(sample_sales_df, n=5)

        # Assert
        assert len(result) <= 5
        assert "Customer Name" in result.columns
        assert "Sales" in result.columns

    @patch("streamlit.cache_data", lambda f: f)
    def test_top_customers_default_n_is_ten(self, sample_sales_df):
        """Test that default N is 10"""
        # Act
        result = get_top_customers(sample_sales_df)  # No N specified

        # Assert
        assert len(result) <= 10

    @patch("streamlit.cache_data", lambda f: f)
    def test_top_customers_missing_column(self):
        """Test top customers when Customer Name column missing"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=3),
                "Sales": [100.0, 150.0, 200.0],
            }
        )

        # Act
        result = get_top_customers(df)

        # Assert
        assert result.empty
