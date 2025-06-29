from pydantic import BaseModel, Field
from typing import Optional
from .raza import RazaResponse

class AnimalBase(BaseModel):
    """Esquema base para Animal"""
    descripcion: str = Field(..., min_length=1, max_length=255, description="Descripción del animal")
    sexo: str = Field(..., min_length=1, max_length=10, description="Sexo del animal (M/F)")
    edad: int = Field(..., ge=0, le=50, description="Edad del animal en años")
    cod_raza: str = Field(..., min_length=1, max_length=50, description="Código de la raza", alias="codRaza")
    color_pelaje: str = Field(..., min_length=1, max_length=100, description="Color del pelaje", alias="colorPelaje")
    color_ojos: str = Field(..., min_length=1, max_length=100, description="Color de los ojos", alias="colorOjos")
    image: Optional[str] = Field(None, max_length=500, description="URL o path de la imagen del animal")

class AnimalCreate(AnimalBase):
    """Esquema para crear un animal"""
    cod_animal: str = Field(..., min_length=1, max_length=50, description="Código único del animal", alias="codAnimal")

class AnimalUpdate(BaseModel):
    """Esquema para actualizar un animal"""
    descripcion: Optional[str] = Field(None, min_length=1, max_length=255)
    sexo: Optional[str] = Field(None, min_length=1, max_length=10)
    edad: Optional[int] = Field(None, ge=0, le=50)
    cod_raza: Optional[str] = Field(None, min_length=1, max_length=50, alias="codRaza")
    color_pelaje: Optional[str] = Field(None, min_length=1, max_length=100, alias="colorPelaje")
    color_ojos: Optional[str] = Field(None, min_length=1, max_length=100, alias="colorOjos")
    image: Optional[str] = Field(None, max_length=500, description="URL o path de la imagen del animal")

class AnimalResponse(AnimalBase):
    """Esquema de respuesta para Animal"""
    cod_animal: str = Field(..., alias="codAnimal")
    raza: Optional["RazaResponse"] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class AnimalListResponse(BaseModel):
    """Esquema para lista de animales"""
    animales: list[AnimalResponse]
    total: int
    page: int
    size: int