# 🪟 Guía de Instalación en Windows - PassiveData

Esta guía te ayudará a instalar y configurar PassiveData en **Windows 10/11**.

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación de Prerequisitos](#instalación-de-prerequisitos)
3. [Instalación de PassiveData](#instalación-de-passivedata)
4. [Configuración de Azure](#configuración-de-azure)
5. [Ejecutar la Aplicación](#ejecutar-la-aplicación)
6. [Solución de Problemas](#solución-de-problemas)

---

## 📋 Requisitos Previos

Necesitas instalar lo siguiente en tu PC Windows:

- ✅ **Python 3.9 o superior**
- ✅ **Node.js 16 o superior**
- ✅ **Git** (opcional, para clonar el repositorio)
- ✅ **Cuenta de Azure** con permisos de administrador

---

## 🔧 Instalación de Prerequisitos

### 1. Instalar Python

#### Opción A: Descarga Directa

1. Ve a [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Descarga **Python 3.11** o superior (recomendado)
3. **IMPORTANTE**: Durante la instalación:
   - ✅ Marca la casilla **"Add Python to PATH"**
   - ✅ Click en **"Install Now"**

#### Opción B: Microsoft Store

1. Abre **Microsoft Store**
2. Busca **"Python 3.11"**
3. Click en **"Obtener"** / **"Get"**

#### Verificar Instalación

Abre **Command Prompt** (Win + R, escribe `cmd`, Enter) y ejecuta:

```cmd
python --version
```

Deberías ver algo como: `Python 3.11.x`

---

### 2. Instalar Node.js

#### Descargar e Instalar

1. Ve a [https://nodejs.org/](https://nodejs.org/)
2. Descarga la versión **LTS** (recomendada)
3. Ejecuta el instalador
4. Acepta las opciones por defecto
5. Click en **"Install"**

#### Verificar Instalación

En **Command Prompt**:

```cmd
node --version
npm --version
```

Deberías ver las versiones instaladas.

---

### 3. Instalar Git (Opcional)

Si quieres clonar el repositorio:

1. Ve a [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Descarga el instalador
3. Ejecuta y acepta las opciones por defecto

#### Verificar Instalación

```cmd
git --version
```

---

## 📦 Instalación de PassiveData

### Método 1: Usando Git (Recomendado)

1. **Abre Command Prompt o PowerShell**
   - Win + R → escribe `cmd` → Enter
   - O Win + X → "Windows PowerShell"

2. **Navega a donde quieres instalar**
   ```cmd
   cd C:\Users\TuUsuario\Documents
   ```

3. **Clona el repositorio**
   ```cmd
   git clone <URL-del-repositorio> passivedata
   cd passivedata
   ```

### Método 2: Descarga Directa (Sin Git)

1. Descarga el archivo ZIP del repositorio
2. Extrae el ZIP en una carpeta (ej: `C:\Users\TuUsuario\Documents\passivedata`)
3. Abre Command Prompt:
   ```cmd
   cd C:\Users\TuUsuario\Documents\passivedata
   ```

---

## ⚙️ Instalación Automática

Una vez en la carpeta del proyecto, tienes dos opciones:

### Opción A: Usando Batch File (cmd)

```cmd
setup.bat
```

### Opción B: Usando PowerShell

1. **Abrir PowerShell como Administrador**
   - Win + X → "Windows PowerShell (Admin)"

2. **Si es la primera vez usando PowerShell scripts**:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   (Acepta con `Y`)

3. **Ejecutar el script**:
   ```powershell
   .\setup.ps1
   ```

### ¿Qué hace el script de setup?

El script automáticamente:
1. ✅ Verifica que Python y Node.js estén instalados
2. ✅ Crea un entorno virtual de Python (`venv`)
3. ✅ Instala todas las dependencias de Python
4. ✅ Instala todas las dependencias de Node.js
5. ✅ Crea el archivo `.env` desde `.env.example`
6. ✅ Inicializa la base de datos

---

## 🔑 Configuración de Azure

### Paso 1: Crear App Registration

Sigue la guía detallada: **[AZURE_SETUP_ES.md](AZURE_SETUP_ES.md)**

En resumen, necesitas:
1. Crear un App Registration en Azure Portal
2. Copiar 3 credenciales:
   - Application (client) ID
   - Directory (tenant) ID
   - Client Secret

### Paso 2: Configurar el archivo .env

1. **Abre el archivo `.env`** con tu editor favorito:

   **Notepad:**
   ```cmd
   notepad .env
   ```

   **Visual Studio Code:**
   ```cmd
   code .env
   ```

   **Notepad++:**
   ```cmd
   notepad++ .env
   ```

2. **Edita las siguientes líneas** con tus credenciales de Azure:

   ```bash
   # Azure App Registration
   MICROSOFT_CLIENT_ID=pega-aqui-tu-client-id
   MICROSOFT_CLIENT_SECRET=pega-aqui-tu-client-secret
   MICROSOFT_TENANT_ID=pega-aqui-tu-tenant-id

   # Estas líneas déjalas como están
   REDIRECT_URI=http://localhost:8000/auth/callback
   SECRET_KEY=cambia-esto-por-algo-seguro-en-produccion
   DEBUG=True
   API_HOST=0.0.0.0
   API_PORT=8000
   FRONTEND_URL=http://localhost:3000
   DATABASE_URL=sqlite:///./passivedata.db
   GRAPH_API_ENDPOINT=https://graph.microsoft.com/v1.0
   GRAPH_API_SCOPES=User.Read User.ReadBasic.All Mail.Read Calendars.Read Chat.Read Chat.ReadBasic
   ```

3. **Guarda el archivo** (Ctrl + S)

---

## 🚀 Ejecutar la Aplicación

### Opción A: Usando Batch File

```cmd
start.bat
```

### Opción B: Usando PowerShell

```powershell
.\start.ps1
```

### ¿Qué hace el script de start?

1. ✅ Verifica que todo esté instalado
2. ✅ Abre dos ventanas:
   - Una para el **Backend (FastAPI)** en puerto 8000
   - Una para el **Frontend (React)** en puerto 3000
3. ✅ Abre automáticamente tu navegador en `http://localhost:3000`

---

## 🌐 Acceder a la Aplicación

Después de ejecutar `start.bat` o `start.ps1`:

- **Frontend (Dashboard)**: http://localhost:3000
- **Backend (API)**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

---

## 🛑 Detener la Aplicación

Para detener los servicios:

1. Ve a las ventanas de Command Prompt / PowerShell que se abrieron
2. Presiona **Ctrl + C** en cada una
3. O simplemente cierra las ventanas

---

## 🔧 Solución de Problemas

### Error: "Python no está instalado o no está en el PATH"

**Solución:**
1. Desinstala Python
2. Reinstala marcando **"Add Python to PATH"**
3. O agrega manualmente Python al PATH:
   - Win + R → `sysdm.cpl` → Enter
   - Pestaña "Opciones avanzadas"
   - "Variables de entorno"
   - En "Variables del sistema", edita "Path"
   - Agrega: `C:\Users\TuUsuario\AppData\Local\Programs\Python\Python311`

### Error: "Node.js no está instalado o no está en el PATH"

**Solución:**
Similar a Python, reinstala Node.js o agrega al PATH:
- Ruta típica: `C:\Program Files\nodejs`

### Error: "cannot be loaded because running scripts is disabled"

**Solución (PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "uvicorn: command not found"

**Solución:**
1. Asegúrate de que el entorno virtual esté activado:
   ```cmd
   venv\Scripts\activate
   ```
2. Reinstala dependencias:
   ```cmd
   pip install -r requirements.txt
   ```

### Error: "npm: command not found"

**Solución:**
Reinstala Node.js y verifica que esté en el PATH.

### Error: "EADDRINUSE" (puerto ya en uso)

**Solución:**
Otro proceso está usando el puerto 8000 o 3000.

**Opción 1: Matar el proceso**
```cmd
netstat -ano | findstr :8000
taskkill /PID <numero-del-pid> /F
```

**Opción 2: Cambiar puerto**
Edita `.env` y cambia `API_PORT=8000` a otro puerto (ej: 8001)

### Error: "Access denied" al instalar dependencias

**Solución:**
Ejecuta Command Prompt o PowerShell **como Administrador**:
- Win + X → "Windows PowerShell (Admin)" o "Command Prompt (Admin)"

### Error: "Microsoft Graph API 403 Forbidden"

**Solución:**
1. Verifica que hayas **concedido consentimiento de administrador** en Azure
2. Revisa que los permisos estén correctos en Azure Portal
3. Ver **[AZURE_SETUP_ES.md](AZURE_SETUP_ES.md)** Paso 5

### La aplicación no abre automáticamente el navegador

**Solución:**
Abre manualmente: http://localhost:3000

### Error de base de datos

**Solución:**
Elimina y recrea la base de datos:
```cmd
del passivedata.db
venv\Scripts\activate
python -c "from backend.src.core.database import init_db; init_db()"
```

---

## 📂 Estructura de Carpetas en Windows

```
C:\Users\TuUsuario\Documents\passivedata\
│
├── backend\                 # Backend FastAPI
│   ├── src\
│   └── main.py
│
├── frontend\                # Frontend React
│   ├── src\
│   └── package.json
│
├── venv\                    # Entorno virtual Python (se crea automático)
│
├── .env                     # Configuración (EDITAR CON CREDENCIALES)
├── setup.bat                # Script de instalación (cmd)
├── setup.ps1                # Script de instalación (PowerShell)
├── start.bat                # Script de inicio (cmd)
├── start.ps1                # Script de inicio (PowerShell)
├── README.md
├── AZURE_SETUP_ES.md        # Guía de configuración de Azure
└── WINDOWS_SETUP.md         # Esta guía
```

---

## 🎯 Resumen de Comandos Rápidos

```cmd
# 1. Instalar (una sola vez)
setup.bat

# 2. Configurar Azure (ver AZURE_SETUP_ES.md)
# Editar .env con credenciales

# 3. Ejecutar aplicación
start.bat

# 4. Acceder
# http://localhost:3000
```

---

## 🔄 Actualizaciones Futuras

Para actualizar a una nueva versión:

```cmd
# Si usas Git
git pull origin main

# Reinstalar dependencias
setup.bat

# Reiniciar aplicación
start.bat
```

---

## 💡 Consejos para Windows

1. **Usa PowerShell** en lugar de cmd para mejor experiencia
2. **Agrega PassiveData al menú inicio**:
   - Crea un acceso directo a `start.bat`
   - Cópialo a: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs`
3. **Ejecuta automáticamente al inicio**:
   - Win + R → `shell:startup`
   - Copia el acceso directo de `start.bat` ahí
4. **Usa Visual Studio Code** como editor (gratuito):
   - [https://code.visualstudio.com/](https://code.visualstudio.com/)

---

## 🔒 Seguridad en Windows

1. **Firewall**: Windows puede preguntar si quieres permitir Python y Node.js
   - Click en **"Permitir acceso"**
2. **Antivirus**: Algunos antivirus pueden bloquear scripts
   - Agrega la carpeta de PassiveData a excepciones
3. **Credenciales**: El archivo `.env` contiene información sensible
   - No lo compartas ni lo subas a repositorios públicos

---

## 📞 Ayuda Adicional

- **Configuración de Azure**: Ver [AZURE_SETUP_ES.md](AZURE_SETUP_ES.md)
- **Documentación general**: Ver [README.md](README.md)
- **Deployment**: Ver [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Última actualización:** 2026-01-16

¡Listo! Ahora tienes PassiveData corriendo en Windows 🎉
