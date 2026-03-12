def calculate_clv(rfm):

    rfm["clv"] = rfm["Monetary"] * rfm["Frequency"]

    return rfm