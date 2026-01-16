@echo off
REM ============================================================================
REM PassiveData - Script para Detener Servicios (Windows)
REM ============================================================================

echo.
echo ================================================
echo   PassiveData - Deteniendo Servicios
echo ================================================
echo.

echo Buscando procesos de PassiveData...
echo.

REM Buscar y matar procesos de uvicorn (Backend)
echo [1/2] Deteniendo Backend (uvicorn)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Deteniendo proceso con PID %%a
    taskkill /F /PID %%a >nul 2>&1
)
echo [OK] Backend detenido

REM Buscar y matar procesos de Node (Frontend)
echo.
echo [2/2] Deteniendo Frontend (Node.js)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
    echo Deteniendo proceso con PID %%a
    taskkill /F /PID %%a >nul 2>&1
)
echo [OK] Frontend detenido

echo.
echo ================================================
echo   Servicios Detenidos
echo ================================================
echo.
pause
