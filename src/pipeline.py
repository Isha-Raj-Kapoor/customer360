import os
import logging
import pandas as pd
from db_connection import get_engine
from rfm import calculate_rfm
from clv import calculate_clv
from basket import market_basket

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logs_dir = os.path.join(BASE_DIR, "logs")
output_dir = os.path.join(BASE_DIR, "output")

os.makedirs(logs_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

log_file = os.path.join(logs_dir, "pipeline.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("🚀 Pipeline Started")

try:

    engine = get_engine()

    df = pd.read_sql("SELECT * FROM sales", engine)

    logging.info("Data loaded from database")

    rfm = calculate_rfm(df)

    rfm_path = os.path.join(output_dir, "rfm_output.csv")
    rfm.to_csv(rfm_path, index=False)

    logging.info("RFM file saved")

    clv = calculate_clv(rfm)

    clv_path = os.path.join(output_dir, "clv_output.csv")
    clv.to_csv(clv_path, index=False)

    logging.info("CLV file saved")

    segments = rfm[["CustomerID", "Segment"]]

    segments_path = os.path.join(output_dir, "customer_segments.csv")
    segments.to_csv(segments_path, index=False)

    logging.info("Customer segments file saved")

    rules = market_basket(df)

    rules_path = os.path.join(output_dir, "basket_rules.csv")
    rules.to_csv(rules_path, index=False)

    logging.info("Market basket rules saved")

    logging.info("✅ Pipeline Completed Successfully")

    print("Pipeline Completed Successfully")

except Exception as e:

    logging.error(f"Pipeline Failed: {str(e)}")
    print("Pipeline Failed:", e)