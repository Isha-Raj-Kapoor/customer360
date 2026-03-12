import streamlit as st
import pandas as pd

st.title("Sales Overview")

rfm = pd.read_csv("output/rfm_output.csv")

total_customers = rfm['CustomerID'].nunique()

st.metric("Total Customers", total_customers)

st.subheader("Customer Frequency Distribution")

st.bar_chart(rfm['Frequency'])