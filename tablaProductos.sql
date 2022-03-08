##########################################################################
# Script SQL para la creacion de un objeto en la base de datos
# Tipo de Objeto: tabla
# Nombre del esquema: farmakon
# Nombre de tabla: productos
#
# Fecha: 2022-02-07
##########################################################################
CREATE TABLE farmakon.productos (
	productoid serial PRIMARY KEY,
	productonom VARCHAR (50) NOT NULL,
	productofabr VARCHAR (50) NOT NULL,
	productocate VARCHAR (50) NOT NULL,
    	created_user VARCHAR(30),
    	created_date VARCHAR(30) DEFAULT current_timestamp);