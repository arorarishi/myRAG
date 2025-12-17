from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.database import engine, Base
from app.models import configuration, document

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

from app.api import ingest, config, documents
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])
app.include_router(config.router, prefix="/api/v1", tags=["config"])
app.include_router(documents.router, prefix="/api/v1", tags=["documents"])

@app.get("/")
def root():
    return {"message": "Welcome to the RAG Framework API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
