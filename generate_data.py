import pandas as pd
import os

# Create the Official Equipment Database which include the correct items present in the warehouse
products = [
    {"id": 101, "name": "Bosch Professional Drill GSB 18V", "category": "Power Tools"},
    {"id": 102, "name": "Makita Cordless Impact Driver", "category": "Power Tools"},
    {"id": 103, "name": "Industrial Safety Helmet (Yellow)", "category": "Safety Gear"},
    {"id": 104, "name": "3M Protective Safety Goggles", "category": "Safety Gear"},
    {"id": 105, "name": "Fluke Digital Multimeter 117", "category": "Electronics"},
    {"id": 106, "name": "Hydraulic Jack 5 Ton", "category": "Automotive"},
    {"id": 107, "name": "Knipex High Leverage Pliers", "category": "Hand Tools"},
    {"id": 108, "name": "Stanley FatMax Tape Measure 5m", "category": "Hand Tools"},
    {"id": 109, "name": "DeWalt Circular Saw 184mm", "category": "Power Tools"},
    {"id": 110, "name": "High Visibility Vest (Orange, L)", "category": "Safety Gear"}
]

# These represent what a user might actually type to use for tests
queries = [
    {"query": "bosch drill 18v", "expected_id": 101},
    {"query": "yellow hard hat", "expected_id": 103}, # Semantic match: Hard hat -> Helmet
    {"query": "measure tape stanley", "expected_id": 108},
    {"query": "protection glasses", "expected_id": 104},
    {"query": "electric saw", "expected_id": 109}
]

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Save to CSV
pd.DataFrame(products).to_csv("data/products.csv", index=False)
pd.DataFrame(queries).to_csv("data/test_queries.csv", index=False)

print("Data generated in 'data/' folder successfully!")