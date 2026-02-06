"""
Layout and grid rendering functions for dashboard
"""

import streamlit as st


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
