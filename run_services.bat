@echo off
REM Launches both legacy and modern bank services in separate visible windows.
cd /d %~dp0
start "Legacy Bank :8001" cmd /k "python -m uvicorn services.legacy_bank:app --port 8001 --host 127.0.0.1"
timeout /t 1 /nobreak >nul
start "Modern Bank :8002" cmd /k "python -m uvicorn services.modern_bank:app --port 8002 --host 127.0.0.1"
echo.
echo Both services launching:
echo   Legacy: http://127.0.0.1:8001/docs
echo   Modern: http://127.0.0.1:8002/docs
echo.
