from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import hashlib
import traceback

from app.database.database import get_db
from app.services.pdf_parser import parse_pdf
from app.services.chunker import TextChunker
from app.providers.factory import get_embedding_provider, get_vector_store
from app.models import configuration, document

router = APIRouter()

async def get_config_value(db: Session, key: str) -> str:
    """Helper to get a config value from database"""
    config_item = db.query(configuration.ConfigurationItem).filter(
        configuration.ConfigurationItem.config_name == key,
        configuration.ConfigurationItem.is_active == True
    ).first()
    return config_item.config_value if config_item else None

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload and process a document:
    1. Parse PDF
    2. Chunk text
    3. Generate embeddings
    4. Store in vector database
    5. Track metadata
    """
    try:
        # Read file content
        content = await file.read()
        file_hash = hashlib.sha256(content).hexdigest()
        
        # Check if document already exists
        existing_doc = db.query(document.Document).filter(
            document.Document.file_hash == file_hash
        ).first()
        
        if existing_doc:
            return {
                "message": "Document already indexed",
                "document_id": existing_doc.id,
                "filename": existing_doc.filename
            }
        
        # Create document record
        doc_record = document.Document(
            filename=file.filename,
            file_hash=file_hash,
            status="processing"
        )
        db.add(doc_record)
        db.commit()
        db.refresh(doc_record)
        
        try:
            # Parse PDF
            parsed_content = parse_pdf(content)
            
            # Chunk text
            chunker = TextChunker()
            chunks = chunker.chunk_with_metadata(parsed_content, file.filename)
            
            # Get configuration
            embedding_provider_name = await get_config_value(db, "embedding_provider") or "OpenAI"
            embedding_model = await get_config_value(db, "embedding_model") or "text-embedding-3-small"
            embedding_api_key = await get_config_value(db, "embedding_api_key")
            vector_store_type = await get_config_value(db, "vector_store") or "faiss"
            pgvector_url = await get_config_value(db, "pgvector_url")
            
            if not embedding_api_key and embedding_provider_name == "OpenAI":
                raise HTTPException(
                    status_code=400,
                    detail="OpenAI API key not configured. Please configure in Settings."
                )
            
            # Initialize provider and vector store
            embedding_provider = get_embedding_provider(
                provider_name=embedding_provider_name,
                api_key=embedding_api_key,
                model=embedding_model
            )
            
            dimension = embedding_provider.get_dimension()
            vector_store = get_vector_store(
                store_type=vector_store_type,
                dimension=dimension,
                connection_string=pgvector_url
            )
            
            # Generate embeddings
            chunk_texts = [chunk["text"] for chunk in chunks]
            embeddings = await embedding_provider.embed_batch(chunk_texts)
            
            # Prepare metadata
            metadata_list = [
                {
                    "document_id": str(doc_record.id),
                    "document_name": file.filename,
                    "chunk_index": chunk["chunk_index"],
                    "text": chunk["text"]
                }
                for chunk in chunks
            ]
            
            # Generate IDs
            ids = [f"{doc_record.id}_{i}" for i in range(len(chunks))]
            
            # Store in vector database
            await vector_store.add_vectors(embeddings, metadata_list, ids)
            
            # Update document record
            doc_record.num_chunks = len(chunks)
            doc_record.status = "completed"
            db.commit()
            
            return {
                "message": "Document processed successfully",
                "document_id": doc_record.id,
                "filename": file.filename,
                "num_chunks": len(chunks),
                "embedding_provider": embedding_provider_name,
                "embedding_model": embedding_model,
                "vector_store": vector_store_type
            }
            
        except Exception as e:
            # Update document status to failed
            doc_record.status = "failed"
            doc_record.error_message = str(e)
            db.commit()
            raise
            
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
