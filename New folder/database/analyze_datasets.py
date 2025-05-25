#!/usr/bin/env python3
"""
Dataset Analysis Script for Handicraft Marketplace Platform

This script analyzes and processes the uploaded datasets for the Handicraft Marketplace platform,
preparing them for import into the Snowflake database.
"""

import os
import pandas as pd
import numpy as np
import json
import uuid
from datetime import datetime

# Create directory for processed data
os.makedirs('/home/ubuntu/handicraft_marketplace/database/processed_data', exist_ok=True)

# Function to generate UUIDs
def generate_uuid():
    return str(uuid.uuid4())

# Function to clean and standardize column names
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')
    return df

# Function to save processed dataframe to CSV
def save_processed_df(df, filename):
    output_path = f'/home/ubuntu/handicraft_marketplace/database/processed_data/{filename}'
    df.to_csv(output_path, index=False)
    print(f"Saved processed data to {output_path}")
    return output_path

# Process artisan data from multiple states
def process_artisan_data():
    artisan_files = [
        '/home/ubuntu/upload/UTTARPRADESH.xlsx',
        '/home/ubuntu/upload/AP.xlsx',
        '/home/ubuntu/upload/MEGHALAYA ARTSIAN DATA.xlsx',
        '/home/ubuntu/upload/MAHARASTRA.xlsx',
        '/home/ubuntu/upload/KARNATAKA.xlsx'
    ]
    
    all_artisans = []
    
    for file_path in artisan_files:
        try:
            print(f"Processing {file_path}...")
            state_name = os.path.basename(file_path).replace('.xlsx', '').replace(' ARTSIAN DATA', '')
            
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Clean column names
            df = clean_column_names(df)
            
            # Print column names for debugging
            print(f"Columns in {state_name}: {df.columns.tolist()}")
            
            # Extract relevant columns (adjust based on actual column names)
            # We'll try to map various column naming patterns to our standardized schema
            artisan_data = []
            
            for _, row in df.iterrows():
                artisan = {
                    'artisan_id': generate_uuid(),
                    'state': state_name
                }
                
                # Map common column patterns to our schema
                for col in df.columns:
                    if 'name' in col:
                        artisan['name'] = str(row[col]) if not pd.isna(row[col]) else ''
                    elif 'location' in col or 'address' in col or 'village' in col:
                        artisan['location'] = str(row[col]) if not pd.isna(row[col]) else ''
                    elif 'craft' in col or 'art' in col or 'skill' in col:
                        artisan['craft_type'] = str(row[col]) if not pd.isna(row[col]) else ''
                    elif 'contact' in col or 'phone' in col or 'mobile' in col:
                        artisan['contact_info'] = str(row[col]) if not pd.isna(row[col]) else ''
                    elif 'experience' in col or 'year' in col:
                        try:
                            artisan['years_active'] = int(row[col]) if not pd.isna(row[col]) else 0
                        except:
                            artisan['years_active'] = 0
                
                # Ensure required fields have values
                if 'name' not in artisan or not artisan['name']:
                    continue  # Skip records without names
                
                # Add default values for missing fields
                if 'location' not in artisan:
                    artisan['location'] = state_name
                if 'craft_type' not in artisan:
                    artisan['craft_type'] = 'Traditional Craft'
                if 'contact_info' not in artisan:
                    artisan['contact_info'] = ''
                if 'years_active' not in artisan:
                    artisan['years_active'] = 0
                
                # Add timestamps
                artisan['created_at'] = datetime.now().isoformat()
                artisan['updated_at'] = datetime.now().isoformat()
                
                # Add bio placeholder
                artisan['bio'] = f"Skilled {artisan['craft_type']} artisan from {artisan['location']}, {state_name}."
                
                # Add image_url placeholder
                artisan['image_url'] = ''
                
                artisan_data.append(artisan)
            
            all_artisans.extend(artisan_data)
            print(f"Processed {len(artisan_data)} artisans from {state_name}")
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    # Convert to DataFrame
    artisans_df = pd.DataFrame(all_artisans)
    
    # Save processed data
    return save_processed_df(artisans_df, 'artisans.csv')

# Process GI tagged products
def process_gi_tagged_products():
    try:
        file_path = '/home/ubuntu/upload/GI tagged products.xlsx'
        print(f"Processing {file_path}...")
        
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Clean column names
        df = clean_column_names(df)
        
        # Print column names for debugging
        print(f"Columns in GI tagged products: {df.columns.tolist()}")
        
        # Process data
        gi_tags = []
        
        for _, row in df.iterrows():
            gi_tag = {
                'gi_tag_id': generate_uuid(),
                'region_id': generate_uuid()  # This will be linked to regions later
            }
            
            # Map columns based on patterns
            for col in df.columns:
                if 'name' in col or 'product' in col:
                    gi_tag['name'] = str(row[col]) if not pd.isna(row[col]) else ''
                elif 'description' in col or 'details' in col:
                    gi_tag['description'] = str(row[col]) if not pd.isna(row[col]) else ''
                elif 'region' in col or 'location' in col or 'place' in col:
                    gi_tag['region_name'] = str(row[col]) if not pd.isna(row[col]) else ''
                elif 'state' in col:
                    gi_tag['state'] = str(row[col]) if not pd.isna(row[col]) else ''
                elif 'date' in col or 'issued' in col:
                    try:
                        gi_tag['issue_date'] = row[col].strftime('%Y-%m-%d') if not pd.isna(row[col]) else None
                    except:
                        gi_tag['issue_date'] = None
            
            # Add default values for missing fields
            if 'name' not in gi_tag or not gi_tag['name']:
                continue  # Skip records without names
            
            if 'description' not in gi_tag:
                gi_tag['description'] = f"GI tagged product: {gi_tag['name']}"
            if 'region_name' not in gi_tag:
                gi_tag['region_name'] = 'Unknown Region'
            if 'state' not in gi_tag:
                gi_tag['state'] = 'Unknown State'
            if 'issue_date' not in gi_tag:
                gi_tag['issue_date'] = None
            
            # Add issuing body
            gi_tag['issuing_body'] = 'Geographical Indications Registry, India'
            
            # Add timestamps
            gi_tag['created_at'] = datetime.now().isoformat()
            gi_tag['updated_at'] = datetime.now().isoformat()
            
            gi_tags.append(gi_tag)
        
        # Convert to DataFrame
        gi_tags_df = pd.DataFrame(gi_tags)
        
        # Create regions dataframe from GI tags
        regions = []
        for gi_tag in gi_tags:
            region = {
                'region_id': gi_tag['region_id'],
                'name': gi_tag['region_name'],
                'state': gi_tag['state'],
                'description': f"Region known for {gi_tag['name']}",
                'famous_for': gi_tag['name'],
                'image_url': '',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            regions.append(region)
        
        regions_df = pd.DataFrame(regions)
        
        # Save processed data
        gi_tags_path = save_processed_df(gi_tags_df, 'gi_tags.csv')
        regions_path = save_processed_df(regions_df, 'regions.csv')
        
        return gi_tags_path, regions_path
        
    except Exception as e:
        print(f"Error processing GI tagged products: {str(e)}")
        return None, None

# Process products and images
def process_products_and_images():
    try:
        file_path = '/home/ubuntu/upload/images adn products.xlsx'
        print(f"Processing {file_path}...")
        
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Clean column names
        df = clean_column_names(df)
        
        # Print column names for debugging
        print(f"Columns in products and images: {df.columns.tolist()}")
        
        # Process data
        products = []
        categories = set()
        
        for _, row in df.iterrows():
            product = {
                'product_id': generate_uuid(),
                'artisan_id': generate_uuid(),  # This will be linked to artisans later
                'category_id': generate_uuid(),  # This will be linked to categories later
                'region_id': generate_uuid(),    # This will be linked to regions later
                'story_id': generate_uuid()      # This will be linked to stories later
            }
            
            # Map columns based on patterns
            for col in df.columns:
                if 'name' in col or 'product' in col:
                    product['name'] = str(row[col]) if not pd.isna(row[col]) else ''
                elif 'description' in col or 'details' in col:
                    product['description'] = str(row[col]) if not pd.isna(row[col]) else ''
                elif 'price' in col or 'cost' in col:
                    try:
                        product['price'] = float(row[col]) if not pd.isna(row[col]) else 0.0
                    except:
                        product['price'] = 0.0
                elif 'category' in col or 'type' in col:
                    product['category_name'] = str(row[col]) if not pd.isna(row[col]) else ''
                    categories.add(product['category_name'])
                elif 'image' in col or 'photo' in col or 'url' in col:
                    product['image_url'] = str(row[col]) if not pd.isna(row[col]) else ''
                elif 'region' in col or 'location' in col:
                    product['region_name'] = str(row[col]) if not pd.isna(row[col]) else ''
                elif 'material' in col:
                    product['materials'] = str(row[col]) if not pd.isna(row[col]) else ''
                elif 'dimension' in col or 'size' in col:
                    product['dimensions'] = str(row[col]) if not pd.isna(row[col]) else ''
                elif 'weight' in col:
                    try:
                        product['weight'] = float(row[col]) if not pd.isna(row[col]) else 0.0
                    except:
                        product['weight'] = 0.0
            
            # Add default values for missing fields
            if 'name' not in product or not product['name']:
                continue  # Skip records without names
            
            if 'description' not in product:
                product['description'] = f"Handcrafted {product['name']}"
            if 'price' not in product:
                product['price'] = 1500.0  # Default price
            if 'category_name' not in product:
                product['category_name'] = 'Traditional Handicraft'
                categories.add(product['category_name'])
            if 'image_url' not in product:
                product['image_url'] = ''
            if 'region_name' not in product:
                product['region_name'] = 'Traditional Region'
            if 'materials' not in product:
                product['materials'] = 'Traditional materials'
            if 'dimensions' not in product:
                product['dimensions'] = 'Various sizes'
            if 'weight' not in product:
                product['weight'] = 0.5
            
            # Set GI tag fields
            product['is_gi_tagged'] = False
            product['gi_tag_id'] = None
            
            # Convert image_url to array format
            product['image_urls'] = [product['image_url']] if product['image_url'] else []
            
            # Add timestamps
            product['created_at'] = datetime.now().isoformat()
            product['updated_at'] = datetime.now().isoformat()
            
            products.append(product)
        
        # Convert to DataFrame
        products_df = pd.DataFrame(products)
        
        # Create categories dataframe
        categories_list = []
        for category_name in categories:
            category = {
                'category_id': generate_uuid(),
                'name': category_name,
                'description': f"Collection of {category_name.lower()} items",
                'image_url': '',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            categories_list.append(category)
        
        categories_df = pd.DataFrame(categories_list)
        
        # Create cultural stories dataframe
        stories = []
        for product in products:
            story = {
                'story_id': product['story_id'],
                'title': f"The Story of {product['name']}",
                'content': f"Discover the rich cultural heritage behind this traditional {product['category_name'].lower()}.",
                'history': f"This craft has been practiced for generations in {product['region_name']}.",
                'cultural_significance': f"This {product['category_name'].lower()} represents an important cultural tradition.",
                'image_urls': product['image_urls'],
                'video_url': '',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            stories.append(story)
        
        stories_df = pd.DataFrame(stories)
        
        # Save processed data
        products_path = save_processed_df(products_df, 'products.csv')
        categories_path = save_processed_df(categories_df, 'categories.csv')
        stories_path = save_processed_df(stories_df, 'cultural_stories.csv')
        
        return products_path, categories_path, stories_path
        
    except Exception as e:
        print(f"Error processing products and images: {str(e)}")
        return None, None, None

# Process tourist statistics
def process_tourist_stats():
    try:
        file_path = '/home/ubuntu/upload/stats.csv'
        print(f"Processing {file_path}...")
        
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Clean column names
        df = clean_column_names(df)
        
        # Print column names for debugging
        print(f"Columns in tourist stats: {df.columns.tolist()}")
        
        # Process data
        stats = []
        
        for _, row in df.iterrows():
            stat = {
                'stat_id': generate_uuid(),
                'region_id': generate_uuid()  # This will be linked to regions later
            }
            
            # Map columns based on patterns
            for col in df.columns:
                if 'region' in col or 'location' in col or 'place' in col:
                    stat['region_name'] = str(row[col]) if not pd.isna(row[col]) else ''
                elif 'year' in col:
                    try:
                        stat['year'] = int(row[col]) if not pd.isna(row[col]) else datetime.now().year
                    except:
                        stat['year'] = datetime.now().year
                elif 'domestic' in col:
                    try:
                        stat['domestic_count'] = int(row[col]) if not pd.isna(row[col]) else 0
                    except:
                        stat['domestic_count'] = 0
                elif 'foreign' in col or 'international' in col:
                    try:
                        stat['foreign_count'] = int(row[col]) if not pd.isna(row[col]) else 0
                    except:
                        stat['foreign_count'] = 0
                elif 'growth' in col:
                    try:
                        stat['growth_rate'] = float(row[col]) if not pd.isna(row[col]) else 0.0
                    except:
                        stat['growth_rate'] = 0.0
                elif 'peak' in col or 'season' in col:
                    stat['peak_season'] = str(row[col]) if not pd.isna(row[col]) else ''
            
            # Add default values for missing fields
            if 'region_name' not in stat or not stat['region_name']:
                continue  # Skip records without region names
            
            if 'year' not in stat:
                stat['year'] = datetime.now().year
            if 'domestic_count' not in stat:
                stat['domestic_count'] = 100000
            if 'foreign_count' not in stat:
                stat['foreign_count'] = 25000
            if 'growth_rate' not in stat:
                stat['growth_rate'] = 5.0
            if 'peak_season' not in stat:
                stat['peak_season'] = 'October-March'
            
            # Add timestamps
            stat['created_at'] = datetime.now().isoformat()
            stat['updated_at'] = datetime.now().isoformat()
            
            stats.append(stat)
        
        # Convert to DataFrame
        stats_df = pd.DataFrame(stats)
        
        # Save processed data
        return save_processed_df(stats_df, 'tourist_stats.csv')
        
    except Exception as e:
        print(f"Error processing tourist stats: {str(e)}")
        return None

# Generate sample partner websites
def generate_partner_websites():
    partners = [
        {
            'partner_id': generate_uuid(),
            'name': 'Rajasthan Crafts',
            'website_url': 'https://www.rajasthancrafts.com',
            'rating': 4.7,
            'review_count': 421,
            'commission_rate': 15.0,
            'shipping_options': json.dumps({
                'standard': {'price': 100, 'days': '3-5'},
                'express': {'price': 250, 'days': '1-2'}
            }),
            'contact_info': 'contact@rajasthancrafts.com',
            'logo_url': '',
            'description': 'Premier marketplace for authentic Rajasthani handicrafts',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        },
        {
            'partner_id': generate_uuid(),
            'name': 'Jaipur Pottery House',
            'website_url': 'https://www.jaipurpotteryhouse.com',
            'rating': 4.5,
            'review_count': 187,
            'commission_rate': 12.0,
            'shipping_options': json.dumps({
                'standard': {'price': 120, 'days': '4-6'},
                'express': {'price': 300, 'days': '1-2'}
            }),
            'contact_info': 'info@jaipurpotteryhouse.com',
            'logo_url': '',
            'description': 'Specializing in traditional blue pottery from Jaipur',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        },
        {
            'partner_id': generate_uuid(),
            'name': 'Artisan Collective',
            'website_url': 'https://www.artisancollective.in',
            'rating': 4.9,
            'review_count': 243,
            'commission_rate': 10.0,
            'shipping_options': json.dumps({
                'standard': {'price': 150, 'days': '3-5'},
                'express': {'price': 350, 'days': '1-2'},
                'premium': {'price': 500, 'days': 'Same day'}
            }),
            'contact_info': 'hello@artisancollective.in',
            'logo_url': '',
            'description': 'Supporting artisans across India with fair trade practices',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        },
        {
            'partner_id': generate_uuid(),
            'name': 'Varanasi Silk Emporium',
            'website_url': 'https://www.varanasisilk.com',
            'rating': 4.8,
            'review_count': 312,
            'commission_rate': 18.0,
            'shipping_options': json.dumps({
                'standard': {'price': 200, 'days': '5-7'},
                'express': {'price': 400, 'days': '2-3'}
            }),
            'contact_info': 'orders@varanasisilk.com',
            'logo_url': '',
            'description': 'Authentic Banarasi silk products direct from weavers',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        },
        {
            'partner_id': generate_uuid(),
            'name': 'Karnataka Handicrafts',
            'website_url': 'https://www.karnatakahandicrafts.com',
            'rating': 4.6,
            'review_count': 178,
            'commission_rate': 14.0,
            'shipping_options': json.dumps({
                'standard': {'price': 120, 'days': '4-6'},
                'express': {'price': 280, 'days': '2-3'}
            }),
            'contact_info': 'support@karnatakahandicrafts.com',
            'logo_url': '',
            'description': 'Showcasing the rich handicraft tradition of Karnataka',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
    ]
    
    # Convert to DataFrame
    partners_df = pd.DataFrame(partners)
    
    # Save processed data
    return save_processed_df(partners_df, 'partner_sites.csv')

# Generate product-partner relationships
def generate_product_partner_relationships(products_path):
    try:
        # Read processed products
        products_df = pd.read_csv(products_path)
        
        # Read processed partners
        partners_df = pd.read_csv('/home/ubuntu/handicraft_marketplace/database/processed_data/partner_sites.csv')
        
        relationships = []
        
        # For each product, create 1-3 partner relationships
        for _, product in products_df.iterrows():
            # Randomly select 1-3 partners
            num_partners = min(len(partners_df), 3)
            selected_partners = partners_df.sample(n=num_partners)
            
            for _, partner in selected_partners.iterrows():
                # Calculate a slightly different price for each partner
                base_price = product['price']
                price_variation = (0.9 + (0.2 * np.random.random()))  # 0.9 to 1.1 variation
                partner_price = round(base_price * price_variation, 2)
                
                relationship = {
                    'id': generate_uuid(),
                    'product_id': product['product_id'],
                    'partner_id': partner['partner_id'],
                    'price': partner_price,
                    'shipping_fee': 100 + (50 * np.random.random()),  # 100-150 shipping fee
                    'availability': np.random.choice(['In Stock', 'Limited Stock', 'Out of Stock'], p=[0.7, 0.2, 0.1]),
                    'estimated_delivery': np.random.choice(['3-5 days', '5-7 days', '7-10 days']),
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                
                relationships.append(relationship)
        
        # Convert to DataFrame
        relationships_df = pd.DataFrame(relationships)
        
        # Save processed data
        return save_processed_df(relationships_df, 'product_partner.csv')
        
    except Exception as e:
        print(f"Error generating product-partner relationships: {str(e)}")
        return None

# Generate sample customers
def generate_sample_customers():
    customers = [
        {
            'customer_id': generate_uuid(),
            'name': 'Priya Sharma',
            'email': 'priya.sharma@example.com',
            'password_hash': 'hashed_password_placeholder',
            'address': '123 Park Street, Mumbai, Maharashtra',
            'phone': '+91 9876543210',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        },
        {
            'customer_id': generate_uuid(),
            'name': 'Rahul Patel',
            'email': 'rahul.patel@example.com',
            'password_hash': 'hashed_password_placeholder',
            'address': '456 Lake View, Bangalore, Karnataka',
            'phone': '+91 8765432109',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        },
        {
            'customer_id': generate_uuid(),
            'name': 'Ananya Singh',
            'email': 'ananya.singh@example.com',
            'password_hash': 'hashed_password_placeholder',
            'address': '789 Hill Road, Delhi, Delhi',
            'phone': '+91 7654321098',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        },
        {
            'customer_id': generate_uuid(),
            'name': 'Vikram Mehta',
            'email': 'vikram.mehta@example.com',
            'password_hash': 'hashed_password_placeholder',
            'address': '101 Sea Face, Chennai, Tamil Nadu',
            'phone': '+91 6543210987',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        },
        {
            'customer_id': generate_uuid(),
            'name': 'Neha Gupta',
            'email': 'neha.gupta@example.com',
            'password_hash': 'hashed_password_placeholder',
            'address': '202 River View, Kolkata, West Bengal',
            'phone': '+91 5432109876',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
    ]
    
    # Convert to DataFrame
    customers_df = pd.DataFrame(customers)
    
    # Save processed data
    return save_processed_df(customers_df, 'customers.csv')

# Generate sample orders and order items
def generate_sample_orders(products_partner_path, customers_path):
    try:
        # Read processed product-partner relationships
        product_partner_df = pd.read_csv(products_partner_path)
        
        # Read processed customers
        customers_df = pd.read_csv(customers_path)
        
        orders = []
        order_items = []
        
        # Generate 10 sample orders
        for i in range(10):
            # Select a random customer
            customer = customers_df.sample(n=1).iloc[0]
            
            # Generate order details
            order_id = generate_uuid()
            order_date = datetime.now().isoformat()
            status = np.random.choice(['Processing', 'Shipped', 'Delivered'], p=[0.3, 0.3, 0.4])
            
            # Select 1-5 random product-partner combinations
            num_items = np.random.randint(1, 6)
            selected_items = product_partner_df.sample(n=num_items)
            
            # Calculate order totals
            total_amount = 0
            platform_fee = 0
            
            for _, item in selected_items.iterrows():
                # Generate order item
                item_id = generate_uuid()
                quantity = np.random.randint(1, 4)
                price = item['price']
                subtotal = price * quantity
                
                # Add to total
                total_amount += subtotal
                
                # Calculate platform fee (assuming 15% average)
                item_platform_fee = subtotal * 0.15
                platform_fee += item_platform_fee
                
                order_item = {
                    'item_id': item_id,
                    'order_id': order_id,
                    'product_id': item['product_id'],
                    'partner_id': item['partner_id'],
                    'quantity': quantity,
                    'price': price,
                    'subtotal': subtotal,
                    'created_at': order_date
                }
                
                order_items.append(order_item)
            
            # Add shipping cost
            shipping_cost = 150
            total_amount += shipping_cost
            
            order = {
                'order_id': order_id,
                'customer_id': customer['customer_id'],
                'order_date': order_date,
                'total_amount': total_amount,
                'status': status,
                'shipping_address': customer['address'],
                'payment_method': np.random.choice(['Credit Card', 'UPI', 'Net Banking', 'Cash on Delivery']),
                'tracking_number': f'TRK{np.random.randint(100000, 999999)}' if status != 'Processing' else None,
                'platform_fee': platform_fee,
                'created_at': order_date,
                'updated_at': order_date
            }
            
            orders.append(order)
        
        # Convert to DataFrames
        orders_df = pd.DataFrame(orders)
        order_items_df = pd.DataFrame(order_items)
        
        # Save processed data
        orders_path = save_processed_df(orders_df, 'orders.csv')
        order_items_path = save_processed_df(order_items_df, 'order_items.csv')
        
        return orders_path, order_items_path
        
    except Exception as e:
        print(f"Error generating sample orders: {str(e)}")
        return None, None

# Generate Snowflake data import script
def generate_snowflake_import_script():
    script = """
-- Snowflake Data Import Script for Handicraft Marketplace Platform

-- Set context
USE DATABASE HANDICRAFT_MARKETPLACE;
USE SCHEMA CORE;

-- Create file formats
CREATE OR REPLACE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null')
    EMPTY_FIELD_AS_NULL = TRUE;

-- Create stages for data loading
CREATE OR REPLACE STAGE handicraft_data
    FILE_FORMAT = csv_format;

-- Instructions for uploading data to stage:
-- 1. Use the Snowflake web interface to upload CSV files to the stage
-- 2. Or use the SnowSQL client with PUT command:
--    PUT file:///path/to/local/file.csv @handicraft_data;

-- Load data into tables
-- Note: Replace with actual stage file paths after uploading

-- 1. Load REGIONS
COPY INTO REGIONS (
    region_id, name, state, description, famous_for, image_url, created_at, updated_at
)
FROM @handicraft_data/regions.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 2. Load ARTISANS
COPY INTO ARTISANS (
    artisan_id, name, location, craft_type, bio, image_url, contact_info, years_active, created_at, updated_at
)
FROM @handicraft_data/artisans.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 3. Load CATEGORIES
COPY INTO CATEGORIES (
    category_id, name, description, image_url, created_at, updated_at
)
FROM @handicraft_data/categories.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 4. Load GI_TAGS
COPY INTO GI_TAGS (
    gi_tag_id, name, description, issuing_body, issue_date, region_id, created_at, updated_at
)
FROM @handicraft_data/gi_tags.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 5. Load CULTURAL_STORIES
COPY INTO CULTURAL_STORIES (
    story_id, title, content, history, cultural_significance, video_url, created_at, updated_at
)
FROM @handicraft_data/cultural_stories.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 6. Load PRODUCTS
COPY INTO PRODUCTS (
    product_id, name, description, price, artisan_id, category_id, region_id, 
    is_gi_tagged, gi_tag_id, story_id, dimensions, weight, materials, created_at, updated_at
)
FROM @handicraft_data/products.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 7. Load PARTNER_SITES
COPY INTO PARTNER_SITES (
    partner_id, name, website_url, rating, review_count, commission_rate, 
    shipping_options, contact_info, logo_url, description, created_at, updated_at
)
FROM @handicraft_data/partner_sites.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 8. Load PRODUCT_PARTNER
COPY INTO PRODUCT_PARTNER (
    id, product_id, partner_id, price, shipping_fee, availability, estimated_delivery, created_at, updated_at
)
FROM @handicraft_data/product_partner.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 9. Load CUSTOMERS
COPY INTO CUSTOMERS (
    customer_id, name, email, password_hash, address, phone, created_at, updated_at
)
FROM @handicraft_data/customers.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 10. Load ORDERS
COPY INTO ORDERS (
    order_id, customer_id, order_date, total_amount, status, 
    shipping_address, payment_method, tracking_number, platform_fee, created_at, updated_at
)
FROM @handicraft_data/orders.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 11. Load ORDER_ITEMS
COPY INTO ORDER_ITEMS (
    item_id, order_id, product_id, partner_id, quantity, price, subtotal, created_at
)
FROM @handicraft_data/order_items.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- 12. Load TOURIST_STATS
COPY INTO TOURIST_STATS (
    stat_id, region_id, year, domestic_count, foreign_count, growth_rate, peak_season, created_at, updated_at
)
FROM @handicraft_data/tourist_stats.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format')
ON_ERROR = 'CONTINUE';

-- Verify data loading
SELECT 'REGIONS' as table_name, COUNT(*) as row_count FROM REGIONS
UNION ALL
SELECT 'ARTISANS', COUNT(*) FROM ARTISANS
UNION ALL
SELECT 'CATEGORIES', COUNT(*) FROM CATEGORIES
UNION ALL
SELECT 'GI_TAGS', COUNT(*) FROM GI_TAGS
UNION ALL
SELECT 'CULTURAL_STORIES', COUNT(*) FROM CULTURAL_STORIES
UNION ALL
SELECT 'PRODUCTS', COUNT(*) FROM PRODUCTS
UNION ALL
SELECT 'PARTNER_SITES', COUNT(*) FROM PARTNER_SITES
UNION ALL
SELECT 'PRODUCT_PARTNER', COUNT(*) FROM PRODUCT_PARTNER
UNION ALL
SELECT 'CUSTOMERS', COUNT(*) FROM CUSTOMERS
UNION ALL
SELECT 'ORDERS', COUNT(*) FROM ORDERS
UNION ALL
SELECT 'ORDER_ITEMS', COUNT(*) FROM ORDER_ITEMS
UNION ALL
SELECT 'TOURIST_STATS', COUNT(*) FROM TOURIST_STATS;
"""
    
    output_path = '/home/ubuntu/handicraft_marketplace/database/snowflake_import.sql'
    with open(output_path, 'w') as f:
        f.write(script)
    
    print(f"Generated Snowflake import script: {output_path}")
    return output_path

# Main execution
if __name__ == "__main__":
    print("Starting dataset analysis and processing...")
    
    # Process artisan data
    artisans_path = process_artisan_data()
    
    # Process GI tagged products
    gi_tags_path, regions_path = process_gi_tagged_products()
    
    # Process products and images
    products_path, categories_path, stories_path = process_products_and_images()
    
    # Process tourist statistics
    tourist_stats_path = process_tourist_stats()
    
    # Generate partner websites
    partners_path = generate_partner_websites()
    
    # Generate product-partner relationships
    product_partner_path = generate_product_partner_relationships(products_path)
    
    # Generate sample customers
    customers_path = generate_sample_customers()
    
    # Generate sample orders
    orders_path, order_items_path = generate_sample_orders(product_partner_path, customers_path)
    
    # Generate Snowflake import script
    snowflake_import_script = generate_snowflake_import_script()
    
    print("Dataset processing complete!")
    print("All processed data files are available in: /home/ubuntu/handicraft_marketplace/database/processed_data/")
    print(f"Snowflake import script generated: {snowflake_import_script}")
