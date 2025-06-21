/*
  Warnings:

  - You are about to drop the `productos` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropTable
DROP TABLE `productos`;

-- CreateTable
CREATE TABLE `Razas` (
    `CodRaza` VARCHAR(50) NOT NULL,
    `Descripcion` VARCHAR(255) NOT NULL,

    PRIMARY KEY (`CodRaza`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `Animales` (
    `CodAnimal` VARCHAR(50) NOT NULL,
    `Descripcion` VARCHAR(255) NOT NULL,
    `Sexo` VARCHAR(10) NOT NULL,
    `Edad` INTEGER NOT NULL,
    `CodRaza` VARCHAR(50) NOT NULL,
    `ColorPelaje` VARCHAR(100) NOT NULL,
    `Color Ojos` VARCHAR(100) NOT NULL,

    PRIMARY KEY (`CodAnimal`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `Animales` ADD CONSTRAINT `Animales_CodRaza_fkey` FOREIGN KEY (`CodRaza`) REFERENCES `Razas`(`CodRaza`) ON DELETE RESTRICT ON UPDATE CASCADE;
