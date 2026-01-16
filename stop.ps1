# ============================================================================
# PassiveData - Script para Detener Servicios (Windows PowerShell)
# ============================================================================

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  PassiveData - Deteniendo Servicios" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Buscando procesos de PassiveData..." -ForegroundColor Yellow
Write-Host ""

# Detener Backend (puerto 8000)
Write-Host "[1/2] Deteniendo Backend (uvicorn en puerto 8000)..." -ForegroundColor Yellow
try {
    $backendProcesses = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue |
                        Select-Object -ExpandProperty OwningProcess -Unique

    if ($backendProcesses) {
        foreach ($pid in $backendProcesses) {
            $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
            if ($process) {
                Write-Host "  Deteniendo proceso: $($process.Name) (PID: $pid)" -ForegroundColor Gray
                Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            }
        }
        Write-Host "[OK] Backend detenido" -ForegroundColor Green
    } else {
        Write-Host "[INFO] No se encontró proceso en puerto 8000" -ForegroundColor Gray
    }
} catch {
    Write-Host "[INFO] No se encontró proceso en puerto 8000" -ForegroundColor Gray
}

Write-Host ""

# Detener Frontend (puerto 3000)
Write-Host "[2/2] Deteniendo Frontend (Node.js en puerto 3000)..." -ForegroundColor Yellow
try {
    $frontendProcesses = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue |
                         Select-Object -ExpandProperty OwningProcess -Unique

    if ($frontendProcesses) {
        foreach ($pid in $frontendProcesses) {
            $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
            if ($process) {
                Write-Host "  Deteniendo proceso: $($process.Name) (PID: $pid)" -ForegroundColor Gray
                Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            }
        }
        Write-Host "[OK] Frontend detenido" -ForegroundColor Green
    } else {
        Write-Host "[INFO] No se encontró proceso en puerto 3000" -ForegroundColor Gray
    }
} catch {
    Write-Host "[INFO] No se encontró proceso en puerto 3000" -ForegroundColor Gray
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Servicios Detenidos" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
pause
