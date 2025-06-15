-- CreateTable
CREATE TABLE `productos` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `codigo` VARCHAR(5) NOT NULL,
    `nombre` VARCHAR(50) NOT NULL,
    `descripcion` TEXT NOT NULL,
    `cantidad` INTEGER NOT NULL,
    `precio` INTEGER NOT NULL,
    `impuesto` INTEGER NOT NULL,
    `imagen_url` VARCHAR(255) NULL,
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `updated_at` DATETIME(3) NOT NULL,

    UNIQUE INDEX `productos_codigo_key`(`codigo`),
    INDEX `productos_codigo_idx`(`codigo`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
