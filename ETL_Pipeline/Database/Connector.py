import os
import time
from sqlalchemy import create_engine
from postgrest import SyncPostgrestClient
import jwt

DB_ROLE_LOAD_DATA_PASS = os.getenv('DB_ROLE_LOAD_DATA_PASS','load_data_pass')
SUPBASE_HOST = os.getenv('SUPBASE_HOST','localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT',5432)
POSTGRES_DB = os.getenv('POSTGRES_DB','supabase_db')
SCHEMA_DB = os.getenv('SCHEMA_DB','meal_prep')
SUPABASE_API_PORT = os.getenv('SUPABASE_API_PORT',2345)
SUPABASE_KEY = os.getenv('SUPABASE_KEY','1fe75e7a6ece9bb222491fa56249cf9ccfb9149ec0806753c2c6247081bc0c8f')

def CreateConnectionToSQL():
    EngineSQL = create_engine(
        f'postgresql+psycopg2://loader_data:{DB_ROLE_LOAD_DATA_PASS}@{SUPBASE_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}',
    )
    return EngineSQL

def CreateConnectionToAPI(Role) -> SyncPostgrestClient: 
    TokenKey = CreateConnectionToken(Role)
    SupabaseAPIClient = SyncPostgrestClient(
        base_url = f'http://{SUPBASE_HOST}:{SUPABASE_API_PORT}',
        headers = {
            'apikey': TokenKey,
            'Authorization': f'Bearer {TokenKey}',
        },
        schema = SCHEMA_DB,
    )
    return SupabaseAPIClient

def CreateConnectionToken(Role):
    Payload = {
        'role': Role,
        'iss': 'supabase',
        'sub': 'python-client',
        'iat': int(time.time()),
        'exp': int(time.time()) + (60 * 60 * 24 * 365)
    }
    return jwt.encode(Payload,SUPABASE_KEY,algorithm="HS256")