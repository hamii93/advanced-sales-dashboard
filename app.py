import pandas as pd
import streamlit as st
import plotly.express as px

# ================= CONFIG =================
st.set_page_config(page_title="Advanced Sales Dashboard", layout="wide")

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    data = pd.read_csv("sales_data_sample.csv", encoding="ISO-8859-1")
    data["ORDERDATE"] = pd.to_datetime(data["ORDERDATE"])
    return data

data = load_data()

# ================= SIDEBAR =================
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Overview", "Regional Analysis", "Product Insights"])

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(data["YEAR_ID"].unique())
)

filtered_data = data[data["YEAR_ID"] == selected_year]

# ================= OVERVIEW =================
if page == "Overview":

    st.title("📊 Sales Overview")

    total_sales = filtered_data["SALES"].sum()
    total_orders = len(filtered_data)
    avg_order_value = filtered_data["SALES"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
    col2.metric("📦 Total Orders", total_orders)
    col3.metric("📈 Avg Order Value", f"${avg_order_value:,.0f}")

    st.divider()

    monthly_sales = (
        filtered_data
        .groupby("MONTH_ID")["SALES"]
        .sum()
        .reset_index()
    )

    fig_month = px.line(
        monthly_sales,
        x="MONTH_ID",
        y="SALES",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig_month, use_container_width=True)


# ================= REGIONAL ANALYSIS =================
elif page == "Regional Analysis":

    st.title("🌍 Regional Sales Analysis")

    country_sales = (
        filtered_data
        .groupby("COUNTRY")["SALES"]
        .sum()
        .reset_index()
        .sort_values("SALES", ascending=False)
    )

    fig_country = px.bar(
        country_sales.head(10),
        x="COUNTRY",
        y="SALES",
        title="Top 10 Countries by Total Sales"
    )

    st.plotly_chart(fig_country, use_container_width=True)

    st.subheader("Average Order Value by Country")

    country_avg = (
        filtered_data
        .groupby("COUNTRY")["SALES"]
        .mean()
        .reset_index()
        .sort_values("SALES", ascending=False)
    )

    st.dataframe(country_avg)


# ================= PRODUCT INSIGHTS =================
elif page == "Product Insights":

    st.title("📦 Product Performance Analysis")

    product_sales = (
        filtered_data
        .groupby("PRODUCTLINE")["SALES"]
        .sum()
        .reset_index()
        .sort_values("SALES", ascending=False)
    )

    fig_product = px.bar(
        product_sales,
        x="PRODUCTLINE",
        y="SALES",
        title="Sales by Product Line"
    )

    st.plotly_chart(fig_product, use_container_width=True)

    st.subheader("Product Demand Across Countries")

    product_country = (
        filtered_data
        .groupby(["COUNTRY", "PRODUCTLINE"])["SALES"]
        .sum()
        .reset_index()
    )

    pivot_table = product_country.pivot(
        index="COUNTRY",
        columns="PRODUCTLINE",
        values="SALES"
    )

    st.dataframe(pivot_table.fillna(0))
