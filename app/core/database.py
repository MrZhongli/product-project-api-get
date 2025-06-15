# app/core/database.py
from prisma import Prisma
# Instancia global de Prisma
prisma = Prisma()

async def connect_db():
    """Conectar a la base de datos"""
    await prisma.connect()

async def disconnect_db():
    """Desconectar de la base de datos"""
    await prisma.disconnect()

def get_db():
    """Obtener instancia de Prisma"""
    return prisma
