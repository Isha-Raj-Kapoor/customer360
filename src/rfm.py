import pandas as pd

def calculate_rfm(df):

    df = df.dropna(subset=["CustomerID"])

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    snapshot_date = df["InvoiceDate"].max()

    rfm = df.groupby("CustomerID").agg({
        "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
        "InvoiceNo": "nunique",
        "Revenue": "sum"
    })

    rfm.columns = ["Recency", "Frequency", "Monetary"]

    rfm.reset_index(inplace=True)

    # ⭐ Create Customer Segments
    rfm["Segment"] = pd.qcut(
        rfm["Monetary"],
        q=3,
        labels=["Low Value", "Medium Value", "High Value"]
    )

    return rfm