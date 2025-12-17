from app.providers.base import EmbeddingProvider, VectorStore
from app.providers.embedding.openai_provider import OpenAIEmbeddingProvider
from app.providers.embedding.cohere_provider import CohereEmbeddingProvider
from app.providers.embedding.huggingface_provider import HuggingFaceEmbeddingProvider
from app.providers.embedding.deepinfra_provider import DeepInfraEmbeddingProvider
from app.providers.embedding.voyage_provider import VoyageEmbeddingProvider
from app.services.vector_stores.faiss_store import FAISSVectorStore
from app.services.vector_stores.pgvector_store import PGVectorStore

def get_embedding_provider(provider_name: str, api_key: str, model: str) -> EmbeddingProvider:
    """
    Factory function to get embedding provider based on configuration
    
    Args:
        provider_name: Name of provider (OpenAI, Cohere, etc.)
        api_key: API key (if required)
        model: Model name
        
    Returns:
        EmbeddingProvider instance
    """
    if provider_name == "OpenAI":
        return OpenAIEmbeddingProvider(api_key=api_key, model=model)
    elif provider_name == "Cohere":
        return CohereEmbeddingProvider(api_key=api_key, model=model)
    elif provider_name == "HuggingFace":
        return HuggingFaceEmbeddingProvider(model=model)
    elif provider_name == "DeepInfra":
        return DeepInfraEmbeddingProvider(api_key=api_key, model=model)
    elif provider_name == "Voyage AI":
        return VoyageEmbeddingProvider(api_key=api_key, model=model)
    else:
        raise ValueError(f"Unknown embedding provider: {provider_name}")

def get_vector_store(store_type: str, dimension: int, connection_string: str = None) -> VectorStore:
    """
    Factory function to get vector store based on configuration
    
    Args:
        store_type: Type of store (faiss, pgvector)
        dimension: Embedding dimension
        connection_string: Connection string for database stores
        
    Returns:
        VectorStore instance
    """
    if store_type == "faiss":
        return FAISSVectorStore(dimension=dimension)
    elif store_type == "pgvector":
        if not connection_string:
            raise ValueError("Connection string required for pgvector")
        return PGVectorStore(connection_string=connection_string)
    else:
        raise ValueError(f"Unknown vector store type: {store_type}")
