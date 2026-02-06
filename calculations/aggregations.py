"""
Aggregation functions with caching for dashboard data queries
"""

import streamlit as st
import pandas as pd


@st.cache_data
def get_monthly_sales(df):
    """
    Aggregate sales by month.

    Args:
        df: DataFrame with columns ['Order Date', 'Sales']

    Returns:
        DataFrame: Aggregated by month with Period strings and Sales
    """
    monthly_sales = (
        df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
    )
    monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)
    return monthly_sales


@st.cache_data
def get_yearly_sales(df):
    """
    Aggregate sales by year.

    Args:
        df: DataFrame with columns ['Order Date', 'Sales']

    Returns:
        DataFrame: Aggregated by year with columns [Year, Sales]
    """
    df_copy = df.copy()
    df_copy["Year"] = df_copy["Order Date"].dt.year
    yearly = df_copy.groupby("Year")["Sales"].sum().reset_index()
    yearly = yearly.sort_values("Year")

    return yearly


@st.cache_data
def get_daily_sales(df):
    """
    Aggregate sales by day.

    Args:
        df: DataFrame with columns ['Order Date', 'Sales']

    Returns:
        DataFrame: Aggregated by day with columns [Date, Sales]
    """
    df_copy = df.copy()
    daily = df_copy.groupby(df_copy["Order Date"].dt.date)["Sales"].sum().reset_index()
    daily.columns = ["Date", "Sales"]

    return daily


@st.cache_data
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
    category = df_copy.groupby("Category")["Sales"].sum().reset_index()
    category = category.sort_values("Sales", ascending=False)

    return category


@st.cache_data
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
    region = df_copy.groupby("Region")["Sales"].sum().reset_index()
    region = region.sort_values("Sales", ascending=False)

    return region


@st.cache_data
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

    df_copy = df.copy()
    top_products = df_copy.groupby("Product Name")["Sales"].sum().reset_index()
    top_products = top_products.sort_values("Sales", ascending=False).head(n)

    return top_products


@st.cache_data
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

    df_copy = df.copy()
    top_customers = df_copy.groupby("Customer Name")["Sales"].sum().reset_index()
    top_customers = top_customers.sort_values("Sales", ascending=False).head(n)

    return top_customers
