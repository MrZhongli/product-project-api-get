from pydantic import BaseModel, Field
from typing import Optional, List

class RazaBase(BaseModel):
    """Esquema base para Raza"""
    descripcion: str = Field(..., min_length=1, max_length=255, description="Descripción de la raza")

class RazaCreate(RazaBase):
    """Esquema para crear una raza"""
    cod_raza: str = Field(..., min_length=1, max_length=50, description="Código único de la raza")

class RazaUpdate(BaseModel):
    """Esquema para actualizar una raza"""
    descripcion: Optional[str] = Field(None, min_length=1, max_length=255)

class RazaResponse(RazaBase):
    """Esquema de respuesta para Raza"""
    cod_raza: str
    
    class Config:
        from_attributes = True

class RazaWithAnimalsResponse(RazaResponse):
    """Esquema de respuesta para Raza con sus animales"""
    total_animales: int = 0
    
class RazaListResponse(BaseModel):
    """Esquema para lista de razas"""
    razas: List[RazaResponse]
    total: int
    page: int
    size: int