@echo off
REM Start Frontend Server for RAG Framework

echo.
echo ======================================
echo   Starting RAG Framework Frontend
echo ======================================
echo.

cd /d "%~dp0frontend"

echo.
echo Starting Vite dev server on http://localhost:5173
echo Press Ctrl+C to stop the server
echo.

npm run dev
