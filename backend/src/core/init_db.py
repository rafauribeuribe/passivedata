"""
Script para inicializar la base de datos
Ejecutar: python -m backend.src.core.init_db
"""
from database import init_db

if __name__ == "__main__":
    print("🔧 Inicializando base de datos...")
    init_db()
    print("✨ Base de datos lista para usar")
