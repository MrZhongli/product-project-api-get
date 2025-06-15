# ============== ROUTES ==============

# app/routes/productos.py
from fastapi import APIRouter, HTTPException
from app.services.producto_service import ProductoService

router = APIRouter(prefix="/api/productos", tags=["productos"])

@router.get("/")
async def obtener_productos():
    response = await ProductoService.get_all()
    
    if response["status"] != 200:
        raise HTTPException(status_code=response["status"], detail=response["message"])
    
    return response

@router.get("/{producto_id}")
async def obtener_producto(producto_id: int):
    response = await ProductoService.get_one(producto_id)
    
    if response["status"] != 200:
        raise HTTPException(status_code=response["status"], detail=response["message"])
    
    return response
