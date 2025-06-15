# ============== ARCHIVOS DE CONFIGURACIÓN ==============

# requirements.txt
"""
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy[asyncio]==2.0.23
aiomysql==0.2.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
python-dotenv==1.0.0
"""

# .env
"""
DATABASE_URL="mysql://root:password@localhost:3306/productos_db"
UPLOAD_DIR=app/uploads/images
MAX_FILE_SIZE=5242880
"""

# ============== COMANDOS PRISMA ==============
"""
# Instalar dependencias
pip install -r requirements.txt

# Generar el cliente Prisma
prisma generate

# Ejecutar migraciones (crear tablas)
prisma db push

# O crear una migración
prisma migrate dev --name init

# Ver la base de datos (Prisma Studio)
prisma studio

# Ejecutar el servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

# ============== SCRIPT SQL INICIAL ==============
# create_database.sql
"""
CREATE DATABASE IF NOT EXISTS productos_db CHARACTER SET utf8mb4;

-- Datos de prueba (ejecutar después de prisma db push)
USE productos_db;

INSERT INTO productos (codigo, nombre, descripcion, cantidad, precio, impuesto, created_at, updated_at) VALUES
('P001', 'Laptop', 'Laptop HP 15 pulgadas', 10, 15000, 2400, NOW(), NOW()),
('P002', 'Mouse', 'Mouse inalámbrico', 50, 350, 56, NOW(), NOW()),
('P003', 'Teclado', 'Teclado mecánico', 25, 1200, 192, NOW(), NOW());
"""