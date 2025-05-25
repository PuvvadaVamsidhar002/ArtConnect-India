"""
Handicraft Marketplace Platform - Flask Backend Application

This is the main application file that initializes the Flask app,
configures it, and registers all API endpoints.
"""

import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API resources
from api.product_resource import ProductResource, ProductDetailResource, ProductsByCategoryResource, ProductsByRegionResource, ProductsByArtisanResource, ProductSearchResource
from api.artisan_resource import ArtisanResource, ArtisanDetailResource, ArtisansByRegionResource, ArtisansByCraftResource
from api.partner_resource import PartnerResource, PartnerDetailResource, PartnersByProductResource
from api.qrcode_resource import QRCodeResource, TransparencyResource
from api.auth_resource import RegisterResource, LoginResource, RefreshResource, LogoutResource
from api.order_resource import OrderResource, OrderDetailResource, OrdersByUserResource, OrderStatusResource

# Import database connection
from utils.snowflake_connector import init_snowflake

def create_app():
    """Create and configure the Flask application"""
    
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 604800))
    
    # Enable CORS
    CORS(app)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize Snowflake connection
    init_snowflake()
    
    # Initialize API
    api = Api(app)
    
    # Register API endpoints
    
    # Product endpoints
    api.add_resource(ProductResource, '/api/products')
    api.add_resource(ProductDetailResource, '/api/products/<string:product_id>')
    api.add_resource(ProductsByCategoryResource, '/api/products/category/<string:category_id>')
    api.add_resource(ProductsByRegionResource, '/api/products/region/<string:region_id>')
    api.add_resource(ProductsByArtisanResource, '/api/products/artisan/<string:artisan_id>')
    api.add_resource(ProductSearchResource, '/api/products/search')
    
    # Artisan endpoints
    api.add_resource(ArtisanResource, '/api/artisans')
    api.add_resource(ArtisanDetailResource, '/api/artisans/<string:artisan_id>')
    api.add_resource(ArtisansByRegionResource, '/api/artisans/region/<string:region_id>')
    api.add_resource(ArtisansByCraftResource, '/api/artisans/craft/<string:craft_type>')
    
    # Partner website endpoints
    api.add_resource(PartnerResource, '/api/partners')
    api.add_resource(PartnerDetailResource, '/api/partners/<string:partner_id>')
    api.add_resource(PartnersByProductResource, '/api/partners/product/<string:product_id>')
    
    # QR code endpoints
    api.add_resource(QRCodeResource, '/api/qrcode/product/<string:product_id>')
    api.add_resource(TransparencyResource, '/api/transparency/<string:product_id>')
    
    # Authentication endpoints
    api.add_resource(RegisterResource, '/api/auth/register')
    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(RefreshResource, '/api/auth/refresh')
    api.add_resource(LogoutResource, '/api/auth/logout')
    
    # Order endpoints
    api.add_resource(OrderResource, '/api/orders')
    api.add_resource(OrderDetailResource, '/api/orders/<string:order_id>')
    api.add_resource(OrdersByUserResource, '/api/orders/user/<string:user_id>')
    api.add_resource(OrderStatusResource, '/api/orders/<string:order_id>/status')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'handicraft-marketplace-api'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=os.getenv('DEBUG', 'True').lower() == 'true')
