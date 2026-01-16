# ============================================================================
# PassiveData - Script de Configuración para Windows (PowerShell)
# ============================================================================

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  PassiveData - Configuración Inicial" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Python está instalado
Write-Host "[1/6] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host $pythonVersion -ForegroundColor Green
    Write-Host "[OK] Python encontrado" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Por favor instala Python 3.9+ desde https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "IMPORTANTE: Marca la opción 'Add Python to PATH' durante la instalación" -ForegroundColor Red
    pause
    exit 1
}

# Verificar si Node.js está instalado
Write-Host ""
Write-Host "[2/6] Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host $nodeVersion -ForegroundColor Green
    Write-Host "[OK] Node.js encontrado" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Por favor instala Node.js 16+ desde https://nodejs.org/" -ForegroundColor Red
    pause
    exit 1
}

# Crear entorno virtual de Python
Write-Host ""
Write-Host "[3/6] Creando entorno virtual de Python..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Entorno virtual ya existe, omitiendo creación..." -ForegroundColor Gray
} else {
    python -m venv venv
    Write-Host "[OK] Entorno virtual creado" -ForegroundColor Green
}

# Activar entorno virtual e instalar dependencias
Write-Host ""
Write-Host "[4/6] Instalando dependencias de Python..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip | Out-Null
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Error al instalar dependencias de Python" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "[OK] Dependencias de Python instaladas" -ForegroundColor Green

# Instalar dependencias de Node.js
Write-Host ""
Write-Host "[5/6] Instalando dependencias de Node.js..." -ForegroundColor Yellow
Push-Location frontend
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Error al instalar dependencias de Node.js" -ForegroundColor Red
    Pop-Location
    pause
    exit 1
}
Pop-Location
Write-Host "[OK] Dependencias de Node.js instaladas" -ForegroundColor Green

# Crear archivo .env si no existe
Write-Host ""
Write-Host "[6/6] Configurando archivo de entorno..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "Archivo .env ya existe, omitiendo..." -ForegroundColor Gray
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] Archivo .env creado desde .env.example" -ForegroundColor Green
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Yellow
    Write-Host "  IMPORTANTE: Configura tus credenciales de Azure" -ForegroundColor Yellow
    Write-Host "============================================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Edita el archivo .env con tus credenciales:"
    Write-Host "  - MICROSOFT_CLIENT_ID"
    Write-Host "  - MICROSOFT_CLIENT_SECRET"
    Write-Host "  - MICROSOFT_TENANT_ID"
    Write-Host ""
    Write-Host "Ver AZURE_SETUP_ES.md para instrucciones detalladas"
    Write-Host "============================================================" -ForegroundColor Yellow
}

# Inicializar base de datos
Write-Host ""
Write-Host "[Extra] Inicializando base de datos..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
try {
    python -c "from backend.src.core.database import init_db; init_db()"
    Write-Host "[OK] Base de datos inicializada" -ForegroundColor Green
} catch {
    Write-Host "[ADVERTENCIA] No se pudo inicializar la base de datos" -ForegroundColor Yellow
    Write-Host "Esto es normal si es la primera vez. Se creará al iniciar." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Configuración Completada!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Edita el archivo .env con tus credenciales de Azure"
Write-Host "  2. Ejecuta .\start.ps1 para iniciar la aplicación"
Write-Host ""
Write-Host "Para más información, consulta:" -ForegroundColor Yellow
Write-Host "  - README.md"
Write-Host "  - AZURE_SETUP_ES.md (configuración de Azure)"
Write-Host "  - WINDOWS_SETUP.md (instrucciones para Windows)"
Write-Host ""
pause
