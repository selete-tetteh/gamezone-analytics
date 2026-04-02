-- =============================================================
-- GameZone Analytics — MySQL Schema
-- Run this in MySQL Workbench to set up the database
-- =============================================================

CREATE DATABASE IF NOT EXISTS gamezone_analytics
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE gamezone_analytics;

-- ---------------------------------------------------------------
-- Raw orders table (mirrors the Excel source exactly)
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders_raw (
    user_id               VARCHAR(50),
    order_id              VARCHAR(50)        PRIMARY KEY,
    purchase_ts           DATETIME,
    ship_ts               DATETIME,
    product_name          VARCHAR(100),
    product_id            VARCHAR(20),
    usd_price             DECIMAL(10, 2),
    purchase_platform     VARCHAR(20),
    marketing_channel     VARCHAR(30),
    account_creation_method VARCHAR(20),
    country_code          CHAR(2),
    created_at            TIMESTAMP          DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------
-- Region lookup table
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS region_lookup (
    country_code  CHAR(2)     PRIMARY KEY,
    region        VARCHAR(20)
);

-- ---------------------------------------------------------------
-- Cleaned orders view (used by all analysis notebooks)
-- Applies business rules:
--   - Excludes $0 prices (likely test/cancelled orders)
--   - Standardises product names
--   - Calculates fulfilment days
-- ---------------------------------------------------------------
CREATE OR REPLACE VIEW orders_clean AS
SELECT
    user_id,
    order_id,
    purchase_ts,
    ship_ts,
    -- Standardise duplicate product names
    CASE
        WHEN product_name = '27inches 4k gaming monitor' THEN '27in 4K gaming monitor'
        ELSE product_name
    END                                             AS product_name,
    product_id,
    usd_price,
    purchase_platform,
    COALESCE(marketing_channel, 'unknown')          AS marketing_channel,
    COALESCE(account_creation_method, 'unknown')    AS account_creation_method,
    o.country_code,
    COALESCE(r.region, 'Other')                     AS region,
    DATEDIFF(ship_ts, purchase_ts)                  AS fulfilment_days,
    YEAR(purchase_ts)                               AS purchase_year,
    MONTH(purchase_ts)                              AS purchase_month
FROM orders_raw o
LEFT JOIN region_lookup r USING (country_code)
WHERE usd_price > 0
  AND purchase_ts IS NOT NULL;

-- ---------------------------------------------------------------
-- Useful analytical queries (saved for reuse)
-- ---------------------------------------------------------------

-- Monthly revenue by product
-- SELECT
--     DATE_FORMAT(purchase_ts, '%Y-%m')  AS month,
--     product_name,
--     COUNT(*)                           AS order_count,
--     ROUND(SUM(usd_price), 2)           AS total_revenue,
--     ROUND(AVG(usd_price), 2)           AS avg_order_value
-- FROM orders_clean
-- GROUP BY 1, 2
-- ORDER BY 1, 2;

-- Revenue by marketing channel and region
-- SELECT
--     region,
--     marketing_channel,
--     COUNT(DISTINCT user_id)            AS unique_customers,
--     COUNT(*)                           AS orders,
--     ROUND(SUM(usd_price), 2)           AS revenue
-- FROM orders_clean
-- GROUP BY 1, 2
-- ORDER BY revenue DESC;
