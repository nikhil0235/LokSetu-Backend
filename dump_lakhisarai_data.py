#!/usr/bin/env python3
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import boto3
import json

# Load environment variables
load_dotenv('.env.postgres')

def get_db_connection():
    """Get database connection using AWS Secrets Manager"""
    try:
        # Get credentials from AWS Secrets Manager
        session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        secrets_client = session.client('secretsmanager')
        secret_value = secrets_client.get_secret_value(SecretId=os.getenv('DB_SECRET_NAME'))
        secret = json.loads(secret_value['SecretString'])
        
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=secret['username'],
            password=secret['password'],
            sslmode=os.getenv('DB_SSLMODE')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def dump_hierarchical_data():
    """Dump state, district, constituency, block, panchayat and booth data"""
    
    # Read Excel data
    df = pd.read_excel('booth_data.xlsx', sheet_name='167-Suryagraha')
    
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        print("🚀 Starting Lakhisarai data dump...")
        
        # 1. Insert State (Bihar)
        state_id = 1
        
        # 2. Insert District (Lakhisarai)
        district_id = 2
        
        # 3. Insert Constituency (Lakhisarai - 168)
        constituency_id = 167
        
        # 4. Insert Blocks
        print("🏢 Inserting block data...")
        blocks = df['Block Name (प्रखंड का नाम)'].unique()
        block_ids = {}
        
        for block_name in blocks:
            cursor.execute("""
                INSERT INTO blocks (block_name, constituency_id) 
                VALUES (%s, %s) 
                ON CONFLICT DO NOTHING
                RETURNING block_id
            """, (block_name, constituency_id))
            result = cursor.fetchone()
            if result:
                block_ids[block_name] = result[0]
            else:
                cursor.execute("SELECT block_id FROM blocks WHERE block_name = %s", (block_name,))
                block_ids[block_name] = cursor.fetchone()[0]
        
        # 5. Insert Panchayats
        print("🏛️  Inserting panchayat data...")
        panchayat_ids = {}
        block_panch_mapping = df[['Block Name (प्रखंड का नाम)', 'Panchayat/ULB Name (पंचायत/निकाय का नाम)']].drop_duplicates()
        
        for _, row in block_panch_mapping.iterrows():
            block_name = row['Block Name (प्रखंड का नाम)']
            panchayat_name = row['Panchayat/ULB Name (पंचायत/निकाय का नाम)']
            
            cursor.execute("""
                INSERT INTO panchayats (panchayat_name, block_id) 
                VALUES (%s, %s) 
                ON CONFLICT DO NOTHING
                RETURNING panchayat_id
            """, (panchayat_name, block_ids[block_name]))
            result = cursor.fetchone()
            if result:
                panchayat_ids[panchayat_name] = result[0]
            else:
                cursor.execute("SELECT panchayat_id FROM panchayats WHERE panchayat_name = %s", (panchayat_name,))
                panchayat_ids[panchayat_name] = cursor.fetchone()[0]
        
        # 6. Insert Booths
        print("🗳️  Inserting booth data...")
        booth_count = 0
        
        for _, row in df.iterrows():
            booth_number = int(row['Part No.'])
            booth_location = row['Building in which it will be located (3)']
            panchayat_name = row['Panchayat/ULB Name (पंचायत/निकाय का नाम)']
            
            cursor.execute("""
                INSERT INTO booths (booth_id, booth_number, booth_location, constituency_id, panchayat_id) 
                VALUES (%s, %s, %s, %s, %s) 
                ON CONFLICT (booth_id) DO NOTHING
            """, (booth_number + 750, booth_number, booth_location, constituency_id, panchayat_ids[panchayat_name]))
            booth_count += 1
        
        conn.commit()
        
        print(f"✅ Successfully dumped Lakhisarai data:")
        print(f"   📍 State: Bihar")
        print(f"   🏘️  District: Lakhisarai") 
        print(f"   🗳️  Constituency: Lakhisarai (168)")
        print(f"   🏢 Blocks: {len(blocks)}")
        print(f"   🏛️  Panchayats: {len(panchayat_ids)}")
        print(f"   🗳️  Booths: {booth_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    dump_hierarchical_data()