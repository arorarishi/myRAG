import requests
import json

url = "http://localhost:8000/api/v1/config"

# Test data in new format
config_data = {
    "configs": {
        "database": "sqlite",
        "vector_store": "faiss",
        "embedding_provider": "OpenAI",
        "embedding_model": "text-embedding-3-small",
        "llm_provider": "Anthropic",
        "llm_model": "claude-3-5-haiku-20241022"
    }
}

try:
    print("=" * 50)
    print("Testing NEW Key-Value Configuration System")
    print("=" * 50)
    
    # Test POST
    print("\n1. Testing POST /api/v1/config...")
    response = requests.post(url, json=config_data)
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Success!")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"   ✗ Failed: {response.text}")
    
    # Test GET
    print("\n2. Testing GET /api/v1/config...")
    response = requests.get(url)
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Config loaded successfully!")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"   ✗ Failed: {response.text}")
    
    # Test GET ALL
    print("\n3. Testing GET /api/v1/config/all...")
    response = requests.get(url + "/all")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ All configs retrieved!")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"   ✗ Failed: {response.text}")
        
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("=" * 50)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
