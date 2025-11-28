import csv
import random
import time

def generate_large_csv(filename="large_products.csv", num_products=500000):
    print(f"Generating {num_products} products...")
    start_time = time.time()
    
    headers = ["sku", "name", "description", "price", "quantity", "is_active"]
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        # Write in chunks for performance
        chunk_size = 10000
        for i in range(0, num_products, chunk_size):
            chunk = []
            for j in range(chunk_size):
                idx = i + j + 1
                if idx > num_products:
                    break
                    
                sku = f"LARGE-PROD-{idx:06d}"
                name = f"Test Product {idx}"
                description = f"Description for test product {idx} - generated for load testing"
                price = round(random.uniform(10.0, 1000.0), 2)
                quantity = random.randint(0, 1000)
                is_active = "true" if random.random() > 0.1 else "false"
                
                chunk.append([sku, name, description, price, quantity, is_active])
            
            writer.writerows(chunk)
            print(f"Generated {min(i + chunk_size, num_products)} products...", end="\r")
            
    end_time = time.time()
    duration = end_time - start_time
    file_size_mb = os.path.getsize(filename) / (1024 * 1024)
    
    print(f"\n✅ Successfully generated {filename}")
    print(f"📊 Total Products: {num_products}")
    print(f"⏱️ Time taken: {duration:.2f} seconds")
    print(f"💾 File size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    import os
    generate_large_csv()
