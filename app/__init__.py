# app/__init__.py

# Importa los paquetes para que sus __init__.py se ejecuten
import app.schemas
import app.services
import app.routes
import app.utils

# Si quieres exponer ciertas clases directamente desde app. Por ejemplo:
from app.schemas import (
    AnimalCreate, AnimalUpdate, AnimalResponse, AnimalListResponse,
    RazaCreate, RazaUpdate, RazaResponse, RazaListResponse, RazaWithAnimalsResponse
)
from app.services import AnimalService, RazaService
from app.routes import animal_router, raza_router
from app.utils.exceptions import (
    BaseAPIException, NotFoundError, AlreadyExistsError,
    ValidationError, DatabaseError, AuthenticationError, AuthorizationError
)

# Puedes definir un __all__ si lo deseas para el paquete principal,
# pero no es tan crítico como en las subcarpetas.
# __all__ = [
#     "AnimalCreate", "AnimalUpdate", "AnimalResponse", "AnimalListResponse",
#     "RazaCreate", "RazaUpdate", "RazaResponse", "RazaListResponse", "RazaWithAnimalsResponse",
#     "AnimalService", "RazaService",
#     "animal_router", "raza_router",
#     "BaseAPIException", "NotFoundError", "AlreadyExistsError",
#     "ValidationError", "DatabaseError", "AuthenticationError", "AuthorizationError"
# ]