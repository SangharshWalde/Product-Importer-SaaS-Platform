import requests
import time
import os
import sys

API_URL = "http://localhost:8000/api"
FILE_PATH = r"c:\Product-Importer-SaaS\large_products.csv"

def verify_upload_speed():
    if not os.path.exists(FILE_PATH):
        print(f"Error: File not found at {FILE_PATH}")
        return

    print(f"Uploading {FILE_PATH} ({os.path.getsize(FILE_PATH) / 1024 / 1024:.2f} MB)...")
    
    try:
        with open(FILE_PATH, 'rb') as f:
            start_time = time.time()
            response = requests.post(f"{API_URL}/upload", files={'file': f})
            upload_time = time.time() - start_time
            
        if response.status_code != 200:
            print(f"Upload failed: {response.text}")
            return

        data = response.json()
        task_id = data['task_id']
        print(f"Upload complete in {upload_time:.2f}s. Task ID: {task_id}")
        
        # Poll progress
        print("Polling progress...")
        for i in range(10):
            time.sleep(2)
            progress_response = requests.get(f"{API_URL}/progress/{task_id}")
            if progress_response.status_code == 200:
                # The endpoint returns a stream format "data: {...}\n\n" usually, 
                # but let's see if we can parse it or if it's a simple JSON endpoint.
                # Wait, the progress endpoint is SSE (Server-Sent Events).
                # Requests won't parse SSE easily with .json().
                # We need to read the text.
                
                content = progress_response.text
                print(f"Time {i*2}s: {content.strip()}")
                
                if "100%" in content or "complete" in content:
                    print("Processing complete!")
                    break
            else:
                print(f"Error getting progress: {progress_response.status_code}")
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    verify_upload_speed()
