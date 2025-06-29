import os
import logging
from typing import Dict, Optional, Any
from prisma import Prisma
from contextlib import asynccontextmanager
import asyncio
from functools import lru_cache

logger = logging.getLogger(__name__)

class DatabaseConfigError(Exception):
    """Excepción para errores de configuración de base de datos"""
    pass

class DatabaseConnectionError(Exception):
    """Excepción para errores de conexión de base de datos"""
    pass

class DatabaseManager:
    """
    Gestor de múltiples configuraciones de base de datos.
    Permite conectar a diferentes bases de datos basado en configuraciones predefinidas.
    """
    
    def __init__(self):
        self._connections: Dict[str, Prisma] = {}
        self._connection_strings: Dict[str, str] = {}
        self._config_mappings = {
            "desarrollo_mysql": "DEV_MYSQL",
            "produccion_mysql": "PROD_MYSQL", 
            "desarrollo_postgresql": "DEV_POSTGRES",
            "produccion_postgresql": "PROD_POSTGRES",
            "clienteA_sqlite": "CLIENTEA_SQLITE",
            "clienteB_sqlite": "CLIENTEB_SQLITE",
            "testing": "TEST"
        }

    def _build_connection_string(self, config: Dict[str, Any]) -> str:
        """Construye la cadena de conexión basada en la configuración"""
        provider = config.get('provider', '').lower()
        
        if provider == 'mysql':
            return (f"mysql://{config['user']}:{config['password']}"
                   f"@{config['host']}:{config['port']}/{config['database']}")
        
        elif provider == 'postgresql':
            return (f"postgresql://{config['user']}:{config['password']}"
                   f"@{config['host']}:{config['port']}/{config['database']}")
        
        elif provider == 'sqlite':
            db_path = config.get('path', './default.db')
            return f"file:{db_path}"
        
        else:
            raise DatabaseConfigError(f"Proveedor de base de datos no soportado: {provider}")

    @lru_cache(maxsize=10)
    def load_db_config(self, config_name: str) -> Dict[str, Any]:
        """
        Carga la configuración de base de datos desde las variables de entorno
        
        Args:
            config_name: Nombre de la configuración (ej: 'desarrollo_mysql')
            
        Returns:
            Dict con la configuración de la base de datos
            
        Raises:
            DatabaseConfigError: Si la configuración no existe o está incompleta
        """
        if config_name not in self._config_mappings:
            available_configs = list(self._config_mappings.keys())
            raise DatabaseConfigError(
                f"Configuración '{config_name}' no encontrada. "
                f"Configuraciones disponibles: {available_configs}"
            )
        
        prefix = self._config_mappings[config_name]
        
        # Casos especiales para SQLite
        if 'SQLITE' in prefix:
            provider = os.getenv(f"{prefix}_DB_PROVIDER")
            path = os.getenv(f"{prefix}_DB_PATH")
            
            if not provider or not path:
                raise DatabaseConfigError(
                    f"Configuración incompleta para {config_name}. "
                    f"Se requieren: {prefix}_DB_PROVIDER, {prefix}_DB_PATH"
                )
            
            return {
                'provider': provider,
                'path': path
            }
        
        # Configuración para MySQL/PostgreSQL
        required_vars = ['PROVIDER', 'HOST', 'PORT', 'USER', 'PASSWORD', 'NAME']
        config = {}
        missing_vars = []
        
        for var in required_vars:
            env_var = f"{prefix}_DB_{var}"
            value = os.getenv(env_var)
            if not value:
                missing_vars.append(env_var)
            else:
                key = var.lower()
                if key == 'name':
                    key = 'database'
                config[key] = value
        
        if missing_vars:
            raise DatabaseConfigError(
                f"Configuración incompleta para {config_name}. "
                f"Variables faltantes: {missing_vars}"
            )
        
        return config

    async def get_prisma_client(self, config_name: str) -> Prisma:
        """
        Obtiene una instancia de PrismaClient conectada para la configuración especificada
        
        Args:
            config_name: Nombre de la configuración de base de datos
            
        Returns:
            Instancia de Prisma conectada
            
        Raises:
            DatabaseConfigError: Si la configuración no existe
            DatabaseConnectionError: Si falla la conexión
        """
        # Si ya existe una conexión activa, la retornamos
        if config_name in self._connections:
            client = self._connections[config_name]
            try:
                # Verificar que la conexión sigue activa
                await client.execute_raw("SELECT 1")
                return client
            except Exception as e:
                logger.warning(f"Conexión existente para {config_name} no válida: {e}")
                # Remover la conexión inválida
                await self._disconnect_client(config_name)
        
        try:
            # Cargar configuración
            config = self.load_db_config(config_name)
            connection_string = self._build_connection_string(config)
            
            # Crear nueva instancia de Prisma
            # Nota: Prisma Python requiere que la URL esté en DATABASE_URL para el cliente
            original_db_url = os.environ.get('DATABASE_URL')
            os.environ['DATABASE_URL'] = connection_string
            
            try:
                client = Prisma()
                await client.connect()
                
                # Verificar conexión
                await client.execute_raw("SELECT 1")
                
                # Guardar cliente y cadena de conexión
                self._connections[config_name] = client
                self._connection_strings[config_name] = connection_string
                
                logger.info(f"Conexión establecida exitosamente para configuración: {config_name}")
                return client
                
            finally:
                # Restaurar DATABASE_URL original
                if original_db_url:
                    os.environ['DATABASE_URL'] = original_db_url
                else:
                    os.environ.pop('DATABASE_URL', None)
                    
        except Exception as e:
            logger.error(f"Error conectando a la base de datos {config_name}: {e}")
            raise DatabaseConnectionError(f"No se pudo conectar a {config_name}: {str(e)}")

    async def _disconnect_client(self, config_name: str):
        """Desconecta un cliente específico"""
        if config_name in self._connections:
            try:
                await self._connections[config_name].disconnect()
            except Exception as e:
                logger.error(f"Error desconectando cliente {config_name}: {e}")
            finally:
                del self._connections[config_name]
                self._connection_strings.pop(config_name, None)

    async def disconnect_all(self):
        """Desconecta todos los clientes activos"""
        for config_name in list(self._connections.keys()):
            await self._disconnect_client(config_name)
        
        logger.info("Todas las conexiones de base de datos han sido cerradas")

    def get_available_configs(self) -> list[str]:
        """Retorna la lista de configuraciones disponibles"""
        return list(self._config_mappings.keys())

    def get_active_connections(self) -> list[str]:
        """Retorna la lista de conexiones activas"""
        return list(self._connections.keys())

    @asynccontextmanager
    async def get_db_session(self, config_name: str):
        """
        Context manager para obtener una sesión de base de datos
        
        Usage:
            async with db_manager.get_db_session('desarrollo_mysql') as db:
                result = await db.animal.find_many()
        """
        client = await self.get_prisma_client(config_name)
        try:
            yield client
        except Exception as e:
            logger.error(f"Error en sesión de base de datos {config_name}: {e}")
            raise
        # No cerramos la conexión aquí ya que se mantiene en caché

# Instancia global del gestor
db_manager = DatabaseManager()

# Funciones de conveniencia
async def get_db_client(config_name: str) -> Prisma:
    """Función de conveniencia para obtener un cliente de base de datos"""
    return await db_manager.get_prisma_client(config_name)

def get_available_db_configs() -> list[str]:
    """Función de conveniencia para obtener configuraciones disponibles"""
    return db_manager.get_available_configs()