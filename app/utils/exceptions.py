from fastapi import HTTPException, status

class BaseAPIException(HTTPException):
    """Excepción base para la API"""
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundError(BaseAPIException):
    """Error cuando no se encuentra un recurso"""
    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)

class AlreadyExistsError(BaseAPIException):
    """Error cuando un recurso ya existe"""
    def __init__(self, detail: str = "El recurso ya existe"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)

class ValidationError(BaseAPIException):
    """Error de validación"""
    def __init__(self, detail: str = "Error de validación"):
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

class DatabaseError(BaseAPIException):
    """Error de base de datos"""
    def __init__(self, detail: str = "Error de base de datos"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AuthenticationError(BaseAPIException):
    """Error de autenticación"""
    def __init__(self, detail: str = "Error de autenticación"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

class AuthorizationError(BaseAPIException):
    """Error de autorización"""
    def __init__(self, detail: str = "No tiene permisos para realizar esta acción"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)