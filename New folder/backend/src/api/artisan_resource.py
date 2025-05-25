"""
Artisan API resources for the Handicraft Marketplace Platform.

This module provides RESTful API endpoints for artisan-related operations.
"""

from flask import request
from flask_restful import Resource
from utils.snowflake_connector import execute_query

class ArtisanResource(Resource):
    """Resource for handling artisan collection operations"""
    
    def get(self):
        """Get a paginated list of artisans"""
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # Query artisans with pagination
        query = f"""
            SELECT 
                a.artisan_id,
                a.name,
                a.location,
                a.craft_type,
                a.bio,
                a.image_url,
                a.years_active,
                COUNT(DISTINCT p.product_id) as product_count
            FROM ARTISANS a
            LEFT JOIN PRODUCTS p ON a.artisan_id = p.artisan_id
            GROUP BY 
                a.artisan_id,
                a.name,
                a.location,
                a.craft_type,
                a.bio,
                a.image_url,
                a.years_active
            ORDER BY a.name
            LIMIT {per_page} OFFSET {offset}
        """
        
        # Count total artisans
        count_query = "SELECT COUNT(*) as total FROM ARTISANS"
        
        # Execute queries
        artisans = execute_query(query)
        count_result = execute_query(count_query)
        total = count_result[0]['TOTAL'] if count_result else 0
        
        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        return {
            'artisans': artisans,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }

class ArtisanDetailResource(Resource):
    """Resource for handling operations on a specific artisan"""
    
    def get(self, artisan_id):
        """Get details of a specific artisan"""
        # Query artisan details
        query = f"""
            SELECT 
                a.artisan_id,
                a.name,
                a.location,
                a.craft_type,
                a.bio,
                a.image_url,
                a.contact_info,
                a.years_active,
                COUNT(DISTINCT p.product_id) as product_count
            FROM ARTISANS a
            LEFT JOIN PRODUCTS p ON a.artisan_id = p.artisan_id
            WHERE a.artisan_id = '{artisan_id}'
            GROUP BY 
                a.artisan_id,
                a.name,
                a.location,
                a.craft_type,
                a.bio,
                a.image_url,
                a.contact_info,
                a.years_active
        """
        
        # Query artisan's products
        products_query = f"""
            SELECT 
                p.product_id,
                p.name,
                p.description,
                p.price,
                c.name as category_name
            FROM PRODUCTS p
            LEFT JOIN CATEGORIES c ON p.category_id = c.category_id
            WHERE p.artisan_id = '{artisan_id}'
            ORDER BY p.name
            LIMIT 10
        """
        
        # Execute queries
        artisan = execute_query(query)
        products = execute_query(products_query)
        
        # Check if artisan exists
        if not artisan:
            return {'error': 'Artisan not found'}, 404
        
        # Add products to artisan
        artisan[0]['products'] = products
        
        # Return artisan details
        return artisan[0]

class ArtisansByRegionResource(Resource):
    """Resource for handling artisans by region"""
    
    def get(self, region_id):
        """Get artisans by region"""
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # Query artisans by region with pagination
        query = f"""
            SELECT 
                a.artisan_id,
                a.name,
                a.location,
                a.craft_type,
                a.bio,
                a.image_url,
                a.years_active
            FROM ARTISANS a
            JOIN PRODUCTS p ON a.artisan_id = p.artisan_id
            WHERE p.region_id = '{region_id}'
            GROUP BY 
                a.artisan_id,
                a.name,
                a.location,
                a.craft_type,
                a.bio,
                a.image_url,
                a.years_active
            ORDER BY a.name
            LIMIT {per_page} OFFSET {offset}
        """
        
        # Count total artisans in region
        count_query = f"""
            SELECT COUNT(DISTINCT a.artisan_id) as total 
            FROM ARTISANS a
            JOIN PRODUCTS p ON a.artisan_id = p.artisan_id
            WHERE p.region_id = '{region_id}'
        """
        
        # Execute queries
        artisans = execute_query(query)
        count_result = execute_query(count_query)
        total = count_result[0]['TOTAL'] if count_result else 0
        
        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        return {
            'artisans': artisans,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }

class ArtisansByCraftResource(Resource):
    """Resource for handling artisans by craft type"""
    
    def get(self, craft_type):
        """Get artisans by craft type"""
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # Query artisans by craft type with pagination
        query = f"""
            SELECT 
                a.artisan_id,
                a.name,
                a.location,
                a.craft_type,
                a.bio,
                a.image_url,
                a.years_active
            FROM ARTISANS a
            WHERE LOWER(a.craft_type) = LOWER('{craft_type}')
            ORDER BY a.name
            LIMIT {per_page} OFFSET {offset}
        """
        
        # Count total artisans with craft type
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM ARTISANS 
            WHERE LOWER(craft_type) = LOWER('{craft_type}')
        """
        
        # Execute queries
        artisans = execute_query(query)
        count_result = execute_query(count_query)
        total = count_result[0]['TOTAL'] if count_result else 0
        
        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        return {
            'artisans': artisans,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }
