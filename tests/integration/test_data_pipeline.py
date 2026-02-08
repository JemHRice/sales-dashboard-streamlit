"""
Integration tests for data pipeline
Tests end-to-end data flow from loading to visualization
"""

import pytest
import pandas as pd
from unittest.mock import patch
from data.loader import load_data, clean_dataframe_columns
from data.validators import validate_csv, validate_sales_column, validate_date_column
from calculations.metrics import calculate_yoy_growth
from calculations.aggregations import (
    get_monthly_sales,
    get_yearly_sales,
    get_category_sales,
)


class TestDataPipeline:
    """Test complete data processing pipeline"""

    @patch("streamlit.cache_data", lambda f: f)
    def test_load_validate_aggregate_pipeline(self, mock_file_system):
        """Test full pipeline: load -> validate -> aggregate"""
        # This is a conceptual test showing integration
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=10),
                "Sales": [100.0 + i * 10 for i in range(10)],
                "Category": ["A"] * 5 + ["B"] * 5,
            }
        )

        # Act - Validate
        is_valid, msg = validate_csv(df)
        assert is_valid

        # Act - Aggregate
        monthly = get_monthly_sales(df)
        yearly = get_yearly_sales(df)

        # Assert
        assert not monthly.empty
        assert not yearly.empty
        assert monthly["Sales"].sum() == df["Sales"].sum()
        assert yearly["Sales"].sum() == df["Sales"].sum()

    @patch("streamlit.cache_data", lambda f: f)
    def test_yoy_calculation_pipeline(self):
        """Test YoY calculation with multi-year data pipeline"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", "2024-12-31", freq="D"),
                "Sales": [100.0] * 365 + [150.0] * 366,  # 2024 is leap year
            }
        )

        # Act - Calculate YoY
        growth = calculate_yoy_growth(df, 2024, 2023)

        # Assert - Should show 50% growth
        assert growth == 50.0

    @patch("streamlit.cache_data", lambda f: f)
    def test_validation_chain(self, sample_sales_df):
        """Test that all validation checks pass for valid data"""
        # Act
        csv_valid, msg = validate_csv(sample_sales_df)
        validate_sales_column(sample_sales_df)
        validate_date_column(sample_sales_df)

        # Assert
        assert csv_valid is True

    def test_column_cleaning_then_validation(self):
        """Test cleaning columns then validating"""
        # Arrange
        df = pd.DataFrame(
            {
                " order date ": pd.date_range("2023-01-01", periods=3),
                " Sales ": [100.0, 200.0, 300.0],
                "Category": ["A", "B", "C"],
            }
        )

        # Act
        df_cleaned, date_found = clean_dataframe_columns(df)
        is_valid, msg = validate_csv(df_cleaned)

        # Assert
        assert date_found is True
        assert is_valid is True
        assert "Order Date" in df_cleaned.columns

    @patch("streamlit.cache_data", lambda f: f)
    def test_aggregation_chain(self, sample_sales_df):
        """Test multiple aggregations on same data"""
        # Act
        monthly = get_monthly_sales(sample_sales_df)
        category = get_category_sales(sample_sales_df)

        # Assert
        assert not monthly.empty
        assert not category.empty
        assert monthly["Sales"].sum() == sample_sales_df["Sales"].sum()
        assert category["Sales"].sum() == sample_sales_df["Sales"].sum()
