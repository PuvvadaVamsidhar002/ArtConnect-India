# Handicraft Marketplace Platform - Deployment Guide

This guide provides instructions for running and deploying the Handicraft Marketplace Platform prototype.

## Project Structure

```
handicraft_marketplace/
├── backend/               # Flask backend API
│   ├── requirements.txt   # Python dependencies
│   └── src/               # Source code
├── database/              # Database scripts and processed data
│   ├── processed_data/    # CSV files for import
│   ├── snowflake_setup.sql    # Database setup script
│   └── snowflake_import.sql   # Data import script
├── docs/                  # Documentation
│   ├── architecture.md    # System architecture
│   ├── schema_design.md   # Database schema design
│   └── todo.md            # Project checklist
└── frontend/              # React frontend
    ├── public/            # Static assets
    └── src/               # Source code
```

## Running the Backend

1. Navigate to the backend directory:
   ```
   cd /path/to/handicraft_marketplace/backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and update with your Snowflake credentials.

5. Run the Flask application:
   ```
   python src/app.py
   ```

The backend API will be available at http://localhost:5000.

## Running the Frontend

1. Navigate to the frontend directory:
   ```
   cd /path/to/handicraft_marketplace/frontend
   ```

2. Install dependencies:
   ```
   pnpm install
   ```

3. Start the development server:
   ```
   pnpm run dev
   ```

The frontend will be available at http://localhost:3000.

## Snowflake Database Setup

1. Connect to your Snowflake instance using the Snowflake web interface or CLI.

2. Run the database setup script:
   ```
   USE ROLE ACCOUNTADMIN;
   CREATE DATABASE HANDICRAFT_MARKETPLACE;
   USE DATABASE HANDICRAFT_MARKETPLACE;
   ```

3. Execute the `snowflake_setup.sql` script to create the schema and tables.

4. Execute the `snowflake_import.sql` script to import the processed data.

## Production Deployment

### Backend Deployment

1. Update the `.env` file with production settings.

2. Install Gunicorn:
   ```
   pip install gunicorn
   ```

3. Run with Gunicorn:
   ```
   gunicorn -w 4 -b 0.0.0.0:5000 "src.app:create_app()"
   ```

### Frontend Deployment

1. Build the production version:
   ```
   cd /path/to/handicraft_marketplace/frontend
   pnpm run build
   ```

2. The build output will be in the `dist` directory, which can be served using any static file server.

## Features Overview

- **Product Browsing**: Browse products by category, region, or artisan
- **Cultural Storytelling**: Learn about the cultural significance of each product
- **QR Code Transparency**: Scan QR codes to view artisan details and pricing breakdown
- **Partner Selection**: Choose from multiple partner websites for each product
- **Shopping Cart**: Add products to cart and proceed to checkout
- **Artisan Profiles**: Learn about the artisans behind the products
- **Revenue Sharing**: Transparent pricing showing how revenue is shared

## API Endpoints

- **Products**: `/api/products`, `/api/products/{id}`, `/api/products/category/{id}`, etc.
- **Artisans**: `/api/artisans`, `/api/artisans/{id}`, etc.
- **Partners**: `/api/partners`, `/api/partners/product/{id}`, etc.
- **QR Code**: `/api/qrcode/product/{id}`, `/api/transparency/{id}`
- **Orders**: `/api/orders`, `/api/orders/{id}`, etc.
- **Authentication**: `/api/auth/register`, `/api/auth/login`, etc.

## Hackathon Presentation Tips

1. **Demo Flow**:
   - Start with the homepage to showcase the overall marketplace
   - Navigate to a product page to demonstrate partner selection
   - Show the QR code transparency feature
   - Highlight the cultural storytelling aspect
   - Demonstrate the revenue sharing model

2. **Key Selling Points**:
   - Ethical marketplace connecting artisans to global customers
   - Transparency in pricing and authenticity
   - Cultural preservation through storytelling
   - Scalable platform with AI-driven recommendations
   - Fair trade ensuring artisans receive 80-90% of revenue

3. **Technical Highlights**:
   - Snowflake database for scalable data management
   - Flask backend with RESTful API design
   - React frontend with responsive design
   - QR code generation and verification system
   - Integration with multiple partner websites
