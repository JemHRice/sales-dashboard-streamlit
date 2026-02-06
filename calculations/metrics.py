"""
Core metrics calculations: year-over-year and month-over-month growth
"""

import pandas as pd


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
