import streamlit as st
import pandas as pd

st.title("Customer Lifetime Value")

clv = pd.read_csv("output/clv_output.csv")

clv.columns = clv.columns.str.lower()

top = clv.sort_values("clv", ascending=False).head(10)

st.subheader("Top Customers")

st.bar_chart(top.set_index("customerid")["clv"])

st.dataframe(top)