from datetime import date, timedelta
import streamlit as st
import pandas as pd

from financial_analytics.daily_analytics import Sale, aggregate_daily_sales
from financial_analytics.financial_metrics import FinancialMetrics
from financial_analytics.inventory_analytics import InventoryItem, analyze_inventory
from financial_analytics.json_reporting import generate_financial_report, report_to_json
from cashflow_forecast import RecurringPayable, forecast_cash_flow

st.set_page_config(page_title="Vyapaari+ Analytics", page_icon="📊", layout="wide")
st.title("📊 Vyapaari+ Financial Analytics")
st.caption("Financial performance, cash-flow forecasting and inventory insights")
st.info("Demo mode: figures are sample inputs, not live business data.")

st.sidebar.header("Business inputs")
revenue = st.sidebar.number_input("Revenue (₹)", min_value=0.0, value=100000.0, step=5000.0)
cost = st.sidebar.number_input("Cost of goods sold (₹)", min_value=0.0, value=60000.0, step=5000.0)
expenses = st.sidebar.number_input("Operating expenses (₹)", min_value=0.0, value=15000.0, step=1000.0)
depreciation = st.sidebar.number_input("Depreciation (₹)", min_value=0.0, value=2000.0, step=500.0)
amortization = st.sidebar.number_input("Amortization (₹)", min_value=0.0, value=1000.0, step=500.0)

metrics = FinancialMetrics(revenue, cost)
report = generate_financial_report(revenue, cost, expenses, depreciation, amortization)

st.header("Financial overview")
a, b, c, d = st.columns(4)
a.metric("Revenue", f"₹{revenue:,.2f}")
b.metric("Gross profit", f"₹{metrics.gross_profit:,.2f}")
c.metric("Gross margin", f"{metrics.gross_margin_percent:.2f}%")
d.metric("EBITDA", f"₹{report['ebitda']:,.2f}")

tab1, tab2, tab3, tab4 = st.tabs([
    "Daily sales", "Cash-flow forecast", "Inventory", "JSON report"
])

with tab1:
    st.subheader("Daily sales aggregation")
    today = date.today()
    sales = [
        Sale(today - timedelta(days=2), 20000, 12000),
        Sale(today - timedelta(days=1), 15000, 8000),
        Sale(today - timedelta(days=1), 5000, 2500),
        Sale(today, revenue, cost),
    ]
    summaries = aggregate_daily_sales(sales)
    rows = [
        {
            "Date": x.sale_date.isoformat(),
            "Revenue (₹)": x.total_revenue,
            "Cost (₹)": x.total_cost,
            "Gross profit (₹)": x.gross_profit,
            "Gross margin (%)": round(x.gross_margin_percent, 2),
        }
        for x in summaries
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.bar_chart(pd.DataFrame(rows).set_index("Date")[["Revenue (₹)", "Gross profit (₹)"]])

with tab2:
    st.subheader("30 / 60 / 90-day cash-flow forecast")
    opening_cash = st.number_input("Opening cash (₹)", min_value=0.0, value=50000.0, step=5000.0)
    daily_receipts = st.number_input("Expected daily receipts (₹)", min_value=0.0, value=3000.0, step=500.0)
    rent = st.number_input("Recurring rent payment (₹)", min_value=0.0, value=10000.0, step=1000.0)
    payable = RecurringPayable("Rent", rent, today + timedelta(days=7), 30)
    forecasts = forecast_cash_flow(today, opening_cash, daily_receipts, [payable])
    forecast_rows = [
        {
            "Period (days)": x.days,
            "End date": x.forecast_end_date.isoformat(),
            "Expected receipts (₹)": x.expected_receipts,
            "Recurring payables (₹)": x.recurring_payables,
            "Projected closing cash (₹)": x.projected_closing_cash,
        }
        for x in forecasts
    ]
    st.dataframe(pd.DataFrame(forecast_rows), use_container_width=True, hide_index=True)
    st.line_chart(pd.DataFrame(forecast_rows).set_index("Period (days)")["Projected closing cash (₹)"])

with tab3:
    st.subheader("Inventory velocity and dead-stock analysis")
    dead_stock_days = st.number_input("Dead-stock threshold (days)", min_value=1, value=90)
    items = [
        InventoryItem("Product A", 40, 250, 30, today - timedelta(days=5)),
        InventoryItem("Product B", 20, 400, 0, today - timedelta(days=100)),
        InventoryItem("Product C", 15, 150, 12, today - timedelta(days=20)),
    ]
    inventory = analyze_inventory(items, today, dead_stock_days)
    inventory_rows = [
        {
            "Product": x.name,
            "Inventory value (₹)": x.inventory_value,
            "Daily sales velocity": round(x.daily_sales_velocity, 2),
            "Days since last sale": x.days_since_last_sale if x.days_since_last_sale is not None else "Never sold",
            "Dead stock": "Yes" if x.is_dead_stock else "No",
        }
        for x in inventory
    ]
    st.dataframe(pd.DataFrame(inventory_rows), use_container_width=True, hide_index=True)
    st.caption("Inventory figures are illustrative sample data.")

with tab4:
    st.subheader("Structured financial report")
    st.json(report)
    st.download_button(
        "Download JSON report",
        data=report_to_json(report),
        file_name="vyapaari_financial_report.json",
        mime="application/json",
    )

st.divider()
st.caption("Vyapaari+ | Financial Analytics & Cash-Flow Forecasting Demo")
