import os
import json
import boto3
import psycopg
from psycopg_pool import ConnectionPool
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
    
    def _get_db_credentials(self):
        secret_name = os.getenv('DB_SECRET_NAME')
        region = os.getenv('AWS_REGION', 'us-east-1')
        
        if not secret_name:
            return {
                'username': os.getenv('DB_USER', 'postgres'),
                'password': os.getenv('DB_PASSWORD', 'password')
            }
        
        try:
            session = boto3.session.Session(
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=region
            )
            client = session.client('secretsmanager')
            response = client.get_secret_value(SecretId=secret_name)
            secret = json.loads(response['SecretString'])
            return {
                'username': secret['username'],
                'password': secret['password']
            }
        except Exception as e:
            logger.error(f"Failed to retrieve credentials from Secrets Manager: {e}")
            raise
    
    def _setup_connection_pool(self):
        try:
            credentials = self._get_db_credentials()
            
            conninfo = f"host={os.getenv('DB_HOST', 'localhost')} port={os.getenv('DB_PORT', '5432')} dbname={os.getenv('DB_NAME', 'voter_management')} user={credentials['username']} password={credentials['password']} sslmode={os.getenv('DB_SSLMODE', 'require')}"
            
            self._connection_pool = ConnectionPool(conninfo, min_size=1, max_size=20)
            
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
            self._connection_pool.close()
            logger.info("All database connections closed")

db_manager = DatabaseManager()

def get_db_connection():
    return db_manager.get_connection()

def close_db_connections():
    db_manager.close_all_connections()