from app.providers.base import EmbeddingProvider
from typing import List

class VoyageEmbeddingProvider(EmbeddingProvider):
    """Voyage AI embedding provider - STUB for future implementation"""
    
    def __init__(self, api_key: str, model: str = "voyage-2"):
        self.api_key = api_key
        self.model = model
        raise NotImplementedError("Voyage AI provider not yet implemented")
    
    async def embed_text(self, text: str) -> List[float]:
        raise NotImplementedError()
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError()
    
    def get_dimension(self) -> int:
        return 1024
