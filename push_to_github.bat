@echo off
echo Pushing to GitHub: https://github.com/arorarishi/myRAG.git
echo.
echo You'll be prompted for credentials:
echo Username: arorarishi
echo Password: Use a Personal Access Token (NOT your GitHub password)
echo.
echo Get a token from: https://github.com/settings/tokens
echo.
pause

git push -u origin main

echo.
echo Done! Check your repository at:
echo https://github.com/arorarishi/myRAG
pause
