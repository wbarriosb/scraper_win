#-----------------------------------------------------------------------#
# Database Parameters
DB_HOST= 'localhost'
DB_NAME='postgres'
DB_USER= 'wbarrios'
DB_PASS= 'wabb2442'
DB_SCHEMA= 'farmakon'
DB_TABLE= 'medicamentos'
#-----------------------------------------------------------------------#
# Scraper Parameters
WEBDRIVER_PATH= 'chromedriver.exe'
IMAGE_FOLDER= 'IMAGENES'
IMAGE_NUM= 3
MIN_RESOLUTION= (0, 0)              # Min Resolution (width,height)
MAX_RESOLUTION= (1920, 1080)        # Max Resolution (width,height)
NUM_THREADS= 4
CATEGORY_DEFAULT= 'FARMACIA'
VAR_STATUS_JOB= 'FLAG_JOB_EXEC'
#-----------------------------------------------------------------------#
# Data Source MinSalud
INPUT_FILE= 'Precios-regulado-referencia-AGOSTO-2021-15-09-2021.xlsx'   # Reporte MinSalud
SKIP_ROWS= 8
#-----------------------------------------------------------------------#
# Data Source: API "3t73-n4q9" from DATOS.GOV.CO
TOKEN= 'skiR8IodQ7IgyGlfHIVkmrUsL'
REGS_LIMIT= 4
API_RUN= True
#-----------------------------------------------------------------------#
# Data Source: Table of Items No-Drugs
FLAG_NODRUGS= False