from pydantic import BaseModel, Field
from typing import Optional
from .raza import RazaResponse

class AnimalBase(BaseModel):
    """Esquema base para Animal"""
    descripcion: str = Field(..., min_length=1, max_length=255, description="Descripción del animal")
    sexo: str = Field(..., min_length=1, max_length=10, description="Sexo del animal (M/F)")
    edad: int = Field(..., ge=0, le=50, description="Edad del animal en años")
    cod_raza: str = Field(..., min_length=1, max_length=50, description="Código de la raza")
    color_pelaje: str = Field(..., min_length=1, max_length=100, description="Color del pelaje")
    color_ojos: str = Field(..., min_length=1, max_length=100, description="Color de los ojos")

class AnimalCreate(AnimalBase):
    """Esquema para crear un animal"""
    cod_animal: str = Field(..., min_length=1, max_length=50, description="Código único del animal")

class AnimalUpdate(BaseModel):
    """Esquema para actualizar un animal"""
    descripcion: Optional[str] = Field(None, min_length=1, max_length=255)
    sexo: Optional[str] = Field(None, min_length=1, max_length=10)
    edad: Optional[int] = Field(None, ge=0, le=50)
    cod_raza: Optional[str] = Field(None, min_length=1, max_length=50)
    color_pelaje: Optional[str] = Field(None, min_length=1, max_length=100)
    color_ojos: Optional[str] = Field(None, min_length=1, max_length=100)

class AnimalResponse(AnimalBase):
    """Esquema de respuesta para Animal"""
    cod_animal: str
    raza: Optional[RazaResponse] = None
    
    class Config:
        from_attributes = True

class AnimalListResponse(BaseModel):
    """Esquema para lista de animales"""
    animals: list[AnimalResponse]
    total: int
    page: int
    size: int