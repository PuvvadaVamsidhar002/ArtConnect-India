# Handicraft Marketplace Platform - Architecture Design

## Overview

The Handicraft Marketplace Platform is a centralized online marketplace that connects multiple local handicraft websites across India. This document outlines the architecture design for both frontend and backend components, ensuring seamless integration with Snowflake database, QR code transparency features, and cultural storytelling elements.

## System Architecture

The platform follows a modern, scalable architecture with clear separation of concerns:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Client Layer   │◄───►│  Backend Layer  │◄───►│  Database Layer │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ React Frontend  │     │  Flask API      │     │   Snowflake     │
│ - Home Page     │     │ - RESTful APIs  │     │   Database      │
│ - Product Page  │     │ - Auth Service  │     │ - Core Schema   │
│ - Artisan Page  │     │ - QR Service    │     │ - Analytics     │
│ - Partner Page  │     │ - Payment       │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │
                        ┌─────────────────┐
                        │ External APIs   │
                        │ - Payment       │
                        │ - Shipping      │
                        │ - Partner Sites │
                        └─────────────────┘
```

## Frontend Architecture

The frontend is built using React with a component-based architecture for maximum reusability and maintainability.

### Key Components

1. **Core Components**
   - Header/Navigation
   - Footer
   - Search Bar
   - Authentication Modal
   - QR Code Scanner/Viewer

2. **Page Components**
   - Home Page
   - Product Listing Page
   - Product Detail Page
   - Artisan Profile Page
   - Partner Website Integration Page
   - Cultural Story Page
   - Shopping Cart & Checkout
   - User Dashboard

3. **Feature Components**
   - Product Card
   - Artisan Card
   - Partner Selection Widget
   - Cultural Story Widget
   - QR Code Transparency Modal
   - Region Explorer
   - Category Browser

### State Management

- Redux for global state management
- React Context for theme and authentication state
- Local component state for UI-specific states

### Responsive Design

- Mobile-first approach using Tailwind CSS
- Responsive breakpoints for various device sizes
- Touch-friendly interactions for mobile users

## Backend Architecture

The backend is built using Flask (Python) with a RESTful API architecture.

### API Structure

1. **Public APIs**
   - Product APIs
   - Artisan APIs
   - Cultural Story APIs
   - Partner Website APIs
   - Region & Category APIs
   - QR Code Generation & Verification APIs

2. **Protected APIs** (require authentication)
   - User Profile APIs
   - Order Management APIs
   - Shopping Cart APIs
   - Wishlist APIs
   - Review & Rating APIs

3. **Admin APIs** (require admin privileges)
   - Dashboard Analytics APIs
   - Partner Management APIs
   - Content Management APIs

### Authentication & Security

- JWT-based authentication
- Role-based access control (Customer, Partner, Admin)
- HTTPS encryption for all communications
- Input validation and sanitization
- Rate limiting for API endpoints

### Snowflake Integration

- Snowflake Python connector for database operations
- Connection pooling for efficient resource utilization
- Prepared statements for secure database queries
- Caching layer for frequently accessed data

## QR Code Transparency System

The QR code system is a key feature that provides transparency about products, artisans, and pricing.

### QR Code Generation

1. Each product is assigned a unique QR code based on its product_id
2. QR codes are generated using the Python `qrcode` library
3. QR codes link to a dedicated transparency page with product details

### QR Code Content

When scanned, the QR code provides:
- Product details and authenticity verification
- Artisan information and background
- Pricing breakdown showing platform fee and artisan earnings
- Cultural significance and story
- Partner website details

### Implementation

```python
# QR Code Generation Service
def generate_product_qr(product_id):
    # Call Snowflake stored procedure to get QR data
    qr_data = snowflake_connector.call_procedure('GET_QR_CODE_DATA', [product_id])
    
    # Generate QR code with product transparency URL
    qr_url = f"https://handicraftheritage.com/transparency/{product_id}"
    qr = qrcode.make(qr_url)
    
    # Save and return QR code image
    qr_path = f"/static/qrcodes/{product_id}.png"
    qr.save(qr_path)
    return qr_path
```

## Data Flow Architecture

### Product Listing Flow

1. User visits the platform
2. Frontend requests product listings from backend API
3. Backend queries Snowflake for product data
4. Backend enriches product data with cultural stories and artisan information
5. Frontend renders product listings with filtering and sorting options

### Product Purchase Flow

1. User selects a product and partner website
2. User adds product to cart and proceeds to checkout
3. Backend validates order and calculates revenue sharing
4. Payment is processed and order is created in database
5. Partner website is notified of the new order
6. Order confirmation is sent to the user

### QR Code Transparency Flow

1. User scans QR code on a product
2. QR code directs to transparency page with product_id
3. Backend retrieves comprehensive product data from Snowflake
4. Frontend displays transparency information including artisan details and pricing breakdown

## Integration Points

### Partner Website Integration

- API endpoints for partner websites to update product availability and pricing
- Webhook notifications for new orders
- Authentication system for secure partner access

### Payment Gateway Integration

- Integration with popular payment gateways (Razorpay, PayTM, etc.)
- Secure handling of payment information
- Support for multiple payment methods

### Analytics Integration

- Event tracking for user interactions
- Conversion funnel analysis
- Sales and revenue reporting

## Scalability Considerations

1. **Horizontal Scaling**
   - Stateless backend services for easy scaling
   - Load balancing across multiple instances
   - Containerization for deployment flexibility

2. **Performance Optimization**
   - CDN for static assets
   - Image optimization and lazy loading
   - Database query optimization
   - Caching strategies for frequently accessed data

3. **Global Reach**
   - Multi-region deployment options
   - Content delivery optimization
   - Internationalization and localization support

## Security Architecture

1. **Data Protection**
   - Encryption of sensitive data at rest and in transit
   - Secure storage of authentication credentials
   - Regular security audits and penetration testing

2. **Application Security**
   - CSRF protection
   - XSS prevention
   - SQL injection prevention
   - Input validation and sanitization

3. **Infrastructure Security**
   - Firewall configuration
   - Network security groups
   - Regular security patches and updates

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Production Environment                 │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │             │    │             │    │             │  │
│  │   Frontend  │    │   Backend   │    │  Snowflake  │  │
│  │   (React)   │    │   (Flask)   │    │  Database   │  │
│  │             │    │             │    │             │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    Staging Environment                   │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │             │    │             │    │             │  │
│  │   Frontend  │    │   Backend   │    │  Snowflake  │  │
│  │   (React)   │    │   (Flask)   │    │  Database   │  │
│  │             │    │             │    │             │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                 Development Environment                  │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │             │    │             │    │             │  │
│  │   Frontend  │    │   Backend   │    │  Snowflake  │  │
│  │   (React)   │    │   (Flask)   │    │  Database   │  │
│  │             │    │             │    │             │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- React.js for UI components
- Redux for state management
- Tailwind CSS for styling
- Axios for API requests
- React Router for navigation
- Jest for testing

### Backend
- Flask (Python) for API server
- Flask-RESTful for API endpoints
- Flask-JWT-Extended for authentication
- SQLAlchemy for ORM (when needed)
- Snowflake connector for database operations
- Pytest for testing

### Database
- Snowflake for primary data storage
- Redis for caching (optional)

### DevOps
- Docker for containerization
- GitHub Actions for CI/CD
- AWS/Azure/GCP for cloud hosting

## API Endpoints

### Product APIs

```
GET /api/products - List all products with pagination
GET /api/products/{id} - Get product details
GET /api/products/category/{category_id} - List products by category
GET /api/products/region/{region_id} - List products by region
GET /api/products/artisan/{artisan_id} - List products by artisan
GET /api/products/search - Search products by keywords
```

### Artisan APIs

```
GET /api/artisans - List all artisans with pagination
GET /api/artisans/{id} - Get artisan details
GET /api/artisans/region/{region_id} - List artisans by region
GET /api/artisans/craft/{craft_type} - List artisans by craft type
```

### Partner Website APIs

```
GET /api/partners - List all partner websites
GET /api/partners/{id} - Get partner details
GET /api/partners/product/{product_id} - List partners offering a product
```

### Order APIs

```
POST /api/orders - Create a new order
GET /api/orders/{id} - Get order details
GET /api/orders/user/{user_id} - List orders by user
PUT /api/orders/{id}/status - Update order status
```

### QR Code APIs

```
GET /api/qrcode/product/{product_id} - Generate QR code for product
GET /api/transparency/{product_id} - Get transparency data for product
```

### Authentication APIs

```
POST /api/auth/register - Register new user
POST /api/auth/login - User login
POST /api/auth/refresh - Refresh access token
POST /api/auth/logout - User logout
```

## Conclusion

This architecture design provides a comprehensive blueprint for implementing the Handicraft Marketplace Platform. The design emphasizes scalability, security, and maintainability while supporting the unique features of the platform such as QR code transparency and cultural storytelling. The clear separation of concerns between frontend, backend, and database layers ensures that each component can be developed, tested, and deployed independently.

The next steps involve implementing this architecture, starting with the backend API development and Snowflake integration, followed by the frontend implementation based on the provided HTML templates.
