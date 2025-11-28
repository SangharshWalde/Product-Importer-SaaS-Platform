import requests
import sys

BASE_URL = "http://localhost:8000/api"

def verify_deletion():
    print("1. Getting list of products...", flush=True)
    try:
        response = requests.get(f"{BASE_URL}/products")
        data = response.json()
        products = data.get("products", [])
        
        if not products:
            print("❌ No products found to delete!", flush=True)
            return
            
        print(f"✅ Found {len(products)} products.", flush=True)
        
        # Pick the first product
        product_to_delete = products[0]
        product_id = product_to_delete["id"]
        sku = product_to_delete["sku"]
        
        print(f"2. Attempting to delete product: {sku} (ID: {product_id})", flush=True)
        
        # Delete request
        delete_response = requests.delete(f"{BASE_URL}/products/{product_id}")
        
        if delete_response.status_code == 200:
            print("✅ Delete request successful (Status 200)", flush=True)
        else:
            print(f"❌ Delete request failed: {delete_response.status_code}", flush=True)
            print(delete_response.text, flush=True)
            return

        # Verify it's gone
        print("3. Verifying deletion...", flush=True)
        verify_response = requests.get(f"{BASE_URL}/products/{product_id}")
        
        if verify_response.status_code == 404:
            print(f"✅ Product {sku} successfully deleted! (404 Not Found)", flush=True)
        else:
            print(f"❌ Product still exists! Status: {verify_response.status_code}", flush=True)
            
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)

if __name__ == "__main__":
    verify_deletion()
