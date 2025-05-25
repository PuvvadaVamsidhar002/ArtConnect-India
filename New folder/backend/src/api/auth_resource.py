"""
Authentication API resources for the Handicraft Marketplace Platform.

This module provides RESTful API endpoints for user authentication operations.
"""

import os
import uuid
import hashlib
from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from utils.snowflake_connector import execute_query

class RegisterResource(Resource):
    """Resource for user registration"""
    
    def post(self):
        """Register a new user"""
        # Get request data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'address', 'phone']
        for field in required_fields:
            if field not in data:
                return {'error': f'Missing required field: {field}'}, 400
        
        # Check if email already exists
        email_check_query = f"SELECT customer_id FROM CUSTOMERS WHERE email = '{data['email']}'"
        existing_user = execute_query(email_check_query)
        
        if existing_user:
            return {'error': 'Email already registered'}, 409
        
        # Generate customer_id
        customer_id = str(uuid.uuid4())
        
        # Hash password
        password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
        
        # Current timestamp
        now = datetime.now().isoformat()
        
        # Insert new customer
        insert_query = f"""
            INSERT INTO CUSTOMERS (
                customer_id, name, email, password_hash, address, phone, created_at, updated_at
            ) VALUES (
                '{customer_id}',
                '{data['name']}',
                '{data['email']}',
                '{password_hash}',
                '{data['address']}',
                '{data['phone']}',
                '{now}',
                '{now}'
            )
        """
        
        try:
            execute_query(insert_query)
            
            # Generate tokens
            access_token = create_access_token(identity=customer_id)
            refresh_token = create_refresh_token(identity=customer_id)
            
            return {
                'message': 'User registered successfully',
                'customer_id': customer_id,
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201
        
        except Exception as e:
            return {'error': f'Registration failed: {str(e)}'}, 500

class LoginResource(Resource):
    """Resource for user login"""
    
    def post(self):
        """Login a user"""
        # Get request data
        data = request.get_json()
        
        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return {'error': 'Email and password are required'}, 400
        
        # Hash password
        password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
        
        # Query user
        query = f"""
            SELECT customer_id, name, email
            FROM CUSTOMERS
            WHERE email = '{data['email']}' AND password_hash = '{password_hash}'
        """
        
        user = execute_query(query)
        
        if not user:
            return {'error': 'Invalid email or password'}, 401
        
        # Generate tokens
        customer_id = user[0]['CUSTOMER_ID']
        access_token = create_access_token(identity=customer_id)
        refresh_token = create_refresh_token(identity=customer_id)
        
        return {
            'message': 'Login successful',
            'customer_id': customer_id,
            'name': user[0]['NAME'],
            'email': user[0]['EMAIL'],
            'access_token': access_token,
            'refresh_token': refresh_token
        }

class RefreshResource(Resource):
    """Resource for refreshing access token"""
    
    @jwt_required(refresh=True)
    def post(self):
        """Refresh access token"""
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        
        return {
            'access_token': access_token
        }

class LogoutResource(Resource):
    """Resource for user logout"""
    
    @jwt_required()
    def post(self):
        """Logout a user"""
        # Note: In a real implementation, we would blacklist the token
        # For this prototype, we'll just return a success message
        
        return {
            'message': 'Logout successful'
        }
