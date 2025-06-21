from prisma import Prisma
from typing import List, Optional
from ..schemas.raza import RazaCreate, RazaUpdate, RazaResponse, RazaWithAnimalsResponse
from ..utils.exceptions import NotFoundError, AlreadyExistsError, ValidationError
import logging

logger = logging.getLogger(__name__)

class RazaService:
    def __init__(self, db: Prisma):
        self.db = db

    async def create_raza(self, raza_data: RazaCreate) -> RazaResponse:
        """Crear una nueva raza"""
        try:
            # Verificar si ya existe una raza con ese código
            existing = await self.db.raza.find_unique(
                where={"codRaza": raza_data.cod_raza}
            )
            if existing:
                raise AlreadyExistsError(f"Raza con código {raza_data.cod_raza} ya existe")
            
            # Crear la raza
            raza = await self.db.raza.create(
                data={
                    "codRaza": raza_data.cod_raza,
                    "descripcion": raza_data.descripcion,
                }
            )
            
            logger.info(f"Raza creada: {raza.codRaza}")
            return raza
            
        except Exception as e:
            logger.error(f"Error creando raza: {e}")
            raise

    async def get_raza_by_code(self, cod_raza: str) -> RazaResponse:
        """Obtener una raza por su código"""
        raza = await self.db.raza.find_unique(
            where={"codRaza": cod_raza}
        )
        
        if not raza:
            raise NotFoundError(f"Raza con código {cod_raza} no encontrada")
        
        return raza

    async def get_raza_with_animals_count(self, cod_raza: str) -> RazaWithAnimalsResponse:
        """Obtener una raza con el conteo de sus animales"""
        raza = await self.db.raza.find_unique(
            where={"codRaza": cod_raza},
            include={"_count": {"select": {"animales": True}}}
        )
        
        if not raza:
            raise NotFoundError(f"Raza con código {cod_raza} no encontrada")
        
        # Convertir a response schema
        raza_response = RazaWithAnimalsResponse(
            cod_raza=raza.codRaza,
            descripcion=raza.descripcion,
            total_animales=raza._count.animales if hasattr(raza, '_count') else 0
        )
        
        return raza_response

    async def get_all_razas(self, skip: int = 0, limit: int = 100) -> tuple[List[RazaResponse], int]:
        """Obtener todas las razas con paginación"""
        razas = await self.db.raza.find_many(
            skip=skip,
            take=limit,
            order={"codRaza": "asc"}
        )
        
        total = await self.db.raza.count()
        
        return razas, total

    async def update_raza(self, cod_raza: str, raza_data: RazaUpdate) -> RazaResponse:
        """Actualizar una raza"""
        # Verificar si la raza existe
        existing = await self.db.raza.find_unique(
            where={"codRaza": cod_raza}
        )
        if not existing:
            raise NotFoundError(f"Raza con código {cod_raza} no encontrada")
        
        # Preparar datos para actualizar (solo campos no nulos)
        update_data = {}
        if raza_data.descripcion is not None:
            update_data["descripcion"] = raza_data.descripcion
        
        if not update_data:
            raise ValidationError("No se proporcionaron datos para actualizar")
        
        # Actualizar la raza
        raza = await self.db.raza.update(
            where={"codRaza": cod_raza},
            data=update_data
        )
        
        logger.info(f"Raza actualizada: {cod_raza}")
        return raza

    async def delete_raza(self, cod_raza: str) -> bool:
        """Eliminar una raza"""
        # Verificar si la raza existe
        existing = await self.db.raza.find_unique(
            where={"codRaza": cod_raza}
        )
        if not existing:
            raise NotFoundError(f"Raza con código {cod_raza} no encontrada")
        
        # Verificar si hay animales asociados a esta raza
        animals_count = await self.db.animal.count(
            where={"codRaza": cod_raza}
        )
        
        if animals_count > 0:
            raise ValidationError(
                f"No se puede eliminar la raza {cod_raza} porque tiene {animals_count} animales asociados"
            )
        
        # Eliminar la raza
        await self.db.raza.delete(
            where={"codRaza": cod_raza}
        )
        
        logger.info(f"Raza eliminada: {cod_raza}")
        return True

    async def get_razas_with_animal_count(self, skip: int = 0, limit: int = 100) -> tuple[List[RazaWithAnimalsResponse], int]:
        """Obtener todas las razas con conteo de animales"""
        razas = await self.db.raza.find_many(
            skip=skip,
            take=limit,
            include={"_count": {"select": {"animales": True}}},
            order={"codRaza": "asc"}
        )
        
        total = await self.db.raza.count()
        
        # Convertir a response schema
        razas_response = [
            RazaWithAnimalsResponse(
                cod_raza=raza.codRaza,
                descripcion=raza.descripcion,
                total_animales=raza._count.animales if hasattr(raza, '_count') else 0
            )
            for raza in razas
        ]
        
        return razas_response, total