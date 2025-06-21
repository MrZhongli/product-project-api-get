from prisma import Prisma
from typing import List, Optional
from ..schemas.animal import AnimalCreate, AnimalUpdate, AnimalResponse
from ..utils.exceptions import NotFoundError, AlreadyExistsError
import logging

logger = logging.getLogger(__name__)

class AnimalService:
    def __init__(self, db: Prisma):
        self.db = db

    async def create_animal(self, animal_data: AnimalCreate) -> AnimalResponse:
        """Crear un nuevo animal"""
        try:
            # Verificar si ya existe un animal con ese código
            existing = await self.db.animal.find_unique(
                where={"codAnimal": animal_data.cod_animal}
            )
            if existing:
                raise AlreadyExistsError(f"Animal con código {animal_data.cod_animal} ya existe")
            
            # Verificar si la raza existe
            raza = await self.db.raza.find_unique(
                where={"codRaza": animal_data.cod_raza}
            )
            if not raza:
                raise NotFoundError(f"Raza con código {animal_data.cod_raza} no encontrada")
            
            # Crear el animal
            animal = await self.db.animal.create(
                data={
                    "codAnimal": animal_data.cod_animal,
                    "descripcion": animal_data.descripcion,
                    "sexo": animal_data.sexo,
                    "edad": animal_data.edad,
                    "codRaza": animal_data.cod_raza,
                    "colorPelaje": animal_data.color_pelaje,
                    "colorOjos": animal_data.color_ojos,
                },
                include={"raza": True}
            )
            
            logger.info(f"Animal creado: {animal.codAnimal}")
            return animal
            
        except Exception as e:
            logger.error(f"Error creando animal: {e}")
            raise

    async def get_animal_by_code(self, cod_animal: str) -> AnimalResponse:
        """Obtener un animal por su código"""
        animal = await self.db.animal.find_unique(
            where={"codAnimal": cod_animal},
            include={"raza": True}
        )
        
        if not animal:
            raise NotFoundError(f"Animal con código {cod_animal} no encontrado")
        
        return animal

    async def get_all_animals(self, skip: int = 0, limit: int = 100) -> tuple[List[AnimalResponse], int]:
        """Obtener todos los animales con paginación"""
        animals = await self.db.animal.find_many(
            skip=skip,
            take=limit,
            include={"raza": True},
            order={"codAnimal": "asc"}
        )
        
        total = await self.db.animal.count()
        
        return animals, total

    async def update_animal(self, cod_animal: str, animal_data: AnimalUpdate) -> AnimalResponse:
        """Actualizar un animal"""
        # Verificar si el animal existe
        existing = await self.db.animal.find_unique(
            where={"codAnimal": cod_animal}
        )
        if not existing:
            raise NotFoundError(f"Animal con código {cod_animal} no encontrado")
        
        # Preparar datos para actualizar (solo campos no nulos)
        update_data = {}
        if animal_data.descripcion is not None:
            update_data["descripcion"] = animal_data.descripcion
        if animal_data.sexo is not None:
            update_data["sexo"] = animal_data.sexo
        if animal_data.edad is not None:
            update_data["edad"] = animal_data.edad
        if animal_data.cod_raza is not None:
            # Verificar si la nueva raza existe
            raza = await self.db.raza.find_unique(
                where={"codRaza": animal_data.cod_raza}
            )
            if not raza:
                raise NotFoundError(f"Raza con código {animal_data.cod_raza} no encontrada")
            update_data["codRaza"] = animal_data.cod_raza
        if animal_data.color_pelaje is not None:
            update_data["colorPelaje"] = animal_data.color_pelaje
        if animal_data.color_ojos is not None:
            update_data["colorOjos"] = animal_data.color_ojos
        
        # Actualizar el animal
        animal = await self.db.animal.update(
            where={"codAnimal": cod_animal},
            data=update_data,
            include={"raza": True}
        )
        
        logger.info(f"Animal actualizado: {cod_animal}")
        return animal

    async def delete_animal(self, cod_animal: str) -> bool:
        """Eliminar un animal"""
        # Verificar si el animal existe
        existing = await self.db.animal.find_unique(
            where={"codAnimal": cod_animal}
        )
        if not existing:
            raise NotFoundError(f"Animal con código {cod_animal} no encontrado")
        
        # Eliminar el animal
        await self.db.animal.delete(
            where={"codAnimal": cod_animal}
        )
        
        logger.info(f"Animal eliminado: {cod_animal}")
        return True

    async def get_animals_by_raza(self, cod_raza: str, skip: int = 0, limit: int = 100) -> tuple[List[AnimalResponse], int]:
        """Obtener animales por raza"""
        animals = await self.db.animal.find_many(
            where={"codRaza": cod_raza},
            skip=skip,
            take=limit,
            include={"raza": True},
            order={"codAnimal": "asc"}
        )
        
        total = await self.db.animal.count(
            where={"codRaza": cod_raza}
        )
        
        return animals, total