#!/bin/bash
# Start Backend Server for RAG Framework

echo ""
echo "======================================"
echo "  Starting RAG Framework Backend"
echo "======================================"
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend"

echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Starting FastAPI server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
