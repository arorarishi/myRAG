from app.providers.base import EmbeddingProvider
from typing import List
import openai

class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embedding provider"""
    
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        """
        Initialize OpenAI embedding provider
        
        Args:
            api_key: OpenAI API key
            model: Model name (text-embedding-3-small, text-embedding-3-large, etc.)
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        
        # Model dimensions
        self.dimensions = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536
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
        return self.dimensions.get(self.model, 1536)
