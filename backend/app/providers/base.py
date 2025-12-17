from abc import ABC, abstractmethod
from typing import List, Dict, Any

class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers"""
    
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as list of floats
        """
        pass
    
    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by this provider
        
        Returns:
            Embedding dimension
        """
        pass


class VectorStore(ABC):
    """Abstract base class for vector stores"""
    
    @abstractmethod
    async def add_vectors(
        self,
        vectors: List[List[float]],
        metadata: List[Dict[str, Any]],
        ids: List[str]
    ) -> None:
        """
        Add vectors with metadata to the store
        
        Args:
            vectors: List of embedding vectors
            metadata: List of metadata dictionaries
            ids: List of unique IDs for each vector
        """
        pass
    
    @abstractmethod
    async def search(
        self,
        query_vector: List[float],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of results with metadata and scores
        """
        pass
    
    @abstractmethod
    async def delete_by_document(self, document_id: str) -> None:
        """
        Delete all vectors associated with a document
        
        Args:
            document_id: Document identifier
        """
        pass


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text completion
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text
        """
        pass
