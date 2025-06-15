from prisma import Prisma
from prisma.models import Producto
from datetime import datetime
from typing import Optional, Dict, Any

prisma = Prisma()

class ProductoService:
    @staticmethod
    async def get_all() -> Dict[str, Any]:
        try:
            productos = await Producto.prisma().find_many()
            
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
            print(f"Error: {e}")
            return {
                'message': 'Algo salió mal, contacta al administrador',
                'status': 500,
                'data': None
            }

    @staticmethod
    async def get_one(id: int) -> Dict[str, Any]:
        try:
            producto = await Producto.prisma().find_unique(where={'id': id})
            
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
            print(f"Error: {e}")
            return {
                'message': 'Algo salió mal, contacta al administrador',
                'status': 500,
                'data': None
            }

    @staticmethod
    async def create_new(producto_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Validar campos requeridos
            required_fields = ['codigo', 'nombre', 'descripcion', 'cantidad', 'precio', 'impuesto']
            if not all(field in producto_data for field in required_fields):
                return {
                    'message': 'Faltan campos requeridos',
                    'status': 400,
                    'data': None
                }
                
            nuevo_producto = await Producto.prisma().create(data=producto_data)
            
            return {
                'message': 'Producto creado exitosamente',
                'status': 201,
                'data': {'producto': nuevo_producto}
            }
            
        except Exception as e:
            print(f"Error: {e}")
            return {
                'message': 'Error al crear producto, verifica los campos',
                'status': 500,
                'data': None
            }

    @staticmethod
    async def update_one(id: int, producto_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            producto = await Producto.prisma().find_unique(where={'id': id})
            
            if not producto:
                return {
                    'message': 'Producto no encontrado',
                    'status': 404,
                    'data': None
                }
                
            producto_actualizado = await Producto.prisma().update(
                where={'id': id},
                data=producto_data
            )
            
            return {
                'message': 'Producto actualizado exitosamente',
                'status': 200,
                'data': {'producto': producto_actualizado}
            }
            
        except Exception as e:
            print(f"Error: {e}")
            return {
                'message': 'Error al actualizar producto',
                'status': 500,
                'data': None
            }

    @staticmethod
    async def delete_one(id: int) -> Dict[str, Any]:
        try:
            producto = await Producto.prisma().find_unique(where={'id': id})
            
            if not producto:
                return {
                    'message': 'Producto no encontrado',
                    'status': 404,
                    'data': None
                }
                
            # Soft delete (marcar como eliminado)
            producto_eliminado = await Producto.prisma().update(
                where={'id': id},
                data={'deleted_at': datetime.now()}
            )
            
            return {
                'message': 'Producto eliminado exitosamente',
                'status': 200,
                'data': {'producto': producto_eliminado}
            }
            
        except Exception as e:
            print(f"Error: {e}")
            return {
                'message': 'Error al eliminar producto',
                'status': 500,
                'data': None
            }