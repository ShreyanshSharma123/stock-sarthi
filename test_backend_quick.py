import requests
import time

print("Testing backend...")
try:
    r = requests.get('http://localhost:8000/health', timeout=3)
    print(f"✅ Backend responding: {r.status_code}")
    print(r.text)
except Exception as e:
    print(f"❌ Backend not responding: {e}")
