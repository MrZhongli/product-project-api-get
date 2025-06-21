from prisma import Prisma
from typing import AsyncGenerator
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instancia global de Prisma
prisma = Prisma()

async def connect_db():
    """Conectar a la base de datos"""
    try:
        await prisma.connect()
        logger.info("✅ Conexión a la base de datos establecida")
    except Exception as e:
        logger.error(f"❌ Error conectando a la base de datos: {e}")
        raise

async def disconnect_db():
    """Desconectar de la base de datos"""
    try:
        await prisma.disconnect()
        logger.info("✅ Desconexión de la base de datos exitosa")
    except Exception as e:
        logger.error(f"❌ Error desconectando de la base de datos: {e}")
        raise

async def get_db() -> AsyncGenerator[Prisma, None]:
    """Dependency para obtener la instancia de Prisma"""
    yield prisma
