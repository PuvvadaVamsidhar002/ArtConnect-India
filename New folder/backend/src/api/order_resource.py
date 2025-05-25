"""
Order API resources for the Handicraft Marketplace Platform.

This module provides RESTful API endpoints for order-related operations.
"""

import uuid
from datetime import datetime
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.snowflake_connector import execute_query

class OrderResource(Resource):
    """Resource for handling order collection operations"""
    
    @jwt_required()
    def get(self):
        """Get a paginated list of orders for the authenticated user"""
        # Get current user
        current_user = get_jwt_identity()
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        offset = (page - 1) * per_page
        
        # Query orders with pagination
        query = f"""
            SELECT 
                o.order_id,
                o.order_date,
                o.total_amount,
                o.status,
                o.shipping_address,
                o.payment_method,
                o.tracking_number,
                COUNT(oi.item_id) as item_count
            FROM ORDERS o
            LEFT JOIN ORDER_ITEMS oi ON o.order_id = oi.order_id
            WHERE o.customer_id = '{current_user}'
            GROUP BY 
                o.order_id,
                o.order_date,
                o.total_amount,
                o.status,
                o.shipping_address,
                o.payment_method,
                o.tracking_number
            ORDER BY o.order_date DESC
            LIMIT {per_page} OFFSET {offset}
        """
        
        # Count total orders
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM ORDERS 
            WHERE customer_id = '{current_user}'
        """
        
        # Execute queries
        orders = execute_query(query)
        count_result = execute_query(count_query)
        total = count_result[0]['TOTAL'] if count_result else 0
        
        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        return {
            'orders': orders,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }
    
    @jwt_required()
    def post(self):
        """Create a new order"""
        # Get current user
        current_user = get_jwt_identity()
        
        # Get request data
        data = request.get_json()
        
        # Validate required fields
        if 'items' not in data or not data['items']:
            return {'error': 'Order items are required'}, 400
        
        if 'shipping_address' not in data:
            return {'error': 'Shipping address is required'}, 400
        
        if 'payment_method' not in data:
            return {'error': 'Payment method is required'}, 400
        
        # Generate order_id
        order_id = str(uuid.uuid4())
        
        # Current timestamp
        now = datetime.now().isoformat()
        
        # Calculate order totals
        total_amount = 0
        platform_fee = 0
        
        # Validate items and calculate totals
        items = []
        for item_data in data['items']:
            if 'product_id' not in item_data or 'partner_id' not in item_data or 'quantity' not in item_data:
                return {'error': 'Invalid order item'}, 400
            
            # Get product and partner details
            product_query = f"""
                SELECT pp.price, ps.commission_rate
                FROM PRODUCT_PARTNER pp
                JOIN PARTNER_SITES ps ON pp.partner_id = ps.partner_id
                WHERE pp.product_id = '{item_data['product_id']}' AND pp.partner_id = '{item_data['partner_id']}'
            """
            
            product_result = execute_query(product_query)
            if not product_result:
                return {'error': f"Product not available from selected partner"}, 400
            
            price = product_result[0]['PRICE']
            commission_rate = product_result[0]['COMMISSION_RATE']
            quantity = item_data['quantity']
            subtotal = price * quantity
            
            # Add to totals
            total_amount += subtotal
            platform_fee += subtotal * (commission_rate / 100)
            
            # Create order item
            item = {
                'item_id': str(uuid.uuid4()),
                'order_id': order_id,
                'product_id': item_data['product_id'],
                'partner_id': item_data['partner_id'],
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            }
            
            items.append(item)
        
        # Add shipping cost (simplified)
        shipping_cost = 150
        total_amount += shipping_cost
        
        # Create order
        order_query = f"""
            INSERT INTO ORDERS (
                order_id, customer_id, order_date, total_amount, status, 
                shipping_address, payment_method, platform_fee, created_at, updated_at
            ) VALUES (
                '{order_id}',
                '{current_user}',
                '{now}',
                {total_amount},
                'Processing',
                '{data['shipping_address']}',
                '{data['payment_method']}',
                {platform_fee},
                '{now}',
                '{now}'
            )
        """
        
        try:
            # Insert order
            execute_query(order_query)
            
            # Insert order items
            for item in items:
                item_query = f"""
                    INSERT INTO ORDER_ITEMS (
                        item_id, order_id, product_id, partner_id, quantity, price, subtotal, created_at
                    ) VALUES (
                        '{item['item_id']}',
                        '{item['order_id']}',
                        '{item['product_id']}',
                        '{item['partner_id']}',
                        {item['quantity']},
                        {item['price']},
                        {item['subtotal']},
                        '{now}'
                    )
                """
                execute_query(item_query)
            
            return {
                'message': 'Order created successfully',
                'order_id': order_id,
                'total_amount': total_amount,
                'platform_fee': platform_fee,
                'item_count': len(items)
            }, 201
        
        except Exception as e:
            return {'error': f'Order creation failed: {str(e)}'}, 500

class OrderDetailResource(Resource):
    """Resource for handling operations on a specific order"""
    
    @jwt_required()
    def get(self, order_id):
        """Get details of a specific order"""
        # Get current user
        current_user = get_jwt_identity()
        
        # Query order details
        query = f"""
            SELECT 
                o.order_id,
                o.customer_id,
                o.order_date,
                o.total_amount,
                o.status,
                o.shipping_address,
                o.payment_method,
                o.tracking_number,
                o.platform_fee
            FROM ORDERS o
            WHERE o.order_id = '{order_id}'
        """
        
        # Query order items
        items_query = f"""
            SELECT 
                oi.item_id,
                oi.product_id,
                p.name as product_name,
                oi.partner_id,
                ps.name as partner_name,
                oi.quantity,
                oi.price,
                oi.subtotal
            FROM ORDER_ITEMS oi
            JOIN PRODUCTS p ON oi.product_id = p.product_id
            JOIN PARTNER_SITES ps ON oi.partner_id = ps.partner_id
            WHERE oi.order_id = '{order_id}'
        """
        
        # Execute queries
        order = execute_query(query)
        items = execute_query(items_query)
        
        # Check if order exists
        if not order:
            return {'error': 'Order not found'}, 404
        
        # Check if user has access to this order
        if order[0]['CUSTOMER_ID'] != current_user:
            return {'error': 'Unauthorized access to order'}, 403
        
        # Add items to order
        order[0]['items'] = items
        
        # Return order details
        return order[0]

class OrdersByUserResource(Resource):
    """Resource for handling orders by user"""
    
    @jwt_required()
    def get(self, user_id):
        """Get orders by user"""
        # Get current user
        current_user = get_jwt_identity()
        
        # Check if user has access to these orders
        if current_user != user_id:
            return {'error': 'Unauthorized access to orders'}, 403
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        offset = (page - 1) * per_page
        
        # Query orders by user with pagination
        query = f"""
            SELECT 
                o.order_id,
                o.order_date,
                o.total_amount,
                o.status,
                o.shipping_address,
                o.payment_method,
                o.tracking_number
            FROM ORDERS o
            WHERE o.customer_id = '{user_id}'
            ORDER BY o.order_date DESC
            LIMIT {per_page} OFFSET {offset}
        """
        
        # Count total orders by user
        count_query = f"""
            SELECT COUNT(*) as total 
            FROM ORDERS 
            WHERE customer_id = '{user_id}'
        """
        
        # Execute queries
        orders = execute_query(query)
        count_result = execute_query(count_query)
        total = count_result[0]['TOTAL'] if count_result else 0
        
        # Calculate pagination metadata
        total_pages = (total + per_page - 1) // per_page
        
        # Return response
        return {
            'orders': orders,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }

class OrderStatusResource(Resource):
    """Resource for handling order status updates"""
    
    @jwt_required()
    def put(self, order_id):
        """Update order status"""
        # Get current user
        current_user = get_jwt_identity()
        
        # Get request data
        data = request.get_json()
        
        # Validate required fields
        if 'status' not in data:
            return {'error': 'Status is required'}, 400
        
        # Valid status values
        valid_statuses = ['Processing', 'Shipped', 'Delivered', 'Cancelled']
        if data['status'] not in valid_statuses:
            return {'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}, 400
        
        # Check if order exists and belongs to user
        check_query = f"""
            SELECT customer_id 
            FROM ORDERS 
            WHERE order_id = '{order_id}'
        """
        
        order = execute_query(check_query)
        
        if not order:
            return {'error': 'Order not found'}, 404
        
        if order[0]['CUSTOMER_ID'] != current_user:
            return {'error': 'Unauthorized access to order'}, 403
        
        # Update order status
        update_query = f"""
            UPDATE ORDERS
            SET status = '{data['status']}', updated_at = '{datetime.now().isoformat()}'
            WHERE order_id = '{order_id}'
        """
        
        try:
            execute_query(update_query)
            
            # If status is Shipped and tracking number is provided, update it
            if data['status'] == 'Shipped' and 'tracking_number' in data:
                tracking_query = f"""
                    UPDATE ORDERS
                    SET tracking_number = '{data['tracking_number']}'
                    WHERE order_id = '{order_id}'
                """
                execute_query(tracking_query)
            
            return {
                'message': 'Order status updated successfully',
                'order_id': order_id,
                'status': data['status']
            }
        
        except Exception as e:
            return {'error': f'Status update failed: {str(e)}'}, 500
