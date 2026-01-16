# ============================================================================
# PassiveData - Script de Inicio para Windows (PowerShell)
# ============================================================================

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  PassiveData - Iniciando Aplicación" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que el entorno virtual existe
if (-not (Test-Path "venv")) {
    Write-Host "[ERROR] No se encontró el entorno virtual de Python" -ForegroundColor Red
    Write-Host "Por favor ejecuta setup.ps1 primero" -ForegroundColor Red
    pause
    exit 1
}

# Verificar que las dependencias de Node están instaladas
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "[ERROR] No se encontraron las dependencias de Node.js" -ForegroundColor Red
    Write-Host "Por favor ejecuta setup.ps1 primero" -ForegroundColor Red
    pause
    exit 1
}

# Verificar que el archivo .env existe
if (-not (Test-Path ".env")) {
    Write-Host "[ERROR] No se encontró el archivo .env" -ForegroundColor Red
    Write-Host "Por favor copia .env.example a .env y configúralo" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Iniciando servicios..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Backend estará disponible en: " -NoNewline
Write-Host "http://localhost:8000" -ForegroundColor Green
Write-Host "Frontend estará disponible en: " -NoNewline
Write-Host "http://localhost:3000" -ForegroundColor Green
Write-Host "API Docs en: " -NoNewline
Write-Host "http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona Ctrl+C para detener ambos servicios" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Obtener la ruta actual
$currentPath = Get-Location

# Iniciar backend en una nueva ventana de PowerShell
$backendScript = @"
Set-Location '$currentPath'
& 'venv\Scripts\Activate.ps1'
Write-Host ''
Write-Host '================================================' -ForegroundColor Cyan
Write-Host '  Backend (FastAPI) Iniciando...' -ForegroundColor Cyan
Write-Host '================================================' -ForegroundColor Cyan
Write-Host ''
Set-Location backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript -WindowStyle Normal

Write-Host "✓ Backend iniciado en nueva ventana" -ForegroundColor Green

# Esperar 3 segundos para que el backend inicie
Start-Sleep -Seconds 3

# Iniciar frontend en una nueva ventana de PowerShell
$frontendScript = @"
Set-Location '$currentPath\frontend'
Write-Host ''
Write-Host '================================================' -ForegroundColor Cyan
Write-Host '  Frontend (React) Iniciando...' -ForegroundColor Cyan
Write-Host '================================================' -ForegroundColor Cyan
Write-Host ''
`$env:BROWSER = 'none'
npm start
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript -WindowStyle Normal

Write-Host "✓ Frontend iniciado en nueva ventana" -ForegroundColor Green

# Esperar 2 segundos
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Servicios Iniciados!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Se abrieron dos ventanas de PowerShell:" -ForegroundColor Yellow
Write-Host "  1. Backend (FastAPI) - Puerto 8000"
Write-Host "  2. Frontend (React) - Puerto 3000"
Write-Host ""
Write-Host "Para detener los servicios:" -ForegroundColor Yellow
Write-Host "  - Cierra ambas ventanas, o"
Write-Host "  - Presiona Ctrl+C en cada ventana"
Write-Host ""
Write-Host "Esperando 5 segundos y luego abriendo el navegador..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Abrir el navegador
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "✓ Navegador abierto en http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Puedes cerrar esta ventana. Los servicios seguirán corriendo." -ForegroundColor Gray
Write-Host ""
pause
