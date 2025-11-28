import requests
import time
import os

BASE_URL = "http://localhost:8000/api"

def print_pass(message):
    print(f"✅ PASS: {message}")

def print_fail(message):
    print(f"❌ FAIL: {message}")

def test_products_crud():
    print("\n--- Testing Products CRUD ---")
    
    # 1. Create Product
    new_product = {
        "sku": "TEST-001",
        "name": "Test Product",
        "description": "A test product",
        "price": 99.99,
        "quantity": 10,
        "is_active": True
    }
    
    response = requests.post(f"{BASE_URL}/products", json=new_product)
    if response.status_code == 200:
        product = response.json()
        print_pass(f"Created product {product['sku']} (ID: {product['id']})")
        product_id = product['id']
    else:
        print_fail(f"Create product failed: {response.text}")
        return

    # 2. Get Product
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    if response.status_code == 200 and response.json()['sku'] == "TEST-001":
        print_pass("Retrieved product details")
    else:
        print_fail("Get product failed")

    # 3. Update Product
    update_data = {"price": 199.99, "name": "Updated Test Product"}
    response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data)
    if response.status_code == 200 and response.json()['price'] == 199.99:
        print_pass("Updated product price")
    else:
        print_fail("Update product failed")

    # 4. List Products
    response = requests.get(f"{BASE_URL}/products")
    if response.status_code == 200:
        products = response.json()['products']
        if any(p['id'] == product_id for p in products):
            print_pass("Product found in list")
        else:
            print_fail("Product not found in list")
    else:
        print_fail("List products failed")

    # 5. Delete Product
    response = requests.delete(f"{BASE_URL}/products/{product_id}")
    if response.status_code == 200:
        print_pass("Deleted product")
    else:
        print_fail("Delete product failed")

    # 6. Verify Deletion
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    if response.status_code == 404:
        print_pass("Verified product deletion")
    else:
        print_fail("Product still exists after deletion")

def test_webhooks():
    print("\n--- Testing Webhooks ---")
    
    # 1. Create Webhook
    webhook_data = {
        "url": "https://httpbin.org/post",
        "event_type": "product.created",
        "is_enabled": True
    }
    
    response = requests.post(f"{BASE_URL}/webhooks", json=webhook_data)
    if response.status_code == 200:
        webhook = response.json()
        print_pass(f"Created webhook (ID: {webhook['id']})")
        webhook_id = webhook['id']
    else:
        print_fail(f"Create webhook failed: {response.text}")
        return

    # 2. Test Webhook Trigger
    response = requests.post(f"{BASE_URL}/webhooks/{webhook_id}/test")
    if response.status_code == 200:
        print_pass("Webhook test trigger successful")
    else:
        print_fail(f"Webhook test failed: {response.text}")

    # 3. Delete Webhook
    response = requests.delete(f"{BASE_URL}/webhooks/{webhook_id}")
    if response.status_code == 200:
        print_pass("Deleted webhook")
    else:
        print_fail("Delete webhook failed")

def test_upload_endpoint():
    print("\n--- Testing Upload Endpoint ---")
    
    # Create a dummy CSV
    with open("test_upload.csv", "w") as f:
        f.write("sku,name,description,price,quantity,is_active\n")
        f.write("UPLOAD-TEST,Upload Product,Desc,10.00,5,true\n")
    
    try:
        with open("test_upload.csv", "rb") as f:
            files = {"file": ("test_upload.csv", f, "text/csv")}
            response = requests.post(f"{BASE_URL}/upload", files=files)
            
        if response.status_code == 202:
            data = response.json()
            print_pass(f"Upload accepted (Task ID: {data['task_id']})")
        else:
            print_fail(f"Upload failed: {response.text}")
            
    finally:
        if os.path.exists("test_upload.csv"):
            os.remove("test_upload.csv")

if __name__ == "__main__":
    print("🚀 Starting System Verification Tests...")
    try:
        # Check if server is up
        requests.get(f"{BASE_URL}/products")
        print_pass("Server is running and accessible")
        
        test_products_crud()
        test_webhooks()
        test_upload_endpoint()
        
        print("\n✨ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print_fail("Could not connect to server. Is it running?")
