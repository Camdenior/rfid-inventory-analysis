"""
RFID Data Generation Script
This creates realistic fake RFID inventory data for analysis
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# Initialize Faker for realistic data generation
fake = Faker()

# CONFIGURATION - These control the data generation
NUM_PRODUCTS = 1000  # Total products in inventory
NUM_LOCATIONS = 5    # Number of warehouse locations
NUM_READERS = 20     # Number of RFID readers
DAYS_OF_DATA = 7     # How many days of historical data

# Step 1: Generate Product Data
print("Generating product data...")

# Product categories that might be in a warehouse
categories = ['Electronics', 'Clothing', 'Food', 'Furniture', 'Books', 'Toys', 'Sports', 'Tools']

# Create products with realistic attributes
products = []
for i in range(NUM_PRODUCTS):
    product = {
        'product_id': f'PROD_{i:04d}',  # PROD_0001, PROD_0002, etc.
        'product_name': fake.catch_phrase(),  # Random product names
        'category': random.choice(categories),
        'price': round(random.uniform(10, 500), 2),
        'location': f'Zone_{random.choice(["A","B","C","D","E"])}',
        'tag_id': f'TAG_{fake.hexify("^^^^-^^^^-^^^^").upper()}',  # Realistic RFID tag format
        'date_added': fake.date_between(start_date='-1y', end_date='today')
    }
    products.append(product)

# Convert to DataFrame for easier manipulation
products_df = pd.DataFrame(products)

# Step 2: Generate RFID Read Events
print("Generating RFID read events...")

# This simulates RFID readers attempting to read tags over time
read_events = []

# Generate reads for each day
start_date = datetime.now() - timedelta(days=DAYS_OF_DATA)

for product in products:
    # Some products get read more often (simulating high-traffic items)
    read_frequency = random.choice([1, 2, 3, 5, 10])
    
    for day in range(DAYS_OF_DATA):
        current_date = start_date + timedelta(days=day)
        
        # Generate multiple reads per day
        for _ in range(read_frequency):
            # Simulate different times of day (business hours)
            hour = random.randint(6, 22)
            minute = random.randint(0, 59)
            timestamp = current_date.replace(hour=hour, minute=minute)
            
            # RFID reads aren't always successful (85% success rate)
            read_success = random.random() < 0.85
            
            # Signal strength varies (affects read success)
            signal_strength = random.uniform(-90, -30) if read_success else random.uniform(-100, -85)
            
            read_event = {
                'event_id': fake.uuid4(),
                'tag_id': product['tag_id'],
                'product_id': product['product_id'],
                'reader_id': f'READER_{random.randint(1, NUM_READERS):02d}',
                'timestamp': timestamp,
                'read_success': read_success,
                'signal_strength': signal_strength,
                'location': product['location'],
                'temperature': round(random.uniform(18, 25), 1),  # Environmental factors
                'humidity': round(random.uniform(30, 70), 1)
            }
            read_events.append(read_event)

# Convert to DataFrame
reads_df = pd.DataFrame(read_events)

# Step 3: Generate Performance Metrics
print("Calculating initial metrics...")

# Calculate read success rate by location
location_performance = reads_df.groupby('location').agg({
    'read_success': 'mean',
    'signal_strength': 'mean',
    'event_id': 'count'
}).round(3)

print("\nLocation Performance Summary:")
print(location_performance)

# Step 4: Save Data to CSV Files
print("\nSaving data files...")

# Create data directory if it doesn't exist
import os
os.makedirs('data', exist_ok=True)

# Save all dataframes
products_df.to_csv('data/products.csv', index=False)
reads_df.to_csv('data/rfid_reads.csv', index=False)
location_performance.to_csv('data/location_performance.csv')

print(f"""
Data Generation Complete!
- {len(products_df)} products created
- {len(reads_df)} RFID read events generated
- Files saved to /data directory

Next step: Run database_setup.py to import this data into SQLite
""")