# PassiveData - Microsoft 365 Metadata Analytics

Aplicación para análisis de datos pasivos de Microsoft 365 (correos, agenda y chats de Teams) de tu organización.

## 🎯 Características

- **Autenticación segura** con Microsoft Graph API
- **Extracción de metadata** de:
  - 📧 Correos electrónicos (remitente, destinatario, timestamp)
  - 📅 Eventos de calendario (organizador, participantes, timestamp)
  - 💬 Chats de Teams (participantes, timestamp)
- **Dashboard interactivo** con React para visualización de datos
- **API REST** para exportación y consulta de datos
- **Base de datos SQLite** para almacenamiento local

## 🏗️ Arquitectura

```
passivedata/
├── backend/                 # FastAPI Backend
│   ├── src/
│   │   ├── auth/           # Autenticación Microsoft Graph
│   │   ├── extractors/     # Extractores de metadata
│   │   ├── models/         # Modelos de base de datos
│   │   ├── api/            # Endpoints API REST
│   │   └── core/           # Configuración y utilidades
│   ├── main.py             # Punto de entrada
│   └── requirements.txt
├── frontend/               # React Dashboard
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── pages/         # Páginas del dashboard
│   │   └── services/      # Servicios API
│   └── package.json
└── .env                   # Variables de entorno
```

## 📋 Requisitos Previos

1. **Python 3.9+**
2. **Node.js 16+** y npm
3. **Cuenta de Azure** con permisos de administrador
4. **App Registration en Azure AD**

## 🪟 Instalación Rápida en Windows

Si estás en **Windows 10/11**, sigue estos pasos simples:

### 1. Instalar Prerequisitos
- **Python 3.9+**: [Descargar aquí](https://www.python.org/downloads/) (marca "Add Python to PATH")
- **Node.js 16+**: [Descargar aquí](https://nodejs.org/)

### 2. Ejecutar Script de Instalación
Abre **Command Prompt** o **PowerShell** en la carpeta del proyecto:

```cmd
# Opción 1: Command Prompt
setup.bat

# Opción 2: PowerShell
.\setup.ps1
```

### 3. Configurar Azure
Sigue la guía detallada en: **[AZURE_SETUP_ES.md](AZURE_SETUP_ES.md)**

### 4. Configurar Credenciales
Edita el archivo `.env` con tus credenciales de Azure (Client ID, Client Secret, Tenant ID)

### 5. Ejecutar la Aplicación
```cmd
# Opción 1: Command Prompt
start.bat

# Opción 2: PowerShell
.\start.ps1
```

🎉 La aplicación se abrirá automáticamente en `http://localhost:3000`

📖 **Ver guía completa**: [WINDOWS_SETUP.md](WINDOWS_SETUP.md)

---

## 🐧 Instalación en Linux/Mac

### Instalación Rápida

```bash
# Ejecutar script de instalación
chmod +x setup.sh
./setup.sh

# Configurar .env con credenciales de Azure
cp .env.example .env
nano .env

# Ejecutar la aplicación
chmod +x start.sh
./start.sh
```

---

## 🚀 Configuración de Azure App Registration

📖 **Guía Detallada Paso a Paso (en Español)**: [AZURE_SETUP_ES.md](AZURE_SETUP_ES.md)

### Resumen Rápido

1. **Crear App Registration** en [Azure Portal](https://portal.azure.com)
   - Nombre: `PassiveData Analyzer`
   - Tipo: Solo cuentas de este directorio (Single tenant)
   - Redirect URI: `http://localhost:8000/auth/callback`

2. **Copiar Credenciales**:
   - Application (client) ID → `MICROSOFT_CLIENT_ID`
   - Directory (tenant) ID → `MICROSOFT_TENANT_ID`

3. **Crear Client Secret** y copiarlo → `MICROSOFT_CLIENT_SECRET`

4. **Agregar Permisos** (Microsoft Graph - Delegated):
   - `User.Read` y `User.ReadBasic.All`
   - `Mail.Read`
   - `Calendars.Read`
   - `Chat.Read` y `Chat.ReadBasic`

5. **⚡ Conceder Consentimiento de Administrador** (¡MUY IMPORTANTE!)

6. **Configurar `.env`** con las 3 credenciales copiadas

⏱️ **Tiempo estimado**: 15-20 minutos

---

## ⚙️ Instalación Manual (Alternativa)

Si prefieres instalar manualmente sin los scripts automáticos:

### Backend

```bash
# Crear entorno virtual Python
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env con tus credenciales de Azure

# Ejecutar servidor
cd backend
uvicorn main:app --reload
```

### Frontend

```bash
# Instalar dependencias
cd frontend
npm install

# Ejecutar servidor
npm start
```

---

## 📊 Uso

### 1. Autenticación

1. Abre el dashboard en `http://localhost:3000`
2. Click en **"Login with Microsoft"**
3. Autentica con tu cuenta de administrador de Microsoft 365
4. Autoriza los permisos solicitados

### 2. Exportar Metadata

Una vez autenticado, puedes:

- **Ver usuarios**: Lista de usuarios en la organización
- **Exportar datos**:
  - Correos: Click en "Export Emails Metadata"
  - Calendario: Click en "Export Calendar Metadata"
  - Teams: Click en "Export Teams Metadata"

### 3. Visualizar Dashboard

El dashboard mostrará:
- **Gráfica de comunicación por correo**: Quién se comunica con quién
- **Timeline de reuniones**: Patrones de reuniones por hora/día
- **Red de chats de Teams**: Conexiones entre usuarios
- **Estadísticas generales**: Totales y promedios

## 🔌 API Endpoints

### Autenticación
- `GET /auth/login` - Iniciar sesión con Microsoft
- `GET /auth/callback` - Callback OAuth
- `GET /auth/logout` - Cerrar sesión

### Extracción de Datos
- `POST /api/extract/emails` - Extraer metadata de correos
- `POST /api/extract/calendar` - Extraer metadata de calendario
- `POST /api/extract/teams` - Extraer metadata de Teams

### Consulta de Datos
- `GET /api/data/emails` - Obtener metadata de correos
- `GET /api/data/calendar` - Obtener metadata de calendario
- `GET /api/data/teams` - Obtener metadata de Teams
- `GET /api/data/stats` - Estadísticas generales

### Usuarios
- `GET /api/users` - Lista de usuarios

## 🔒 Seguridad y Privacidad

- **Solo metadata**: No se almacena el contenido de correos o mensajes
- **Autenticación segura**: OAuth 2.0 con MSAL
- **Tokens encriptados**: Los tokens de acceso se almacenan de forma segura
- **Datos locales**: Base de datos SQLite local, no en la nube
- **Permisos de administrador**: Solo administradores pueden acceder

## 🛠️ Desarrollo

### Ejecutar Tests

```bash
# Backend tests
pytest backend/tests/

# Frontend tests
cd frontend && npm test
```

### Estructura de Base de Datos

```sql
-- Tabla de correos
emails (
  id, sender_email, recipient_email, timestamp, subject_hash
)

-- Tabla de eventos de calendario
calendar_events (
  id, organizer_email, participant_email, timestamp, duration_minutes
)

-- Tabla de chats de Teams
teams_chats (
  id, sender_email, recipient_email, timestamp, chat_type
)
```

## 📝 Próximas Mejoras

- [ ] Exportación a CSV/Excel
- [ ] Análisis de patrones de comunicación con ML
- [ ] Detección de anomalías
- [ ] Dashboard más interactivo con filtros
- [ ] Soporte para múltiples organizaciones
- [ ] API GraphQL
- [ ] Enriquecimiento de datos con fuentes externas

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es privado y confidencial.

## 📧 Contacto

Para preguntas o soporte, contacta al equipo de desarrollo.
