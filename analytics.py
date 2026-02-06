"""
analytics.py
Helper functions for sales analytics and data calculations.
Used by the Streamlit dashboard for data aggregation and growth metrics.
"""

import streamlit as st
import pandas as pd


def clean_dataframe_columns(df):
    """
    Clean column names by stripping whitespace and find date column (case-insensitive).

    Args:
        df: DataFrame with potentially messy column names

    Returns:
        tuple: (cleaned DataFrame, bool indicating if date column was found)
    """
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Find the date column (case-insensitive)
    date_col = None
    for col in df.columns:
        if col.lower() == "order date":
            date_col = col
            break

    # If not found with exact match, rename it
    if date_col and date_col != "Order Date":
        df = df.rename(columns={date_col: "Order Date"})

    return df, date_col is not None


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


def calculate_yoy_growth(df, current_year, previous_year, metric_col="Sales"):
    """
    Calculate Year-over-Year growth percentage.

    Args:
        df: DataFrame with 'Order Date' column
        current_year: Current year for comparison
        previous_year: Previous year for comparison
        metric_col: Column to calculate growth for (default: 'Sales')

    Returns:
        float: YoY growth percentage
    """
    current = df[df["Order Date"].dt.year == current_year][metric_col].sum()
    previous = df[df["Order Date"].dt.year == previous_year][metric_col].sum()
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100


def calculate_mom_change(df, current_month, previous_month, metric_col="Sales"):
    """
    Calculate Month-over-Month change percentage.

    Args:
        df: DataFrame with 'Order Date' column
        current_month: Tuple of (year, month) for current period
        previous_month: Tuple of (year, month) for previous period
        metric_col: Column to calculate change for (default: 'Sales')

    Returns:
        float: MoM change percentage
    """
    current = df[
        (df["Order Date"].dt.year == current_month[0])
        & (df["Order Date"].dt.month == current_month[1])
    ][metric_col].sum()
    previous = df[
        (df["Order Date"].dt.year == previous_month[0])
        & (df["Order Date"].dt.month == previous_month[1])
    ][metric_col].sum()
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100


@st.cache_data
def load_data(file_path):
    """
    Load and cache CSV data with comprehensive error handling.

    Args:
        file_path: Path to CSV file

    Returns:
        DataFrame with 'Order Date' column converted to datetime

    Raises:
        ValueError: If CSV cannot be parsed or required columns are missing
    """
    # Delimiters to try in order of likelihood
    delimiters = [",", ";", "\t", "|"]
    df = None
    successful_delimiter = None
    delimiter_errors = []

    for delimiter in delimiters:
        try:
            # Try UTF-8 first
            try:
                df = pd.read_csv(file_path, encoding="utf-8", sep=delimiter)
            except UnicodeDecodeError:
                # Fall back to latin-1 if UTF-8 fails
                df = pd.read_csv(file_path, encoding="latin-1", sep=delimiter)

            # Check if we got a valid dataframe with reasonable columns
            if len(df.columns) > 1 and len(df) > 0:
                successful_delimiter = delimiter
                break
        except Exception as e:
            delimiter_errors.append(f"Delimiter '{repr(delimiter)}': {str(e)[:50]}")
            continue

    if df is None or len(df) == 0:
        error_msg = "❌ **Failed to parse CSV file.**\n\nTried delimiters: comma (,), semicolon (;), tab, pipe (|)\n\n**Possible causes:**\n"
        error_msg += "- File is corrupted or not a valid CSV\n"
        error_msg += "- Unusual encoding (try UTF-8 or Latin-1)\n"
        error_msg += "- File might be empty\n"
        raise ValueError(error_msg)

    # Clean column names
    df, has_date_col = clean_dataframe_columns(df)

    # Check for required columns
    required_cols = ["Order Date", "Sales"]
    missing_required = [col for col in required_cols if col not in df.columns]

    if missing_required:
        available_cols = ", ".join(df.columns.tolist()[:15])
        if len(df.columns) > 15:
            available_cols += f" ... and {len(df.columns) - 15} more"
        error_msg = (
            f"❌ **Missing required columns:** {', '.join(missing_required)}\n\n"
        )
        error_msg += f"**Available columns:** {available_cols}\n\n"
        error_msg += "Your CSV must have 'Order Date' and 'Sales' columns."
        raise ValueError(error_msg)

    # Validate 'Sales' column is numeric
    try:
        df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
        if df["Sales"].isna().all():
            raise ValueError(
                "❌ **'Sales' column contains no valid numbers.** Values found: "
                + str(df["Sales"].unique()[:3])
            )
    except Exception as e:
        raise ValueError(f"❌ **'Sales' column must be numeric.** Error: {str(e)}")

    # Try to parse dates with automatic format detection
    date_formats = [
        ("mixed", {"format": "mixed", "dayfirst": True}),
        ("DD/MM/YYYY", {"format": "%d/%m/%Y"}),
        ("DD-MM-YYYY", {"format": "%d-%m-%Y"}),
        ("YYYY-MM-DD", {"format": "%Y-%m-%d"}),
        ("auto-infer", {"infer_datetime_format": True}),
    ]

    date_parse_success = False
    for format_name, format_kwargs in date_formats:
        try:
            if "infer_datetime_format" in format_kwargs:
                df["Order Date"] = pd.to_datetime(
                    df["Order Date"], infer_datetime_format=True
                )
            else:
                df["Order Date"] = pd.to_datetime(df["Order Date"], **format_kwargs)
            date_parse_success = True
            break
        except Exception as e:
            continue

    if not date_parse_success:
        sample_dates = df["Order Date"].head(3).tolist()
        error_msg = f"❌ **Cannot parse 'Order Date' column.**\n\n"
        error_msg += f"**Sample values found:** {sample_dates}\n\n"
        error_msg += "**Supported formats:** DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD, or standard ISO format\n"
        error_msg += "Make sure all dates are in a consistent format."
        raise ValueError(error_msg)

    return df


@st.cache_data
def get_monthly_sales(df):
    """
    Calculate and cache monthly sales aggregation.

    Args:
        df: DataFrame with 'Order Date' and 'Sales' columns

    Returns:
        DataFrame with monthly sales by period
    """
    monthly_sales = (
        df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
    )
    monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)
    return monthly_sales


@st.cache_data
def get_yearly_sales(df):
    """
    Calculate and cache yearly sales aggregation.

    Args:
        df: DataFrame with 'Order Date' and 'Sales' columns

    Returns:
        DataFrame with yearly sales totals
    """
    yearly_sales = df.groupby(df["Order Date"].dt.year)["Sales"].sum().reset_index()
    yearly_sales.columns = ["Year", "Sales"]
    return yearly_sales


@st.cache_data
def get_daily_sales(df):
    """
    Calculate and cache daily sales aggregation.

    Args:
        df: DataFrame with 'Order Date' and 'Sales' columns

    Returns:
        DataFrame with daily sales totals
    """
    daily_sales = df.groupby(df["Order Date"].dt.date)["Sales"].sum().reset_index()
    daily_sales.columns = ["Date", "Sales"]
    return daily_sales


@st.cache_data
def get_category_sales(df):
    """
    Calculate and cache sales by category.

    Args:
        df: DataFrame with 'Category' and 'Sales' columns

    Returns:
        DataFrame with category sales or None if Category column doesn't exist
    """
    if "Category" not in df.columns:
        return None
    category_sales = df.groupby("Category")["Sales"].sum().reset_index()
    category_sales = category_sales.sort_values("Sales", ascending=False)
    return category_sales


@st.cache_data
def get_region_sales(df):
    """
    Calculate and cache sales by region.

    Args:
        df: DataFrame with 'Region' and 'Sales' columns

    Returns:
        DataFrame with regional sales or None if Region column doesn't exist
    """
    if "Region" not in df.columns:
        return None
    region_sales = df.groupby("Region")["Sales"].sum().reset_index()
    return region_sales


@st.cache_data
def get_top_products(df, n=10):
    """
    Calculate and cache top products by sales.

    Args:
        df: DataFrame with 'Product Name' and 'Sales' columns
        n: Number of top products to return (default: 10)

    Returns:
        Series with top product names and sales, or None if Product Name column doesn't exist
    """
    if "Product Name" not in df.columns:
        return None
    top_products = (
        df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(n)
    )
    return top_products


@st.cache_data
def get_top_customers(df, n=10):
    """
    Calculate and cache top customers by sales.

    Args:
        df: DataFrame with 'Customer Name' and 'Sales' columns
        n: Number of top customers to return (default: 10)

    Returns:
        Series with top customer names and sales, or None if Customer Name column doesn't exist
    """
    if "Customer Name" not in df.columns:
        return None
    top_customers = (
        df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(n)
    )
    return top_customers


def render_chart_grid(charts_list, columns=2):
    """
    Render a list of charts in a dynamic responsive grid that auto-fills empty spaces.

    Args:
        charts_list: List of dicts with keys 'figure' (plotly fig) and 'title' (str)
                     Example: [{'figure': fig1, 'title': 'Chart 1'}, ...]
                     Charts with figure=None are automatically skipped.
        columns: Number of columns (default: 2)

    Returns:
        None (renders directly to Streamlit)

    Example:
        charts = [
            {'figure': fig_trend, 'title': 'Sales Trend'},
            {'figure': fig_category, 'title': 'Sales by Category'},  # Can be None
            {'figure': fig_region, 'title': 'Sales by Region'},
        ]
        render_chart_grid(charts, columns=2)
    """
    # Filter out charts with None figures
    valid_charts = [c for c in charts_list if c.get("figure") is not None]

    if not valid_charts:
        return  # No charts to display

    # Create rows of columns dynamically
    current_row_charts = []
    for i, chart_dict in enumerate(valid_charts):
        current_row_charts.append(chart_dict)

        # When row is full or it's the last chart, render the row
        if len(current_row_charts) == columns or i == len(valid_charts) - 1:
            cols = st.columns(len(current_row_charts))
            for col, chart_dict in zip(cols, current_row_charts):
                with col:
                    st.plotly_chart(chart_dict["figure"], width="stretch")
            current_row_charts = []
