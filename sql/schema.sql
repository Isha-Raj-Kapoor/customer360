CREATE TABLE dim_customer (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(200),
    country VARCHAR(100),
    signup_date DATE,
    first_purchase_date DATE,
    customer_segment VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_product (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(300),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    unit_price DECIMAL(10,2),
    supplier VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    week INT,
    day_of_week INT,
    is_weekend BOOLEAN
);

CREATE TABLE dim_geography (
    country_id SERIAL PRIMARY KEY,
    country VARCHAR(100),
    region VARCHAR(100),
    continent VARCHAR(50)
);

CREATE TABLE fact_sales (
    sale_id BIGSERIAL PRIMARY KEY,
    invoice_no VARCHAR(50),
    customer_id VARCHAR(50) REFERENCES dim_customer(customer_id),
    product_id VARCHAR(50) REFERENCES dim_product(product_id),
    date_id DATE REFERENCES dim_date(date_id),
    country_id INT REFERENCES dim_geography(country_id),
    quantity INT,
    unit_price DECIMAL(10,2),
    revenue DECIMAL(12,2),
    discount DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_customer (customer_id),
    INDEX idx_product (product_id),
    INDEX idx_date (date_id),
    INDEX idx_invoice (invoice_no)
);

CREATE INDEX idx_fact_sales_date ON fact_sales(date_id);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_id);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_id);
CREATE INDEX idx_fact_sales_revenue ON fact_sales(revenue);