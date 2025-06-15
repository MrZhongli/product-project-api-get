from prisma import Prisma
from typing import Dict, Any

prisma = Prisma()

class ProductoService:
    @staticmethod
    async def get_all() -> Dict[str, Any]:
        try:
            await prisma.connect()
            productos = await prisma.producto.find_many()
            await prisma.disconnect()
            
            if not productos:
                return {
                    'message': 'No se encontraron productos',
                    'status': 404,
                    'data': {'productos': []}
                }
                
            return {
                'message': 'Productos encontrados',
                'status': 200,
                'data': {'productos': productos}
            }
            
        except Exception as e:
            print(f"Error tipo: {type(e).__name__}, mensaje: {e}")
            return {
                'message': 'Algo salió mal, contacta al administrador',
                'status': 500,
                'data': None
            }

    @staticmethod
    async def get_one(id: int) -> Dict[str, Any]:
        try:
            await prisma.connect()
            producto = await prisma.producto.find_unique(where={'id': id})
            await prisma.disconnect()
            
            if not producto:
                return {
                    'message': 'Producto no encontrado',
                    'status': 404,
                    'data': None
                }
                
            return {
                'message': 'Producto encontrado',
                'status': 200,
                'data': {'producto': producto}
            }
            
        except Exception as e:
            print(f"Error tipo: {type(e).__name__}, mensaje: {e}")
            return {
                'message': 'Algo salió mal, contacta al administrador',
                'status': 500,
                'data': None
            }
