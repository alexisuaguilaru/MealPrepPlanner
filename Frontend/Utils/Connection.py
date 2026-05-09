import os
import time
from postgrest import SyncPostgrestClient
import jwt

SUPBASE_HOST = os.getenv('SUPBASE_HOST','localhost')
SCHEMA_DB = os.getenv('SCHEMA_DB','meal_prep')
SUPABASE_API_PORT = os.getenv('SUPABASE_API_PORT',2345)
SUPABASE_KEY = os.getenv('SUPABASE_KEY','1fe75e7a6ece9bb222491fa56249cf9ccfb9149ec0806753c2c6247081bc0c8f')

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

ConnectionToAPI = CreateConnectionToAPI('reader_data')