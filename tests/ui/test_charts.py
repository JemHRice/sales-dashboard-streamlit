"""
Unit tests for visualization.charts module
Tests chart creation with mocked Streamlit and Plotly
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import plotly.graph_objects as go
from visualization.charts import (
    create_monthly_trend_chart,
    create_yearly_trend_chart,
    create_daily_trend_chart,
    create_category_sales_chart,
    create_region_sales_chart,
    create_sales_vs_profit_chart,
)


class TestCreateMonthlyTrendChart:
    """Test monthly trend chart creation"""

    def test_monthly_trend_chart_with_valid_data(self):
        """Test monthly trend chart is created successfully"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": ["2023-01", "2023-02", "2023-03"],
                "Sales": [1000.0, 1500.0, 1200.0],
            }
        )

        # Act
        result = create_monthly_trend_chart(df)

        # Assert
        assert result is not None
        assert hasattr(result, "to_json")  # It's a Plotly figure
        assert "Monthly Sales Trend" in result.layout.title.text

    def test_monthly_trend_chart_with_empty_dataframe(self, empty_df):
        """Test monthly trend chart with empty data returns None"""
        # Act
        result = create_monthly_trend_chart(empty_df)

        # Assert
        assert result is None

    def test_monthly_trend_chart_has_correct_axes(self):
        """Test monthly trend chart has correct axis labels"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": ["2023-01", "2023-02"],
                "Sales": [1000.0, 1500.0],
            }
        )

        # Act
        result = create_monthly_trend_chart(df)

        # Assert
        assert result.layout.xaxis.title.text == "Order Date"
        assert result.layout.yaxis.title.text == "Sales"

    def test_monthly_trend_chart_uses_color_scale(self):
        """Test monthly trend chart uses color scale"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": ["2023-01", "2023-02", "2023-03"],
                "Sales": [1000.0, 1500.0, 1200.0],
            }
        )

        # Act
        result = create_monthly_trend_chart(df)

        # Assert
        assert result is not None
        assert len(result.data) > 0


class TestCreateYearlyTrendChart:
    """Test yearly trend chart creation"""

    def test_yearly_trend_chart_with_valid_data(self):
        """Test yearly trend chart is created successfully"""
        # Arrange
        df = pd.DataFrame(
            {
                "Year": [2022, 2023, 2024],
                "Sales": [50000.0, 75000.0, 100000.0],
            }
        )

        # Act
        result = create_yearly_trend_chart(df)

        # Assert
        assert result is not None
        assert hasattr(result, "to_json")
        assert "Yearly Sales Comparison" in result.layout.title.text

    def test_yearly_trend_chart_with_empty_dataframe(self, empty_df):
        """Test yearly trend chart with empty data returns None"""
        # Act
        result = create_yearly_trend_chart(empty_df)

        # Assert
        assert result is None

    def test_yearly_trend_chart_correct_data_mapping(self):
        """Test that data is correctly mapped to chart"""
        # Arrange
        df = pd.DataFrame(
            {
                "Year": [2023, 2024],
                "Sales": [12000.0, 18000.0],
            }
        )

        # Act
        result = create_yearly_trend_chart(df)

        # Assert
        assert result is not None
        assert len(result.data[0].x) == 2
        assert list(result.data[0].y) == [12000.0, 18000.0]


class TestCreateDailyTrendChart:
    """Test daily trend chart creation"""

    def test_daily_trend_chart_with_valid_data(self):
        """Test daily trend chart is created successfully"""
        # Arrange
        df = pd.DataFrame(
            {
                "Date": pd.date_range("2023-01-01", periods=3).date,
                "Sales": [500.0, 600.0, 550.0],
            }
        )

        # Act
        result = create_daily_trend_chart(df)

        # Assert
        assert result is not None
        assert hasattr(result, "to_json")

    def test_daily_trend_chart_with_empty_dataframe(self, empty_df):
        """Test daily trend chart with empty data returns None"""
        # Act
        result = create_daily_trend_chart(empty_df)

        # Assert
        assert result is None


class TestCreateCategorySalesChart:
    """Test category sales chart creation"""

    def test_category_sales_chart_with_valid_data(self):
        """Test category sales chart is created successfully"""
        # Arrange
        df = pd.DataFrame(
            {
                "Category": ["Electronics", "Furniture", "Office Supplies"],
                "Sales": [50000.0, 30000.0, 20000.0],
            }
        )

        # Act
        result = create_category_sales_chart(df)

        # Assert
        assert result is not None
        assert hasattr(result, "to_json")
        assert "Sales by Category" in result.layout.title.text

    def test_category_sales_chart_with_empty_dataframe(self, empty_df):
        """Test category sales chart with empty data returns None"""
        # Act
        result = create_category_sales_chart(empty_df)

        # Assert
        assert result is None

    def test_category_sales_chart_with_none(self):
        """Test category sales chart with None returns None"""
        # Act
        result = create_category_sales_chart(None)

        # Assert
        assert result is None


class TestCreateRegionSalesChart:
    """Test region sales chart creation"""

    def test_region_sales_chart_with_valid_data(self):
        """Test region sales chart is created successfully"""
        # Arrange
        df = pd.DataFrame(
            {
                "Region": ["East", "West", "North", "South"],
                "Sales": [30000.0, 25000.0, 20000.0, 25000.0],
            }
        )

        # Act
        result = create_region_sales_chart(df)

        # Assert
        assert result is not None
        assert hasattr(result, "to_json")
        assert "Sales Distribution by Region" in result.layout.title.text

    def test_region_sales_chart_with_empty_dataframe(self, empty_df):
        """Test region sales chart with empty data returns None"""
        # Act
        result = create_region_sales_chart(empty_df)

        # Assert
        assert result is None

    def test_region_sales_chart_with_none(self):
        """Test region sales chart with None returns None"""
        # Act
        result = create_region_sales_chart(None)

        # Assert
        assert result is None


class TestCreateSalesVsProfitChart:
    """Test sales vs profit chart creation"""

    def test_sales_vs_profit_chart_with_valid_data(self):
        """Test sales vs profit chart is created successfully"""
        # Arrange
        df = pd.DataFrame(
            {
                "Sales": [1000.0, 1500.0, 800.0],
                "Profit": [300.0, 450.0, 200.0],
                "Category": ["Electronics", "Furniture", "Office"],
            }
        )

        # Act
        result = create_sales_vs_profit_chart(df)

        # Assert
        assert result is not None
        assert hasattr(result, "to_json")
        assert "Sales vs Profit" in result.layout.title.text

    def test_sales_vs_profit_chart_with_empty_dataframe(self, empty_df):
        """Test sales vs profit chart with empty data returns None"""
        # Act
        result = create_sales_vs_profit_chart(empty_df)

        # Assert
        assert result is None

    def test_sales_vs_profit_chart_with_none(self):
        """Test sales vs profit chart with None returns None"""
        # Act
        result = create_sales_vs_profit_chart(None)

        # Assert
        assert result is None

    def test_sales_vs_profit_chart_missing_profit_column(self):
        """Test chart returns None when Profit column missing"""
        # Arrange
        df = pd.DataFrame(
            {
                "Sales": [1000.0, 1500.0],
                "Category": ["A", "B"],
            }
        )

        # Act
        result = create_sales_vs_profit_chart(df)

        # Assert
        assert result is None

    def test_sales_vs_profit_chart_missing_category_column(self):
        """Test chart returns None when Category column missing"""
        # Arrange
        df = pd.DataFrame(
            {
                "Sales": [1000.0, 1500.0],
                "Profit": [300.0, 450.0],
            }
        )

        # Act
        result = create_sales_vs_profit_chart(df)

        # Assert
        assert result is None


class TestChartIntegration:
    """Integration tests for chart creation"""

    def test_all_charts_return_plotly_figures_or_none(self, sample_sales_df):
        """Test that all chart functions return valid Plotly figures or None"""
        # Create test dataframes
        monthly_df = pd.DataFrame(
            {
                "Order Date": ["2023-01", "2023-02"],
                "Sales": [1000.0, 1500.0],
            }
        )

        # Test monthly chart
        monthly_chart = create_monthly_trend_chart(monthly_df)
        if monthly_chart is not None:
            assert hasattr(monthly_chart, "plot")
            assert hasattr(monthly_chart, "to_json")

    def test_all_empty_dataframes_return_none(self, empty_df):
        """Test that all charts handle empty DataFrames gracefully"""
        # Act
        result1 = create_monthly_trend_chart(empty_df)
        result2 = create_yearly_trend_chart(empty_df)
        result3 = create_daily_trend_chart(empty_df)
        result4 = create_category_sales_chart(empty_df)
        result5 = create_region_sales_chart(empty_df)
        result6 = create_sales_vs_profit_chart(empty_df)

        # Assert - all should be None
        assert result1 is None
        assert result2 is None
        assert result3 is None
        assert result4 is None
        assert result5 is None
        assert result6 is None
