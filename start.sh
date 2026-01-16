#!/bin/bash

echo "🚀 PassiveData - Starting Application"
echo "======================================"
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Verificar que el setup se haya ejecutado
if [ ! -f ".env" ]; then
    echo "❌ Archivo .env no encontrado. Ejecuta ./setup.sh primero."
    exit 1
fi

# Iniciar Backend
echo -e "${BLUE}🔧 Iniciando Backend...${NC}"
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend iniciado en http://localhost:8000${NC}"
cd ..

# Esperar un momento
sleep 2

# Iniciar Frontend
echo -e "${BLUE}🎨 Iniciando Frontend...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend iniciado en http://localhost:3000${NC}"
cd ..

echo ""
echo -e "${GREEN}✨ Aplicación iniciada!${NC}"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Para detener la aplicación, presiona Ctrl+C"
echo ""

# Esperar a que el usuario detenga los procesos
wait $BACKEND_PID $FRONTEND_PID
