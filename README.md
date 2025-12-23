# RAG Framework

A full-stack RAG (Retrieval-Augmented Generation) application with document indexing, vector search, and chat interface.

## Features

- 📄 PDF document upload and processing
- 🔍 Semantic search using embeddings (OpenAI, DeepInfra, Cohere, Voyage AI, HuggingFace)
- 💬 Chat interface with context-aware responses
- 🗂️ Multiple vector store support (FAISS, pgvector)
- ⚙️ Configurable embedding and LLM providers
- 📊 Document management with status tracking

## UI Screens 
#### Screen 1 - Chat Window
<img width="1740" height="851" alt="image" src="https://github.com/user-attachments/assets/8edaa13b-de34-4f1c-a321-6adf8d7eb9e4" />
#### Screen 2 - Document Upload 
<img width="1695" height="871" alt="image" src="https://github.com/user-attachments/assets/2d9e8ff2-99e7-40d5-a1b3-03c747c36589" />
#### Screen 3 - Settings to Selct Model of You Ch0ice
<img width="1920" height="1832" alt="RAG_Settings" src="https://github.com/user-attachments/assets/52cca639-47f8-4b71-bfa1-d3c163c90643" />

## Tech Stack

**Backend:**
- FastAPI (Python)
- SQLAlchemy + SQLite
- FAISS / pgvector
- Multiple LLM providers (OpenAI, DeepInfra, etc.)

**Frontend:**
- React + Vite
- Axios for API calls
- Modern responsive UI

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. The database will be created automatically on first run.

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start Backend

**Windows:**
```bash
.\start_backend.bat
```

**Mac/Linux:**
```bash
chmod +x start_backend.sh  # First time only
./start_backend.sh
```

Backend will run on: http://localhost:8000

### Start Frontend

**Windows:**
```bash
.\start_frontend.bat
```

**Mac/Linux:**
```bash
chmod +x start_frontend.sh  # First time only
./start_frontend.sh
```

Frontend will run on: http://localhost:5173

## Configuration

1. Open the application at http://localhost:5173
2. Navigate to the **Settings** tab
3. Configure:
   - **Database**: SQLite (default) or PostgreSQL
   - **Vector Store**: FAISS (default) or pgvector
   - **Embedding Provider**: OpenAI, DeepInfra, Cohere, Voyage AI, or HuggingFace
   - **Embedding Model**: Model name for your chosen provider
   - **API Keys**: Enter your API keys for the chosen providers
   - **LLM Provider**: OpenAI or DeepInfra
   - **LLM Model**: Model name for chat responses

4. Click **Save Configuration**

## Usage

### Upload Documents

1. Go to the **Documents** tab
2. Click **Choose PDF File** and select a PDF
3. Click **Upload & Index**
4. Wait for processing to complete

### Chat with Documents

1. Go to the **Chat** tab
2. Ask questions about your uploaded documents
3. The system will retrieve relevant context and generate responses

## API Endpoints

- `GET /api/v1/documents` - List all documents
- `POST /api/v1/ingest` - Upload and index a document
- `DELETE /api/v1/documents/{id}` - Delete a document
- `GET /api/v1/config` - Get configuration
- `POST /api/v1/config` - Save configuration
- `GET /health` - Health check

## Project Structure

```
myRAG/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core configuration
│   │   ├── database/      # Database setup
│   │   ├── models/        # SQLAlchemy models
│   │   ├── providers/     # Embedding & LLM providers
│   │   └── services/      # Business logic
│   ├── venv/              # Virtual environment
│   └── main.py            # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── contexts/      # React contexts
│   │   └── services/      # API services
│   └── package.json
├── .gitignore
├── README.md
├── start_backend.bat      # Windows backend startup
├── start_backend.sh       # Mac/Linux backend startup
├── start_frontend.bat     # Windows frontend startup
└── start_frontend.sh      # Mac/Linux frontend startup
```

## Supported Embedding Providers

- **OpenAI**: text-embedding-3-small, text-embedding-3-large
- **DeepInfra**: BAAI/bge-base-en-v1.5, BAAI/bge-large-en-v1.5
- **Cohere**: embed-english-v3.0, embed-multilingual-v3.0
- **Voyage AI**: voyage-2, voyage-large-2
- **HuggingFace**: sentence-transformers models

## Troubleshooting

**Backend won't start:**
- Ensure Python 3.11+ is installed
- Check that virtual environment is activated
- Verify all dependencies are installed

**Frontend won't start:**
- Ensure Node.js 18+ is installed
- Run `npm install` in frontend directory
- Check for port conflicts on 5173

**Upload fails:**
- Verify embedding provider API key is configured
- Check backend logs for detailed error messages
- Ensure PDF is valid and readable

**"Document already indexed" error:**
- Documents are deduplicated by content hash
- Delete the existing document first to re-upload

## License

MIT
