from app.providers.base import EmbeddingProvider
from typing import List
import openai

class DeepInfraEmbeddingProvider(EmbeddingProvider):
    """DeepInfra embedding provider using OpenAI-compatible API"""
    
    def __init__(self, api_key: str, model: str = "BAAI/bge-base-en-v1.5"):
        """
        Initialize DeepInfra embedding provider
        
        Args:
            api_key: DeepInfra API key
            model: Model name (BAAI/bge-base-en-v1.5, sentence-transformers/all-MiniLM-L6-v2, etc.)
        """
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepinfra.com/v1/openai"
        )
        self.model = model
        
        # Model dimensions (approximate)
        self.dimensions = {
            "BAAI/bge-base-en-v1.5": 768,
            "sentence-transformers/all-MiniLM-L6-v2": 384,
            "BAAI/bge-large-en-v1.5": 1024,
            "BAAI/bge-small-en-v1.5": 384
        }
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self.dimensions.get(self.model, 768)
