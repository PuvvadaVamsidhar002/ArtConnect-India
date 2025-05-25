"""
Partner API resources for the Handicraft Marketplace Platform.

This module provides RESTful API endpoints for partner website-related operations.
"""

from flask import request
from flask_restful import Resource
from utils.snowflake_connector import execute_query

class PartnerResource(Resource):
    """Resource for handling partner website collection operations"""
    
    def get(self):
        """Get a paginated list of partner websites"""
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # Query partner websites with pagination
        query = f"""
            SELECT 
                ps.partner_id,
                ps.name,
                ps.website_url,
                ps.rating,
                ps.review_count,
                ps.logo_url,
                ps.description,
                COUNT(DISTINCT pp.product_id) as product_count
            FROM PARTNER_SITES ps
            LEFT JOIN PRODUCT_PARTNER pp ON ps.partner_id = pp.partner_id
            GROUP BY 
                ps.partner_id,
                ps.name,
                ps.website_url,
                ps.rating,
                ps.review_count,
                ps.logo_url,
                ps.description
            ORDER BY ps.name
            LIMIT {per_page} OFFSET {offset}
        """
        
        # Count total partner websites
        count_query = "SELECT COUNT(*) as total FROM PARTNER_SITES"
        
        # Execute queries
        partners = execute_query(query)
        count_result = execute_query(count_query)
        total = count_result[0]['TOTAL'] if count_result else 0
        
        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        return {
            'partners': partners,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }

class PartnerDetailResource(Resource):
    """Resource for handling operations on a specific partner website"""
    
    def get(self, partner_id):
        """Get details of a specific partner website"""
        # Query partner details
        query = f"""
            SELECT 
                ps.partner_id,
                ps.name,
                ps.website_url,
                ps.rating,
                ps.review_count,
                ps.commission_rate,
                ps.shipping_options,
                ps.logo_url,
                ps.description,
                COUNT(DISTINCT pp.product_id) as product_count
            FROM PARTNER_SITES ps
            LEFT JOIN PRODUCT_PARTNER pp ON ps.partner_id = pp.partner_id
            WHERE ps.partner_id = '{partner_id}'
            GROUP BY 
                ps.partner_id,
                ps.name,
                ps.website_url,
                ps.rating,
                ps.review_count,
                ps.commission_rate,
                ps.shipping_options,
                ps.logo_url,
                ps.description
        """
        
        # Query partner's products
        products_query = f"""
            SELECT 
                p.product_id,
                p.name,
                p.description,
                pp.price,
                pp.shipping_fee,
                pp.availability,
                pp.estimated_delivery,
                c.name as category_name
            FROM PRODUCT_PARTNER pp
            JOIN PRODUCTS p ON pp.product_id = p.product_id
            LEFT JOIN CATEGORIES c ON p.category_id = c.category_id
            WHERE pp.partner_id = '{partner_id}'
            ORDER BY p.name
            LIMIT 10
        """
        
        # Execute queries
        partner = execute_query(query)
        products = execute_query(products_query)
        
        # Check if partner exists
        if not partner:
            return {'error': 'Partner website not found'}, 404
        
        # Add products to partner
        partner[0]['products'] = products
        
        # Return partner details
        return partner[0]

class PartnersByProductResource(Resource):
    """Resource for handling partners by product"""
    
    def get(self, product_id):
        """Get partners offering a specific product"""
        # Query partners by product
        query = f"""
            SELECT 
                ps.partner_id,
                ps.name,
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
            ORDER BY pp.price ASC
        """
        
        # Execute query
        partners = execute_query(query)
        
        # Return response
        return {
            'product_id': product_id,
            'partners': partners
        }
