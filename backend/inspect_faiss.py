"""
Script to access and inspect FAISS index
"""
import sys
sys.path.insert(0, '.')

from app.services.vector_stores.faiss_store import FAISSVectorStore

# Initialize FAISS store (it will load existing index if it exists)
print("Loading FAISS index...")
vector_store = FAISSVectorStore(dimension=768)

print(f"\nFAISS Index Info:")
print(f"- Total vectors: {vector_store.index.ntotal}")
print(f"- Dimension: {vector_store.dimension}")
print(f"- Metadata entries: {len(vector_store.metadata_store)}")

if vector_store.metadata_store:
    print("\n=== Metadata Entries ===")
    for idx, meta in list(vector_store.metadata_store.items())[:10]:  # Show first 10
        doc_id = meta.get('document_id', 'N/A')
        doc_name = meta.get('document_name', 'N/A')
        chunk_idx = meta.get('chunk_index', 'N/A')
        print(f"  Index {idx}: Doc ID={doc_id}, Name={doc_name}, Chunk={chunk_idx}")
    
    if len(vector_store.metadata_store) > 10:
        print(f"  ... and {len(vector_store.metadata_store) - 10} more")
    
    # Group by document
    docs = {}
    for meta in vector_store.metadata_store.values():
        doc_id = meta.get('document_id')
        if doc_id:
            docs[doc_id] = docs.get(doc_id, 0) + 1
    
    print(f"\n=== Documents in FAISS ===")
    for doc_id, count in docs.items():
        print(f"  Document ID {doc_id}: {count} chunks")
else:
    print("\n✗ FAISS index is empty")
