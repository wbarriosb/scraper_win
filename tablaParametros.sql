##########################################################################
# Script SQL para la creacion de un objeto en la base de datos
# Tipo de Objeto: tabla
# Nombre del esquema: farmakon
# Nombre de tabla: parametros
#
# Fecha: 2022-02-21
##########################################################################
CREATE TABLE farmakon.parametros (
	codigo serial PRIMARY KEY,
	variable VARCHAR (50) NOT NULL,
	valor VARCHAR (50) NOT NULL,
    	created_user VARCHAR(30),
    	created_date VARCHAR(30) DEFAULT current_timestamp,
		started_date VARCHAR(30),
		ended_date VARCHAR(30));


##########################################################################
# Script SQL para la insercion de la variable para controlar la ejecucion
# del proceso de Scraping
# Nombre del esquema: farmakon
# Nombre de tabla: parametros
## Fecha: 2022-02-21
##########################################################################
INSERT INTO farmakon.parametros (variable, valor, created_user, created_date, started_date, ended_date)
VALUES ('FLAG_JOB_EXEC', 'False', 'postgre', current_timestamp, current_timestamp, current_timestamp);

