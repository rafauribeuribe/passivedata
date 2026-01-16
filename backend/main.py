"""
PassiveData - Main FastAPI Application
Aplicación para análisis de datos pasivos de Microsoft 365
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from src.core.config import settings
from src.api import auth, users, extract, data

# Crear aplicación FastAPI
app = FastAPI(
    title="PassiveData API",
    description="API para análisis de metadata de Microsoft 365",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(extract.router, prefix="/api/extract", tags=["Data Extraction"])
app.include_router(data.router, prefix="/api/data", tags=["Data Query"])


@app.get("/")
async def root():
    """Endpoint raíz - información de la API"""
    return {
        "name": "PassiveData API",
        "version": "1.0.0",
        "description": "API para análisis de metadata de Microsoft 365",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """Eventos al iniciar la aplicación"""
    print("🚀 PassiveData API iniciando...")
    print(f"📝 Documentación disponible en: http://{settings.API_HOST}:{settings.API_PORT}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Eventos al cerrar la aplicación"""
    print("👋 PassiveData API cerrando...")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
