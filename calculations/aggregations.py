"""
Aggregation functions with caching for dashboard data queries
"""

import streamlit as st
import pandas as pd


@st.cache_resource
def get_monthly_sales(df):
    """
    Aggregate sales by month.

    Args:
        df: DataFrame with columns ['Order Date', 'Sales']

    Returns:
        DataFrame: Aggregated by month with Period strings and Sales
    """
    df_copy = df.copy()
    df_copy["Sales"] = pd.to_numeric(df_copy["Sales"], errors="coerce")
    # Convert to year-month strings to avoid Arrow serialization issues
    df_copy["YearMonth"] = df_copy["Order Date"].dt.strftime("%Y-%m")
    monthly_sales = df_copy.groupby("YearMonth")["Sales"].sum().reset_index()
    monthly_sales.columns = ["Order Date", "Sales"]
    return monthly_sales


@st.cache_resource
def get_yearly_sales(df):
    """
    Aggregate sales by year.

    Args:
        df: DataFrame with columns ['Order Date', 'Sales']

    Returns:
        DataFrame: Aggregated by year with columns [Year, Sales]
    """
    df_copy = df.copy()

    # Ensure Order Date is datetime (in case of caching/serialization issues)
    if not pd.api.types.is_datetime64_any_dtype(df_copy["Order Date"]):
        df_copy["Order Date"] = pd.to_datetime(df_copy["Order Date"])

    df_copy["Sales"] = pd.to_numeric(df_copy["Sales"], errors="coerce")
    df_copy["Year"] = df_copy["Order Date"].dt.year.astype(int)
    yearly = df_copy.groupby("Year")["Sales"].sum().reset_index()

    # Ensure Year column is integer (handles string values from caching)
    yearly["Year"] = pd.to_numeric(yearly["Year"], errors="coerce").astype(int)
    yearly = yearly.sort_values("Year")

    return yearly


@st.cache_resource
def get_daily_sales(df):
    """
    Aggregate sales by day.

    Args:
        df: DataFrame with columns ['Order Date', 'Sales']

    Returns:
        DataFrame: Aggregated by day with columns [Date, Sales]
    """
    df_copy = df.copy()
    df_copy["Sales"] = pd.to_numeric(df_copy["Sales"], errors="coerce")
    # Convert to date strings to avoid Arrow serialization issues
    df_copy["Date"] = df_copy["Order Date"].dt.strftime("%Y-%m-%d")
    daily = df_copy.groupby("Date")["Sales"].sum().reset_index()

    return daily


@st.cache_resource
def get_category_sales(df):
    """
    Aggregate sales by product category.

    Args:
        df: DataFrame with 'Category' and 'Sales' columns

    Returns:
        DataFrame: Aggregated by category with columns [Category, Sales]
    """
    if "Category" not in df.columns:
        return pd.DataFrame({"Category": [], "Sales": []})

    df_copy = df.copy()
    df_copy["Sales"] = pd.to_numeric(df_copy["Sales"], errors="coerce")
    category = df_copy.groupby("Category")["Sales"].sum().reset_index()
    category = category.sort_values("Sales", ascending=False)

    return category


@st.cache_resource
def get_region_sales(df):
    """
    Aggregate sales by region.

    Args:
        df: DataFrame with 'Region' and 'Sales' columns

    Returns:
        DataFrame: Aggregated by region with columns [Region, Sales]
    """
    if "Region" not in df.columns:
        return pd.DataFrame({"Region": [], "Sales": []})

    df_copy = df.copy()
    df_copy["Sales"] = pd.to_numeric(df_copy["Sales"], errors="coerce")
    region = df_copy.groupby("Region")["Sales"].sum().reset_index()
    region = region.sort_values("Sales", ascending=False)

    return region


@st.cache_resource
def get_top_products(df, n=10):
    """
    Get top N products by sales.

    Args:
        df: DataFrame with 'Product Name' and 'Sales' columns
        n: Number of top products to return

    Returns:
        DataFrame: Top products with columns [Product Name, Sales]
    """
    if "Product Name" not in df.columns:
        return pd.DataFrame({"Product Name": [], "Sales": []})

    # Ensure n is a valid integer (handles string values from caching/serialization)
    try:
        n = int(n) if n is not None else 10
        # Validate n is positive
        if n <= 0:
            n = 10
    except (ValueError, TypeError):
        n = 10

    df_copy = df.copy()
    # Ensure Sales column is numeric
    df_copy["Sales"] = pd.to_numeric(df_copy["Sales"], errors="coerce")
    top_products = df_copy.groupby("Product Name")["Sales"].sum().reset_index()

    # Only call .head() if we have results
    if len(top_products) > 0:
        top_products = top_products.sort_values("Sales", ascending=False).head(n)
    else:
        top_products = pd.DataFrame({"Product Name": [], "Sales": []})

    return top_products


@st.cache_resource
def get_top_customers(df, n=10):
    """
    Get top N customers by sales.

    Args:
        df: DataFrame with 'Customer Name' and 'Sales' columns
        n: Number of top customers to return

    Returns:
        DataFrame: Top customers with columns [Customer Name, Sales]
    """
    if "Customer Name" not in df.columns:
        return pd.DataFrame({"Customer Name": [], "Sales": []})

    # Ensure n is a valid integer (handles string values from caching/serialization)
    try:
        n = int(n) if n is not None else 10
        # Validate n is positive
        if n <= 0:
            n = 10
    except (ValueError, TypeError):
        n = 10

    df_copy = df.copy()
    # Ensure Sales column is numeric
    df_copy["Sales"] = pd.to_numeric(df_copy["Sales"], errors="coerce")
    top_customers = df_copy.groupby("Customer Name")["Sales"].sum().reset_index()

    # Only call .head() if we have results
    if len(top_customers) > 0:
        top_customers = top_customers.sort_values("Sales", ascending=False).head(n)
    else:
        top_customers = pd.DataFrame({"Customer Name": [], "Sales": []})

    return top_customers
