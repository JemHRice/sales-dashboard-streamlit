"""
Formatting utilities for data display
"""


def format_currency(value):
    """
    Format numeric value as currency.

    Args:
        value: Numeric value to format

    Returns:
        str: Formatted currency string (e.g., "$1,234.56")
    """
    if value is None:
        return "$0.00"
    return f"${value:,.2f}"


def format_percentage(value):
    """
    Format numeric value as percentage.

    Args:
        value: Numeric value to format as percentage

    Returns:
        str: Formatted percentage string (e.g., "+12.3%" or "-5.1%")
    """
    if value is None:
        return "0.0%"
    return f"{value:+.1f}%"


def format_integer(value):
    """
    Format numeric value with thousands separator.

    Args:
        value: Integer value to format

    Returns:
        str: Formatted integer string (e.g., "1,234")
    """
    if value is None:
        return "0"
    return f"{value:,}"
