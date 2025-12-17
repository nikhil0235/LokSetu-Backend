import os
from dotenv import load_dotenv
from psycopg2 import pool

load_dotenv()

POOL = pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=5,
    host=os.getenv("SUPABASE_DB_HOST"),
    port=int(os.getenv("SUPABASE_DB_PORT", "5432")),
    database=os.getenv("SUPABASE_DB_NAME", "postgres"),
    user=os.getenv("SUPABASE_DB_USER"),
    password=os.getenv("SUPABASE_DB_PASSWORD"),
    sslmode=os.getenv("SUPABASE_DB_SSLMODE", "require")
)

def with_conn(fn):
    conn = POOL.getconn()
    try:
        with conn:
            with conn.cursor() as cur:
                return fn(cur)
    finally:
        POOL.putconn(conn)

def init_and_insert():
    def work(cur):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_details (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            phone_no TEXT,
            address TEXT
        );
        """)
        cur.execute("""
        INSERT INTO user_details (name, phone_no, address) 
        VALUES (%s, %s, %s)
        """, ("Subodh", "dfdf", "123 Main St, City"))
    with_conn(work)
    print("Done")

if _name_ == "_main_":
    init_and_insert()
    POOL.closeall()