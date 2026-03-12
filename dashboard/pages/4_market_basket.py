import streamlit as st
import pandas as pd

st.title("Market Basket Analysis")

rules = pd.read_csv("output/basket_rules.csv")

st.subheader("Association Rules")

st.dataframe(rules.head())

product = st.text_input("Enter product name")

if product:

    rec = rules[rules['antecedents'].str.contains(product)]

    st.subheader("Recommended Products")

    st.dataframe(rec[['consequents','confidence','lift']])