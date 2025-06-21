# app/routes/__init__.py

from .animal_routes import router as animal_router # Asumiendo que tus rutas están en un APIRouter llamado 'router'
from .raza_routes import router as raza_router

__all__ = [
    "animal_router", "raza_router"
]