# ============== ROUTES ==============

# app/routes/productos.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from decimal import Decimal
from prisma import Prisma

from app.core.database import get_db
from app.services.producto_service import ProductoService
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse, ApiResponse

router = APIRouter(prefix="/api/productos", tags=["productos"])

def get_producto_service(db: Prisma = Depends(get_db)) -> ProductoService:
    return ProductoService(db)

@router.get("/", response_model=ApiResponse)
async def obtener_productos(
    service: ProductoService = Depends(get_producto_service)
):
    try:
        productos = await service.obtener_productos()
        productos_response = [ProductoResponse.from_orm(p) for p in productos]
        
        return ApiResponse(
            success=True,
            message="Productos obtenidos exitosamente",
            data={
                "productos": [p.dict() for p in productos_response],
                "total": len(productos_response)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/{producto_id}", response_model=ApiResponse)
async def obtener_producto(
    producto_id: int,
    service: ProductoService = Depends(get_producto_service)
):
    try:
        producto = await service.obtener_producto_por_id(producto_id)
        return ApiResponse(
            success=True,
            message="Producto encontrado",
            data=ProductoResponse.from_orm(producto).dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
