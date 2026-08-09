@echo off
cd /d "%~dp0"

echo Starting Heart Disease ML app...
start "" /B cmd /c python backend\server.py
start "" /B cmd /c python -m http.server 8080 --directory frontend

echo Waiting for services to start...
ping -n 3 127.0.0.1 >nul

start "" http://127.0.0.1:8080/index.html

echo Backend and frontend started.
echo Open http://127.0.0.1:8080/index.html
