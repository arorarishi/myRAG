from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import document
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class DocumentResponse(BaseModel):
    id: int
    filename: str
    upload_date: datetime
    num_chunks: int
    status: str
    error_message: str = None

    class Config:
        from_attributes = True

@router.get("/documents", response_model=List[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    """Get list of all uploaded documents"""
    documents = db.query(document.Document).order_by(
        document.Document.upload_date.desc()
    ).all()
    return documents

@router.delete("/documents/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document and its vectors"""
    doc = db.query(document.Document).filter(
        document.Document.id == document_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Delete vectors from FAISS store (using default FAISS setup)
        from app.services.vector_stores.faiss_store import FAISSVectorStore
        
        # Try to delete from vector store (best effort - may fail if store not initialized)
        try:
            vector_store = FAISSVectorStore(dimension=768)  # Default dimension
            await vector_store.delete_by_document(str(document_id))
        except Exception as vs_error:
            # Log but don't fail if vector store cleanup fails
            print(f"Warning: Could not delete vectors: {vs_error}")
        
        # Delete document from database
        db.delete(doc)
        db.commit()
        
        return {"message": "Document deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")
