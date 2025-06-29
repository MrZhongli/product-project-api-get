from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, List # Asegúrate de importar List si tu Python es < 3.9

class Settings(BaseSettings):
    # =========================================================================
    # CONFIGURACIONES DE BASES DE DATOS MÚLTIPLES (Coincide con tu .env)
    # =========================================================================

    # Configuración por defecto (mantener compatibilidad)
    database_url: str = Field(..., alias="DATABASE_URL")

    # CONFIGURACIÓN: desarrollo_mysql
    dev_mysql_db_provider: str = Field(..., alias="DEV_MYSQL_DB_PROVIDER")
    dev_mysql_db_host: str = Field(..., alias="DEV_MYSQL_DB_HOST")
    dev_mysql_db_port: int = Field(..., alias="DEV_MYSQL_DB_PORT") # Convertir a int
    dev_mysql_db_user: str = Field(..., alias="DEV_MYSQL_DB_USER")
    dev_mysql_db_password: str = Field(..., alias="DEV_MYSQL_DB_PASSWORD")
    dev_mysql_db_name: str = Field(..., alias="DEV_MYSQL_DB_NAME")

    # CONFIGURACIÓN: produccion_mysql
    prod_mysql_db_provider: str = Field(..., alias="PROD_MYSQL_DB_PROVIDER")
    prod_mysql_db_host: str = Field(..., alias="PROD_MYSQL_DB_HOST")
    prod_mysql_db_port: int = Field(..., alias="PROD_MYSQL_DB_PORT") # Convertir a int
    prod_mysql_db_user: str = Field(..., alias="PROD_MYSQL_DB_USER")
    prod_mysql_db_password: str = Field(..., alias="PROD_MYSQL_DB_PASSWORD")
    prod_mysql_db_name: str = Field(..., alias="PROD_MYSQL_DB_NAME")

    # CONFIGURACIÓN: desarrollo_postgresql
    dev_postgres_db_provider: str = Field(..., alias="DEV_POSTGRES_DB_PROVIDER")
    dev_postgres_db_host: str = Field(..., alias="DEV_POSTGRES_DB_HOST")
    dev_postgres_db_port: int = Field(..., alias="DEV_POSTGRES_DB_PORT") # Convertir a int
    dev_postgres_db_user: str = Field(..., alias="DEV_POSTGRES_DB_USER")
    dev_postgres_db_password: str = Field(..., alias="DEV_POSTGRES_DB_PASSWORD")
    dev_postgres_db_name: str = Field(..., alias="DEV_POSTGRES_DB_NAME")

    # CONFIGURACIÓN: produccion_postgresql
    prod_postgres_db_provider: str = Field(..., alias="PROD_POSTGRES_DB_PROVIDER")
    prod_postgres_db_host: str = Field(..., alias="PROD_POSTGRES_DB_HOST")
    prod_postgres_db_port: int = Field(..., alias="PROD_POSTGRES_DB_PORT") # Convertir a int
    prod_postgres_db_user: str = Field(..., alias="PROD_POSTGRES_DB_USER")
    prod_postgres_db_password: str = Field(..., alias="PROD_POSTGRES_DB_PASSWORD")
    prod_postgres_db_name: str = Field(..., alias="PROD_POSTGRES_DB_NAME")

    # CONFIGURACIÓN: clienteA_sqlite
    clientea_sqlite_db_provider: str = Field(..., alias="CLIENTEA_SQLITE_DB_PROVIDER")
    clientea_sqlite_db_path: str = Field(..., alias="CLIENTEA_SQLITE_DB_PATH")

    # CONFIGURACIÓN: clienteB_sqlite
    clienteb_sqlite_db_provider: str = Field(..., alias="CLIENTEB_SQLITE_DB_PROVIDER")
    clienteb_sqlite_db_path: str = Field(..., alias="CLIENTEB_SQLITE_DB_PATH")

    # CONFIGURACIÓN: testing
    test_db_provider: str = Field(..., alias="TEST_DB_PROVIDER")
    test_db_path: str = Field(..., alias="TEST_DB_PATH")

    # =========================================================================
    # CONFIGURACIONES GENERALES (Coincide con tu .env)
    # =========================================================================

    api_title: str = Field(..., alias="API_TITLE")
    api_description: str = Field(..., alias="API_DESCRIPTION")
    api_version: str = Field(..., alias="API_VERSION")
    
    # ENVIRONMENT también está en general
    environment: str = Field(..., alias="ENVIRONMENT")
    debug: bool = Field(..., alias="DEBUG") # Pydantic-settings manejará el booleano
    
    # Upload
    upload_dir: str = Field(..., alias="UPLOAD_DIR")
    max_file_size: int = Field(..., alias="MAX_FILE_SIZE") # Convertir a int

    # CORS - Nota: Pydantic-settings puede parsear listas si están bien formadas en .env (ej. ["*"])
    cors_origins: List[str] = Field(..., alias="CORS_ORIGINS")
    cors_methods: List[str] = Field(..., alias="CORS_METHODS")
    cors_headers: List[str] = Field(..., alias="CORS_HEADERS")


    # =========================================================================
    # CONFIGURACIÓN DE Pydantic-Settings (model_config para Pydantic v2+)
    # =========================================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive = False, # Establece esto en True si tus variables de entorno distinguen mayúsculas/minúsculas
        extra = "forbid" # Mantenemos 'forbid' porque ahora declaramos todo
    )

# Instancia de la configuración
settings = Settings()