-- Snowflake Database Setup Script for Handicraft Marketplace Platform

-- Create database
CREATE DATABASE IF NOT EXISTS HANDICRAFT_MARKETPLACE;
USE DATABASE HANDICRAFT_MARKETPLACE;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS CORE;
CREATE SCHEMA IF NOT EXISTS ANALYTICS;

-- Set context
USE SCHEMA CORE;

-- Create tables based on schema design

-- 1. ARTISANS table
CREATE OR REPLACE TABLE ARTISANS (
    artisan_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    craft_type VARCHAR(50) NOT NULL,
    bio TEXT,
    image_url VARCHAR(255),
    contact_info VARCHAR(255),
    years_active INTEGER,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 2. CATEGORIES table
CREATE OR REPLACE TABLE CATEGORIES (
    category_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    image_url VARCHAR(255),
    parent_category_id VARCHAR(36),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (parent_category_id) REFERENCES CATEGORIES(category_id)
);

-- 3. REGIONS table
CREATE OR REPLACE TABLE REGIONS (
    region_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    description TEXT,
    tourist_count INTEGER,
    famous_for TEXT,
    image_url VARCHAR(255),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 4. GI_TAGS table
CREATE OR REPLACE TABLE GI_TAGS (
    gi_tag_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    issuing_body VARCHAR(100),
    issue_date DATE,
    region_id VARCHAR(36),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (region_id) REFERENCES REGIONS(region_id)
);

-- 5. CULTURAL_STORIES table
CREATE OR REPLACE TABLE CULTURAL_STORIES (
    story_id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT,
    history TEXT,
    cultural_significance TEXT,
    image_urls ARRAY,
    video_url VARCHAR(255),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 6. PRODUCTS table
CREATE OR REPLACE TABLE PRODUCTS (
    product_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    artisan_id VARCHAR(36),
    category_id VARCHAR(36),
    region_id VARCHAR(36),
    is_gi_tagged BOOLEAN DEFAULT FALSE,
    gi_tag_id VARCHAR(36),
    story_id VARCHAR(36),
    image_urls ARRAY,
    dimensions VARCHAR(100),
    weight DECIMAL(6,2),
    materials VARCHAR(255),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (artisan_id) REFERENCES ARTISANS(artisan_id),
    FOREIGN KEY (category_id) REFERENCES CATEGORIES(category_id),
    FOREIGN KEY (region_id) REFERENCES REGIONS(region_id),
    FOREIGN KEY (gi_tag_id) REFERENCES GI_TAGS(gi_tag_id),
    FOREIGN KEY (story_id) REFERENCES CULTURAL_STORIES(story_id)
);

-- 7. PARTNER_SITES table
CREATE OR REPLACE TABLE PARTNER_SITES (
    partner_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    website_url VARCHAR(255),
    rating DECIMAL(3,2),
    review_count INTEGER DEFAULT 0,
    commission_rate DECIMAL(4,2) NOT NULL,
    shipping_options VARIANT,
    contact_info VARCHAR(255),
    logo_url VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 8. PRODUCT_PARTNER junction table
CREATE OR REPLACE TABLE PRODUCT_PARTNER (
    id VARCHAR(36) PRIMARY KEY,
    product_id VARCHAR(36) NOT NULL,
    partner_id VARCHAR(36) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    shipping_fee DECIMAL(6,2) DEFAULT 0,
    availability VARCHAR(20) DEFAULT 'In Stock',
    estimated_delivery VARCHAR(50),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (product_id) REFERENCES PRODUCTS(product_id),
    FOREIGN KEY (partner_id) REFERENCES PARTNER_SITES(partner_id)
);

-- 9. CUSTOMERS table
CREATE OR REPLACE TABLE CUSTOMERS (
    customer_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- 10. ORDERS table
CREATE OR REPLACE TABLE ORDERS (
    order_id VARCHAR(36) PRIMARY KEY,
    customer_id VARCHAR(36) NOT NULL,
    order_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    total_amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Processing',
    shipping_address TEXT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    tracking_number VARCHAR(100),
    platform_fee DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id)
);

-- 11. ORDER_ITEMS table
CREATE OR REPLACE TABLE ORDER_ITEMS (
    item_id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    partner_id VARCHAR(36) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (order_id) REFERENCES ORDERS(order_id),
    FOREIGN KEY (product_id) REFERENCES PRODUCTS(product_id),
    FOREIGN KEY (partner_id) REFERENCES PARTNER_SITES(partner_id)
);

-- 12. TOURIST_STATS table
CREATE OR REPLACE TABLE TOURIST_STATS (
    stat_id VARCHAR(36) PRIMARY KEY,
    region_id VARCHAR(36) NOT NULL,
    year INTEGER NOT NULL,
    domestic_count INTEGER,
    foreign_count INTEGER,
    growth_rate DECIMAL(5,2),
    peak_season VARCHAR(50),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (region_id) REFERENCES REGIONS(region_id)
);

-- Create analytics views
USE SCHEMA ANALYTICS;

-- View for product sales analytics
CREATE OR REPLACE VIEW PRODUCT_SALES_ANALYTICS AS
SELECT 
    p.product_id,
    p.name AS product_name,
    p.category_id,
    c.name AS category_name,
    p.region_id,
    r.name AS region_name,
    p.artisan_id,
    a.name AS artisan_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.subtotal) AS total_revenue,
    AVG(oi.price) AS average_selling_price
FROM CORE.PRODUCTS p
JOIN CORE.CATEGORIES c ON p.category_id = c.category_id
JOIN CORE.REGIONS r ON p.region_id = r.region_id
JOIN CORE.ARTISANS a ON p.artisan_id = a.artisan_id
JOIN CORE.ORDER_ITEMS oi ON p.product_id = oi.product_id
JOIN CORE.ORDERS o ON oi.order_id = o.order_id
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8;

-- View for partner performance analytics
CREATE OR REPLACE VIEW PARTNER_PERFORMANCE_ANALYTICS AS
SELECT 
    ps.partner_id,
    ps.name AS partner_name,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    SUM(oi.quantity) AS total_products_sold,
    SUM(oi.subtotal) AS total_revenue,
    SUM(o.platform_fee) AS total_platform_fees,
    (SUM(oi.subtotal) - SUM(o.platform_fee)) AS partner_revenue
FROM CORE.PARTNER_SITES ps
JOIN CORE.ORDER_ITEMS oi ON ps.partner_id = oi.partner_id
JOIN CORE.ORDERS o ON oi.order_id = o.order_id
GROUP BY 1, 2;

-- View for regional sales and tourism correlation
CREATE OR REPLACE VIEW REGION_TOURISM_SALES_CORRELATION AS
SELECT 
    r.region_id,
    r.name AS region_name,
    r.state,
    ts.year,
    ts.domestic_count,
    ts.foreign_count,
    (ts.domestic_count + ts.foreign_count) AS total_tourists,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.subtotal) AS total_sales
FROM CORE.REGIONS r
JOIN CORE.TOURIST_STATS ts ON r.region_id = ts.region_id
JOIN CORE.PRODUCTS p ON r.region_id = p.region_id
JOIN CORE.ORDER_ITEMS oi ON p.product_id = oi.product_id
JOIN CORE.ORDERS o ON oi.order_id = o.order_id
WHERE EXTRACT(YEAR FROM o.order_date) = ts.year
GROUP BY 1, 2, 3, 4, 5, 6, 7;

-- Create stored procedures for common operations

-- Procedure to generate QR code data for a product
CREATE OR REPLACE PROCEDURE GET_QR_CODE_DATA(PRODUCT_ID VARCHAR)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS
$$
    var sql = `
        SELECT 
            p.product_id,
            p.name AS product_name,
            p.description,
            p.price AS base_price,
            p.dimensions,
            p.weight,
            p.materials,
            a.artisan_id,
            a.name AS artisan_name,
            a.location AS artisan_location,
            a.craft_type,
            a.years_active,
            r.name AS region_name,
            r.state,
            CASE WHEN p.is_gi_tagged THEN g.name ELSE NULL END AS gi_tag_name,
            CASE WHEN p.is_gi_tagged THEN g.description ELSE NULL END AS gi_tag_description,
            cs.title AS story_title,
            cs.content AS story_content,
            cs.history,
            cs.cultural_significance
        FROM CORE.PRODUCTS p
        LEFT JOIN CORE.ARTISANS a ON p.artisan_id = a.artisan_id
        LEFT JOIN CORE.REGIONS r ON p.region_id = r.region_id
        LEFT JOIN CORE.GI_TAGS g ON p.gi_tag_id = g.gi_tag_id
        LEFT JOIN CORE.CULTURAL_STORIES cs ON p.story_id = cs.story_id
        WHERE p.product_id = ?
    `;
    
    var stmt = snowflake.createStatement({sqlText: sql, binds: [PRODUCT_ID]});
    var result = stmt.execute();
    
    if (result.next()) {
        var product_data = {};
        
        // Basic product info
        product_data.product_id = result.getColumnValue(1);
        product_data.product_name = result.getColumnValue(2);
        product_data.description = result.getColumnValue(3);
        product_data.base_price = result.getColumnValue(4);
        product_data.dimensions = result.getColumnValue(5);
        product_data.weight = result.getColumnValue(6);
        product_data.materials = result.getColumnValue(7);
        
        // Artisan info
        product_data.artisan = {
            id: result.getColumnValue(8),
            name: result.getColumnValue(9),
            location: result.getColumnValue(10),
            craft_type: result.getColumnValue(11),
            years_active: result.getColumnValue(12)
        };
        
        // Region info
        product_data.region = {
            name: result.getColumnValue(13),
            state: result.getColumnValue(14)
        };
        
        // GI tag info if applicable
        if (result.getColumnValue(15)) {
            product_data.gi_tag = {
                name: result.getColumnValue(15),
                description: result.getColumnValue(16)
            };
        }
        
        // Cultural story
        product_data.cultural_story = {
            title: result.getColumnValue(17),
            content: result.getColumnValue(18),
            history: result.getColumnValue(19),
            cultural_significance: result.getColumnValue(20)
        };
        
        // Get partner pricing
        var partner_sql = `
            SELECT 
                ps.partner_id,
                ps.name,
                ps.rating,
                ps.review_count,
                pp.price,
                pp.shipping_fee,
                pp.availability,
                pp.estimated_delivery
            FROM CORE.PRODUCT_PARTNER pp
            JOIN CORE.PARTNER_SITES ps ON pp.partner_id = ps.partner_id
            WHERE pp.product_id = ?
        `;
        
        var partner_stmt = snowflake.createStatement({sqlText: partner_sql, binds: [PRODUCT_ID]});
        var partner_result = partner_stmt.execute();
        
        var partners = [];
        while (partner_result.next()) {
            partners.push({
                partner_id: partner_result.getColumnValue(1),
                name: partner_result.getColumnValue(2),
                rating: partner_result.getColumnValue(3),
                review_count: partner_result.getColumnValue(4),
                price: partner_result.getColumnValue(5),
                shipping_fee: partner_result.getColumnValue(6),
                availability: partner_result.getColumnValue(7),
                estimated_delivery: partner_result.getColumnValue(8)
            });
        }
        
        product_data.partners = partners;
        
        return product_data;
    } else {
        return { error: "Product not found" };
    }
$$;

-- Procedure to calculate revenue sharing
CREATE OR REPLACE PROCEDURE CALCULATE_REVENUE_SHARING(ORDER_ID VARCHAR)
RETURNS TABLE(partner_id STRING, partner_name STRING, gross_amount FLOAT, platform_fee FLOAT, partner_revenue FLOAT)
LANGUAGE SQL
AS
$$
    SELECT 
        ps.partner_id,
        ps.name AS partner_name,
        SUM(oi.subtotal) AS gross_amount,
        SUM(oi.subtotal * (ps.commission_rate / 100)) AS platform_fee,
        SUM(oi.subtotal * (1 - ps.commission_rate / 100)) AS partner_revenue
    FROM CORE.ORDER_ITEMS oi
    JOIN CORE.PARTNER_SITES ps ON oi.partner_id = ps.partner_id
    WHERE oi.order_id = ORDER_ID
    GROUP BY 1, 2
$$;

-- Create sample data insertion script (to be used with actual data)
-- This is a placeholder for the actual data import that will happen with the datasets

-- Sample data for REGIONS
INSERT INTO CORE.REGIONS (region_id, name, state, description, tourist_count, famous_for)
VALUES
    ('r-001', 'Jaipur', 'Rajasthan', 'Known as the Pink City, Jaipur is famous for its handicrafts and artisanal work.', 5000000, 'Blue Pottery, Block Printing, Jewelry'),
    ('r-002', 'Varanasi', 'Uttar Pradesh', 'One of the oldest continuously inhabited cities in the world, known for its silk weaving.', 6500000, 'Banarasi Silk, Wooden Toys, Carpets'),
    ('r-003', 'Moradabad', 'Uttar Pradesh', 'Known as the Brass City, famous for its brass handicrafts and artware.', 1200000, 'Brass Work, Metal Crafts'),
    ('r-004', 'Kutch', 'Gujarat', 'Known for its distinctive embroidery and mirror work textiles.', 2000000, 'Embroidery, Mirror Work, Bandhani');

-- Sample data for CATEGORIES
INSERT INTO CORE.CATEGORIES (category_id, name, description)
VALUES
    ('c-001', 'Pottery', 'Handcrafted items made from clay and ceramic materials'),
    ('c-002', 'Textiles', 'Handwoven and handprinted fabrics and garments'),
    ('c-003', 'Woodwork', 'Carved and crafted items made from various types of wood'),
    ('c-004', 'Metalwork', 'Items crafted from brass, copper, and other metals');

-- Sample data for GI_TAGS
INSERT INTO CORE.GI_TAGS (gi_tag_id, name, description, issuing_body, issue_date, region_id)
VALUES
    ('gi-001', 'Blue Pottery of Jaipur', 'A traditional craft involving blue-glazed pottery with Persian influences', 'Geographical Indications Registry, India', '2008-09-14', 'r-001'),
    ('gi-002', 'Banarasi Silk', 'Fine silk fabric with intricate designs woven with gold or silver threads', 'Geographical Indications Registry, India', '2009-09-16', 'r-002');

-- Create secure views for sensitive data
USE SCHEMA CORE;

-- Secure view for artisan contact information (accessible only to authorized users)
CREATE OR REPLACE SECURE VIEW ARTISAN_CONTACT_INFO AS
SELECT 
    artisan_id,
    name,
    contact_info
FROM ARTISANS;

-- Secure view for customer information (accessible only to authorized users)
CREATE OR REPLACE SECURE VIEW CUSTOMER_INFO AS
SELECT 
    customer_id,
    name,
    email,
    address,
    phone
FROM CUSTOMERS;

-- Grant appropriate permissions
GRANT USAGE ON DATABASE HANDICRAFT_MARKETPLACE TO ROLE PUBLIC;
GRANT USAGE ON SCHEMA CORE TO ROLE PUBLIC;
GRANT USAGE ON SCHEMA ANALYTICS TO ROLE PUBLIC;
GRANT SELECT ON ALL TABLES IN SCHEMA CORE TO ROLE PUBLIC;
GRANT SELECT ON ALL VIEWS IN SCHEMA ANALYTICS TO ROLE PUBLIC;
