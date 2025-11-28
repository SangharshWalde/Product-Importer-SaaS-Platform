import requests
import json

API_URL = "http://localhost:8000/api"

def add_sample_product():
    product_data = {
        "sku": "MANUAL-001",
        "name": "Manual Test Product",
        "description": "Added via verification script",
        "price": 99.99,
        "quantity": 10,
        "is_active": True
    }
    
    print("Adding sample product...")
    response = requests.post(f"{API_URL}/products", json=product_data)
    
    if response.status_code in [200, 201]:
        print("Product added successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed to add product: {response.text}")
        return

    print("\nVerifying Search...")
    search_response = requests.get(f"{API_URL}/products?search=MANUAL-001")
    if search_response.status_code == 200:
        data = search_response.json()
        products = data.get("products", [])
        if len(products) > 0:
            print(f"Search successful! Found {len(products)} product(s).")
            print(f"First match: {products[0]['name']} ({products[0]['sku']})")
        else:
            print("Search returned no results.")
    else:
        print(f"Search failed: {search_response.status_code}")

if __name__ == "__main__":
    add_sample_product()
