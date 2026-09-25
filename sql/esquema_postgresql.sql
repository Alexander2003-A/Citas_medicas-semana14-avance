CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    stock INTEGER NOT NULL,
    id_proveedor INTEGER,
    FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
);

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    cedula VARCHAR(20),
    telefono VARCHAR(20),
    correo VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    fecha DATE NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);