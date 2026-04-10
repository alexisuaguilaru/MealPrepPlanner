import os
from sqlalchemy import create_engine

DB_ROLE_LOAD_DATA_PASS = os.getenv('DB_ROLE_LOAD_DATA_PASS','load_data_pass')
SUPBASE_HOST = os.getenv('SUPBASE_HOST','localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT',5432)
POSTGRES_DB = os.getenv('POSTGRES_DB','supabase_db')

def CreateConnectionToSQL():
    EngineSQL = create_engine(
        f'postgresql+psycopg2://loader_data:{DB_ROLE_LOAD_DATA_PASS}@{SUPBASE_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}',
    )
    return EngineSQL