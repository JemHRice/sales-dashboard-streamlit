"""
Data loading and file parsing functions
"""

import streamlit as st
import pandas as pd
from .validators import validate_csv, validate_sales_column, validate_date_column
from utils.exceptions import DataLoadError, DataValidationError


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


def parse_csv_file(file_path, encoding="utf-8", sep=","):
    """
    Parse a CSV file with specific encoding and separator.

    Args:
        file_path: Path to CSV file
        encoding: Character encoding (default: 'utf-8')
        sep: Column separator (default: ',')

    Returns:
        DataFrame or None if parsing fails
    """
    try:
        df = pd.read_csv(file_path, encoding=encoding, sep=sep)
        if len(df.columns) > 1 and len(df) > 0:
            return df
    except Exception:
        return None
    return None


@st.cache_data
def load_data(file_path):
    """
    Load and cache CSV data with comprehensive error handling.
    Automatically detects delimiters and encodings.

    Args:
        file_path: Path to CSV file

    Returns:
        DataFrame with 'Order Date' column converted to datetime

    Raises:
        DataLoadError: If CSV cannot be parsed or required columns are missing
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
                df = parse_csv_file(file_path, encoding="utf-8", sep=delimiter)
            except Exception:
                # Fall back to latin-1 if UTF-8 fails
                df = parse_csv_file(file_path, encoding="latin-1", sep=delimiter)

            # Check if we got a valid dataframe
            if df is not None:
                successful_delimiter = delimiter
                break
        except Exception as e:
            delimiter_errors.append(f"Delimiter '{repr(delimiter)}': {str(e)[:50]}")
            continue

    if df is None or len(df) == 0:
        error_msg = "Failed to parse CSV file. "
        error_msg += "Tried delimiters: comma (,), semicolon (;), tab, pipe (|). "
        error_msg += "File may be corrupted, empty, or in an unusual format."
        raise DataLoadError(error_msg)

    # Clean column names
    df, has_date_col = clean_dataframe_columns(df)

    # Validate CSV structure
    is_valid, message = validate_csv(df)
    if not is_valid:
        raise DataLoadError(f"CSV validation failed: {message}")

    # Validate Sales column
    is_valid, message = validate_sales_column(df)
    if not is_valid:
        raise DataLoadError(f"Sales column validation failed: {message}")

    # Parse dates with automatic format detection
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
        except Exception:
            continue

    if not date_parse_success:
        sample_dates = df["Order Date"].head(3).tolist()
        error_msg = f"Cannot parse 'Order Date' column. "
        error_msg += f"Sample values: {sample_dates}. "
        error_msg += (
            "Supported formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD, ISO format."
        )
        raise DataLoadError(error_msg)

    # Validate date column
    is_valid, message = validate_date_column(df)
    if not is_valid:
        raise DataLoadError(f"Date column validation failed: {message}")

    return df
