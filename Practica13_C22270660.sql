#practica13.base de datos para la tortilleria Uziel
#autor:Gabriela Berenice Gomez Santiz
# \. C:\administraBASE\Practica13_C22270660.sql

CREATE DATABASE IF NOT EXISTS Practica13_C22270660;
USE Practica13_C22270660;

CREATE TABLE Trabajadores (
    id_trabajador INT PRIMARY KEY,
    nombre VARCHAR(255),
    numero_telefono VARCHAR(20)
);

CREATE TABLE Proveedores (
    id_proveedor INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    materia_prima VARCHAR(255) NOT NULL
);

CREATE TABLE Productos (  -- Se crea antes de MateriaPrima para evitar errores de referencia
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    formato_presentacion VARCHAR(255),
    precio DECIMAL(10,2)
);

CREATE TABLE MateriaPrima (
    id_materia INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    cantidad INT NOT NULL,
    costo DECIMAL(10,2) NOT NULL,
    id_proveedor INT,
    id_producto INT, 
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor) ON DELETE SET NULL,
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto) ON DELETE CASCADE
);

CREATE TABLE InventarioDiario (
    id_inventario INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT,
    id_trabajador INT,  -- Se agregó la columna antes de la clave foránea
    produccion INT NOT NULL,
    precio DECIMAL(10,2),
    unidades INT NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto) ON DELETE CASCADE,
    FOREIGN KEY (id_trabajador) REFERENCES Trabajadores(id_trabajador) ON DELETE SET NULL
);


