from app.providers.base import EmbeddingProvider
from typing import List

class CohereEmbeddingProvider(EmbeddingProvider):
    """Cohere embedding provider - STUB for future implementation"""
    
    def __init__(self, api_key: str, model: str = "embed-english-v3.0"):
        self.api_key = api_key
        self.model = model
        raise NotImplementedError("Cohere provider not yet implemented")
    
    async def embed_text(self, text: str) -> List[float]:
        raise NotImplementedError()
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError()
    
    def get_dimension(self) -> int:
        return 1024
