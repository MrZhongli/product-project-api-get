from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from .core.config import settings
from .core.database import connect_db, disconnect_db
from .routes import animal_routes, raza_routes
from .utils.exceptions import BaseAPIException

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    logger.info("🚀 Iniciando la aplicación...")
    await connect_db()
    logger.info("✅ Aplicación iniciada correctamente")
    
    yield
    
    # Shutdown
    logger.info("🔄 Cerrando la aplicación...")
    await disconnect_db()
    logger.info("✅ Aplicación cerrada correctamente")

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Manejador de excepciones personalizado
@app.exception_handler(BaseAPIException)
async def api_exception_handler(request, exc: BaseAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Error interno del servidor",
            "status_code": 500
        }
    )

# Rutas principales
@app.get("/", tags=["Root"])
async def root():
    """Endpoint de bienvenida"""
    return {
        "message": "🐾 API de Gestión de Animales - Grupo Rafael Moreno",
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Verificación de salud de la API"""
    return {
        "status": "healthy",
        "message": "API funcionando correctamente",
        "version": settings.api_version
    }

# Incluir routers
app.include_router(animal_routes.router, prefix="/api/v1")
app.include_router(raza_routes.router, prefix="/api/v1")

# Información adicional para el desarrollador
if settings.debug:
    @app.get("/debug/info", tags=["Debug"], include_in_schema=False)
    async def debug_info():
        """Información de debug (solo en desarrollo)"""
        return {
            "environment": settings.environment,
            "debug": settings.debug,
            "database_url": settings.database_url.split("@")[-1] if "@" in settings.database_url else "No configurada"
        }
