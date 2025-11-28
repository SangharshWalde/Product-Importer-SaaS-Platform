import requests
import time
import sys

API_URL = "http://localhost:8000/api"
TASK_ID = "e8103212-7d1e-4b86-a137-65127c05d8a9"

def verify_progress():
    print(f"Polling progress for task {TASK_ID}...")
    for i in range(10):
        try:
            progress_response = requests.get(f"{API_URL}/progress/{TASK_ID}")
            if progress_response.status_code == 200:
                content = progress_response.text
                print(f"Time {i*2}s: {content.strip()}")
                
                if "100%" in content or "complete" in content:
                    print("Processing complete!")
                    break
            else:
                print(f"Error getting progress: {progress_response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    verify_progress()
