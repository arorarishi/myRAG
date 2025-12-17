#!/bin/bash
# Copy RAG Framework to Pendrive (Mac/Linux)
# Usage: ./copy_to_pendrive.sh /Volumes/PENDRIVE/myRAG

if [ -z "$1" ]; then
    echo "Usage: ./copy_to_pendrive.sh [PENDRIVE_PATH]"
    echo "Example: ./copy_to_pendrive.sh /Volumes/PENDRIVE/myRAG"
    exit 1
fi

DEST="$1"

echo "======================================"
echo "  Copying RAG Framework to Pendrive"
echo "======================================"
echo ""
echo "Destination: $DEST"
echo ""

# Create destination directory
mkdir -p "$DEST"

echo "Copying project files..."
echo ""

# Copy backend (excluding venv and database files)
echo "[1/5] Copying backend code..."
mkdir -p "$DEST/backend"
cp -r backend/app "$DEST/backend/"
cp backend/requirements.txt "$DEST/backend/" 2>/dev/null

# Copy frontend (excluding node_modules)
echo "[2/5] Copying frontend code..."
mkdir -p "$DEST/frontend"
cp -r frontend/src "$DEST/frontend/"
cp -r frontend/public "$DEST/frontend/" 2>/dev/null
cp frontend/package.json "$DEST/frontend/" 2>/dev/null
cp frontend/vite.config.js "$DEST/frontend/" 2>/dev/null
cp frontend/index.html "$DEST/frontend/" 2>/dev/null

# Copy root files
echo "[3/5] Copying startup scripts..."
cp start_backend.bat "$DEST/" 2>/dev/null
cp start_backend.sh "$DEST/" 2>/dev/null
cp start_frontend.bat "$DEST/" 2>/dev/null
cp start_frontend.sh "$DEST/" 2>/dev/null
chmod +x "$DEST/start_backend.sh" "$DEST/start_frontend.sh" 2>/dev/null

echo "[4/5] Copying documentation..."
cp README.md "$DEST/" 2>/dev/null
cp .gitignore "$DEST/" 2>/dev/null

echo "[5/5] Creating setup instructions..."
cat > "$DEST/SETUP_INSTRUCTIONS.txt" << 'EOF'
# Setup Instructions After Copying

## 1. Backend Setup
cd backend
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows
pip install -r requirements.txt

## 2. Frontend Setup
cd frontend
npm install

## 3. Run the application
Use start_backend.sh and start_frontend.sh (Mac/Linux)
Or start_backend.bat and start_frontend.bat (Windows)
EOF

echo ""
echo "======================================"
echo "  Copy Complete!"
echo "======================================"
echo ""
echo "Files copied to: $DEST"
echo ""
echo "IMPORTANT: On the new machine, you need to:"
echo "1. Install Python 3.11+ and Node.js 18+"
echo "2. Run backend setup: cd backend, create venv, pip install -r requirements.txt"
echo "3. Run frontend setup: cd frontend, npm install"
echo "4. See SETUP_INSTRUCTIONS.txt in the destination folder"
echo ""
