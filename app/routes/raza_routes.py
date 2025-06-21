from fastapi import APIRouter, Depends, Query, Path
from typing import List
from prisma import Prisma

from ..core.database import get_db
from ..services.raza_service import RazaService
from ..schemas.raza import (
    RazaCreate, 
    RazaUpdate, 
    RazaResponse, 
    RazaListResponse,
    RazaWithAnimalsResponse
)
from ..utils.exceptions import NotFoundError, AlreadyExistsError, ValidationError

router = APIRouter(prefix="/razas", tags=["Razas"])

@router.post("/", response_model=RazaResponse, status_code=201)
async def crear_raza(
    raza_data: RazaCreate,
    db: Prisma = Depends(get_db)
):
    """Crear una nueva raza"""
    service = RazaService(db)
    return await service.create_raza(raza_data)

@router.get("/", response_model=RazaListResponse)
async def listar_razas(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    db: Prisma = Depends(get_db)
):
    """Obtener lista de razas con paginación"""
    service = RazaService(db)
    skip = (page - 1) * size
    razas, total = await service.get_all_razas(skip=skip, limit=size)
    
    return RazaListResponse(
        razas=razas,
        total=total,
        page=page,
        size=size
    )

@router.get("/with-count", response_model=List[RazaWithAnimalsResponse])
async def listar_razas_con_conteo(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    db: Prisma = Depends(get_db)
):
    """Obtener lista de razas con conteo de animales"""
    service = RazaService(db)
    skip = (page - 1) * size
    razas, total = await service.get_razas_with_animal_count(skip=skip, limit=size)
    return razas

@router.get("/{cod_raza}", response_model=RazaResponse)
async def obtener_raza(
    cod_raza: str = Path(..., description="Código de la raza"),
    db: Prisma = Depends(get_db)
):
    """Obtener una raza específica por su código"""
    service = RazaService(db)
    return await service.get_raza_by_code(cod_raza)

@router.get("/{cod_raza}/with-count", response_model=RazaWithAnimalsResponse)
async def obtener_raza_con_conteo(
    cod_raza: str = Path(..., description="Código de la raza"),
    db: Prisma = Depends(get_db)
):
    """Obtener una raza con el conteo de sus animales"""
    service = RazaService(db)
    return await service.get_raza_with_animals_count(cod_raza)

@router.put("/{cod_raza}", response_model=RazaResponse)
async def actualizar_raza(
    raza_data: RazaUpdate,
    cod_raza: str = Path(..., description="Código de la raza"),
    db: Prisma = Depends(get_db)
):
    """Actualizar una raza existente"""
    service = RazaService(db)
    return await service.update_raza(cod_raza, raza_data)

@router.delete("/{cod_raza}", status_code=204)
async def eliminar_raza(
    cod_raza: str = Path(..., description="Código de la raza"),
    db: Prisma = Depends(get_db)
):
    """Eliminar una raza (solo si no tiene animales asociados)"""
    service = RazaService(db)
    await service.delete_raza(cod_raza)