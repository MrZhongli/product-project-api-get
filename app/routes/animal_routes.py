from fastapi import APIRouter, Depends, Query, Path
from typing import List
from prisma import Prisma

from ..core.database import get_db
from ..services.animal_service import AnimalService
from ..schemas.animal import (
    AnimalCreate, 
    AnimalUpdate, 
    AnimalResponse, 
    AnimalListResponse
)
from ..utils.exceptions import NotFoundError, AlreadyExistsError, ValidationError

router = APIRouter(prefix="/animales", tags=["Animales"])

@router.post("/", response_model=AnimalResponse, status_code=201)
async def crear_animal(
    animal_data: AnimalCreate,
    db: Prisma = Depends(get_db)
):
    """Crear un nuevo animal"""
    service = AnimalService(db)
    return await service.create_animal(animal_data)

@router.get("/", response_model=AnimalListResponse)
async def listar_animales(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    db: Prisma = Depends(get_db)
):
    """Obtener lista de animales con paginación"""
    service = AnimalService(db)
    skip = (page - 1) * size
    animals, total = await service.get_all_animals(skip=skip, limit=size)
    
    return AnimalListResponse(
        animals=animals,
        total=total,
        page=page,
        size=size
    )

@router.get("/{cod_animal}", response_model=AnimalResponse)
async def obtener_animal(
    cod_animal: str = Path(..., description="Código del animal"),
    db: Prisma = Depends(get_db)
):
    """Obtener un animal específico por su código"""
    service = AnimalService(db)
    return await service.get_animal_by_code(cod_animal)

@router.put("/{cod_animal}", response_model=AnimalResponse)
async def actualizar_animal(
    animal_data: AnimalUpdate,
    cod_animal: str = Path(..., description="Código del animal"),
    db: Prisma = Depends(get_db)
):
    """Actualizar un animal existente"""
    service = AnimalService(db)
    return await service.update_animal(cod_animal, animal_data)

@router.delete("/{cod_animal}", status_code=204)
async def eliminar_animal(
    cod_animal: str = Path(..., description="Código del animal"),
    db: Prisma = Depends(get_db)
):
    """Eliminar un animal"""
    service = AnimalService(db)
    await service.delete_animal(cod_animal)

@router.get("/raza/{cod_raza}", response_model=AnimalListResponse)
async def listar_animales_por_raza(
    cod_raza: str = Path(..., description="Código de la raza"),
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    db: Prisma = Depends(get_db)
):
    """Obtener animales de una raza específica"""
    service = AnimalService(db)
    skip = (page - 1) * size
    animals, total = await service.get_animals_by_raza(
        cod_raza=cod_raza, 
        skip=skip, 
        limit=size
    )
    
    return AnimalListResponse(
        animals=animals,
        total=total,
        page=page,
        size=size
    )