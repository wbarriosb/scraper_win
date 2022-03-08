import psycopg2
import constants as cons

def Connect():
    conn_string = 'postgresql://' + cons.DB_USER+':' + cons.DB_PASS+'@' + cons.DB_HOST+'/' + cons.DB_NAME
    conn = psycopg2.connect(conn_string)
    return conn

def Disconnect(conn):
    conn.commit()
    conn.close()
