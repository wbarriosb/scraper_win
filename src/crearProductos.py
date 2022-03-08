# Programa python para crear tabla farmakon.productos y cargar un CSV file
# con nuevos registros
import src.dbOps as dbOps
import src.constants as cons
import argparse
#
TAB_NAME= 'productos'
#
def createTable():
    tableOK= True
    conn= dbOps.Connect()
    cursor = conn.cursor()
    try : 
        SQLstmt= "CREATE TABLE IF NOT EXISTS "+ cons.DB_SCHEMA +"." + TAB_NAME + "(productoid serial PRIMARY KEY, productonom VARCHAR(50) NOT NULL, productofabr VARCHAR(50) NOT NULL, productocate VARCHAR(50) NOT NULL, created_user VARCHAR(30), created_date VARCHAR(30) DEFAULT current_timestamp);"
        cursor.execute(SQLstmt)
    except Exception as e:
        tableOK= False
        print(f'[ERROR] Contacta al Administrador de la Base de datos... {e}')
    dbOps.Disconnect(conn)
    return tableOK
# Function to check the initial parameters of job execution
def inputParse():
    description = ('Validador de parametros...')
    p = argparse.ArgumentParser(description= description)
    p.add_argument('-file_csv', '--file_csv', default= None, type= str,
                   help='path/to/file.csv (Linux) path\\to\\file.csv (Win)', required= True)
    args = p.parse_args()
    return args
#
def loadFile(file_csv):
    try: 
        conn= dbOps.Connect()
        cursor = conn.cursor()
        SQLstmt= "COPY "+ cons.DB_SCHEMA + "."+ TAB_NAME + "(productonom, productofabr, productocate, created_user) FROM '"+ file_csv + "' DELIMITER ';' CSV HEADER;" 
        cursor.execute(SQLstmt)
        print('[INFO] Archivo CSV cargado en la tabla de PRODUCTOS ...')
    except Exception as e:
        print(f'[ERROR] Falla al cargar archivo CSV en tabla de PRODUCTOS ... {e}')
    dbOps.Disconnect(conn)
#
def main(file_csv):
    tabON= createTable()
    if tabON:
        loadFile(file_csv)
        print('[INFO]: Proceso finalizado ...')
#
if __name__ == '__main__':
    args = inputParse()
    main(**vars(args))
