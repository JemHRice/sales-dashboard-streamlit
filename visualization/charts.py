"""
Chart creation functions for visualization
"""

import plotly.express as px
import pandas as pd


def create_monthly_trend_chart(monthly_sales_df):
    """
    Create monthly sales trend bar chart.

    Args:
        monthly_sales_df: DataFrame with columns ['Order Date', 'Sales']

    Returns:
        plotly.graph_objects.Figure
    """
    if monthly_sales_df.empty:
        return None

    fig = px.bar(
        monthly_sales_df,
        x="Order Date",
        y="Sales",
        title="Monthly Sales Trend",
        template="plotly_white",
        color="Sales",
        color_continuous_scale="RdYlBu",
    )
    return fig


def create_yearly_trend_chart(yearly_sales_df):
    """
    Create yearly sales comparison bar chart.

    Args:
        yearly_sales_df: DataFrame with columns ['Year', 'Sales']

    Returns:
        plotly.graph_objects.Figure
    """
    if yearly_sales_df.empty:
        return None

    fig = px.bar(
        yearly_sales_df,
        x="Year",
        y="Sales",
        title="Year-over-Year Sales Comparison",
        template="plotly_white",
        color="Sales",
        color_continuous_scale="RdYlBu",
    )
    return fig


def create_daily_trend_chart(daily_sales_df):
    """
    Create daily sales trend line chart.

    Args:
        daily_sales_df: DataFrame with columns ['Date', 'Sales']

    Returns:
        plotly.graph_objects.Figure
    """
    if daily_sales_df.empty:
        return None

    fig = px.line(
        daily_sales_df,
        x="Date",
        y="Sales",
        title="Sales Trend Over Time",
        template="plotly_white",
    )
    fig.update_traces(line_color="#1f77b4", line_width=2)
    return fig


def create_category_sales_chart(category_sales_df):
    """
    Create sales by category bar chart.

    Args:
        category_sales_df: DataFrame with columns ['Category', 'Sales']

    Returns:
        plotly.graph_objects.Figure or None if empty
    """
    if category_sales_df is None or category_sales_df.empty:
        return None

    fig = px.bar(
        category_sales_df,
        x="Category",
        y="Sales",
        title="Sales by Category",
        template="plotly_white",
        color="Sales",
        color_continuous_scale="RdYlBu",
    )
    return fig


def create_region_sales_chart(region_sales_df):
    """
    Create sales distribution by region pie chart.

    Args:
        region_sales_df: DataFrame with columns ['Region', 'Sales']

    Returns:
        plotly.graph_objects.Figure or None if empty
    """
    if region_sales_df is None or region_sales_df.empty:
        return None

    fig = px.pie(
        region_sales_df,
        values="Sales",
        names="Region",
        title="Sales Distribution by Region",
        template="plotly_white",
    )
    return fig


def create_sales_vs_profit_chart(filtered_df):
    """
    Create sales vs profit scatter chart by category.

    Args:
        filtered_df: DataFrame with columns ['Sales', 'Profit', 'Category']

    Returns:
        plotly.graph_objects.Figure or None if missing required columns
    """
    if filtered_df is None or filtered_df.empty:
        return None

    if "Profit" not in filtered_df.columns or "Category" not in filtered_df.columns:
        return None

    hover_data = ["Product Name"] if "Product Name" in filtered_df.columns else None

    fig = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        color="Category",
        title="Sales vs Profit by Category",
        template="plotly_white",
        hover_data=hover_data,
    )
    return fig
