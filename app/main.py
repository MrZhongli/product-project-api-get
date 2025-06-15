# ============== MAIN APP ==============

# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routes import productos
from app.core.config import settings
from app.core.database import connect_db, disconnect_db

app = FastAPI(
    title="API de Productos",
    description="API simple para gestión de productos",
    version="1.0.0"
)

# CORS


# Archivos estáticos
if not os.path.exists(settings.upload_dir):
    os.makedirs(settings.upload_dir, exist_ok=True)

app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

# Rutas
app.include_router(productos.router)

@app.get("/")
async def root():
    return {
        "message": "API de Productos funcionando",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}