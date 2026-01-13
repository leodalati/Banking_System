import streamlit as st
import pandas as pd

st.set_page_config(page_title="Banking BI Dashboard", layout="wide")

st.title("🏦 Banking Transaction BI Dashboard")

# Load transaction data
try:
    df = pd.read_csv("transactions.csv")
    df["date"] = pd.to_datetime(df["date"])
except FileNotFoundError:
    st.warning("No transactions found yet.")
    st.stop()

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", len(df))
col2.metric("Total Deposited", df[df["transaction_type"] == "Deposit"]["amount"].sum())
col3.metric("Total Withdrawn", df[df["transaction_type"] == "Withdraw"]["amount"].sum())

st.divider()

# Charts
st.subheader("Transaction Volume Over Time")
st.line_chart(df.groupby(df["date"].dt.date)["amount"].sum())

st.subheader("Transaction Breakdown")
st.bar_chart(df["transaction_type"].value_counts())

st.subheader("Raw Transaction Data")
st.dataframe(df)
