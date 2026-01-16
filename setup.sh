#!/bin/bash

echo "🚀 PassiveData - Setup Script"
echo "================================"
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
echo -e "${BLUE}Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 encontrado${NC}"

# Verificar Node.js
echo -e "${BLUE}Verificando Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js encontrado${NC}"
echo ""

# Backend Setup
echo -e "${BLUE}📦 Configurando Backend...${NC}"
cd backend

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias de Python..."
pip install -r ../requirements.txt

# Copiar .env si no existe
if [ ! -f "../.env" ]; then
    echo "Copiando archivo .env.example a .env..."
    cp ../.env.example ../.env
    echo -e "${RED}⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales de Azure${NC}"
fi

# Inicializar base de datos
echo "Inicializando base de datos..."
python -c "from src.core.database import init_db; init_db()"

echo -e "${GREEN}✓ Backend configurado${NC}"
cd ..
echo ""

# Frontend Setup
echo -e "${BLUE}📦 Configurando Frontend...${NC}"
cd frontend

# Instalar dependencias
echo "Instalando dependencias de Node.js..."
npm install

# Copiar .env si no existe
if [ ! -f ".env" ]; then
    echo "Copiando archivo .env.example a .env..."
    cp .env.example .env
fi

echo -e "${GREEN}✓ Frontend configurado${NC}"
cd ..
echo ""

echo -e "${GREEN}✨ Setup completado!${NC}"
echo ""
echo "Próximos pasos:"
echo "1. Edita el archivo .env con tus credenciales de Azure"
echo "2. Ejecuta './start.sh' para iniciar la aplicación"
echo ""
