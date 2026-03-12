WITH raw_cleaned AS (
    SELECT DISTINCT ON (invoice_no, stock_code, customer_id, invoice_date)
        COALESCE(NULLIF(TRIM(customer_id), ''), 'UNKNOWN') as customer_id,
        COALESCE(NULLIF(TRIM(description), ''), 'Unknown Product') as description,
        COALESCE(stock_code, 'UNKNOWN') as stock_code,
        ABS(quantity) as quantity,  
        ABS(unit_price) as unit_price,  
        invoice_date::TIMESTAMP as invoice_date,
        TRIM(invoice_no) as invoice_no,
        TRIM(country) as country,
        ABS(quantity) * ABS(unit_price) as revenue,
        DATE(invoice_date) as transaction_date,
        EXTRACT(YEAR FROM invoice_date) as year,
        EXTRACT(MONTH FROM invoice_date) as month,
        EXTRACT(QUARTER FROM invoice_date) as quarter
    FROM raw_transactions
    WHERE invoice_no NOT LIKE 'C%'  
        AND quantity > 0 
        AND unit_price > 0
        AND invoice_date IS NOT NULL
        AND LENGTH(TRIM(customer_id)) >= 5  
)

INSERT INTO dim_customer (customer_id, country, first_purchase_date)
SELECT DISTINCT
    customer_id,
    country,
    MIN(transaction_date) as first_purchase_date
FROM raw_cleaned
WHERE customer_id != 'UNKNOWN'
GROUP BY customer_id, country
ON CONFLICT (customer_id) 
DO UPDATE SET 
    country = EXCLUDED.country,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dim_product (product_id, product_name, unit_price)
SELECT DISTINCT
    stock_code,
    description,
    unit_price
FROM raw_cleaned
ON CONFLICT (product_id) 
DO NOTHING;

INSERT INTO fact_sales (
    invoice_no,
    customer_id,
    product_id,
    date_id,
    quantity,
    unit_price,
    revenue
)
SELECT
    invoice_no,
    customer_id,
    stock_code,
    transaction_date,
    quantity,
    unit_price,
    revenue
FROM raw_cleaned
WHERE customer_id IN (SELECT customer_id FROM dim_customer);

SELECT 
    'High Value Transactions' as check_name,
    COUNT(*) as count,
    AVG(revenue) as avg_value,
    MAX(revenue) as max_value
FROM fact_sales
WHERE revenue > (SELECT AVG(revenue) + 3*STDDEV(revenue) FROM fact_sales);