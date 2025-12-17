"""
Quick script to update configuration to use DeepInfra for embeddings
"""
import requests
import json

API_URL = "http://localhost:8000/api/v1/config"

# Get current configuration
print("Fetching current configuration...")
response = requests.get(API_URL)
current_config = response.json()

print("\nCurrent configuration:")
print(json.dumps(current_config, indent=2))

# Update to use DeepInfra
print("\n" + "="*50)
print("Updating to use DeepInfra...")
print("="*50)

# Get the API key from current config
api_key = current_config['configs'].get('embedding_api_key', '')

new_config = {
    "configs": {
        "database": current_config['configs'].get('database', 'sqlite'),
        "vector_store": current_config['configs'].get('vector_store', 'faiss'),
        "embedding_provider": "DeepInfra",
        "embedding_model": "BAAI/bge-base-en-v1.5",
        "embedding_api_key": api_key if api_key else input("Enter your DeepInfra API key: "),
        "reranking_provider": current_config['configs'].get('reranking_provider'),
        "reranking_model": current_config['configs'].get('reranking_model'),
        "reranking_api_key": current_config['configs'].get('reranking_api_key'),
        "llm_provider": current_config['configs'].get('llm_provider'),
        "llm_model": current_config['configs'].get('llm_model'),
        "llm_api_key": current_config['configs'].get('llm_api_key'),
    }
}

# Save configuration
response = requests.post(API_URL, json=new_config)

if response.status_code == 200:
    print("\n✅ Configuration updated successfully!")
    print("\nNew configuration:")
    print(json.dumps(response.json(), indent=2))
    print("\n✅ You can now upload documents using DeepInfra embeddings!")
else:
    print(f"\n❌ Error updating configuration: {response.status_code}")
    print(response.text)
