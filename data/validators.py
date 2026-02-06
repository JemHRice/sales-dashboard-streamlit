"""
Data validation functions for CSV files
"""

from utils.exceptions import DataValidationError


def validate_csv(df):
    """
    Validate that CSV has required columns and data integrity.

    Args:
        df: DataFrame to validate

    Returns:
        tuple: (bool: is_valid, str: message)
    """
    required_columns = ["Order Date", "Sales"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"

    # Check for at least one row of data
    if len(df) == 0:
        return False, "CSV file is empty (no data rows)"

    return True, "Valid"


def validate_sales_column(df):
    """
    Validate that Sales column contains numeric values.

    Args:
        df: DataFrame to validate

    Raises:
        DataValidationError: If Sales column is not numeric
    """
    if "Sales" not in df.columns:
        raise DataValidationError("'Sales' column not found")

    try:
        df["Sales"] = df["Sales"].astype(float)
    except (ValueError, TypeError):
        sample_values = df["Sales"].unique()[:5]
        raise DataValidationError(
            f"'Sales' column must be numeric. Found: {sample_values}"
        )


def validate_date_column(df):
    """
    Validate that Order Date column is datetime format.

    Args:
        df: DataFrame to validate

    Raises:
        DataValidationError: If Order Date cannot be parsed
    """
    if "Order Date" not in df.columns:
        raise DataValidationError("'Order Date' column not found")

    # Check if already datetime
    if (
        not hasattr(df["Order Date"].dtype, "kind")
        or df["Order Date"].dtype.kind != "M"
    ):
        raise DataValidationError(
            f"'Order Date' column is not datetime format. Type: {df['Order Date'].dtype}"
        )
