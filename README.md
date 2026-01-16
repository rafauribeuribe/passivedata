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

## 🚀 Configuración de Azure App Registration

### Paso 1: Crear App Registration

1. Ve a [Azure Portal](https://portal.azure.com)
2. Navega a **Azure Active Directory** > **App registrations** > **New registration**
3. Configura:
   - **Name**: PassiveData Analyzer
   - **Supported account types**: Accounts in this organizational directory only
   - **Redirect URI**: Web - `http://localhost:8000/auth/callback`

### Paso 2: Configurar Permisos

En tu App Registration, ve a **API permissions** y agrega:

**Microsoft Graph - Delegated permissions:**
- `User.Read` - Para leer perfil del usuario
- `User.ReadBasic.All` - Para leer perfiles básicos de usuarios
- `Mail.Read` - Para leer correos
- `Calendars.Read` - Para leer calendarios
- `Chat.Read` - Para leer chats de Teams

**IMPORTANTE**: Después de agregar permisos, haz clic en **Grant admin consent** para la organización.

### Paso 3: Crear Client Secret

1. Ve a **Certificates & secrets**
2. Click **New client secret**
3. Copia el valor del secret (solo se muestra una vez)

### Paso 4: Obtener IDs

Copia estos valores de la página **Overview**:
- **Application (client) ID**
- **Directory (tenant) ID**

## ⚙️ Instalación y Configuración

### Backend Setup

```bash
# Clonar el repositorio
git clone <repository-url>
cd passivedata

# Crear entorno virtual Python
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de Azure

# Inicializar base de datos
python -m backend.src.core.init_db

# Ejecutar servidor de desarrollo
uvicorn backend.main:app --reload
```

El backend estará disponible en `http://localhost:8000`

### Frontend Setup

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env.local
# Editar .env.local si es necesario

# Ejecutar servidor de desarrollo
npm start
```

El frontend estará disponible en `http://localhost:3000`

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
