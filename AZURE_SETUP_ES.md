# Guía Paso a Paso: Configurar Azure App Registration (Español)

Esta guía te llevará paso a paso por la configuración de Azure App Registration para PassiveData.

---

## 📋 Requisitos Previos

- Cuenta de Azure activa
- Permisos de **Administrador Global** o **Administrador de Aplicaciones** en Azure AD
- Acceso al portal de Azure

---

## 🚀 Paso 1: Crear el Registro de Aplicación

### 1.1 Acceder al Portal de Azure

1. Ve a [https://portal.azure.com](https://portal.azure.com)
2. Inicia sesión con tu cuenta de administrador de Microsoft 365

### 1.2 Navegar a Azure Active Directory

1. En el portal de Azure, busca **"Azure Active Directory"** en la barra de búsqueda superior
2. O navega desde el menú lateral:
   - Click en el **menú hamburguesa** (≡) en la esquina superior izquierda
   - Busca y click en **"Azure Active Directory"** o **"Microsoft Entra ID"**

### 1.3 Crear Nuevo Registro

1. En el panel izquierdo de Azure Active Directory, busca y click en:
   ```
   Administrar → Registros de aplicaciones
   ```
   (o "Manage → App registrations" si aparece en inglés)

2. En la parte superior, click en el botón:
   ```
   + Nuevo registro
   ```
   (o "+ New registration")

### 1.4 Configurar el Registro

Completa el formulario con la siguiente información:

#### **Nombre**
```
PassiveData Analyzer
```
- Este nombre aparecerá cuando los usuarios autoricen la aplicación

#### **Tipos de cuenta admitidos**
Selecciona:
```
⚫ Solo las cuentas de este directorio organizativo (Solo <TuOrganización> - Inquilino único)
```
- Opción en español: "Cuentas en este directorio organizativo únicamente"
- En inglés: "Accounts in this organizational directory only (Single tenant)"

#### **URI de redirección (opcional)**

1. En el dropdown, selecciona: **"Web"**

2. En el campo de texto, ingresa:
   ```
   http://localhost:8000/auth/callback
   ```

3. **IMPORTANTE**: Asegúrate de que sea exactamente esa URL (sin espacios ni caracteres extra)

#### Resumen del formulario:
```
┌─────────────────────────────────────────────────────┐
│ Nombre: PassiveData Analyzer                        │
│                                                      │
│ Tipos de cuenta admitidos:                          │
│   ⚫ Solo cuentas de este directorio                │
│   ⚪ Cuentas de cualquier directorio                │
│   ⚪ Cuentas personales de Microsoft                │
│                                                      │
│ URI de redirección (opcional):                      │
│   Plataforma: [Web ▼]                               │
│   URI: http://localhost:8000/auth/callback          │
└─────────────────────────────────────────────────────┘
```

4. Click en el botón **"Registrar"** (o "Register")

---

## 🔑 Paso 2: Obtener Credenciales

Después de crear el registro, serás redirigido a la página de **Información general**.

### 2.1 Copiar IDs Importantes

En la página de **Información general** (Overview), verás:

```
┌────────────────────────────────────────────────────────┐
│ Información esencial                                   │
├────────────────────────────────────────────────────────┤
│ Nombre para mostrar:  PassiveData Analyzer            │
│ Id. de aplicación (cliente): xxxxxxxx-xxxx-xxxx-xxxx  │ ← COPIAR ESTE
│ Id. de directorio (inquilino): xxxxxxxx-xxxx-xxxx-xxx │ ← COPIAR ESTE
│ URI de id. de aplicación: api://xxxxxxxx-xxxx-xxxx... │
└────────────────────────────────────────────────────────┘
```

**Copia estos dos valores:**

1. **Id. de aplicación (cliente)** / "Application (client) ID"
   - Este es tu `MICROSOFT_CLIENT_ID`
   - Formato: `12345678-1234-1234-1234-123456789abc`

2. **Id. de directorio (inquilino)** / "Directory (tenant) ID"
   - Este es tu `MICROSOFT_TENANT_ID`
   - Formato: `87654321-4321-4321-4321-cba987654321`

💡 **Consejo**: Ábrelos en un editor de texto temporal para usarlos después.

---

## 🔐 Paso 3: Crear Client Secret (Secreto de Cliente)

### 3.1 Navegar a Certificados y Secretos

1. En el panel izquierdo de tu aplicación, busca:
   ```
   Administrar → Certificados y secretos
   ```
   (o "Manage → Certificates & secrets")

### 3.2 Crear Nuevo Secreto

1. En la pestaña **"Secretos de cliente"** (Client secrets), click en:
   ```
   + Nuevo secreto de cliente
   ```
   (o "+ New client secret")

2. Se abrirá un panel lateral. Completa:

   **Descripción:**
   ```
   PassiveData Secret
   ```

   **Expira:**
   Selecciona una de las opciones:
   ```
   ⚪ 6 meses
   ⚪ 12 meses
   ⚪ 24 meses
   ⚫ Personalizada    ← Recomendado: 24 meses
   ```

3. Click en **"Agregar"** (o "Add")

### 3.3 Copiar el Valor del Secreto

⚠️ **MUY IMPORTANTE**: El secreto se mostrará **SOLO UNA VEZ**.

```
┌─────────────────────────────────────────────────────────┐
│ Secretos de cliente                                     │
├──────────────┬──────────────────┬──────────────────────┤
│ Descripción  │ Valor            │ Expira              │
├──────────────┼──────────────────┼──────────────────────┤
│ PassiveData  │ abc123~xyz...    │ 16/01/2027          │
│              │ [📋 Copiar]      │                      │
└──────────────┴──────────────────┴──────────────────────┘
```

1. Click en el icono de **copiar** (📋) junto al valor
2. **Pega este valor inmediatamente** en un lugar seguro
3. Este es tu `MICROSOFT_CLIENT_SECRET`

⚠️ **Si cierras la página sin copiar el secreto, tendrás que crear uno nuevo.**

---

## 🔓 Paso 4: Configurar Permisos de API

### 4.1 Navegar a Permisos de API

1. En el panel izquierdo, click en:
   ```
   Administrar → Permisos de API
   ```
   (o "Manage → API permissions")

2. Verás que ya existe un permiso por defecto:
   ```
   Microsoft Graph → User.Read (Delegado)
   ```

### 4.2 Agregar Permisos Necesarios

#### Paso 4.2.1: Click en "Agregar un permiso"

Click en el botón:
```
+ Agregar un permiso
```
(o "+ Add a permission")

#### Paso 4.2.2: Seleccionar Microsoft Graph

En el panel que se abre, click en:
```
Microsoft Graph
```

#### Paso 4.2.3: Seleccionar Tipo de Permisos

Click en:
```
Permisos delegados
```
(o "Delegated permissions")

#### Paso 4.2.4: Agregar Permisos Uno por Uno

Necesitas agregar **5 permisos**. Para cada uno:

1. **User.ReadBasic.All**
   - En el buscador, escribe: `User.ReadBasic.All`
   - Marca la casilla: `User.ReadBasic.All`
   - Click en **"Agregar permisos"**

2. **Mail.Read**
   - Click nuevamente en **"+ Agregar un permiso"**
   - Click en **"Microsoft Graph"** → **"Permisos delegados"**
   - Busca: `Mail.Read`
   - Marca la casilla: `Mail.Read`
   - Click en **"Agregar permisos"**

3. **Calendars.Read**
   - Repetir el proceso
   - Buscar: `Calendars.Read`
   - Marcar y agregar

4. **Chat.Read**
   - Repetir el proceso
   - Buscar: `Chat.Read`
   - Marcar y agregar

5. **Chat.ReadBasic** (opcional, pero recomendado)
   - Repetir el proceso
   - Buscar: `Chat.ReadBasic`
   - Marcar y agregar

### 4.3 Estado Final de Permisos

Después de agregar todos, deberías ver:

```
┌────────────────────────────────────────────────────────────────┐
│ Permisos configurados                                          │
├──────────────────────┬──────────────┬──────────────────────────┤
│ API / Nombre permiso │ Tipo         │ Estado                   │
├──────────────────────┼──────────────┼──────────────────────────┤
│ Microsoft Graph      │              │                          │
│   User.Read          │ Delegado     │ Concedido para...        │
│   User.ReadBasic.All │ Delegado     │ No concedido             │
│   Mail.Read          │ Delegado     │ No concedido             │
│   Calendars.Read     │ Delegado     │ No concedido             │
│   Chat.Read          │ Delegado     │ No concedido             │
│   Chat.ReadBasic     │ Delegado     │ No concedido             │
└──────────────────────┴──────────────┴──────────────────────────┘
```

---

## ✅ Paso 5: Conceder Consentimiento de Administrador

Este es el paso **MÁS IMPORTANTE** - sin esto, la aplicación no funcionará.

### 5.1 Conceder Permisos

1. En la página de **Permisos de API**, busca el botón:
   ```
   ⚡ Conceder consentimiento de administrador para <TuOrganización>
   ```
   (o "Grant admin consent for <YourOrg>")

2. **Click en ese botón**

3. Aparecerá un diálogo de confirmación:
   ```
   ¿Conceder consentimiento para los permisos solicitados?

   Esta aplicación podrá:
   - Leer tu perfil básico
   - Leer perfiles básicos de usuarios
   - Leer tu correo
   - Leer tu calendario
   - Leer tus chats

   [Cancelar]  [Sí]
   ```

4. Click en **"Sí"**

### 5.2 Verificar que los Permisos fueron Concedidos

Después de conceder, todos los permisos deben mostrar estado **"Concedido"**:

```
┌────────────────────────────────────────────────────────────────┐
│ Permisos configurados                                          │
├──────────────────────┬──────────────┬──────────────────────────┤
│ API / Nombre permiso │ Tipo         │ Estado                   │
├──────────────────────┼──────────────┼──────────────────────────┤
│ Microsoft Graph      │              │                          │
│   User.Read          │ Delegado     │ ✅ Concedido para...     │
│   User.ReadBasic.All │ Delegado     │ ✅ Concedido para...     │
│   Mail.Read          │ Delegado     │ ✅ Concedido para...     │
│   Calendars.Read     │ Delegado     │ ✅ Concedido para...     │
│   Chat.Read          │ Delegado     │ ✅ Concedido para...     │
│   Chat.ReadBasic     │ Delegado     │ ✅ Concedido para...     │
└──────────────────────┴──────────────┴──────────────────────────┘
```

✅ **Si ves las marcas verdes (✅) o dice "Concedido", ¡perfecto!**

---

## 📝 Paso 6: Configurar Variables de Entorno

Ahora que tienes todas las credenciales, configura tu aplicación.

### 6.1 Abrir el Archivo .env

En tu proyecto PassiveData:

```bash
cd /home/user/passivedata
cp .env.example .env
nano .env
```

(O ábrelo con tu editor favorito: vim, code, etc.)

### 6.2 Completar las Credenciales

Reemplaza los valores con los que copiaste:

```bash
# Azure App Registration
MICROSOFT_CLIENT_ID=<PEGA_AQUI_TU_APPLICATION_CLIENT_ID>
MICROSOFT_CLIENT_SECRET=<PEGA_AQUI_TU_CLIENT_SECRET>
MICROSOFT_TENANT_ID=<PEGA_AQUI_TU_DIRECTORY_TENANT_ID>

# Redirect URI (debe coincidir con Azure)
REDIRECT_URI=http://localhost:8000/auth/callback

# Application Settings
SECRET_KEY=tu-clave-secreta-muy-segura-cambiala
DEBUG=True

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Database
DATABASE_URL=sqlite:///./passivedata.db

# Microsoft Graph API
GRAPH_API_ENDPOINT=https://graph.microsoft.com/v1.0
GRAPH_API_SCOPES=User.Read User.ReadBasic.All Mail.Read Calendars.Read Chat.Read Chat.ReadBasic
```

### 6.3 Ejemplo Completo

```bash
# EJEMPLO (reemplaza con tus valores reales)
MICROSOFT_CLIENT_ID=12345678-1234-1234-1234-123456789abc
MICROSOFT_CLIENT_SECRET=abc123~XyZ456.qWe789-RtY012
MICROSOFT_TENANT_ID=87654321-4321-4321-4321-cba987654321
REDIRECT_URI=http://localhost:8000/auth/callback
SECRET_KEY=mi-super-secreto-2024-cambiar-en-prod
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:3000
DATABASE_URL=sqlite:///./passivedata.db
GRAPH_API_ENDPOINT=https://graph.microsoft.com/v1.0
GRAPH_API_SCOPES=User.Read User.ReadBasic.All Mail.Read Calendars.Read Chat.Read Chat.ReadBasic
```

### 6.4 Guardar el Archivo

- En **nano**: `Ctrl + X`, luego `Y`, luego `Enter`
- En **vim**: `Esc`, luego `:wq`, luego `Enter`

---

## 🎉 ¡Configuración Completa!

### Resumen de lo que hiciste:

✅ Creaste un App Registration en Azure
✅ Copiaste el **Client ID**
✅ Copiaste el **Tenant ID**
✅ Creaste y copiaste el **Client Secret**
✅ Configuraste la **URI de redirección**
✅ Agregaste **permisos de Microsoft Graph**
✅ Concediste **consentimiento de administrador**
✅ Configuraste el archivo **.env**

### Credenciales que Necesitaste:

| Credencial | Dónde la Encontraste | Variable de Entorno |
|------------|----------------------|---------------------|
| Application (client) ID | Información general | `MICROSOFT_CLIENT_ID` |
| Directory (tenant) ID | Información general | `MICROSOFT_TENANT_ID` |
| Client Secret | Certificados y secretos | `MICROSOFT_CLIENT_SECRET` |

---

## 🚀 Próximos Pasos

Ahora estás listo para ejecutar la aplicación:

```bash
# 1. Ejecutar setup (instala dependencias)
chmod +x setup.sh
./setup.sh

# 2. Iniciar la aplicación
chmod +x start.sh
./start.sh
```

La aplicación estará disponible en:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

---

## ❓ Solución de Problemas

### Error: "Redirect URI mismatch"
- Verifica que la URI en Azure sea exactamente: `http://localhost:8000/auth/callback`
- Verifica que en `.env` sea la misma URI

### Error: "Invalid client secret"
- El secret puede haber expirado o ser incorrecto
- Crea un nuevo secret en Azure y actualiza `.env`

### Error: "Insufficient privileges"
- Asegúrate de haber **concedido consentimiento de administrador**
- Verifica que todos los permisos muestren estado "Concedido"

### No puedo conceder consentimiento de administrador
- Necesitas rol de **Administrador Global** o **Administrador de Aplicaciones**
- Contacta a tu administrador de TI

---

## 📞 ¿Necesitas Ayuda?

Si tienes problemas en algún paso específico, avísame en qué paso estás y qué error ves.

---

**Última actualización:** 2026-01-16
