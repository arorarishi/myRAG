from app.providers.base import EmbeddingProvider
from typing import List

class HuggingFaceEmbeddingProvider(EmbeddingProvider):
    """HuggingFace local embedding provider - STUB for future implementation"""
    
    def __init__(self, model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = model
        raise NotImplementedError("HuggingFace provider not yet implemented")
    
    async def embed_text(self, text: str) -> List[float]:
        raise NotImplementedError()
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError()
    
    def get_dimension(self) -> int:
        return 384
