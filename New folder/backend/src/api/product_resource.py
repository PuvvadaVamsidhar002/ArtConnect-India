"""
Product API resources for the Handicraft Marketplace Platform.

This module provides RESTful API endpoints for product-related operations.
"""

from flask import request
from flask_restful import Resource
from utils.snowflake_connector import execute_query

class ProductResource(Resource):
    """Resource for handling product collection operations"""
    
    def get(self):
        """Get a paginated list of products"""
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # Query products with pagination
        query = f"""
            SELECT 
                p.product_id,
                p.name,
                p.description,
                p.price,
                p.dimensions,
                p.weight,
                p.materials,
                a.name as artisan_name,
                c.name as category_name,
                r.name as region_name,
                r.state,
                ARRAY_AGG(DISTINCT pp.partner_id) as partner_ids
            FROM PRODUCTS p
            LEFT JOIN ARTISANS a ON p.artisan_id = a.artisan_id
            LEFT JOIN CATEGORIES c ON p.category_id = c.category_id
            LEFT JOIN REGIONS r ON p.region_id = r.region_id
            LEFT JOIN PRODUCT_PARTNER pp ON p.product_id = pp.product_id
            GROUP BY 
                p.product_id,
                p.name,
                p.description,
                p.price,
                p.dimensions,
                p.weight,
                p.materials,
                a.name,
                c.name,
                r.name,
                r.state
            ORDER BY p.name
            LIMIT {per_page} OFFSET {offset}
        """
        
        # Count total products
        count_query = "SELECT COUNT(*) as total FROM PRODUCTS"
        
        # Execute queries
        products = execute_query(query)
        count_result = execute_query(count_query)
        total = count_result[0]['TOTAL'] if count_result else 0
        
        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        return {
            'products': products,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }

class ProductDetailResource(Resource):
    """Resource for handling operations on a specific product"""
    
    def get(self, product_id):
        """Get details of a specific product"""
        # Query product details
        query = f"""
            SELECT 
                p.product_id,
                p.name,
                p.description,
                p.price,
                p.dimensions,
                p.weight,
                p.materials,
                p.is_gi_tagged,
                a.artisan_id,
                a.name as artisan_name,
                a.location as artisan_location,
                a.craft_type,
                a.bio as artisan_bio,
                a.image_url as artisan_image_url,
                c.category_id,
                c.name as category_name,
                r.region_id,
                r.name as region_name,
                r.state,
                cs.story_id,
                cs.title as story_title,
                cs.content as story_content,
                cs.history,
                cs.cultural_significance
            FROM PRODUCTS p
            LEFT JOIN ARTISANS a ON p.artisan_id = a.artisan_id
            LEFT JOIN CATEGORIES c ON p.category_id = c.category_id
            LEFT JOIN REGIONS r ON p.region_id = r.region_id
            LEFT JOIN CULTURAL_STORIES cs ON p.story_id = cs.story_id
            WHERE p.product_id = '{product_id}'
        """
        
        # Query partner offerings
        partners_query = f"""
            SELECT 
                pp.id as product_partner_id,
                pp.partner_id,
                ps.name as partner_name,
                ps.website_url,
                ps.rating,
                ps.review_count,
                pp.price,
                pp.shipping_fee,
                pp.availability,
                pp.estimated_delivery
            FROM PRODUCT_PARTNER pp
            JOIN PARTNER_SITES ps ON pp.partner_id = ps.partner_id
            WHERE pp.product_id = '{product_id}'
        """
        
        # Execute queries
        product = execute_query(query)
        partners = execute_query(partners_query)
        
        # Check if product exists
        if not product:
            return {'error': 'Product not found'}, 404
        
        # Add partner offerings to product
        product[0]['partners'] = partners
        
        # Return product details
        return product[0]

class ProductsByCategoryResource(Resource):
    """Resource for handling products by category"""
    
    def get(self, category_id):
        """Get products by category"""
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # Query products by category with pagination
        query = f"""
            SELECT 
                p.product_id,
                p.name,
                p.description,
                p.price,
                a.name as artisan_name,
                r.name as region_name,
                r.state
            FROM PRODUCTS p
            LEFT JOIN ARTISANS a ON p.artisan_id = a.artisan_id
            LEFT JOIN REGIONS r ON p.region_id = r.region_id
            WHERE p.category_id = '{category_id}'
            ORDER BY p.name
            LIMIT {per_page} OFFSET {offset}
        """
        
        # Count total products in category
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM PRODUCTS 
            WHERE category_id = '{category_id}'
        """
        
        # Execute queries
        products = execute_query(query)
        count_result = execute_query(count_query)
        total = count_result[0]['TOTAL'] if count_result else 0
        
        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        return {
            'products': products,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }

class ProductsByRegionResource(Resource):
    """Resource for handling products by region"""
    
    def get(self, region_id):
        """Get products by region"""
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # Query products by region with pagination
        query = f"""
            SELECT 
                p.product_id,
                p.name,
                p.description,
                p.price,
                a.name as artisan_name,
                c.name as category_name
            FROM PRODUCTS p
            LEFT JOIN ARTISANS a ON p.artisan_id = a.artisan_id
            LEFT JOIN CATEGORIES c ON p.category_id = c.category_id
            WHERE p.region_id = '{region_id}'
            ORDER BY p.name
            LIMIT {per_page} OFFSET {offset}
        """
        
        # Count total products in region
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM PRODUCTS 
            WHERE region_id = '{region_id}'
        """
        
        # Execute queries
        products = execute_query(query)
        count_result = execute_query(count_query)
        total = count_result[0]['TOTAL'] if count_result else 0
        
        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        return {
            'products': products,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }

class ProductsByArtisanResource(Resource):
    """Resource for handling products by artisan"""
    
    def get(self, artisan_id):
        """Get products by artisan"""
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # Query products by artisan with pagination
        query = f"""
            SELECT 
                p.product_id,
                p.name,
                p.description,
                p.price,
                c.name as category_name,
                r.name as region_name
            FROM PRODUCTS p
            LEFT JOIN CATEGORIES c ON p.category_id = c.category_id
            LEFT JOIN REGIONS r ON p.region_id = r.region_id
            WHERE p.artisan_id = '{artisan_id}'
            ORDER BY p.name
            LIMIT {per_page} OFFSET {offset}
        """
        
        # Count total products by artisan
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM PRODUCTS 
            WHERE artisan_id = '{artisan_id}'
        """
        
        # Execute queries
        products = execute_query(query)
        count_result = execute_query(count_query)
        total = count_result[0]['TOTAL'] if count_result else 0
        
        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        return {
            'products': products,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }

class ProductSearchResource(Resource):
    """Resource for searching products"""
    
    def get(self):
        """Search products by keywords"""
        # Get query parameters
        keywords = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # Prepare search terms
        search_terms = keywords.split()
        search_condition = " OR ".join([f"LOWER(p.name) LIKE LOWER('%{term}%') OR LOWER(p.description) LIKE LOWER('%{term}%')" for term in search_terms])
        
        # Query products by search terms with pagination
        query = f"""
            SELECT 
                p.product_id,
                p.name,
                p.description,
                p.price,
                a.name as artisan_name,
                c.name as category_name,
                r.name as region_name,
                r.state
            FROM PRODUCTS p
            LEFT JOIN ARTISANS a ON p.artisan_id = a.artisan_id
            LEFT JOIN CATEGORIES c ON p.category_id = c.category_id
            LEFT JOIN REGIONS r ON p.region_id = r.region_id
            WHERE {search_condition}
            ORDER BY p.name
            LIMIT {per_page} OFFSET {offset}
        """
        
        # Count total search results
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM PRODUCTS p
            WHERE {search_condition}
        """
        
        # Execute queries
        products = execute_query(query)
        count_result = execute_query(count_query)
        total = count_result[0]['TOTAL'] if count_result else 0
        
        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        return {
            'products': products,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }
