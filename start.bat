@echo off
REM ============================================================================
REM PassiveData - Script de Inicio para Windows
REM ============================================================================

echo.
echo ================================================
echo   PassiveData - Iniciando Aplicacion
echo ================================================
echo.

REM Verificar que el entorno virtual existe
if not exist venv (
    echo [ERROR] No se encontro el entorno virtual de Python
    echo Por favor ejecuta setup.bat primero
    pause
    exit /b 1
)

REM Verificar que las dependencias de Node están instaladas
if not exist frontend\node_modules (
    echo [ERROR] No se encontraron las dependencias de Node.js
    echo Por favor ejecuta setup.bat primero
    pause
    exit /b 1
)

REM Verificar que el archivo .env existe
if not exist .env (
    echo [ERROR] No se encontro el archivo .env
    echo Por favor copia .env.example a .env y configuralo
    pause
    exit /b 1
)

echo Iniciando servicios...
echo.
echo Backend estara disponible en: http://localhost:8000
echo Frontend estara disponible en: http://localhost:3000
echo API Docs en: http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener ambos servicios
echo.
echo ================================================
echo.

REM Crear un archivo temporal para los comandos
echo @echo off > %TEMP%\start_backend.bat
echo cd /d "%CD%" >> %TEMP%\start_backend.bat
echo call venv\Scripts\activate.bat >> %TEMP%\start_backend.bat
echo title PassiveData - Backend (FastAPI) >> %TEMP%\start_backend.bat
echo echo. >> %TEMP%\start_backend.bat
echo echo ================================================ >> %TEMP%\start_backend.bat
echo echo   Backend (FastAPI) Iniciando... >> %TEMP%\start_backend.bat
echo echo ================================================ >> %TEMP%\start_backend.bat
echo echo. >> %TEMP%\start_backend.bat
echo cd backend >> %TEMP%\start_backend.bat
echo uvicorn main:app --reload --host 0.0.0.0 --port 8000 >> %TEMP%\start_backend.bat

echo @echo off > %TEMP%\start_frontend.bat
echo cd /d "%CD%\frontend" >> %TEMP%\start_frontend.bat
echo title PassiveData - Frontend (React) >> %TEMP%\start_frontend.bat
echo echo. >> %TEMP%\start_frontend.bat
echo echo ================================================ >> %TEMP%\start_frontend.bat
echo echo   Frontend (React) Iniciando... >> %TEMP%\start_frontend.bat
echo echo ================================================ >> %TEMP%\start_frontend.bat
echo echo. >> %TEMP%\start_frontend.bat
echo set BROWSER=none >> %TEMP%\start_frontend.bat
echo npm start >> %TEMP%\start_frontend.bat

REM Iniciar backend en una nueva ventana
start "PassiveData - Backend" cmd /k %TEMP%\start_backend.bat

REM Esperar 3 segundos para que el backend inicie
timeout /t 3 /nobreak >nul

REM Iniciar frontend en una nueva ventana
start "PassiveData - Frontend" cmd /k %TEMP%\start_frontend.bat

REM Esperar 2 segundos
timeout /t 2 /nobreak >nul

echo.
echo ================================================
echo   Servicios Iniciados!
echo ================================================
echo.
echo Se abrieron dos ventanas:
echo   1. Backend (FastAPI) - Puerto 8000
echo   2. Frontend (React) - Puerto 3000
echo.
echo Para detener los servicios:
echo   - Cierra ambas ventanas, o
echo   - Presiona Ctrl+C en cada ventana
echo.
echo Esperando 5 segundos y luego abriendo el navegador...
timeout /t 5 /nobreak >nul

REM Abrir el navegador
start http://localhost:3000

echo.
echo Navegador abierto en http://localhost:3000
echo.
echo Puedes cerrar esta ventana. Los servicios seguiran corriendo.
echo.
pause
