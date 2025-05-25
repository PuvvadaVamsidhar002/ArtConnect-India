# Handicraft Marketplace Platform - Database Schema Design

## Overview
This document outlines the database schema design for the Handicraft Marketplace Platform, a centralized online marketplace that connects multiple local handicraft websites across India. The schema is designed for implementation in Snowflake and supports all core functionalities including product listings, artisan profiles, partner website integration, order management, QR code transparency, and cultural storytelling.

## Entity Relationship Diagram

```
+----------------+       +----------------+       +----------------+
| ARTISANS       |       | PRODUCTS       |       | PARTNER_SITES  |
+----------------+       +----------------+       +----------------+
| artisan_id (PK)|<----->| product_id (PK)|<----->| partner_id (PK)|
| name           |       | name           |       | name           |
| location       |       | description    |       | website_url    |
| craft_type     |       | price          |       | rating         |
| bio            |       | artisan_id (FK)|       | review_count   |
| image_url      |       | category_id (FK)|      | commission_rate|
| contact_info   |       | region_id (FK) |       | shipping_options|
| years_active   |       | is_gi_tagged   |       | contact_info   |
+----------------+       | gi_tag_id (FK) |       +----------------+
                         | story_id (FK)  |             |
                         | image_urls     |             |
                         +----------------+             |
                                |                       |
                                |                       |
                                v                       v
+----------------+       +----------------+       +----------------+
| CATEGORIES     |       | PRODUCT_PARTNER|       | ORDERS         |
+----------------+       +----------------+       +----------------+
| category_id (PK)|      | id (PK)        |       | order_id (PK)  |
| name           |       | product_id (FK)|       | customer_id (FK)|
| description    |       | partner_id (FK)|       | order_date     |
| image_url      |       | price          |       | total_amount   |
+----------------+       | shipping_fee   |       | status         |
                         | availability   |       | shipping_address|
                         +----------------+       | payment_method |
                                                 +----------------+
                                                        |
                                                        |
                                                        v
+----------------+       +----------------+       +----------------+
| REGIONS        |       | ORDER_ITEMS    |       | CUSTOMERS      |
+----------------+       +----------------+       +----------------+
| region_id (PK) |       | item_id (PK)   |       | customer_id (PK)|
| name           |       | order_id (FK)  |       | name           |
| state          |       | product_id (FK)|       | email          |
| description    |       | partner_id (FK)|       | password_hash  |
| tourist_count  |       | quantity       |       | address        |
| famous_for     |       | price          |       | phone          |
| image_url      |       | subtotal       |       | created_at     |
+----------------+       +----------------+       +----------------+

+----------------+       +----------------+       +----------------+
| GI_TAGS        |       | CULTURAL_STORIES|      | TOURIST_STATS  |
+----------------+       +----------------+       +----------------+
| gi_tag_id (PK) |       | story_id (PK)  |       | stat_id (PK)   |
| name           |       | title          |       | region_id (FK) |
| description    |       | content        |       | year           |
| issuing_body   |       | history        |       | domestic_count |
| issue_date     |       | cultural_signif|       | foreign_count  |
| region_id (FK) |       | image_urls     |       | growth_rate    |
+----------------+       | video_url      |       | peak_season    |
                         +----------------+       +----------------+
```

## Table Definitions

### 1. ARTISANS
Stores information about the artisans who create the handicraft products.

| Column | Type | Description |
|--------|------|-------------|
| artisan_id | VARCHAR(36) | Primary key, unique identifier for each artisan |
| name | VARCHAR(100) | Full name of the artisan |
| location | VARCHAR(100) | City/village and state where the artisan is based |
| craft_type | VARCHAR(50) | Primary craft specialty of the artisan |
| bio | TEXT | Biographical information about the artisan |
| image_url | VARCHAR(255) | URL to the artisan's profile image |
| contact_info | VARCHAR(255) | Contact information (may be encrypted) |
| years_active | INTEGER | Number of years the artisan has been practicing their craft |
| created_at | TIMESTAMP | When the artisan record was created |
| updated_at | TIMESTAMP | When the artisan record was last updated |

### 2. PRODUCTS
Stores information about the handicraft products available on the platform.

| Column | Type | Description |
|--------|------|-------------|
| product_id | VARCHAR(36) | Primary key, unique identifier for each product |
| name | VARCHAR(100) | Name of the product |
| description | TEXT | Detailed description of the product |
| price | DECIMAL(10,2) | Base price of the product (in INR) |
| artisan_id | VARCHAR(36) | Foreign key referencing ARTISANS table |
| category_id | VARCHAR(36) | Foreign key referencing CATEGORIES table |
| region_id | VARCHAR(36) | Foreign key referencing REGIONS table |
| is_gi_tagged | BOOLEAN | Whether the product has a geographical indication tag |
| gi_tag_id | VARCHAR(36) | Foreign key referencing GI_TAGS table (if applicable) |
| story_id | VARCHAR(36) | Foreign key referencing CULTURAL_STORIES table |
| image_urls | ARRAY | Array of URLs to product images |
| dimensions | VARCHAR(100) | Physical dimensions of the product |
| weight | DECIMAL(6,2) | Weight of the product in grams |
| materials | VARCHAR(255) | Materials used in creating the product |
| created_at | TIMESTAMP | When the product record was created |
| updated_at | TIMESTAMP | When the product record was last updated |

### 3. PARTNER_SITES
Stores information about the partner websites that sell products through the platform.

| Column | Type | Description |
|--------|------|-------------|
| partner_id | VARCHAR(36) | Primary key, unique identifier for each partner |
| name | VARCHAR(100) | Name of the partner website/business |
| website_url | VARCHAR(255) | URL to the partner's website |
| rating | DECIMAL(3,2) | Average rating of the partner (out of 5) |
| review_count | INTEGER | Number of reviews for the partner |
| commission_rate | DECIMAL(4,2) | Platform commission rate for this partner (%) |
| shipping_options | VARIANT | JSON object containing shipping options and prices |
| contact_info | VARCHAR(255) | Contact information for the partner |
| logo_url | VARCHAR(255) | URL to the partner's logo |
| description | TEXT | Description of the partner business |
| created_at | TIMESTAMP | When the partner record was created |
| updated_at | TIMESTAMP | When the partner record was last updated |

### 4. CATEGORIES
Stores information about product categories.

| Column | Type | Description |
|--------|------|-------------|
| category_id | VARCHAR(36) | Primary key, unique identifier for each category |
| name | VARCHAR(50) | Name of the category |
| description | TEXT | Description of the category |
| image_url | VARCHAR(255) | URL to the category image |
| parent_category_id | VARCHAR(36) | Self-referencing foreign key for hierarchical categories |
| created_at | TIMESTAMP | When the category record was created |
| updated_at | TIMESTAMP | When the category record was last updated |

### 5. PRODUCT_PARTNER
Junction table that links products to partner websites with specific pricing and availability.

| Column | Type | Description |
|--------|------|-------------|
| id | VARCHAR(36) | Primary key |
| product_id | VARCHAR(36) | Foreign key referencing PRODUCTS table |
| partner_id | VARCHAR(36) | Foreign key referencing PARTNER_SITES table |
| price | DECIMAL(10,2) | Price offered by this partner (may differ from base price) |
| shipping_fee | DECIMAL(6,2) | Shipping fee charged by this partner |
| availability | VARCHAR(20) | Availability status (In Stock, Out of Stock, etc.) |
| estimated_delivery | VARCHAR(50) | Estimated delivery timeframe |
| created_at | TIMESTAMP | When the record was created |
| updated_at | TIMESTAMP | When the record was last updated |

### 6. ORDERS
Stores information about customer orders.

| Column | Type | Description |
|--------|------|-------------|
| order_id | VARCHAR(36) | Primary key, unique identifier for each order |
| customer_id | VARCHAR(36) | Foreign key referencing CUSTOMERS table |
| order_date | TIMESTAMP | When the order was placed |
| total_amount | DECIMAL(12,2) | Total order amount including shipping |
| status | VARCHAR(20) | Order status (Processing, Shipped, Delivered, etc.) |
| shipping_address | TEXT | Shipping address for the order |
| payment_method | VARCHAR(50) | Payment method used |
| tracking_number | VARCHAR(100) | Shipping tracking number |
| platform_fee | DECIMAL(10,2) | Platform fee amount |
| created_at | TIMESTAMP | When the order record was created |
| updated_at | TIMESTAMP | When the order record was last updated |

### 7. ORDER_ITEMS
Stores information about individual items within an order.

| Column | Type | Description |
|--------|------|-------------|
| item_id | VARCHAR(36) | Primary key |
| order_id | VARCHAR(36) | Foreign key referencing ORDERS table |
| product_id | VARCHAR(36) | Foreign key referencing PRODUCTS table |
| partner_id | VARCHAR(36) | Foreign key referencing PARTNER_SITES table |
| quantity | INTEGER | Quantity ordered |
| price | DECIMAL(10,2) | Price per unit at time of purchase |
| subtotal | DECIMAL(10,2) | Subtotal for this item (price * quantity) |
| created_at | TIMESTAMP | When the record was created |

### 8. CUSTOMERS
Stores information about registered customers.

| Column | Type | Description |
|--------|------|-------------|
| customer_id | VARCHAR(36) | Primary key, unique identifier for each customer |
| name | VARCHAR(100) | Customer's full name |
| email | VARCHAR(100) | Customer's email address |
| password_hash | VARCHAR(255) | Hashed password |
| address | TEXT | Customer's address |
| phone | VARCHAR(20) | Customer's phone number |
| created_at | TIMESTAMP | When the customer record was created |
| updated_at | TIMESTAMP | When the customer record was last updated |

### 9. REGIONS
Stores information about geographical regions where products originate.

| Column | Type | Description |
|--------|------|-------------|
| region_id | VARCHAR(36) | Primary key, unique identifier for each region |
| name | VARCHAR(50) | Name of the region |
| state | VARCHAR(50) | State where the region is located |
| description | TEXT | Description of the region and its craft heritage |
| tourist_count | INTEGER | Annual tourist count (reference to detailed stats) |
| famous_for | TEXT | Crafts and products the region is famous for |
| image_url | VARCHAR(255) | URL to an image representing the region |
| created_at | TIMESTAMP | When the region record was created |
| updated_at | TIMESTAMP | When the region record was last updated |

### 10. GI_TAGS
Stores information about Geographical Indication tags for products.

| Column | Type | Description |
|--------|------|-------------|
| gi_tag_id | VARCHAR(36) | Primary key, unique identifier for each GI tag |
| name | VARCHAR(100) | Name of the GI tag |
| description | TEXT | Description of what the GI tag represents |
| issuing_body | VARCHAR(100) | Organization that issued the GI tag |
| issue_date | DATE | When the GI tag was issued |
| region_id | VARCHAR(36) | Foreign key referencing REGIONS table |
| created_at | TIMESTAMP | When the record was created |
| updated_at | TIMESTAMP | When the record was last updated |

### 11. CULTURAL_STORIES
Stores cultural and historical information about crafts and products.

| Column | Type | Description |
|--------|------|-------------|
| story_id | VARCHAR(36) | Primary key, unique identifier for each story |
| title | VARCHAR(100) | Title of the cultural story |
| content | TEXT | Main content of the story |
| history | TEXT | Historical background |
| cultural_significance | TEXT | Cultural significance of the craft/product |
| image_urls | ARRAY | Array of URLs to images related to the story |
| video_url | VARCHAR(255) | URL to a video about the craft/story |
| created_at | TIMESTAMP | When the record was created |
| updated_at | TIMESTAMP | When the record was last updated |

### 12. TOURIST_STATS
Stores detailed tourist statistics by region and year.

| Column | Type | Description |
|--------|------|-------------|
| stat_id | VARCHAR(36) | Primary key |
| region_id | VARCHAR(36) | Foreign key referencing REGIONS table |
| year | INTEGER | Year of the statistics |
| domestic_count | INTEGER | Number of domestic tourists |
| foreign_count | INTEGER | Number of foreign tourists |
| growth_rate | DECIMAL(5,2) | Year-over-year growth rate (%) |
| peak_season | VARCHAR(50) | Peak tourist season for the region |
| created_at | TIMESTAMP | When the record was created |
| updated_at | TIMESTAMP | When the record was last updated |

## QR Code Transparency System

The database schema supports the QR code transparency feature through the following mechanism:

1. Each product will have a unique QR code generated based on its `product_id`
2. When scanned, the QR code will retrieve information from multiple tables:
   - Product details from PRODUCTS table
   - Artisan information from ARTISANS table
   - Pricing breakdown from PRODUCT_PARTNER table
   - Authenticity verification from GI_TAGS table (if applicable)
   - Cultural significance from CULTURAL_STORIES table

This comprehensive data model ensures that customers can access complete transparency about each product's origin, creator, and pricing structure.

## Snowflake-Specific Considerations

1. **Data Warehousing**: The schema is designed to take advantage of Snowflake's columnar storage for efficient analytics on tourist statistics and sales patterns.

2. **Semi-structured Data**: JSON/VARIANT types are used for shipping options and other complex nested data structures.

3. **Time Travel**: Snowflake's time travel capability will be utilized for data recovery and historical analysis of sales trends.

4. **Zero-copy Cloning**: Development and testing environments will leverage Snowflake's zero-copy cloning to maintain data consistency.

5. **Secure Views**: To protect sensitive artisan and customer information, secure views will be implemented in Snowflake.

## Data Flow

1. Product data flows from partner websites into the central platform
2. Customer orders are processed through the platform and distributed to partner websites
3. Revenue sharing calculations are automated based on commission rates
4. Tourist statistics are used for marketing targeting and regional promotion

This schema design provides a solid foundation for the Handicraft Marketplace Platform, supporting all required features while maintaining flexibility for future expansion.
