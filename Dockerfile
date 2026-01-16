# Dockerfile para Backend de PassiveData
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del backend
COPY backend/ ./backend/

# Copiar .env (en producción, usar secrets)
COPY .env .env

# Exponer puerto
EXPOSE 8000

# Crear directorio para base de datos
RUN mkdir -p /app/data

# Inicializar base de datos
RUN cd backend && python -c "from src.core.database import init_db; init_db()"

# Comando de inicio
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
