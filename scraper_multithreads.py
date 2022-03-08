import threading
import psutil
import psycopg2
import datetime as dt
import pandas as pd
import warnings
import sys
import os
import dbOps
import constants as cons
from sqlalchemy import create_engine
from GoogleImageScraper import GoogleImageScraper
from scriptSodapy import run_api

def LoadDFMinS():
    report_file= cons.INPUT_FILE
    try:
        df= pd.read_excel(report_file, skiprows=cons.SKIP_ROWS, sheet_name='Precio_CUM', usecols={'CUM','Medicamento','EXPEDIENTE','PRODUCTO','TITULAR','REGISTRO SANITARIO','PRINCIPIO ACTIVO'})
        # Change Column Names
        df.columns = ['cum','medicamento', 'expediente','producto','fabricante','registro','principio_activo']
    except:
        sys.exit(f"[ERROR] leyendo Archivo: {report_file}")
    df = df.dropna()
    # Replace special char \ o /
    df.replace(to_replace=r'/', value=' ', regex=True, inplace=True)
    df.replace(to_replace=r'®', value=' ', regex=True, inplace=True)
    df.replace(to_replace=r'\\', value=' ', regex=True, inplace=True)
    return df

def DFtoTable(df):
    # Load Dataframe into Postgre table named DB_TABLE
    conn_string = 'postgresql://' + cons.DB_USER+':' + cons.DB_PASS+'@' + cons.DB_HOST+'/' + cons.DB_NAME
    datab = create_engine(conn_string)
    conn = datab.connect()
    df.to_sql(cons.DB_TABLE, con=conn, schema=cons.DB_SCHEMA, if_exists='replace', index=False)
    conn = psycopg2.connect(conn_string)
    conn.autocommit = True
    # Adding new columns to table Created User and Created Date
    cursor = conn.cursor()
    date_exec= dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('ALTER TABLE %s.%s ADD COLUMN %s text' % (cons.DB_SCHEMA, cons.DB_TABLE, 'categoria'))
    cursor.execute('ALTER TABLE %s.%s ADD COLUMN %s text' % (cons.DB_SCHEMA, cons.DB_TABLE, 'created_user'))
    cursor.execute('ALTER TABLE %s.%s ADD COLUMN %s text' % (cons.DB_SCHEMA, cons.DB_TABLE, 'created_date'))
    cursor.execute("UPDATE %s.%s SET %s= '%s', %s= '%s', %s= '%s';" % (cons.DB_SCHEMA, cons.DB_TABLE, 'categoria', cons.CATEGORY_DEFAULT,'created_user', cons.DB_USER, 'created_date', date_exec)) 
    dbOps.Disconnect(conn)
#
def LoadDataAPI(df):    
    conn= dbOps.Connect()
    cursor = conn.cursor()   
    for index, row in df.iterrows():
        try:
            date_exec= dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO "+cons.DB_SCHEMA+"."+cons.DB_TABLE+" VALUES (Null, '%s', Null, '%s', '%s', Null, '%s', '%s', '%s', '%s');" % (row[4], row[4] + " " + row[5], row[5], row[0], cons.CATEGORY_DEFAULT, cons.DB_USER, date_exec))
        except Exception as Error:
            print( f"[ERROR] al Insertar Registros en Tabla {cons.DB_TABLE}: {Error}")
    dbOps.Disconnect(conn)
#
def ListProductToScraper():
    conn= dbOps.Connect()
    cursor = conn.cursor()
    productList= []
    SQLstmt = "SELECT DISTINCT producto, categoria FROM " + cons.DB_SCHEMA + "." + cons.DB_TABLE + " ORDER BY 1 ASC;"
    cursor.execute(SQLstmt)
    # for row in cursor.fetchall():
    #     productList.append(row[0], row[1])   # Creating Product List
    # #
    productList= cursor.fetchall()
    dbOps.Disconnect(conn)
    return productList
#
def ListNotProducts():
    conn= dbOps.Connect()
    cursor = conn.cursor()
    SQLstmt = "SELECT * FROM " + cons.DB_SCHEMA + ".productos;"
    cursor.execute(SQLstmt)
    for row in cursor.fetchall():
        try:
            date_exec= dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO "+cons.DB_SCHEMA+"."+cons.DB_TABLE+" VALUES (Null, '%s', Null, '%s', '%s', Null, Null, '%s', '%s', '%s');" % (row[1], row[1], row[2], row[3], cons.DB_USER, date_exec))
        except Exception as Error:
            print( f"[ERROR] al Insertar Registros en Tabla {cons.DB_TABLE}: {Error}")
    #
    dbOps.Disconnect(conn)
#
def UpdFlagJob(flag_valor):
    try: 
        conn= dbOps.Connect()
        cursor = conn.cursor()
        if flag_valor== 'True':
            SQLstmt = "UPDATE "+ cons.DB_SCHEMA + ".parametros SET valor= %s , started_date= current_timestamp, ended_date= '' WHERE variable='" + cons.VAR_STATUS_JOB + "';"
        else :
            SQLstmt = "UPDATE "+ cons.DB_SCHEMA + ".parametros SET valor= %s , ended_date= current_timestamp WHERE variable='" + cons.VAR_STATUS_JOB + "';"
        cursor.execute(SQLstmt, (flag_valor,))
        conn.commit()
    except Exception as Error:
            print( f"[ERROR] al actualizar FLAG_JOB_EXEC en Tabla de parametros:  {Error}")
    dbOps.Disconnect(conn)
#
def GenerateImages(keys):
    # image_path = os.getcwd()+"\\"+cons.IMAGE_FOLDER
    headless = True
    print("Starting process ... Images Generator --->")
    print(f"There are {len(keys)}  items...")
    i= 1
    for key in keys:
        search_key= key[0].rstrip()
        category_path= key[1].rstrip()
        image_path = os.getcwd()+"\\"+cons.IMAGE_FOLDER+"\\"+category_path
        print(f"Item No. {i}: {search_key} ")
        image_scrapper = GoogleImageScraper(cons.WEBDRIVER_PATH, image_path, search_key, cons.IMAGE_NUM, headless, cons.MIN_RESOLUTION, cons.MAX_RESOLUTION)
        image_urls = image_scrapper.find_image_urls()
        image_scrapper.save_images(image_urls)
        i += 1
    print("Ending process ... Images Generator ****")
#
def GetCores():
    return psutil.cpu_count()
#
if __name__ == '__main__':
    UpdFlagJob('True')
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'Starting....')
    if cons.NUM_THREADS == -1:
        cons.NUM_THREADS= GetCores()
    if cons.NUM_THREADS<=0:
        print( f"[ERROR] no hay LOGICAL CPUs suficientes para ejecutar el proceso... ")
    else :
        print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'Loading data ...')
        dataframe= LoadDFMinS()
        if len(dataframe.index) == 0:
            print('Precio-regulado-MinSalud file without records ...')
        else :
            print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'Loading table ...')
            DFtoTable(dataframe)
            # Validate API Datos.gov.co flag execution
            if cons.API_RUN:
                print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'Loading data from API datos.gov ...')
                df= run_api()
                if len(df.index) != 0:
                    LoadDataAPI(df)
                else :
                    print('API-Datos.gov.co Dataframe without records ...')
            #
            if cons.FLAG_NODRUGS:
                print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'Loading table items no-drugs ...')
                ListNotProducts()
            #
            print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'Generating images ...')
            items= ListProductToScraper()

            size_df= int(len(items)//cons.NUM_THREADS)
            # Executing by scraping threads according to NUM_THREADS constant
            for i in range(cons.NUM_THREADS-1):
                nom_thread= "scraper_"+str(i)
                threadScraper= threading.Thread(name=nom_thread, target= GenerateImages, args=(items[i*size_df: (i+1)*size_df],))
                threadScraper.start()
            nom_thread= "scraper_"+str(cons.NUM_THREADS-1)
            threadScraper= threading.Thread(name=nom_thread, target= GenerateImages, args=(items[(cons.NUM_THREADS-1)*size_df:],))
            threadScraper.start()
            # Thread Main
            threadMain= threading.main_thread()
            #
            for threadScraper in threading.enumerate():
                if threadScraper is threadMain:
                    continue
                threadScraper.join()
            #
    # Setea a FALSO variable FLAG_JOB_EXEC
    UpdFlagJob('False')
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'Ending process ...')