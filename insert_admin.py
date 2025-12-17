import os
from dotenv import load_dotenv
from psycopg2 import pool
import bcrypt

load_dotenv(dotenv_path=".env.postgres")

POOL = pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=5,
    host=os.getenv("SUPABASE_DB_HOST"),
    port=int(os.getenv("SUPABASE_DB_PORT", "5432")),
    database=os.getenv("SUPABASE_DB_NAME", "postgres"),
    user=os.getenv("SUPABASE_DB_USER"),
    password=os.getenv("SUPABASE_DB_PASSWORD"),
    sslmode=os.getenv("SUPABASE_DB_SSLMODE", "require"),
    gssencmode="disable"
)

def insert_admin():
    conn = POOL.getconn()
    try:
        with conn:
            with conn.cursor() as cur:
                password = "admin123"
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                cur.execute("""
                INSERT INTO users (username, password_hash, role, full_name, phone, email, is_active) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (username) DO NOTHING
                RETURNING user_id, username, role
                """, ("admin", password_hash, "super_admin", "System Administrator", "9999999999", "admin@loksetu.com", True))
                
                result = cur.fetchone()
                if result:
                    print(f"✓ Admin user created: ID={result[0]}, Username={result[1]}, Role={result[2]}")
                else:
                    print("Admin user already exists")
    finally:
        POOL.putconn(conn)
        POOL.closeall()

if __name__ == "__main__":
    insert_admin()
