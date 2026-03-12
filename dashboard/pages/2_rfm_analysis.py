import streamlit as st
import pandas as pd
import os

st.title("RFM Customer Segmentation")

file = "output/customer_segments.csv"

if os.path.exists(file) and os.path.getsize(file) > 0:

    rfm = pd.read_csv(file)

    st.bar_chart(rfm["Segment"].value_counts())

    st.dataframe(rfm)

else:
    st.error("customer_segments.csv is empty. Run rfm_analysis.py first.")