import asyncio
import os
from app.providers.embedding.deepinfra_provider import DeepInfraEmbeddingProvider

async def test_deepinfra():
    """Test DeepInfra embedding provider"""
    
    # You'll need to set your DeepInfra API key
    api_key = os.getenv("DEEPINFRA_API_KEY", "YOUR_API_KEY_HERE")
    
    if api_key == "YOUR_API_KEY_HERE":
        print("❌ Please set DEEPINFRA_API_KEY environment variable or edit this file")
        return
    
    print("=" * 60)
    print("Testing DeepInfra Embedding Provider")
    print("=" * 60)
    
    try:
        # Initialize provider
        provider = DeepInfraEmbeddingProvider(
            api_key=api_key,
            model="BAAI/bge-base-en-v1.5"
        )
        
        print(f"\n✓ Provider initialized")
        print(f"  Model: {provider.model}")
        print(f"  Dimension: {provider.get_dimension()}")
        
        # Test single embedding
        print("\n1. Testing single text embedding...")
        text = "This is a test document about machine learning and AI."
        embedding = await provider.embed_text(text)
        print(f"   ✓ Generated embedding")
        print(f"   Dimension: {len(embedding)}")
        print(f"   First 5 values: {embedding[:5]}")
        
        # Test batch embedding
        print("\n2. Testing batch embeddings...")
        texts = [
            "Machine learning is a subset of artificial intelligence.",
            "Deep learning uses neural networks with multiple layers.",
            "Natural language processing enables computers to understand text."
        ]
        embeddings = await provider.embed_batch(texts)
        print(f"   ✓ Generated {len(embeddings)} embeddings")
        for i, emb in enumerate(embeddings):
            print(f"   Text {i+1}: dimension = {len(emb)}")
        
        print("\n" + "=" * 60)
        print("✅ All tests passed! DeepInfra provider is working.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_deepinfra())
