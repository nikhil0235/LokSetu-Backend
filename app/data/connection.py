import os
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import logging
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.postgres")

logger = logging.getLogger(__name__)

class DatabaseManager:
    _instance = None
    _connection_pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self._setup_connection_pool()
    
    # def _get_db_credentials(self):
    #     secret_name = os.getenv('DB_SECRET_NAME')
    #     region = os.getenv('AWS_REGION', 'us-east-1')
        
    #     if not secret_name:
    #         return {
    #             'username': os.getenv('DB_USER', 'postgres'),
    #             'password': os.getenv('DB_PASSWORD', 'password')
    #         }
        
    #     try:
    #         session = boto3.session.Session(
    #             aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    #             aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    #             region_name=region
    #         )
    #         client = session.client('secretsmanager')
    #         response = client.get_secret_value(SecretId=secret_name)
    #         secret = json.loads(response['SecretString'])
    #         return {
    #             'username': secret['username'],
    #             'password': secret['password']
    #         }
    #     except Exception as e:
    #         logger.error(f"Failed to retrieve credentials from Secrets Manager: {e}")
    #         raise
    
    def _setup_connection_pool(self):
        try:
            supabase_db_url = os.getenv("SUPABASE_DB_URL")
            if not supabase_db_url:
                raise RuntimeError("SUPABASE_DB_URL is not set")

            self._connection_pool = pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=20,
                host=os.getenv("SUPABASE_DB_HOST"),
                port=int(os.getenv("SUPABASE_DB_PORT", "5432")),
                database=os.getenv("SUPABASE_DB_NAME", "postgres"),
                user=os.getenv("SUPABASE_DB_USER"),
                password=os.getenv("SUPABASE_DB_PASSWORD"),
                sslmode=os.getenv("SUPABASE_DB_SSLMODE", "require"),
                gssencmode="disable"
            )
            
            logger.info("Database connection pool created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = self._connection_pool.getconn()
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database operation failed: {e}")
            raise
        finally:
            if conn:
                self._connection_pool.putconn(conn)
    
    def close_all_connections(self):
        if self._connection_pool:
            self._connection_pool.closeall()
            logger.info("All database connections closed")

db_manager = DatabaseManager()

def get_db_connection():
    return db_manager.get_connection()

def close_db_connections():
    db_manager.close_all_connections()