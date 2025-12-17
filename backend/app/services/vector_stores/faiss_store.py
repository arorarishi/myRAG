from app.providers.base import VectorStore
from typing import List, Dict, Any
import faiss
import numpy as np
import pickle
import os

class FAISSVectorStore(VectorStore):
    """FAISS vector store with persistence"""
    
    def __init__(self, dimension: int, index_path: str = "faiss_index"):
        """
        Initialize FAISS vector store
        
        Args:
            dimension: Dimension of embedding vectors
            index_path: Path to save/load index
        """
        self.dimension = dimension
        self.index_path = index_path
        self.metadata_path = f"{index_path}_metadata.pkl"
        
        # Load or create index
        if os.path.exists(f"{index_path}.index"):
            self.index = faiss.read_index(f"{index_path}.index")
            with open(self.metadata_path, 'rb') as f:
                self.metadata_store = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(dimension)
            self.metadata_store = {}
    
    async def add_vectors(
        self,
        vectors: List[List[float]],
        metadata: List[Dict[str, Any]],
        ids: List[str]
    ) -> None:
        """Add vectors with metadata to FAISS"""
        # Convert to numpy array
        vectors_np = np.array(vectors).astype('float32')
        
        # Get starting index
        start_idx = self.index.ntotal
        
        # Add to FAISS
        self.index.add(vectors_np)
        
        # Store metadata
        for i, (id_, meta) in enumerate(zip(ids, metadata)):
            self.metadata_store[start_idx + i] = {
                "id": id_,
                **meta
            }
        
        # Save to disk
        self._save()
    
    async def search(
        self,
        query_vector: List[float],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        # Convert to numpy
        query_np = np.array([query_vector]).astype('float32')
        
        # Search
        distances, indices = self.index.search(query_np, top_k)
        
        # Build results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx in self.metadata_store:
                result = self.metadata_store[idx].copy()
                result["score"] = float(dist)
                results.append(result)
        
        return results
    
    async def delete_by_document(self, document_id: str) -> None:
        """Delete all vectors for a document (requires rebuild for FAISS)"""
        # FAISS doesn't support deletion, would need to rebuild index
        # For now, just remove from metadata
        indices_to_remove = [
            idx for idx, meta in self.metadata_store.items()
            if meta.get("document_id") == document_id
        ]
        for idx in indices_to_remove:
            del self.metadata_store[idx]
        self._save()
    
    def _save(self):
        """Save index and metadata to disk"""
        faiss.write_index(self.index, f"{self.index_path}.index")
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata_store, f)
