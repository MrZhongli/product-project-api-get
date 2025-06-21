# app/schemas/__init__.py

from .animal import AnimalCreate, AnimalUpdate, AnimalResponse, AnimalListResponse
from .raza import RazaCreate, RazaUpdate, RazaResponse, RazaListResponse, RazaWithAnimalsResponse

__all__ = [
    "AnimalCreate", "AnimalUpdate", "AnimalResponse", "AnimalListResponse",
    "RazaCreate", "RazaUpdate", "RazaResponse", "RazaListResponse", "RazaWithAnimalsResponse"
]