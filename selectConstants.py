import dbOps
import constants as cons
#
def selectTable():
    tableOK= True
    conn= dbOps.Connect()
    cursor= conn.cursor()
    try : 
        SQLstmt= "SELECT * FROM farmakon.constantes;" 
        cursor.execute(SQLstmt)
        valores= cursor.fetchall()
        constantes={}
        for i in range(len(valores)):
            tipo= valores[i][3]
            if tipo=='N':
                constantes[valores[i][1]]= int(valores[i][2])
            elif tipo=='B':
                constantes[valores[i][1]]= bool(valores[i][2])
            else :
                constantes[valores[i][1]]= str(valores[i][2])
        print(constantes)
    except Exception as e:
        tableOK= False
        print('Error en la base de datos')
        print(f'[ERROR] Contacta al Administrador de la Base de datos... {e}')
    dbOps.Disconnect(conn)
    return tableOK
#
if __name__=='__main__':
    tableOK= selectTable()
    print(tableOK)