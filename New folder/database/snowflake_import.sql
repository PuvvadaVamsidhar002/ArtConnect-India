
-- Snowflake Data Import Script for Handicraft Marketplace Platform

-- Set context
USE DATABASE HANDICRAFT_MARKETPLACE;
USE SCHEMA CORE;

-- Create file formats
CREATE OR REPLACE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null')
    EMPTY_FIELD_AS_NULL = TRUE;

-- Create stages for data loading
CREATE OR REPLACE STAGE handicraft_data
    FILE_FORMAT = csv_format;

-- Instructions for uploading data to stage:
-- 1. Use the Snowflake web interface to upload CSV files to the stage
-- 2. Or use the SnowSQL client with PUT command:
--    PUT file:///path/to/local/file.csv @handicraft_data;

-- Load data into tables
-- Note: Replace with actual stage file paths after uploading

-- 1. Load REGIONS
COPY INTO REGIONS (
    region_id, name, state, description, famous_for, image_url, created_at, updated_at
)
FROM @handicraft_data/regions.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 2. Load ARTISANS
COPY INTO ARTISANS (
    artisan_id, name, location, craft_type, bio, image_url, contact_info, years_active, created_at, updated_at
)
FROM @handicraft_data/artisans.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 3. Load CATEGORIES
COPY INTO CATEGORIES (
    category_id, name, description, image_url, created_at, updated_at
)
FROM @handicraft_data/categories.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 4. Load GI_TAGS
COPY INTO GI_TAGS (
    gi_tag_id, name, description, issuing_body, issue_date, region_id, created_at, updated_at
)
FROM @handicraft_data/gi_tags.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 5. Load CULTURAL_STORIES
COPY INTO CULTURAL_STORIES (
    story_id, title, content, history, cultural_significance, video_url, created_at, updated_at
)
FROM @handicraft_data/cultural_stories.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 6. Load PRODUCTS
COPY INTO PRODUCTS (
    product_id, name, description, price, artisan_id, category_id, region_id, 
    is_gi_tagged, gi_tag_id, story_id, dimensions, weight, materials, created_at, updated_at
)
FROM @handicraft_data/products.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 7. Load PARTNER_SITES
COPY INTO PARTNER_SITES (
    partner_id, name, website_url, rating, review_count, commission_rate, 
    shipping_options, contact_info, logo_url, description, created_at, updated_at
)
FROM @handicraft_data/partner_sites.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 8. Load PRODUCT_PARTNER
COPY INTO PRODUCT_PARTNER (
    id, product_id, partner_id, price, shipping_fee, availability, estimated_delivery, created_at, updated_at
)
FROM @handicraft_data/product_partner.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 9. Load CUSTOMERS
COPY INTO CUSTOMERS (
    customer_id, name, email, password_hash, address, phone, created_at, updated_at
)
FROM @handicraft_data/customers.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 10. Load ORDERS
COPY INTO ORDERS (
    order_id, customer_id, order_date, total_amount, status, 
    shipping_address, payment_method, tracking_number, platform_fee, created_at, updated_at
)
FROM @handicraft_data/orders.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 11. Load ORDER_ITEMS
COPY INTO ORDER_ITEMS (
    item_id, order_id, product_id, partner_id, quantity, price, subtotal, created_at
)
FROM @handicraft_data/order_items.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 12. Load TOURIST_STATS
COPY INTO TOURIST_STATS (
    stat_id, region_id, year, domestic_count, foreign_count, growth_rate, peak_season, created_at, updated_at
)
FROM @handicraft_data/tourist_stats.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- Verify data loading
SELECT 'REGIONS' as table_name, COUNT(*) as row_count FROM REGIONS
UNION ALL
SELECT 'ARTISANS', COUNT(*) FROM ARTISANS
UNION ALL
SELECT 'CATEGORIES', COUNT(*) FROM CATEGORIES
UNION ALL
SELECT 'GI_TAGS', COUNT(*) FROM GI_TAGS
UNION ALL
SELECT 'CULTURAL_STORIES', COUNT(*) FROM CULTURAL_STORIES
UNION ALL
SELECT 'PRODUCTS', COUNT(*) FROM PRODUCTS
UNION ALL
SELECT 'PARTNER_SITES', COUNT(*) FROM PARTNER_SITES
UNION ALL
SELECT 'PRODUCT_PARTNER', COUNT(*) FROM PRODUCT_PARTNER
UNION ALL
SELECT 'CUSTOMERS', COUNT(*) FROM CUSTOMERS
UNION ALL
SELECT 'ORDERS', COUNT(*) FROM ORDERS
UNION ALL
SELECT 'ORDER_ITEMS', COUNT(*) FROM ORDER_ITEMS
UNION ALL
SELECT 'TOURIST_STATS', COUNT(*) FROM TOURIST_STATS;
