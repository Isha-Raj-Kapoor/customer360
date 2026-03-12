# Customer 360 – RFM, CLV & Market Basket Engine

This project builds a production-style customer analytics pipeline using:

- MySQL (Data Storage & Cleaning)
- Python (RFM, CLV, Association Rules)
- Power BI (Dashboard)

## How to Run

1. Import OnlineRetail.csv into MySQL
2. Run cleaning_queries.sql
3. Install requirements:

pip install -r requirements.txt

4. Run pipeline:

python src/pipeline.py

Outputs are generated in /output folder.