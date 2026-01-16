@echo off
REM ============================================================================
REM PassiveData - Script de Configuración para Windows
REM ============================================================================

echo.
echo ================================================
echo   PassiveData - Configuracion Inicial
echo ================================================
echo.

REM Verificar si Python está instalado
echo [1/6] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.9+ desde https://www.python.org/downloads/
    echo IMPORTANTE: Marca la opcion "Add Python to PATH" durante la instalacion
    pause
    exit /b 1
)
python --version
echo [OK] Python encontrado

REM Verificar si Node.js está instalado
echo.
echo [2/6] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js no esta instalado o no esta en el PATH
    echo Por favor instala Node.js 16+ desde https://nodejs.org/
    pause
    exit /b 1
)
node --version
echo [OK] Node.js encontrado

REM Crear entorno virtual de Python
echo.
echo [3/6] Creando entorno virtual de Python...
if exist venv (
    echo Entorno virtual ya existe, omitiendo creacion...
) else (
    python -m venv venv
    echo [OK] Entorno virtual creado
)

REM Activar entorno virtual e instalar dependencias
echo.
echo [4/6] Instalando dependencias de Python...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Error al instalar dependencias de Python
    pause
    exit /b 1
)
echo [OK] Dependencias de Python instaladas

REM Instalar dependencias de Node.js
echo.
echo [5/6] Instalando dependencias de Node.js...
cd frontend
call npm install
if errorlevel 1 (
    echo [ERROR] Error al instalar dependencias de Node.js
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] Dependencias de Node.js instaladas

REM Crear archivo .env si no existe
echo.
echo [6/6] Configurando archivo de entorno...
if exist .env (
    echo Archivo .env ya existe, omitiendo...
) else (
    copy .env.example .env
    echo [OK] Archivo .env creado desde .env.example
    echo.
    echo ============================================================
    echo   IMPORTANTE: Configura tus credenciales de Azure
    echo ============================================================
    echo.
    echo Edita el archivo .env con tus credenciales:
    echo   - MICROSOFT_CLIENT_ID
    echo   - MICROSOFT_CLIENT_SECRET
    echo   - MICROSOFT_TENANT_ID
    echo.
    echo Ver AZURE_SETUP_ES.md para instrucciones detalladas
    echo ============================================================
)

REM Inicializar base de datos
echo.
echo [Extra] Inicializando base de datos...
call venv\Scripts\activate.bat
python -c "from backend.src.core.database import init_db; init_db()"
if errorlevel 1 (
    echo [ADVERTENCIA] No se pudo inicializar la base de datos
    echo Esto es normal si es la primera vez. Se creara al iniciar.
)

echo.
echo ================================================
echo   Configuracion Completada!
echo ================================================
echo.
echo Proximos pasos:
echo   1. Edita el archivo .env con tus credenciales de Azure
echo   2. Ejecuta start.bat para iniciar la aplicacion
echo.
echo Para mas informacion, consulta:
echo   - README.md
echo   - AZURE_SETUP_ES.md (configuracion de Azure)
echo   - WINDOWS_SETUP.md (instrucciones para Windows)
echo.
pause
