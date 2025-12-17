from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

class TextChunker:
    """Service for chunking text documents into semantic pieces"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize text chunker
        
        Args:
            chunk_size: Maximum characters per chunk
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        return self.splitter.split_text(text)
    
    def chunk_with_metadata(self, text: str, document_name: str) -> List[dict]:
        """
        Split text into chunks with metadata
        
        Args:
            text: Input text to chunk
            document_name: Name of the source document
            
        Returns:
            List of dictionaries with chunk text and metadata
        """
        chunks = self.chunk_text(text)
        return [
            {
                "text": chunk,
                "document_name": document_name,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            for i, chunk in enumerate(chunks)
        ]
