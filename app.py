import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Advanced Sales Dashboard")

# Load data
data = pd.read_csv("sales_data_sample.csv", encoding="ISO-8859-1")

# Convert date
data["ORDERDATE"] = pd.to_datetime(data["ORDERDATE"])

# Sidebar filter
st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Select Year", sorted(data["YEAR_ID"].unique()))

filtered_data = data[data["YEAR_ID"] == selected_year]

# ================= KPI SECTION =================
total_sales = filtered_data["SALES"].sum()
total_orders = len(filtered_data)
avg_order_value = filtered_data["SALES"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("📈 Avg Order Value", f"${avg_order_value:,.0f}")

st.divider()

# ================= Monthly Sales =================
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
    title="Monthly Sales Trend",
)

st.plotly_chart(fig_month, use_container_width=True)

# ================= Product Line =================
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
    title="Sales by Product Line",
)

st.plotly_chart(fig_product, use_container_width=True)

# ================= Country =================
country_sales = (
    filtered_data
    .groupby("COUNTRY")["SALES"]
    .sum()
    .reset_index()
    .sort_values("SALES", ascending=False)
    .head(10)
)

fig_country = px.bar(
    country_sales,
    x="COUNTRY",
    y="SALES",
    title="Top 10 Countries by Sales",
)

st.plotly_chart(fig_country, use_container_width=True)
