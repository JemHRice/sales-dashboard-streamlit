"""
Unit tests for calculations.metrics module
Tests pure functions for YoY and MoM growth calculations
"""

import pytest
import pandas as pd
from calculations.metrics import calculate_yoy_growth, calculate_mom_change


class TestCalculateYoYGrowth:
    """Test Year-over-Year growth calculations"""

    def test_yoy_growth_with_positive_growth(self, sample_sales_df):
        """Test YoY calculation with positive growth (50% increase)"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=24, freq="ME"),
                "Sales": [100] * 12 + [150] * 12,  # 2023: $1200, 2024: $1800
            }
        )

        # Act
        result = calculate_yoy_growth(df, 2024, 2023)

        # Assert
        assert result == 50.0
        assert isinstance(result, float)

    def test_yoy_growth_with_negative_growth(self):
        """Test YoY calculation with negative growth (25% decline)"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=24, freq="ME"),
                "Sales": [200] * 12 + [150] * 12,  # 2023: $2400, 2024: $1800
            }
        )

        # Act
        result = calculate_yoy_growth(df, 2024, 2023)

        # Assert
        assert result == -25.0

    def test_yoy_growth_with_zero_growth(self):
        """Test YoY calculation with no growth (same sales)"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=24, freq="ME"),
                "Sales": [100] * 24,
            }
        )

        # Act
        result = calculate_yoy_growth(df, 2024, 2023)

        # Assert
        assert result == 0.0

    def test_yoy_growth_with_zero_previous_year(self):
        """Test YoY calculation when previous year has zero sales (avoid division by zero)"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=24, freq="ME"),
                "Sales": [0] * 12 + [100] * 12,
            }
        )

        # Act
        result = calculate_yoy_growth(df, 2024, 2023)

        # Assert
        assert result == 0.0  # Graceful handling, not inf or NaN

    def test_yoy_growth_with_empty_dataframe(self):
        """Test YoY calculation with empty DataFrame"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.Series([], dtype="datetime64[ns]"),
                "Sales": pd.Series([], dtype="float64"),
            }
        )

        # Act
        result = calculate_yoy_growth(df, 2024, 2023)

        # Assert
        assert result == 0.0

    def test_yoy_growth_with_custom_metric(self):
        """Test YoY calculation with custom metric column (not Sales)"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=24, freq="ME"),
                "Revenue": [100] * 12 + [200] * 12,
            }
        )

        # Act
        result = calculate_yoy_growth(df, 2024, 2023, metric_col="Revenue")

        # Assert
        assert result == 100.0  # 100% growth

    def test_yoy_growth_with_fractional_result(self):
        """Test YoY calculation with fractional percentage result"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=24, freq="ME"),
                "Sales": [100] * 12 + [133.33] * 12,
            }
        )

        # Act
        result = calculate_yoy_growth(df, 2024, 2023)

        # Assert
        assert abs(result - 33.33) < 0.01  # Allow small float precision difference


class TestCalculateMoMChange:
    """Test Month-over-Month growth calculations"""

    def test_mom_change_with_positive_growth(self):
        """Test MoM calculation with positive growth (50% increase)"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=12, freq="MS"),
                "Sales": [100] * 12,
            }
        )
        # Modify for testing: Jan = 100, Feb = 150
        df.loc[df["Order Date"].dt.month == 2, "Sales"] = 150.0

        # Act
        result = calculate_mom_change(df, (2023, 2), (2023, 1))

        # Assert
        assert result == 50.0

    def test_mom_change_with_negative_growth(self):
        """Test MoM calculation with negative growth (decline)"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=12, freq="MS"),
                "Sales": [100] * 12,
            }
        )
        df.loc[df["Order Date"].dt.month == 2, "Sales"] = 75.0

        # Act
        result = calculate_mom_change(df, (2023, 2), (2023, 1))

        # Assert
        assert result == -25.0

    def test_mom_change_with_zero_previous_month(self):
        """Test MoM calculation when previous month has zero sales"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=12, freq="MS"),
                "Sales": [100] * 12,
            }
        )
        df.loc[df["Order Date"].dt.month == 1, "Sales"] = 0.0

        # Act
        result = calculate_mom_change(df, (2023, 2), (2023, 1))

        # Assert
        assert result == 0.0

    def test_mom_change_with_zero_growth(self):
        """Test MoM calculation with no change"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=12, freq="MS"),
                "Sales": [100.0] * 12,
            }
        )

        # Act
        result = calculate_mom_change(df, (2023, 2), (2023, 1))

        # Assert
        assert result == 0.0

    def test_mom_change_across_year_boundary(self):
        """Test MoM calculation from December to January (year boundary)"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-12-01", periods=3, freq="MS"),
                "Sales": [200.0, 100.0, 150.0],
            }
        )

        # Act
        result = calculate_mom_change(df, (2024, 1), (2023, 12))

        # Assert
        assert result == -50.0  # 100 is 50% less than 200

    def test_mom_change_with_multiple_period_entries(self):
        """Test MoM calculation with multiple entries in same month"""
        # Arrange: Multiple entries per month
        df = pd.DataFrame(
            {
                "Order Date": pd.to_datetime(
                    ["2023-01-05", "2023-01-15", "2023-02-10", "2023-02-20"]
                ),
                "Sales": [50.0, 50.0, 100.0, 50.0],
            }
        )

        # Act
        result = calculate_mom_change(df, (2023, 2), (2023, 1))

        # Assert
        # Jan: 100, Feb: 150, so growth = 50%
        assert result == 50.0

    def test_mom_change_with_custom_metric(self):
        """Test MoM calculation with custom metric column"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": pd.date_range("2023-01-01", periods=12, freq="MS"),
                "Revenue": [100] * 12,
            }
        )
        df.loc[df["Order Date"].dt.month == 2, "Revenue"] = 200.0

        # Act
        result = calculate_mom_change(df, (2023, 2), (2023, 1), metric_col="Revenue")

        # Assert
        assert result == 100.0
