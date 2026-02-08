"""
Test fixtures and helper functions for data generation
"""

import pandas as pd


def generate_sample_csv_data(n_rows: int = 100) -> pd.DataFrame:
    """
    Generate sample sales data for testing

    Args:
        n_rows: Number of rows to generate

    Returns:
        DataFrame with sample sales data
    """
    import numpy as np

    dates = pd.date_range("2023-01-01", periods=n_rows, freq="D")
    categories = ["Electronics", "Furniture", "Office Supplies"] * (n_rows // 3 + 1)
    regions = ["East", "West", "North", "South"] * (n_rows // 4 + 1)

    df = pd.DataFrame(
        {
            "Order Date": dates,
            "Sales": np.random.uniform(50, 500, n_rows),
            "Category": categories[:n_rows],
            "Region": regions[:n_rows],
            "Product Name": [f"Product_{i % 20}" for i in range(n_rows)],
            "Customer Name": [f"Customer_{i % 50}" for i in range(n_rows)],
        }
    )

    return df
