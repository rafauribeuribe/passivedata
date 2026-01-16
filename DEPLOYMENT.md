# Guía de Deployment - PassiveData

Esta guía te ayudará a desplegar PassiveData en diferentes entornos.

## 📋 Contenidos

- [Desarrollo Local](#desarrollo-local)
- [Docker](#docker)
- [Producción](#producción)
- [Azure App Service](#azure-app-service)

---

## 🖥️ Desarrollo Local

### Requisitos

- Python 3.9+
- Node.js 16+
- Git

### Instalación Rápida

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd passivedata

# 2. Ejecutar script de setup
chmod +x setup.sh
./setup.sh

# 3. Configurar variables de entorno
# Editar .env con tus credenciales de Azure

# 4. Iniciar aplicación
chmod +x start.sh
./start.sh
```

### Instalación Manual

#### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r ../requirements.txt

# Configurar .env
cp ../.env.example ../.env
# Editar .env con tus credenciales

# Inicializar base de datos
python -c "from src.core.database import init_db; init_db()"

# Ejecutar servidor
uvicorn main:app --reload
```

El backend estará disponible en `http://localhost:8000`

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env

# Ejecutar servidor de desarrollo
npm start
```

El frontend estará disponible en `http://localhost:3000`

---

## 🐳 Docker

### Docker Compose (Recomendado)

```bash
# Construir y ejecutar
docker-compose up --build

# En modo detached
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### Docker Manual

#### Backend

```bash
# Construir imagen
docker build -t passivedata-backend .

# Ejecutar contenedor
docker run -p 8000:8000 \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/data:/app/data \
  passivedata-backend
```

#### Frontend

```bash
# Construir imagen
cd frontend
docker build -t passivedata-frontend -f Dockerfile.frontend .

# Ejecutar contenedor
docker run -p 3000:3000 passivedata-frontend
```

---

## 🚀 Producción

### Checklist Pre-Deployment

- [ ] Configurar variables de entorno de producción
- [ ] Actualizar `SECRET_KEY` con valor seguro
- [ ] Configurar `DEBUG=False`
- [ ] Configurar CORS para tu dominio
- [ ] Configurar HTTPS
- [ ] Configurar base de datos (SQLite → PostgreSQL recomendado)
- [ ] Configurar backup automático de base de datos
- [ ] Revisar permisos de Microsoft Graph
- [ ] Configurar logging
- [ ] Configurar monitoreo

### Variables de Entorno de Producción

```bash
# Azure App Registration
MICROSOFT_CLIENT_ID=<production-client-id>
MICROSOFT_CLIENT_SECRET=<production-client-secret>
MICROSOFT_TENANT_ID=<production-tenant-id>
REDIRECT_URI=https://yourdomain.com/auth/callback

# Application
SECRET_KEY=<generate-secure-random-key>
DEBUG=False
API_HOST=0.0.0.0
API_PORT=8000

# Frontend
FRONTEND_URL=https://yourdomain.com

# Database (PostgreSQL recomendado)
DATABASE_URL=postgresql://user:password@host:5432/passivedata
```

### Backend - Producción

```bash
# Instalar servidor ASGI de producción
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn backend.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Frontend - Producción

```bash
cd frontend

# Build de producción
npm run build

# Servir con servidor estático (nginx, serve, etc.)
npx serve -s build -l 3000
```

---

## ☁️ Azure App Service

### Backend en Azure App Service

1. **Crear App Service**

```bash
az webapp create \
  --name passivedata-backend \
  --resource-group your-resource-group \
  --plan your-app-service-plan \
  --runtime "PYTHON:3.11"
```

2. **Configurar Variables de Entorno**

```bash
az webapp config appsettings set \
  --name passivedata-backend \
  --resource-group your-resource-group \
  --settings \
    MICROSOFT_CLIENT_ID="your-client-id" \
    MICROSOFT_CLIENT_SECRET="your-client-secret" \
    MICROSOFT_TENANT_ID="your-tenant-id" \
    SECRET_KEY="your-secret-key" \
    DEBUG="False"
```

3. **Deploy**

```bash
# Deploy desde Git
az webapp deployment source config \
  --name passivedata-backend \
  --resource-group your-resource-group \
  --repo-url https://github.com/your-repo/passivedata \
  --branch main \
  --manual-integration
```

### Frontend en Azure Static Web Apps

1. **Crear Static Web App**

```bash
az staticwebapp create \
  --name passivedata-frontend \
  --resource-group your-resource-group \
  --source https://github.com/your-repo/passivedata \
  --location "East US 2" \
  --branch main \
  --app-location "/frontend" \
  --output-location "build"
```

2. **Configurar Variables de Entorno**

En el portal de Azure:
- Navega a Static Web App
- Configuration → Application settings
- Agregar: `REACT_APP_API_URL=https://your-backend-url.azurewebsites.net`

---

## 🔒 Seguridad

### Mejores Prácticas

1. **Nunca commitear credenciales**
   - Usar Azure Key Vault para secrets
   - Variables de entorno para configuración

2. **HTTPS Obligatorio**
   - Configurar SSL/TLS
   - Redirigir HTTP a HTTPS

3. **Autenticación**
   - Implementar refresh tokens
   - Timeouts de sesión
   - Rate limiting

4. **Base de Datos**
   - Backups automáticos
   - Encripción en reposo
   - Minimizar acceso

5. **Logging**
   - No loggear información sensible
   - Monitorear accesos
   - Alertas de seguridad

---

## 📊 Monitoreo

### Logs

```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Azure logs
az webapp log tail --name passivedata-backend --resource-group your-resource-group
```

### Health Checks

- Backend: `http://your-backend/health`
- Documentación API: `http://your-backend/docs`

### Métricas a Monitorear

- Tiempo de respuesta de API
- Tasa de errores
- Uso de CPU/Memoria
- Espacio en disco (base de datos)
- Tokens expirados
- Llamadas a Microsoft Graph API

---

## 🔄 Actualizaciones

### Pull Latest Changes

```bash
git pull origin main

# Backend
cd backend
source venv/bin/activate
pip install -r ../requirements.txt
# Reiniciar servidor

# Frontend
cd frontend
npm install
npm run build
# Reiniciar servidor
```

### Migraciones de Base de Datos

Si cambias los modelos:

```bash
cd backend
# Backup base de datos actual
cp ../passivedata.db ../passivedata.db.backup

# Aplicar cambios (puede requerir Alembic)
python -c "from src.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

---

## 🆘 Troubleshooting

### Backend no inicia

```bash
# Verificar dependencias
pip list

# Verificar .env
cat .env

# Verificar logs
tail -f logs/app.log
```

### Frontend no se conecta al Backend

1. Verificar CORS en backend
2. Verificar `REACT_APP_API_URL` en frontend
3. Verificar network en DevTools

### Errores de Autenticación

1. Verificar credenciales de Azure
2. Verificar redirect URI en Azure Portal
3. Verificar permisos de Microsoft Graph
4. Verificar tokens no expirados

---

## 📞 Soporte

Para problemas o preguntas:
1. Revisar logs
2. Consultar documentación de Microsoft Graph
3. Crear issue en el repositorio

---

**Última actualización:** 2025-01-16
