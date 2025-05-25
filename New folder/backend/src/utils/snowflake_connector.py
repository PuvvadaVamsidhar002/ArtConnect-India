"""
Mock Snowflake connector utility for the Handicraft Marketplace Platform.
Uses local JSON files instead of connecting to Snowflake.
"""
import os
import json
import random
from datetime import datetime

# Path to mock data files
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mock_data')

# Create mock_data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

# Mock data files
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')
ARTISANS_FILE = os.path.join(DATA_DIR, 'artisans.json')
PARTNERS_FILE = os.path.join(DATA_DIR, 'partners.json')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.json')
REGIONS_FILE = os.path.join(DATA_DIR, 'regions.json')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')

# Initialize mock data if files don't exist
def initialize_mock_data():
    # Create mock products
    if not os.path.exists(PRODUCTS_FILE):
        products = []
        for i in range(1, 51):
            product = {
                "PRODUCT_ID": str(i),
                "NAME": f"Handcrafted Product {i}",
                "DESCRIPTION": f"This is a beautiful handcrafted product from India. Product {i} showcases traditional craftsmanship.",
                "PRICE": random.randint(500, 5000),
                "CATEGORY_ID": str(random.randint(1, 6)),
                "ARTISAN_ID": str(random.randint(1, 20)),
                "REGION_ID": str(random.randint(1, 10)),
                "MATERIALS": "Cotton, Silk, Wood",
                "DIMENSIONS": f"{random.randint(10, 50)}cm x {random.randint(10, 50)}cm",
                "WEIGHT": f"{random.randint(100, 2000)}g",
                "IS_GI_TAGGED": random.choice([True, False]),
                "CREATED_AT": datetime.now().isoformat(),
                "UPDATED_AT": datetime.now().isoformat(),
                "ARTISAN_NAME": f"Artisan {random.randint(1, 20)}",
                "CATEGORY_NAME": random.choice(["Textiles", "Pottery", "Woodwork", "Metalwork", "Jewelry", "Paintings"]),
                "REGION_NAME": random.choice(["Delhi", "Mumbai", "Kolkata", "Chennai", "Jaipur", "Varanasi"]),
                "STATE": random.choice(["Uttar Pradesh", "Maharashtra", "West Bengal", "Tamil Nadu", "Rajasthan", "Bihar"]),
                "STORY_TITLE": f"The Story of Product {i}",
                "STORY_CONTENT": f"This product has a rich cultural history dating back centuries. It represents the traditional craftsmanship of the region.",
                "HISTORY": "This craft has been practiced for generations and has significant cultural importance.",
                "CULTURAL_SIGNIFICANCE": "This item plays an important role in local festivals and ceremonies."
            }
            products.append(product)
        
        with open(PRODUCTS_FILE, 'w') as f:
            json.dump(products, f, indent=2)
    
    # Create mock artisans
    if not os.path.exists(ARTISANS_FILE):
        artisans = []
        for i in range(1, 21):
            artisan = {
                "ARTISAN_ID": str(i),
                "NAME": f"Artisan {i}",
                "LOCATION": random.choice(["Delhi", "Mumbai", "Kolkata", "Chennai", "Jaipur", "Varanasi"]),
                "CRAFT_TYPE": random.choice(["Weaver", "Potter", "Woodcarver", "Metalsmith", "Jeweler", "Painter"]),
                "BIO": f"Artisan {i} has been practicing their craft for over {random.randint(5, 40)} years. They learned from their ancestors and are now passing the knowledge to the next generation.",
                "CONTACT_INFO": f"artisan{i}@example.com",
                "YEARS_ACTIVE": random.randint(5, 40),
                "REGION_ID": str(random.randint(1, 10)),
                "IMAGE_URL": f"/artisans/{i}.jpg",
                "CREATED_AT": datetime.now().isoformat(),
                "UPDATED_AT": datetime.now().isoformat()
            }
            artisans.append(artisan)
        
        with open(ARTISANS_FILE, 'w') as f:
            json.dump(artisans, f, indent=2)
    
    # Create mock partners
    if not os.path.exists(PARTNERS_FILE):
        partners = []
        for i in range(1, 11):
            partner = {
                "PARTNER_ID": str(i),
                "NAME": f"Local Handicraft Website {i}",
                "WEBSITE_URL": f"https://localhandicraft{i}.example.com",
                "DESCRIPTION": f"A local website specializing in handicrafts from various regions of India.",
                "CONTACT_EMAIL": f"contact@localhandicraft{i}.example.com",
                "CONTACT_PHONE": f"+91 9876543{i:03d}",
                "REGION_ID": str(random.randint(1, 10 )),
                "COMMISSION_RATE": random.uniform(0.1, 0.2),
                "RATING": random.uniform(3.5, 5.0),
                "REVIEW_COUNT": random.randint(10, 500),
                "CREATED_AT": datetime.now().isoformat(),
                "UPDATED_AT": datetime.now().isoformat()
            }
            partners.append(partner)
        
        with open(PARTNERS_FILE, 'w') as f:
            json.dump(partners, f, indent=2)
    
    # Create mock categories
    if not os.path.exists(CATEGORIES_FILE):
        categories = [
            {"CATEGORY_ID": "1", "NAME": "Textiles", "DESCRIPTION": "Handwoven and handcrafted textiles including sarees, shawls, and fabrics."},
            {"CATEGORY_ID": "2", "NAME": "Pottery", "DESCRIPTION": "Traditional pottery and ceramics from various regions of India."},
            {"CATEGORY_ID": "3", "NAME": "Woodwork", "DESCRIPTION": "Handcrafted wooden items including furniture, toys, and decorative pieces."},
            {"CATEGORY_ID": "4", "NAME": "Metalwork", "DESCRIPTION": "Metal crafts including brass, copper, and bronze items."},
            {"CATEGORY_ID": "5", "NAME": "Jewelry", "DESCRIPTION": "Traditional and contemporary jewelry made with various materials."},
            {"CATEGORY_ID": "6", "NAME": "Paintings", "DESCRIPTION": "Traditional art forms including Madhubani, Warli, and Pattachitra."}
        ]
        
        with open(CATEGORIES_FILE, 'w') as f:
            json.dump(categories, f, indent=2)
    
    # Create mock regions
    if not os.path.exists(REGIONS_FILE):
        regions = [
            {"REGION_ID": "1", "NAME": "Delhi", "STATE": "Delhi", "DESCRIPTION": "The capital region known for various crafts."},
            {"REGION_ID": "2", "NAME": "Mumbai", "STATE": "Maharashtra", "DESCRIPTION": "Financial capital with rich artistic traditions."},
            {"REGION_ID": "3", "NAME": "Kolkata", "STATE": "West Bengal", "DESCRIPTION": "Known for textiles and traditional art forms."},
            {"REGION_ID": "4", "NAME": "Chennai", "STATE": "Tamil Nadu", "DESCRIPTION": "Rich in traditional crafts and bronze work."},
            {"REGION_ID": "5", "NAME": "Jaipur", "STATE": "Rajasthan", "DESCRIPTION": "Famous for textiles, jewelry, and pottery."},
            {"REGION_ID": "6", "NAME": "Varanasi", "STATE": "Uttar Pradesh", "DESCRIPTION": "Known for silk weaving and metalwork."},
            {"REGION_ID": "7", "NAME": "Hyderabad", "STATE": "Telangana", "DESCRIPTION": "Famous for pearls and bidri work."},
            {"REGION_ID": "8", "NAME": "Ahmedabad", "STATE": "Gujarat", "DESCRIPTION": "Known for textiles and embroidery."},
            {"REGION_ID": "9", "NAME": "Bhopal", "STATE": "Madhya Pradesh", "DESCRIPTION": "Rich in tribal arts and crafts."},
            {"REGION_ID": "10", "NAME": "Lucknow", "STATE": "Uttar Pradesh", "DESCRIPTION": "Famous for chikankari embroidery and pottery."}
        ]
        
        with open(REGIONS_FILE, 'w') as f:
            json.dump(regions, f, indent=2)
    
    # Create mock orders
    if not os.path.exists(ORDERS_FILE):
        orders = []
        for i in range(1, 31):
            order_items = []
            for j in range(random.randint(1, 5)):
                product_id = str(random.randint(1, 50))
                partner_id = str(random.randint(1, 10))
                price = random.randint(500, 5000)
                quantity = random.randint(1, 3)
                
                order_item = {
                    "ITEM_ID": f"{i}-{j}",
                    "PRODUCT_ID": product_id,
                    "PARTNER_ID": partner_id,
                    "PRICE": price,
                    "QUANTITY": quantity,
                    "SUBTOTAL": price * quantity
                }
                order_items.append(order_item)
            
            total_amount = sum(item["SUBTOTAL"] for item in order_items)
            platform_fee = round(total_amount * random.uniform(0.1, 0.2), 2)
            
            order = {
                "ORDER_ID": str(i),
                "CUSTOMER_ID": str(random.randint(1, 100)),
                "ORDER_DATE": (datetime.now().replace(day=random.randint(1, 28), month=random.randint(1, 12))).isoformat(),
                "STATUS": random.choice(["Processing", "Shipped", "Delivered"]),
                "TOTAL_AMOUNT": total_amount,
                "PLATFORM_FEE": platform_fee,
                "PARTNER_AMOUNT": total_amount - platform_fee,
                "SHIPPING_ADDRESS": f"{random.randint(1, 999)} Example Street, City, State, India",
                "PAYMENT_METHOD": random.choice(["Credit Card", "Debit Card", "UPI", "Net Banking"]),
                "ITEMS": order_items
            }
            orders.append(order)
        
        with open(ORDERS_FILE, 'w') as f:
            json.dump(orders, f, indent=2)

# Initialize mock data
initialize_mock_data()

def execute_query(query, params=None):
    """
    Mock function to execute queries against local JSON files instead of Snowflake.
    """
    # Extract table name from query (very simplified parsing)
    query_lower = query.lower()
    
    # Handle SELECT queries
    if query_lower.startswith('select'):
        # Products queries
        if 'products' in query_lower:
            with open(PRODUCTS_FILE, 'r') as f:
                products = json.load(f)
            
            # Filter by product ID
            if params and 'product_id' in params:
                return [p for p in products if p['PRODUCT_ID'] == params['product_id']]
            
            # Filter by category
            if params and 'category_id' in params:
                return [p for p in products if p['CATEGORY_ID'] == params['category_id']]
            
            # Filter by region
            if params and 'region_id' in params:
                return [p for p in products if p['REGION_ID'] == params['region_id']]
            
            # Filter by artisan
            if params and 'artisan_id' in params:
                return [p for p in products if p['ARTISAN_ID'] == params['artisan_id']]
            
            # Search by name
            if params and 'search_term' in params:
                search_term = params['search_term'].lower()
                return [p for p in products if search_term in p['NAME'].lower() or search_term in p['DESCRIPTION'].lower()]
            
            # Pagination
            if params and 'limit' in params and 'offset' in params:
                limit = params['limit']
                offset = params['offset']
                return products[offset:offset+limit]
            
            return products
        
        # Artisans queries
        elif 'artisans' in query_lower:
            with open(ARTISANS_FILE, 'r') as f:
                artisans = json.load(f)
            
            # Filter by artisan ID
            if params and 'artisan_id' in params:
                return [a for a in artisans if a['ARTISAN_ID'] == params['artisan_id']]
            
            # Pagination
            if params and 'limit' in params and 'offset' in params:
                limit = params['limit']
                offset = params['offset']
                return artisans[offset:offset+limit]
            
            return artisans
        
        # Partners queries
        elif 'partners' in query_lower:
            with open(PARTNERS_FILE, 'r') as f:
                partners = json.load(f)
            
            # Filter by partner ID
            if params and 'partner_id' in params:
                return [p for p in partners if p['PARTNER_ID'] == params['partner_id']]
            
            # Filter by product ID (mock relationship)
            if params and 'product_id' in params:
                # Randomly select 2-5 partners for this product
                num_partners = random.randint(2, 5)
                selected_partners = random.sample(partners, min(num_partners, len(partners)))
                
                # Add product-specific pricing
                for partner in selected_partners:
                    partner['PRICE'] = random.randint(500, 5000)
                    partner['SHIPPING_FEE'] = random.randint(50, 200)
                    partner['ESTIMATED_DELIVERY'] = f"{random.randint(3, 10)} days"
                
                return selected_partners
            
            return partners
        
        # Categories queries
        elif 'categories' in query_lower:
            with open(CATEGORIES_FILE, 'r') as f:
                categories = json.load(f)
            
            # Filter by category ID
            if params and 'category_id' in params:
                return [c for c in categories if c['CATEGORY_ID'] == params['category_id']]
            
            return categories
        
        # Regions queries
        elif 'regions' in query_lower:
            with open(REGIONS_FILE, 'r') as f:
                regions = json.load(f)
            
            # Filter by region ID
            if params and 'region_id' in params:
                return [r for r in regions if r['REGION_ID'] == params['region_id']]
            
            return regions
        
        # Orders queries
        elif 'orders' in query_lower:
            with open(ORDERS_FILE, 'r') as f:
                orders = json.load(f)
            
            # Filter by order ID
            if params and 'order_id' in params:
                return [o for o in orders if o['ORDER_ID'] == params['order_id']]
            
            # Filter by customer ID
            if params and 'customer_id' in params:
                return [o for o in orders if o['CUSTOMER_ID'] == params['customer_id']]
            
            return orders
    
    # Handle INSERT queries (simplified)
    elif query_lower.startswith('insert'):
        if 'orders' in query_lower and params and 'order_data' in params:
            with open(ORDERS_FILE, 'r') as f:
                orders = json.load(f)
            
            order_data = params['order_data']
            order_data['ORDER_ID'] = str(len(orders) + 1)
            orders.append(order_data)
            
            with open(ORDERS_FILE, 'w') as f:
                json.dump(orders, f, indent=2)
            
            return [{'ORDER_ID': order_data['ORDER_ID']}]
    
    # Default empty response
    return []

def get_connection():
    """
    Mock function to return a dummy connection object.
    """
    class MockConnection:
        def cursor(self):
            class MockCursor:
                def execute(self, query, params=None):
                    self.results = execute_query(query, params)
                    self.rowcount = len(self.results)
                
                def fetchall(self):
                    return self.results
                
                def fetchone(self):
                    return self.results[0] if self.results else None
                
                def close(self):
                    pass
            
            return MockCursor()
        
        def close(self):
            pass
    
    return MockConnection()

def execute_procedure(procedure_name, params=None):
    """
    Mock function to execute stored procedures.
    """
    # For QR code generation, return a mock URL
    if procedure_name.lower() == 'generate_qr_code':
        product_id = params.get('product_id', '1')
        return f"https://example.com/qr/{product_id}"
    
    # Default empty response
    return []

def init_snowflake():
    """
    Mock function to initialize Snowflake connection.
    """
    print("Mock Snowflake initialized with local JSON data")
    # Initialize mock data
    initialize_mock_data()
    return True
