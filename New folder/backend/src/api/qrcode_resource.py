"""
QR Code API resources for the Handicraft Marketplace Platform.

This module provides RESTful API endpoints for QR code generation and transparency data.
"""

import os
import qrcode
from flask import request, send_file
from flask_restful import Resource
from utils.snowflake_connector import execute_query, execute_procedure

class QRCodeResource(Resource):
    """Resource for generating QR codes for products"""
    
    def get(self, product_id):
        """Generate and return a QR code for a specific product"""
        # Check if product exists
        product_query = f"SELECT product_id, name FROM PRODUCTS WHERE product_id = '{product_id}'"
        product = execute_query(product_query)
        
        if not product:
            return {'error': 'Product not found'}, 404
        
        # Create directory for QR codes if it doesn't exist
        qr_dir = os.path.join(os.getcwd(), 'static', 'qrcodes')
        os.makedirs(qr_dir, exist_ok=True)
        
        # Generate QR code with transparency URL
        qr_url = f"{os.getenv('APP_URL', 'http://localhost:5000')}/api/transparency/{product_id}"
        qr = qrcode.make(qr_url)
        
        # Save QR code
        qr_path = os.path.join(qr_dir, f"{product_id}.png")
        qr.save(qr_path)
        
        # Return QR code image
        return send_file(qr_path, mimetype='image/png')

class TransparencyResource(Resource):
    """Resource for product transparency data"""
    
    def get(self, product_id):
        """Get transparency data for a specific product"""
        # Call Snowflake stored procedure to get QR code data
        # Note: In a real implementation, we would use execute_procedure
        # For this prototype, we'll simulate it with a direct query
        
        # Query product details for transparency
        query = f"""
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
            FROM PRODUCTS p
            LEFT JOIN ARTISANS a ON p.artisan_id = a.artisan_id
            LEFT JOIN REGIONS r ON p.region_id = r.region_id
            LEFT JOIN GI_TAGS g ON p.gi_tag_id = g.gi_tag_id
            LEFT JOIN CULTURAL_STORIES cs ON p.story_id = cs.story_id
            WHERE p.product_id = '{product_id}'
        """
        
        # Query partner offerings for pricing transparency
        partners_query = f"""
            SELECT 
                ps.partner_id,
                ps.name,
                ps.rating,
                ps.review_count,
                ps.commission_rate,
                pp.price,
                pp.shipping_fee,
                pp.availability,
                pp.estimated_delivery
            FROM PRODUCT_PARTNER pp
            JOIN PARTNER_SITES ps ON pp.partner_id = ps.partner_id
            WHERE pp.product_id = '{product_id}'
        """
        
        # Execute queries
        product_data = execute_query(query)
        partners_data = execute_query(partners_query)
        
        # Check if product exists
        if not product_data:
            return {'error': 'Product not found'}, 404
        
        # Format transparency data
        transparency_data = product_data[0]
        
        # Add artisan info
        transparency_data['artisan'] = {
            'id': transparency_data.pop('ARTISAN_ID', None),
            'name': transparency_data.pop('ARTISAN_NAME', None),
            'location': transparency_data.pop('ARTISAN_LOCATION', None),
            'craft_type': transparency_data.pop('CRAFT_TYPE', None),
            'years_active': transparency_data.pop('YEARS_ACTIVE', None)
        }
        
        # Add region info
        transparency_data['region'] = {
            'name': transparency_data.pop('REGION_NAME', None),
            'state': transparency_data.pop('STATE', None)
        }
        
        # Add GI tag info if applicable
        gi_tag_name = transparency_data.pop('GI_TAG_NAME', None)
        if gi_tag_name:
            transparency_data['gi_tag'] = {
                'name': gi_tag_name,
                'description': transparency_data.pop('GI_TAG_DESCRIPTION', None)
            }
        
        # Add cultural story
        transparency_data['cultural_story'] = {
            'title': transparency_data.pop('STORY_TITLE', None),
            'content': transparency_data.pop('STORY_CONTENT', None),
            'history': transparency_data.pop('HISTORY', None),
            'cultural_significance': transparency_data.pop('CULTURAL_SIGNIFICANCE', None)
        }
        
        # Add partner pricing and calculate revenue sharing
        partners = []
        for partner in partners_data:
            commission_rate = partner.get('COMMISSION_RATE', 15)
            price = partner.get('PRICE', 0)
            
            # Calculate revenue sharing
            platform_fee = price * (commission_rate / 100)
            artisan_revenue = price - platform_fee
            
            partners.append({
                'partner_id': partner.get('PARTNER_ID'),
                'name': partner.get('NAME'),
                'rating': partner.get('RATING'),
                'review_count': partner.get('REVIEW_COUNT'),
                'price': price,
                'shipping_fee': partner.get('SHIPPING_FEE'),
                'availability': partner.get('AVAILABILITY'),
                'estimated_delivery': partner.get('ESTIMATED_DELIVERY'),
                'revenue_sharing': {
                    'platform_fee': platform_fee,
                    'platform_fee_percentage': commission_rate,
                    'artisan_revenue': artisan_revenue,
                    'artisan_revenue_percentage': 100 - commission_rate
                }
            })
        
        transparency_data['partners'] = partners
        
        # Return transparency data
        return transparency_data
