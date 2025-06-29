from fastapi import APIRouter, Depends, Query, Path, HTTPException, Header
from typing import List, Optional
from prisma import Prisma

from ..core.database_manager import get_db_client, get_available_db_configs
from ..services.animal_service import AnimalService
from ..schemas.animal import (
    AnimalCreate,
    AnimalUpdate,
    AnimalResponse,
    AnimalListResponse
)
from ..utils.exceptions import NotFoundError, AlreadyExistsError, ValidationError

router = APIRouter(prefix="/animales", tags=["Animales"])

async def get_animal_service(
    db_config_name: str = Query(
        default="desarrollo_mysql",
        description="Nombre de la configuración de base de datos a usar",
        example="desarrollo_mysql"
    )
) -> AnimalService:
    """
    Dependency para obtener el servicio de animales con la configuración de BD especificada
    """
    try:
        # Validar que la configuración existe
        available_configs = get_available_db_configs()
        if db_config_name not in available_configs:
            raise HTTPException(
                status_code=400,
                detail=f"Configuración de BD '{db_config_name}' no válida. "
                       f"Configuraciones disponibles: {available_configs}"
            )
        
        # Obtener cliente de base de datos
        db_client = await get_db_client(db_config_name)
        return AnimalService(db_client)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error conectando a la base de datos '{db_config_name}': {str(e)}"
        )

@router.get("/configs", response_model=dict)
async def get_database_configs():
    """
    Obtener lista de configuraciones de base de datos disponibles
    """
    return {
        "available_configs": get_available_db_configs(),
        "default_config": "desarrollo_mysql"
    }

@router.post("/", response_model=AnimalResponse, status_code=201)
async def crear_animal(
    animal_data: AnimalCreate,
    service: AnimalService = Depends(get_animal_service)
):
    """
    Crear un nuevo animal
    """
    try:
        return await service.create_animal(animal_data)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/", response_model=AnimalListResponse)
async def listar_animales(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    service: AnimalService = Depends(get_animal_service)
):
    """
    Obtener lista de animales con paginación
    """
    skip = (page - 1) * size
    animals, total = await service.get_all_animals(skip=skip, limit=size)
    
    return AnimalListResponse(
        animales=animals,
        total=total,
        page=page,
        size=size
    )

@router.get("/{cod_animal}", response_model=AnimalResponse)
async def obtener_animal(
    cod_animal: str = Path(..., description="Código del animal"),
    service: AnimalService = Depends(get_animal_service)
):
    """
    Obtener un animal específico por su código
    """
    try:
        return await service.get_animal_by_code(cod_animal)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{cod_animal}", response_model=AnimalResponse)
async def actualizar_animal(
    cod_animal: str = Path(..., description="Código del animal"),
    animal_data: AnimalUpdate = ...,
    service: AnimalService = Depends(get_animal_service)
):
    """
    Actualizar un animal existente
    """
    try:
        return await service.update_animal(cod_animal, animal_data)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.delete("/{cod_animal}", status_code=204)
async def eliminar_animal(
    cod_animal: str = Path(..., description="Código del animal"),
    service: AnimalService = Depends(get_animal_service)
):
    """
    Eliminar un animal
    """
    try:
        await service.delete_animal(cod_animal)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Ejemplo de endpoint que permite especificar la BD en el header (alternativa)
@router.get("/advanced/search", response_model=AnimalListResponse)
async def buscar_animales_avanzado(
    search_term: str = Query(..., description="Término de búsqueda"),
    db_config: str = Header(
        default="desarrollo_mysql",
        alias="X-Database-Config",
        description="Configuración de base de datos a usar"
    ),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    """
    Búsqueda avanzada de animales especificando la BD en el header
    """
    try:
        # Validar configuración
        available_configs = get_available_db_configs()
        if db_config not in available_configs:
            raise HTTPException(
                status_code=400,
                detail=f"Configuración de BD '{db_config}' no válida"
            )
        
        # Obtener cliente y servicio
        db_client = await get_db_client(db_config)
        service = AnimalService(db_client)
        
        # --- Aquí iría la lógica de búsqueda real, por ejemplo:
        # animals, total = await service.search_animals(search_term, skip=(page - 1) * size, limit=size)
        # return AnimalListResponse(animales=animals, total=total, page=page, size=size)
        
        # Como es un ejemplo y la lógica no está implementada, retornamos una lista vacía por ahora
        return AnimalListResponse(animales=[], total=0, page=page, size=size)

    except HTTPException as e:
        # Relanza las HTTPException ya definidas (por ejemplo, la 400 por configuración inválida)
        raise e
    except Exception as e:
        # Captura cualquier otra excepción inesperada y la convierte en un error 500
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor durante la búsqueda avanzada: {str(e)}"
        )