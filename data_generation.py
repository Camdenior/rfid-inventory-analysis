"""
This creates realistic fake RFID inventory data for analysis.
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# Initialize Faker for realistic data generation
fake = Faker()

# CONFIGURATION - These control the data generation
NUM_PRODUCTS = 1000 # Total products in inventory
NUM_LOCATIONS = 5 # Number of warehouse locations
NUM_READERS = 20 # Number of RFID readers
DAYS_OF_DATA = 7 # How many days of historical data

# Step 1: Generate product data
print("Generating product data...")

categories = ['Electronics', 'Clothing', 'Food', 'Furniture', 'Books', 'Toys', 'Sports', 'Tools']

products = []
for i in range(NUM_PRODUCTS):
    product = {
        'product_id': f'prod_{i+1:04d}', #PROD_0001, PROD_0002, etc.
        'product_name': fake.catch_phrase(), # Random product names
        'category': random.choice(categories), 
        'price': round(random.uniform(5.0, 500.0), 2),
        'location': f'Zone_{random.choice(["A", "B", "C", "D", "E"])}', 
        'tag_id': f'TAG_{fake.hexify("^^^^_^^^^_^^^^").upper()}' # Random RFID tag ID
        'date added': fake.date_between(start_date='-1y', end_date='today')
    }
    products.append(product)

products_df = pd.DataFrame(products)

# Step 2: Generate RFID reader data
print("Generating RFID read events...")

read_events = []
start_date = datetime.now() - timedelta(days=DAYS_OF_DATA)

for product in products:
    read_frequency = random.choice([1, 2, 3, 5, 10])

    for day in range(DAYS_OF_DATA):
        current_date = start_date + timedelta(days=day)

        for _ in range(read_frequency):
            hour = random.randint(6, 22)
            minute = random.randint(0, 59)
            timestamp = current_date.replace(hour=hour, minute=minute)

            read_event = {
                'event_id': fake.uuid4(),
                'tag_id': product['tag_id'],
                'product_id': product['product_id'],
                'reader_id': f'READER_{random.randint(1, NUM_READERS):02d}',
                'timestamp': timestamp,
                'read_success': read_success,
                'signal_strength': signal_strength,
                'location': product['location'],
                'temperature': round(random.uniform(18, 25), 1),
                'humidity': round(random.uniform(30, 70), 1)
            }
            read_events.append(read_event)

reads_df = pd.DataFrame(read_events)

#Step 3: Generate Performance Metrics
print("Calculating initial metrics...")

location_performance = reads_df.groupby('location').agg({
    'read_success': 'mean',
    'signal_strength': 'mean',
    'event_id': 'count'
}).round(3)

print('\nLocation Performance Summary:')
print(location_performance)

# Step 4: Save Data to CSV Files
print("\nSaving data files...")

os.makedirs('data', exist_ok=True)

products_df.to_csv('data/products.csv', index=False)
reads_df.to_csv('data/rfid_reads.csv', index=False)
location_performance.to_csv('data/location_performance.csv')

print(f"""
Data generation complete!
- {len(products_df)} products created
- {len(reads_df)} RFID read events generated
- Files saved to /data directory

Next step: Run database_setup.py to import this data into SQLite.
""")