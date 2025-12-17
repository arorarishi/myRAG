#!/bin/bash
# Start Frontend Server for RAG Framework

echo ""
echo "======================================"
echo "  Starting RAG Framework Frontend"
echo "======================================"
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

echo "Starting Vite dev server on http://localhost:5173"
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev
