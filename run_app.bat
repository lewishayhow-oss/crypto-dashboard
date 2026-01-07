@echo off
echo Starting CryptoDashboard...
echo.
echo Make sure you have installed dependencies first!
echo (pip install -r requirements.txt)
echo (cd market-stream/frontend && npm install)
echo.
echo Starting Engine, API, and Frontend...

npx concurrently -k -n "ENGINE,API,UI" -c "blue,magenta,green" ^
  "venv\Scripts\python market-stream/data-engine/server.py" ^
  "venv\Scripts\python market-stream/api-gateway/app.py" ^
  "npm run dev --prefix market-stream/frontend"

pause
