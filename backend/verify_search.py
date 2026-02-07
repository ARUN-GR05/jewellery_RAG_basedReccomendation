import requests
import time

url = "http://127.0.0.1:8000/search"
data = {"query": "heart ring", "top_k": 5}

start_time = time.time()
try:
    response = requests.post(url, data=data)
    end_time = time.time()
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        print(f"Status: {response.status_code}")
        print(f"Time: {end_time - start_time:.4f} seconds")
        print(f"Results found: {len(results)}")
        for i, res in enumerate(results):
             print(f"{i+1}. Score: {res.get('score')} | Caption: {res.get('caption')}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Request failed: {e}")
