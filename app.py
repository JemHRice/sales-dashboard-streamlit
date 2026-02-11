# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

from data import load_data, clean_dataframe_columns, validate_csv
from calculations import (
    calculate_yoy_growth,
    calculate_mom_change,
    get_monthly_sales,
    get_yearly_sales,
    get_daily_sales,
    get_category_sales,
    get_region_sales,
    get_top_products,
    get_top_customers,
)
from visualization import render_chart_grid

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .metric-card {padding: 20px; border-radius: 10px; background: #f0f2f6;}
    </style>
""",
    unsafe_allow_html=True,
)


st.title("📊 Sales Analytics Dashboard")
st.markdown("---")

# Initialize session state for sample data toggle
if "show_sample_data" not in st.session_state:
    st.session_state.show_sample_data = False


# Show CSV format instructions prominently at top
with st.expander("📋 CSV Format Requirements (Click to expand)", expanded=False):
    st.markdown(
        """
    #### Required Columns:
    - **Order Date** (required) - Date format (e.g., 2023-01-15)
    - **Sales** (required) - Numeric value (e.g., 100.50)
    
    #### Optional Columns (recommended):
    - **Profit** - Numeric value for profit calculations
    - **Category** - Text for category grouping
    - **Region** - Text for regional analysis
    - **Product Name** - Text for product performance
    - **Customer Name** - Text for customer analysis
    
    #### What Happens with Missing Optional Columns?
    ✅ **Dashboard still works!** If optional columns are missing:
    - **No Profit** → Profit metrics won't display, no scatter plot
    - **No Category** → Category chart skipped, multiselect filter hidden
    - **No Region** → Region chart skipped, regional filter hidden
    - **No Product Name** → Top products table won't display
    - **No Customer Name** → Top customers table won't display
    
    The dashboard shows only the charts and metrics for columns that exist.
    
    #### Sample CSV Format:
    | Order Date | Sales | Profit | Category | Region | Product Name | Customer Name |
    |---|---|---|---|---|---|---|
    | 2023-01-15 | 500 | 120 | Technology | West | Laptop | John Doe |
    | 2023-01-16 | 300 | 75 | Furniture | East | Chair | Jane Smith |
    
    ### Sample Datasets:
    - [Superstore Sales (Kaggle)](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
    - [Global Superstore (Kaggle)](https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset)
    """
    )

# Auto-load sample data or allow file upload
sample_file = "Sample - Superstore.csv"
uploaded_file = None

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    uploaded_file = st.file_uploader("📤 Upload Your CSV File", type=["csv"])

with col2:
    if os.path.exists(sample_file):
        st.session_state.show_sample_data = st.checkbox(
            "👁️ Show Sample Data",
            value=st.session_state.show_sample_data,
            help="Toggle to view the sample Superstore dataset",
        )

with col3:
    if st.session_state.show_sample_data and os.path.exists(sample_file):
        st.info("📌 Sample data active")

# Load and validate data
df = None
is_sample_data = False

if uploaded_file:
    # Load uploaded file
    try:
        # Try different delimiters
        delimiters = [",", ";", "\t", "|"]
        df = None

        for delimiter in delimiters:
            try:
                # Reset file pointer
                uploaded_file.seek(0)

                # Try UTF-8 first
                try:
                    df = pd.read_csv(uploaded_file, encoding="utf-8", sep=delimiter)
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    # Fall back to latin-1 if UTF-8 fails
                    df = pd.read_csv(uploaded_file, encoding="latin-1", sep=delimiter)

                # Check if we got a valid dataframe with reasonable columns
                if len(df.columns) > 1 and len(df) > 0:
                    break
            except:
                continue

        if df is None or len(df) == 0:
            st.error(
                "❌ **Could not parse CSV file.** File appears to be empty or corrupted. "
                "Tried delimiters: comma (,), semicolon (;), tab, and pipe (|)."
            )
            df = None
        else:
            # Clean column names
            df, has_date_col = clean_dataframe_columns(df)

            if not has_date_col:
                # Show what columns were found for debugging
                found_cols = ", ".join(
                    df.columns.tolist()[:15]
                )  # Show first 15 columns
                if len(df.columns) > 15:
                    found_cols += f" ... and {len(df.columns) - 15} more"
                st.error(
                    f"❌ **Missing 'Order Date' column.** \n\nFound columns: {found_cols}\n\n"
                    "Your CSV must have a column named 'Order Date' (case-insensitive, whitespace ignored)."
                )
                df = None
            else:
                # Check for Sales column
                if "Sales" not in df.columns:
                    found_cols = ", ".join(df.columns.tolist()[:15])
                    if len(df.columns) > 15:
                        found_cols += f" ... and {len(df.columns) - 15} more"
                    st.error(
                        f"❌ **Missing 'Sales' column.** \n\nFound columns: {found_cols}\n\n"
                        "Your CSV must have a column named 'Sales' with numeric values."
                    )
                    df = None
                else:
                    # Try to parse dates with automatic format detection
                    date_formats = [
                        ("mixed", {"format": "mixed", "dayfirst": True}),
                        ("DD/MM/YYYY", {"format": "%d/%m/%Y"}),
                        ("DD-MM-YYYY", {"format": "%d-%m-%Y"}),
                        ("YYYY-MM-DD", {"format": "%Y-%m-%d"}),
                    ]

                    date_parse_success = False
                    for format_name, format_kwargs in date_formats:
                        try:
                            df["Order Date"] = pd.to_datetime(
                                df["Order Date"], **format_kwargs
                            )
                            date_parse_success = True
                            break
                        except:
                            continue

                    if not date_parse_success:
                        try:
                            df["Order Date"] = pd.to_datetime(
                                df["Order Date"], infer_datetime_format=True
                            )
                            date_parse_success = True
                        except:
                            pass

                    if not date_parse_success:
                        sample_dates = df["Order Date"].head(3).tolist()
                        st.error(
                            f"❌ **Cannot parse 'Order Date' column.** \n\n"
                            f"Sample values: {sample_dates}\n\n"
                            f"Supported formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD\n"
                            "Make sure dates are in a consistent format."
                        )
                        df = None
                    else:
                        # Validate that Sales column is numeric
                        try:
                            df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
                            if df["Sales"].isna().all():
                                st.error(
                                    "❌ **'Sales' column contains no valid numbers.** \n\n"
                                    f"Sample values from column: {df['Sales'].unique()[:5]}\n\n"
                                    "Please ensure the 'Sales' column contains only numeric values."
                                )
                                df = None
                            else:
                                # Validate CSV
                                is_valid, message = validate_csv(df)
                                if not is_valid:
                                    st.error(f"❌ {message}")
                                    df = None
                                else:
                                    st.success(
                                        "✅ File loaded successfully! Data is ready for analysis."
                                    )
                        except Exception as e:
                            st.error(
                                f"❌ **Sales column validation failed:** {str(e)}\n\n"
                                "The 'Sales' column must contain numeric values (numbers, not text)."
                            )
                            df = None

    except Exception as e:
        st.error(f"❌ **Unexpected error loading file:** {str(e)[:200]}")
        st.info(
            "💡 **Tip:** Your CSV should have 'Order Date' and 'Sales' columns. "
            "See 'CSV Format Requirements' at the top for more details."
        )
        df = None

elif st.session_state.show_sample_data and os.path.exists(sample_file):
    # Load sample data only if checkbox is checked
    try:
        df = load_data(sample_file)
        is_valid, message = validate_csv(df)
        if not is_valid:
            st.error(f"❌ {message}")
            df = None
        else:
            st.info("📊 Loaded sample superstore data")
            is_sample_data = True
    except Exception as e:
        st.error(f"❌ **Error loading sample file:** {str(e)[:200]}")
        st.info(
            "The sample data file may be missing or corrupted. "
            "Please upload your own CSV file instead."
        )
        df = None

if df is not None:
    # Load data
    try:

        # Sidebar filters
        st.sidebar.header("🔍 Filters")

        # Date range
        st.sidebar.write("**Date Range (dd/mm/yyyy)**")
        min_date = df["Order Date"].min().date()
        max_date = df["Order Date"].max().date()
        date_range = st.sidebar.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            format="DD/MM/YYYY",
            label_visibility="collapsed",
        )

        # Category filter
        if "Category" in df.columns:
            categories = st.sidebar.multiselect(
                "Category",
                options=df["Category"].unique(),
                default=df["Category"].unique(),
            )
        else:
            categories = None

        # Region filter (if exists)
        if "Region" in df.columns:
            regions = st.sidebar.multiselect(
                "Region", options=df["Region"].unique(), default=df["Region"].unique()
            )
        else:
            regions = None

        # Apply filters
        mask = (df["Order Date"].dt.date >= date_range[0]) & (
            df["Order Date"].dt.date <= date_range[1]
        )
        filtered_df = df[mask].copy()

        if categories:
            filtered_df = filtered_df[filtered_df["Category"].isin(categories)]
        if regions:
            filtered_df = filtered_df[filtered_df["Region"].isin(regions)]

        # For YoY/MoM growth calculations, apply only category/region filters (NOT date range)
        # This allows us to compare full years/months even if date range is restricted
        growth_calculation_df = df.copy()
        if categories:
            growth_calculation_df = growth_calculation_df[
                growth_calculation_df["Category"].isin(categories)
            ]
        if regions:
            growth_calculation_df = growth_calculation_df[
                growth_calculation_df["Region"].isin(regions)
            ]

        # Key metrics
        st.subheader("📈 Key Performance Indicators")
        col1, col2, col3, col4, col5 = st.columns(5)

        total_sales = filtered_df["Sales"].sum()
        total_profit = (
            filtered_df["Profit"].sum() if "Profit" in filtered_df.columns else 0
        )
        total_orders = len(filtered_df)
        avg_order = filtered_df["Sales"].mean()

        # Calculate YoY and MoM growth using actual data years/months, not current date
        # Find the max year in the data for meaningful YoY comparison
        max_year = growth_calculation_df["Order Date"].dt.year.max()
        min_year = growth_calculation_df["Order Date"].dt.year.min()

        # For YoY: compare max year with previous year (if available)
        if max_year - min_year >= 1:
            # We have at least 2 years of data
            current_year = max_year
            previous_year = max_year - 1
        else:
            # Only 1 year of data, compare with dummy values that will result in 0%
            current_year = max_year
            previous_year = max_year

        # For MoM: find the latest month in data and compare with previous month
        latest_date = growth_calculation_df["Order Date"].max()
        latest_year = latest_date.year
        latest_month_num = latest_date.month

        current_month = (latest_year, latest_month_num)
        if latest_month_num > 1:
            previous_month = (latest_year, latest_month_num - 1)
        else:
            previous_month = (latest_year - 1, 12)

        yoy_growth = calculate_yoy_growth(
            growth_calculation_df, current_year, previous_year, "Sales"
        )
        mom_growth = calculate_mom_change(
            growth_calculation_df, current_month, previous_month, "Sales"
        )

        col1.metric("Total Sales", f"${total_sales:,.0f}", f"{yoy_growth:+.1f}% YoY")
        col2.metric("Total Profit", f"${total_profit:,.0f}")
        col3.metric("Orders", f"{total_orders:,}", f"{mom_growth:+.1f}% MoM")
        col4.metric("Avg Order Value", f"${avg_order:,.2f}")

        # Profit margin if profit exists
        if "Profit" in filtered_df.columns:
            profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
            yoy_profit = calculate_yoy_growth(
                growth_calculation_df, current_year, previous_year, "Profit"
            )
            col5.metric(
                "Profit Margin", f"{profit_margin:.1f}%", f"{yoy_profit:+.1f}% YoY"
            )

        st.markdown("---")

        # Advanced metrics section
        st.subheader("📊 Advanced Metrics & Trends")
        adv_col1, adv_col2 = st.columns(2)

        with adv_col1:
            # Monthly trend
            monthly_sales = get_monthly_sales(filtered_df)
            fig_monthly = px.bar(
                monthly_sales,
                x="Order Date",
                y="Sales",
                title="Monthly Sales Trend",
                template="plotly_white",
                color="Sales",
                color_continuous_scale="RdYlBu",
            )
            st.plotly_chart(fig_monthly, width="stretch")

        with adv_col2:
            # YoY comparison
            yearly_sales = get_yearly_sales(filtered_df)
            fig_yearly = px.bar(
                yearly_sales,
                x="Year",
                y="Sales",
                title="Year-over-Year Sales Comparison",
                template="plotly_white",
                color="Sales",
                color_continuous_scale="RdYlBu",
            )
            st.plotly_chart(fig_yearly, width="stretch")

        st.markdown("---")

        # Charts row 1 - Using dynamic grid layout
        st.subheader("📊 Sales Analysis")

        # Create figures for row 1
        daily_sales = get_daily_sales(filtered_df)
        fig_trend = px.line(
            daily_sales,
            x="Date",
            y="Sales",
            title="Sales Trend Over Time",
            template="plotly_white",
        )
        fig_trend.update_traces(line_color="#1f77b4", line_width=2)

        # Sales by category
        category_sales = get_category_sales(filtered_df)
        fig_category = None
        if category_sales is not None:
            fig_category = px.bar(
                category_sales,
                x="Category",
                y="Sales",
                title="Sales by Category",
                template="plotly_white",
                color="Sales",
                color_continuous_scale="RdYlBu",
            )

        # Render row 1
        row1_charts = [
            {"figure": fig_trend, "title": "Sales Trend Over Time"},
            {"figure": fig_category, "title": "Sales by Category"},
        ]
        render_chart_grid(row1_charts, columns=2)

        st.markdown("---")

        # Charts row 2 - Using dynamic grid layout
        # Create figures for row 2
        region_sales = get_region_sales(filtered_df)
        fig_region = None
        if region_sales is not None:
            fig_region = px.pie(
                region_sales,
                values="Sales",
                names="Region",
                title="Sales Distribution by Region",
                template="plotly_white",
            )

        fig_scatter = None
        if "Profit" in filtered_df.columns and "Category" in filtered_df.columns:
            fig_scatter = px.scatter(
                filtered_df,
                x="Sales",
                y="Profit",
                color="Category",
                title="Sales vs Profit by Category",
                template="plotly_white",
                hover_data=(
                    ["Product Name"] if "Product Name" in filtered_df.columns else None
                ),
            )

        # Render row 2
        row2_charts = [
            {"figure": fig_region, "title": "Sales Distribution by Region"},
            {"figure": fig_scatter, "title": "Sales vs Profit by Category"},
        ]
        render_chart_grid(row2_charts, columns=2)

        st.markdown("---")

        # Top performers
        st.subheader("🏆 Top Performers")
        try:
            col1, col2 = st.columns(2)

            with col1:
                # Top products
                top_products = get_top_products(filtered_df, n=10)
                if top_products is not None and not top_products.empty:
                    st.write("**Top 10 Products by Sales**")
                    display_df = top_products.copy()
                    display_df.columns = ["Product", "Sales"]
                    display_df["Sales"] = display_df["Sales"].apply(
                        lambda x: f"${float(x):,.0f}"
                    )
                    st.dataframe(display_df, hide_index=True, width="stretch")

            with col2:
                # Top customers (if exists)
                top_customers = get_top_customers(filtered_df, n=10)
                if top_customers is not None and not top_customers.empty:
                    st.write("**Top 10 Customers by Sales**")
                    display_df = top_customers.copy()
                    display_df.columns = ["Customer", "Sales"]
                    display_df["Sales"] = display_df["Sales"].apply(
                        lambda x: f"${float(x):,.0f}"
                    )
                    st.dataframe(display_df, hide_index=True, width="stretch")
        except Exception as e:
            st.error(
                f"❌ Error in Top Performers section:\n\n**{type(e).__name__}**: {str(e)}\n\nFull details:\n{repr(e)}"
            )
            import traceback

            st.code(traceback.format_exc(), language="python")

        st.markdown("---")

        # Summary statistics
        with st.expander("📊 Summary Statistics"):
            st.write(filtered_df.describe())

        # Raw data
        with st.expander("📋 View Raw Data"):
            # Create display dataframe with Order Date as string to avoid Arrow serialization issues
            display_df = filtered_df.copy()
            display_df["Order Date"] = display_df["Order Date"].dt.strftime("%Y-%m-%d")
            st.dataframe(display_df, width="stretch")

            # Download button
            csv = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Filtered Data as CSV",
                data=csv,
                file_name=f'sales_data_{datetime.now().strftime("%Y%m%d")}.csv',
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        st.info(
            "Make sure your CSV has columns like: Order Date, Sales, Profit, Category, etc."
        )

else:
    # Landing page
    st.info(
        "👆 **Upload a CSV file or toggle 'Show Sample Data' above to get started!**"
    )
    st.markdown(
        """
    ### Quick Start:
    1. **Upload your CSV** using the file uploader above, OR
    2. **Check the "Show Sample Data"** checkbox to view the Superstore sample dataset
    
    See the **"CSV Format Requirements"** section at the top for details on the required data format.
    """
    )
