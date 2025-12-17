from app.providers.base import VectorStore
from typing import List, Dict, Any

class PGVectorStore(VectorStore):
    """PostgreSQL pgvector store - STUB for future implementation"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        raise NotImplementedError("pgvector store not yet implemented")
    
    async def add_vectors(
        self,
        vectors: List[List[float]],
        metadata: List[Dict[str, Any]],
        ids: List[str]
    ) -> None:
        raise NotImplementedError()
    
    async def search(
        self,
        query_vector: List[float],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()
    
    async def delete_by_document(self, document_id: str) -> None:
        raise NotImplementedError()
