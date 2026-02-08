"""
Unit tests for data.validators module
Tests data validation logic and edge cases
"""

import pytest
import pandas as pd
from data.validators import validate_csv, validate_sales_column, validate_date_column
from utils.exceptions import DataValidationError


class TestValidateCSV:
    """Test CSV validation function"""

    def test_validate_csv_with_valid_data(self, sample_sales_df):
        """Test validation passes with correct columns and data"""
        # Act
        is_valid, message = validate_csv(sample_sales_df)

        # Assert
        assert is_valid is True
        assert message == "Valid"

    def test_validate_csv_missing_order_date_column(self):
        """Test validation fails when Order Date column missing"""
        # Arrange
        df = pd.DataFrame({"Sales": [100.0, 200.0]})

        # Act
        is_valid, message = validate_csv(df)

        # Assert
        assert is_valid is False
        assert "Order Date" in message

    def test_validate_csv_missing_sales_column(self):
        """Test validation fails when Sales column missing"""
        # Arrange
        df = pd.DataFrame({"Order Date": pd.date_range("2023-01-01", periods=2)})

        # Act
        is_valid, message = validate_csv(df)

        # Assert
        assert is_valid is False
        assert "Sales" in message

    def test_validate_csv_missing_both_columns(self):
        """Test validation fails when both required columns missing"""
        # Arrange
        df = pd.DataFrame({"Product": ["A", "B"]})

        # Act
        is_valid, message = validate_csv(df)

        # Assert
        assert is_valid is False
        assert "Order Date" in message and "Sales" in message

    def test_validate_csv_with_empty_dataframe(self, empty_df):
        """Test validation fails with empty DataFrame"""
        # Act
        is_valid, message = validate_csv(empty_df)

        # Assert
        assert is_valid is False
        assert "empty" in message.lower()

    def test_validate_csv_with_additional_columns(self, sample_sales_df):
        """Test validation passes with extra columns"""
        # Arrange
        df = sample_sales_df.copy()
        df["Extra"] = "data"

        # Act
        is_valid, message = validate_csv(df)

        # Assert
        assert is_valid is True

    def test_validate_csv_with_single_row(self):
        """Test validation passes with single row"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": [pd.Timestamp("2023-01-01")],
                "Sales": [100.0],
            }
        )

        # Act
        is_valid, message = validate_csv(df)

        # Assert
        assert is_valid is True


class TestValidateSalesColumn:
    """Test Sales column validation"""

    def test_validate_sales_column_with_numeric_values(self, sample_sales_df):
        """Test sales column validation passes with numeric values"""
        # Act
        is_valid, message = validate_sales_column(sample_sales_df)

        # Assert
        assert is_valid is True
        assert message == "Valid"

    def test_validate_sales_column_missing_column(self):
        """Test validation fails when Sales column missing"""
        # Arrange
        df = pd.DataFrame({"Product": [1, 2, 3]})

        # Act
        is_valid, message = validate_sales_column(df)

        # Assert
        assert is_valid is False
        assert "Sales" in message

    def test_validate_sales_column_with_non_numeric_values(self, invalid_sales_df):
        """Test validation fails with non-numeric Sales values"""
        # Act
        is_valid, message = validate_sales_column(invalid_sales_df)

        # Assert
        assert is_valid is False
        assert "numeric" in message.lower()

    def test_validate_sales_column_with_strings(self):
        """Test validation fails with string values"""
        # Arrange
        df = pd.DataFrame({"Sales": ["100", "two hundred", "300"]})

        # Act
        is_valid, message = validate_sales_column(df)

        # Assert
        assert is_valid is False
        assert "numeric" in message.lower()

    def test_validate_sales_column_converts_to_float(self):
        """Test that sales column is converted to float type"""
        # Arrange
        df = pd.DataFrame({"Sales": [100, 200, 300]})  # Integers

        # Act
        is_valid, message = validate_sales_column(df)

        # Assert
        assert is_valid is True
        assert df["Sales"].dtype == "float64"

    def test_validate_sales_column_with_mixed_types(self):
        """Test validation fails with mixed numeric and non-numeric"""
        # Arrange
        df = pd.DataFrame({"Sales": [100.5, "invalid", 300.75]})

        # Act
        is_valid, message = validate_sales_column(df)

        # Assert
        assert is_valid is False
        assert "numeric" in message.lower()

    def test_validate_sales_column_with_null_values(self):
        """Test validation handles NULL/NaN values"""
        # Arrange
        df = pd.DataFrame({"Sales": [100.0, None, 300.0]})

        # Act
        is_valid, message = validate_sales_column(df)

        # Assert - NaN can be converted to float
        assert is_valid is True

    def test_validate_sales_column_with_negative_values(self):
        """Test validation passes with negative sales values"""
        # Arrange
        df = pd.DataFrame({"Sales": [100.0, -50.0, 200.0]})

        # Act
        is_valid, message = validate_sales_column(df)

        # Assert
        assert is_valid is True

    def test_validate_sales_column_with_zero(self):
        """Test validation passes with zero sales"""
        # Arrange
        df = pd.DataFrame({"Sales": [0.0, 100.0, 200.0]})

        # Act
        is_valid, message = validate_sales_column(df)

        # Assert
        assert is_valid is True


class TestValidateDateColumn:
    """Test Order Date column validation"""

    def test_validate_date_column_with_datetime_type(self, sample_sales_df):
        """Test date validation passes with datetime type"""
        # Act
        is_valid, message = validate_date_column(sample_sales_df)

        # Assert
        assert is_valid is True
        assert message == "Valid"

    def test_validate_date_column_missing_column(self):
        """Test validation fails when Order Date column missing"""
        # Arrange
        df = pd.DataFrame({"Sales": [100.0, 200.0]})

        # Act
        is_valid, message = validate_date_column(df)

        # Assert
        assert is_valid is False
        assert "Order Date" in message

    def test_validate_date_column_with_string_dates(self, string_date_df):
        """Test validation fails when dates are strings"""
        # Act
        is_valid, message = validate_date_column(string_date_df)

        # Assert
        assert is_valid is False
        assert "datetime" in message.lower()

    def test_validate_date_column_with_numeric_values(self):
        """Test validation fails when dates are numeric"""
        # Arrange
        df = pd.DataFrame(
            {
                "Order Date": [20230101, 20230102, 20230103],
                "Sales": [100.0, 200.0, 300.0],
            }
        )

        # Act
        is_valid, message = validate_date_column(df)

        # Assert
        assert is_valid is False

    def test_validate_date_column_type_check(self, sample_sales_df):
        """Test that date column has correct dtype"""
        # Arrange
        df = sample_sales_df.copy()

        # Act
        is_valid, message = validate_date_column(df)

        # Assert - Order Date should be datetime
        assert is_valid is True
        assert df["Order Date"].dtype == "datetime64[ns]"
