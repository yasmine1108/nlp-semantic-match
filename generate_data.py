import pandas as pd
import os

import random

categories = {
    "Power Tools": [
        "Cordless Drill", "Impact Driver", "Angle Grinder", "Circular Saw",
        "Jigsaw", "Rotary Hammer", "Heat Gun", "Power Sander"
    ],
    "Hand Tools": [
        "Hammer", "Screwdriver Set", "Pliers", "Wrench Set",
        "Tape Measure", "Utility Knife", "Hex Key Set"
    ],
    "Safety Gear": [
        "Safety Helmet", "Safety Goggles", "Face Shield",
        "High Visibility Vest", "Protective Gloves", "Ear Protection"
    ],
    "Electronics": [
        "Digital Multimeter", "Laser Distance Meter",
        "Clamp Meter", "Voltage Tester"
    ],
    "Automotive": [
        "Hydraulic Jack", "Torque Wrench",
        "Car Battery Charger", "Oil Filter Wrench"
    ]
}

brands = [
    "Bosch", "Makita", "DeWalt", "Milwaukee",
    "Stanley", "Fluke", "Knipex", "3M"
]

def generate_products(count=300):
    products = []
    product_id = 1000

    for _ in range(count):
        category = random.choice(list(categories.keys()))
        item = random.choice(categories[category])
        brand = random.choice(brands)
        model = f"{random.randint(10,99)}{random.choice(['V','X','Pro','Max'])}"

        products.append({
            "id": product_id,
            "name": f"{brand} {item} {model}",
            "category": category
        })
        product_id += 1

    return products


def generate_queries(products, count=300):
    queries = []

    semantic_templates = {
        "Drill": [
            "{brand} drill",
            "{brand} cordless drill",
            "{brand} power drill"
        ],
        "Helmet": [
            "{brand} safety helmet",
            "{brand} hard hat",
            "{brand} head protection"
        ],
        "Goggles": [
            "{brand} safety goggles",
            "{brand} eye protection"
        ],
        "Tape Measure": [
            "{brand} tape measure",
            "{brand} measuring tape"
        ],
        "Saw": [
            "{brand} circular saw",
            "{brand} electric saw"
        ],
        "Multimeter": [
            "{brand} multimeter",
            "{brand} digital multimeter"
        ],
        "Pliers": [
            "{brand} pliers",
            "{brand} hand pliers"
        ],
        "Jack": [
            "{brand} hydraulic jack",
            "{brand} car jack"
        ]
    }

    for _ in range(count):
        product = random.choice(products)

        # Extract brand (first word)
        brand = product["name"].split()[0]

        # Find matching keyword
        keyword = next(
            (k for k in semantic_templates if k in product["name"]),
            None
        )

        if keyword:
            query = random.choice(semantic_templates[keyword]).format(brand=brand.lower())
        else:
            # Fallback: brand + product type words
            query = " ".join(product["name"].lower().split()[:2])

        queries.append({
            "query": query,
            "expected_id": product["id"]
        })

    return queries



# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Save to CSV
products = generate_products(500)   
queries = generate_queries(products, 500)  

pd.DataFrame(products).to_csv("data/products.csv", index=False)
pd.DataFrame(queries).to_csv("data/test_queries.csv", index=False)

print("Data generated in 'data/' folder successfully!")