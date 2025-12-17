@echo off
REM Copy RAG Framework to Pendrive
REM Usage: copy_to_pendrive.bat E:\
REM Where E:\ is your pendrive drive letter

if "%~1"=="" (
    echo Usage: copy_to_pendrive.bat [PENDRIVE_PATH]
    echo Example: copy_to_pendrive.bat E:\myRAG
    exit /b 1
)

set DEST=%~1

echo ======================================
echo   Copying RAG Framework to Pendrive
echo ======================================
echo.
echo Destination: %DEST%
echo.

REM Create destination directory
if not exist "%DEST%" mkdir "%DEST%"

echo Copying project files...
echo.

REM Copy backend (excluding venv and database files)
echo [1/5] Copying backend code...
xcopy /E /I /Y "backend\app" "%DEST%\backend\app"
xcopy /Y "backend\requirements.txt" "%DEST%\backend\" 2>nul

REM Copy frontend (excluding node_modules)
echo [2/5] Copying frontend code...
xcopy /E /I /Y "frontend\src" "%DEST%\frontend\src"
xcopy /E /I /Y "frontend\public" "%DEST%\frontend\public" 2>nul
xcopy /Y "frontend\package.json" "%DEST%\frontend\" 2>nul
xcopy /Y "frontend\vite.config.js" "%DEST%\frontend\" 2>nul
xcopy /Y "frontend\index.html" "%DEST%\frontend\" 2>nul

REM Copy root files
echo [3/5] Copying startup scripts...
xcopy /Y "start_backend.bat" "%DEST%\" 2>nul
xcopy /Y "start_backend.sh" "%DEST%\" 2>nul
xcopy /Y "start_frontend.bat" "%DEST%\" 2>nul
xcopy /Y "start_frontend.sh" "%DEST%\" 2>nul

echo [4/5] Copying documentation...
xcopy /Y "README.md" "%DEST%\" 2>nul
xcopy /Y ".gitignore" "%DEST%\" 2>nul

echo [5/5] Creating setup instructions...
(
echo # Setup Instructions After Copying
echo.
echo ## 1. Backend Setup
echo cd backend
echo python -m venv venv
echo venv\Scripts\activate  # Windows
echo # source venv/bin/activate  # Mac/Linux
echo pip install -r requirements.txt
echo.
echo ## 2. Frontend Setup
echo cd frontend
echo npm install
echo.
echo ## 3. Run the application
echo Use start_backend.bat and start_frontend.bat ^(Windows^)
echo Or start_backend.sh and start_frontend.sh ^(Mac/Linux^)
) > "%DEST%\SETUP_INSTRUCTIONS.txt"

echo.
echo ======================================
echo   Copy Complete!
echo ======================================
echo.
echo Files copied to: %DEST%
echo.
echo IMPORTANT: On the new machine, you need to:
echo 1. Install Python 3.11+ and Node.js 18+
echo 2. Run backend setup: cd backend, create venv, pip install -r requirements.txt
echo 3. Run frontend setup: cd frontend, npm install
echo 4. See SETUP_INSTRUCTIONS.txt in the destination folder
echo.
pause
