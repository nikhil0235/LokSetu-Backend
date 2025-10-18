#!/usr/bin/env python3
"""
Excel to PostgreSQL Migration Script
Migrates data from Excel files to PostgreSQL database
"""

import os
import sys
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from datetime import datetime
import json
import logging
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.postgres")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExcelToPostgresMigrator:
    def __init__(self, db_config: Dict[str, str], excel_dir: str):
        self.db_config = db_config
        self.excel_dir = excel_dir
        self.conn = None
        
    def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.conn.autocommit = False
            logger.info("Connected to PostgreSQL database")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def close_db(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def execute_schema(self, schema_file: str):
        """Execute schema creation script"""
        try:
            with open(schema_file, 'r') as f:
                schema_sql = f.read()
            
            with self.conn.cursor() as cur:
                cur.execute(schema_sql)
                self.conn.commit()
                logger.info("Schema created successfully")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Schema creation failed: {e}")
            raise
    
    def migrate_constituencies_and_booths(self, excel_files: List[str]):
        """Extract and migrate constituency and booth data"""
        constituencies = {}
        booths = {}
        
        for excel_file in excel_files:
            try:
                # Extract constituency ID from filename (e.g., Constituency_1.xlsx -> 1)
                constituency_id = int(excel_file.split('_')[1].split('.')[0])
                
                df = pd.read_excel(os.path.join(self.excel_dir, excel_file), sheet_name='Voters_Data')
                
                if not df.empty:
                    # Get constituency info
                    constituency_name = df['ConstituencyName'].iloc[0] if 'ConstituencyName' in df.columns else f"Constituency {constituency_id}"
                    state_name = df['StateName'].iloc[0] if 'StateName' in df.columns else "Bihar"
                    
                    constituencies[constituency_id] = {
                        'constituency_name': constituency_name,
                        'state_name': state_name
                    }
                    
                    # Get unique booths
                    booth_data = df[['BoothID', 'BoothNumber', 'BoothLocation']].drop_duplicates()
                    for _, row in booth_data.iterrows():
                        if pd.notna(row['BoothID']):
                            booths[int(row['BoothID'])] = {
                                'booth_number': int(row['BoothNumber']) if pd.notna(row['BoothNumber']) else None,
                                'booth_location': row['BoothLocation'] if pd.notna(row['BoothLocation']) else None,
                                'constituency_id': constituency_id
                            }
                            
            except Exception as e:
                logger.error(f"Error processing {excel_file}: {e}")
                continue
        
        # Insert states, constituencies, and booths
        self._insert_states_constituencies_booths(constituencies, booths)
    
    def _insert_states_constituencies_booths(self, constituencies: Dict, booths: Dict):
        """Insert states, constituencies, and booths into database"""
        try:
            with self.conn.cursor() as cur:
                # Insert Bihar state
                cur.execute("""
                    INSERT INTO states (state_name, state_code) 
                    VALUES ('Bihar', 'BR') 
                    ON CONFLICT (state_name) DO NOTHING
                """)
                
                # Get Bihar state ID
                cur.execute("SELECT state_id FROM states WHERE state_name = 'Bihar'")
                state_id = cur.fetchone()[0]
                
                # Insert constituencies
                constituency_values = [
                    (const_id, data['constituency_name'], state_id)
                    for const_id, data in constituencies.items()
                ]
                
                execute_values(
                    cur,
                    """INSERT INTO constituencies (constituency_id, constituency_name, state_id) 
                       VALUES %s ON CONFLICT (constituency_id) DO NOTHING""",
                    constituency_values
                )
                
                # Insert booths
                booth_values = [
                    (booth_id, data['booth_number'], data['booth_location'], data['constituency_id'])
                    for booth_id, data in booths.items()
                ]
                
                execute_values(
                    cur,
                    """INSERT INTO booths (booth_id, booth_number, booth_location, constituency_id) 
                       VALUES %s ON CONFLICT (booth_id) DO NOTHING""",
                    booth_values
                )
                
                self.conn.commit()
                logger.info(f"Inserted {len(constituencies)} constituencies and {len(booths)} booths")
                
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error inserting constituencies/booths: {e}")
            raise
    
    def migrate_users(self, excel_files: List[str]):
        """Migrate users from Excel files"""
        all_users = []
        
        for excel_file in excel_files:
            try:
                df = pd.read_excel(os.path.join(self.excel_dir, excel_file), sheet_name='Users')
                
                for _, row in df.iterrows():
                    if pd.notna(row.get('Username')):
                        user_data = {
                            'user_id': int(row['UserID']) if pd.notna(row.get('UserID')) else None,
                            'username': row['Username'],
                            'password_hash': row.get('PasswordHash', '$2b$12$default_hash'),
                            'role': row.get('Role', 'booth_boy'),
                            'full_name': row.get('FullName'),
                            'phone': row.get('Phone'),
                            'email': row.get('Email'),
                            'assigned_booth_ids': row.get('AssignedBoothIDs'),
                            'assigned_constituency_ids': row.get('AssignedConstituencyIDs')
                        }
                        if user_data['user_id'] == 1: continue
                        all_users.append(user_data)
                        
            except Exception as e:
                logger.error(f"Error processing users from {excel_file}: {e}")
                continue
        
        self._insert_users(all_users)
    
    def _insert_users(self, users: List[Dict]):
        """Insert users into database"""
        try:
            with self.conn.cursor() as cur:
                for user in users:
                    # Insert user
                    cur.execute("""
                        INSERT INTO users (user_id, username, password_hash, role, full_name, phone, email)
                        VALUES (%(user_id)s, %(username)s, %(password_hash)s, %(role)s, %(full_name)s, %(phone)s, %(email)s)
                        ON CONFLICT (username) DO NOTHING
                    """, user)
                    
                    # Insert booth assignments
                    if user.get('assigned_booth_ids'):
                        booth_ids = str(user['assigned_booth_ids']).split(',')
                        for booth_id in booth_ids:
                            if booth_id:  # Make sure it's not empty
                                try:
                                    booth_id_int = int(booth_id)
                                    cur.execute("""
                                        INSERT INTO user_booths (user_id, booth_id)
                                        VALUES (%(user_id)s, %(booth_id)s)
                                        ON CONFLICT DO NOTHING
                                    """, {
                                        'user_id': user['user_id'],
                                        'booth_id': booth_id_int
                                    })
                                except ValueError:
                                    # Handle the case where booth_id is not a valid integer
                                    print(f"Invalid booth_id encountered: {booth_id}")
                    
                    # Insert constituency assignments
                    if user.get('assigned_constituency_ids'):
                        const_ids = [1]
                        for const_id in const_ids:
                            if const_id:
                                cur.execute("""
                                    INSERT INTO user_constituencies (user_id, constituency_id)
                                    VALUES (%(user_id)s, %(constituency_id)s)
                                    ON CONFLICT DO NOTHING
                                """, {'user_id': user['user_id'], 'constituency_id': int(const_id)})
                
                self.conn.commit()
                logger.info(f"Inserted {len(users)} users")
                
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error inserting users: {e}")
            raise
    
    def migrate_voters(self, excel_files: List[str], batch_size: int = 1000):
        """Migrate voters from Excel files in batches"""
        total_voters = 0
        
        for excel_file in excel_files:
            try:
                logger.info(f"Processing voters from {excel_file}")
                df = pd.read_excel(os.path.join(self.excel_dir, excel_file), sheet_name='Voters_Data')
                
                # Process in batches
                for i in range(0, len(df), batch_size):
                    batch_df = df.iloc[i:i+batch_size]
                    batch_voters = self._prepare_voter_batch(batch_df)
                    self._insert_voter_batch(batch_voters)
                    total_voters += len(batch_voters)
                    logger.info(f"Processed {total_voters} voters so far...")
                    
            except Exception as e:
                logger.error(f"Error processing voters from {excel_file}: {e}")
                continue
        
        logger.info(f"Total voters migrated: {total_voters}")
    
    def _prepare_voter_batch(self, df: pd.DataFrame) -> List[Dict]:
        """Prepare voter data for batch insertion"""
        voters = []
        
        for _, row in df.iterrows():
            if pd.notna(row.get('VoterEPIC')):
                # Convert pandas values to Python types
                voter_data = {}
                for col in df.columns:
                    value = row[col]
                    if pd.isna(value):
                        voter_data[col.lower()] = None
                    elif isinstance(value, (pd.Timestamp, datetime)):
                        voter_data[col.lower()] = value.date() if col == 'DOB' else value
                    elif col == 'Feedback' and value:
                        try:
                            voter_data[col.lower()] = json.loads(str(value)) if isinstance(value, str) else value
                        except:
                            voter_data[col.lower()] = '{}'
                    else:
                        voter_data[col.lower()] = value
                
                voters.append(voter_data)
        
        logger.info(f"Prepared {len(voters)} voters for batch insertion")
        return voters
    
    def _insert_voter_batch(self, voters: List[Dict]):
        """Insert batch of voters"""
        if not voters:
            return
            
        try:
            with self.conn.cursor() as cur:
                # Prepare INSERT statement with all columns
                columns = [
                    'epic_id', 'serial_no_in_list', 'part_number', 'constituency_id', 'booth_id',
                    'voter_fname', 'voter_lname', 'voter_fname_hin', 'voter_lname_hin',
                    'relation', 'guardian_fname', 'guardian_lname', 'guardian_fname_hin', 'guardian_lname_hin',
                    'house_no', 'street', 'area', 'landmark', 'village_ward', 'pin_code', 'post_office',
                    'gender', 'dob', 'age', 'mobile', 'email_id', 'family_contact_number', 'family_contact_person',
                    'last_voted_party', 'voting_preference', 'certainty_of_vote', 'vote_type', 'availability',
                    'first_time_voter', 'religion', 'category', 'obc_subtype', 'caste', 'caste_other',
                    'language_pref', 'language_other', 'communication_language', 'education_level',
                    'employment_status', 'govt_job_type', 'govt_job_group', 'job_role', 'monthly_salary_range',
                    'private_job_role', 'private_salary_range', 'self_employed_service', 'business_type',
                    'business_type_other', 'business_name', 'business_turnover_range', 'gig_worker_role',
                    'company_name', 'salary_range', 'work_experience', 'unemployment_reason',
                    'land_holding', 'crop_type', 'residing_in', 'current_location', 'other_city',
                    'permanent_in_bihar', 'migrated', 'migration_reason', 'years_since_migration',
                    'family_head_id', 'family_relation', 'family_votes_together', 'custom_relation_name',
                    'house_type', 'is_party_worker', 'party_worker_party', 'party_worker_other_party',
                    'influenced_by_leaders', 'mla_satisfaction', 'most_important_issue', 'issues_faced',
                    'other_issues', 'development_suggestions', 'community_participation', 'community_details',
                    'govt_schemes', 'additional_comments', 'address_notes', 'address_proof', 'data_consent',
                    'verification_status', 'feedback'
                ]
                
                # Map Excel columns to database columns
                column_mapping = {
                    'voterepic': 'epic_id',
                    'serialnoinlist': 'serial_no_in_list',
                    'partno': 'part_number',
                    'constituencyid': 'constituency_id',
                    'boothid': 'booth_id',
                    'voter_fname': 'voter_fname',
                    'voter_lname': 'voter_lname',
                    'voter_fname_hin': 'voter_fname_hin',
                    'voter_lname_hin': 'voter_lname_hin',
                    'houseno': 'house_no',
                    'dob': 'dob',
                    'emailid': 'email_id',
                    'lastvotedparty': 'last_voted_party',
                    'votingpreference': 'voting_preference',
                    'certaintyofvote': 'certainty_of_vote',
                    'votetype': 'vote_type',
                    'firsttimevoter': 'first_time_voter',
                    'obcsubtype': 'obc_subtype',
                    'languagepref': 'language_pref',
                    'educationlevel': 'education_level',
                    'employmentstatus': 'employment_status',
                    'govtjobtype': 'govt_job_type',
                    'govtjobgroup': 'govt_job_group',
                    'jobrole': 'job_role',
                    'monthlysalaryrange': 'monthly_salary_range',
                    'privatejobRole': 'private_job_role',
                    'privatesalaryrange': 'private_salary_range',
                    'selfemployedservice': 'self_employed_service',
                    'businesstype': 'business_type',
                    'businessturnoverrange': 'business_turnover_range',
                    'gigworkerrole': 'gig_worker_role',
                    'residingin': 'residing_in',
                    'verificationstatus': 'verification_status'
                }
                
                # Prepare values for batch insert
                values = []
                for voter in voters:
                    row_values = []
                    for col in columns:
                        # Map column name
                        excel_col = None
                        for excel_key, db_key in column_mapping.items():
                            if db_key == col:
                                excel_col = excel_key
                                break
                        
                        if excel_col and excel_col in voter:
                            row_values.append(voter[excel_col])
                        elif col in voter:
                            row_values.append(voter[col])
                        else:
                            row_values.append(None)

                    values.append(tuple(row_values))
                
                # Execute batch insert
                placeholders = ','.join(['%s'] * len(columns))
                insert_sql = f"""
                    INSERT INTO voters ({','.join(columns)})
                    VALUES ({placeholders})
                    ON CONFLICT (epic_id) DO NOTHING
                """
                
                cur.executemany(insert_sql, values)
                self.conn.commit()
                
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error inserting voter batch: {e}")
            raise
    
    def migrate_audit_logs(self, excel_files: List[str]):
        """Migrate audit logs from Excel files"""
        total_logs = 0
        
        for excel_file in excel_files:
            try:
                df = pd.read_excel(os.path.join(self.excel_dir, excel_file), sheet_name='Voter_Updates')
                
                with self.conn.cursor() as cur:
                    for _, row in df.iterrows():
                        if pd.notna(row.get('VoterEPIC')):
                            try:
                                changes = json.loads(row.get('Changes', '{}')) if row.get('Changes') else {}
                            except:
                                changes = {}
                            
                            cur.execute("""
                                INSERT INTO voter_updates (voter_epic_id, user_id, old_values, new_values, created_at)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (
                                row['VoterEPIC'],
                                row.get('UserID'),
                                json.dumps(changes.get('old_values', {})),
                                json.dumps(changes.get('new_values', {})),
                                row.get('CreatedAt', datetime.now())
                            ))
                            total_logs += 1
                
                self.conn.commit()
                logger.info(f"Migrated audit logs from {excel_file}")
                
            except Exception as e:
                logger.error(f"Error migrating audit logs from {excel_file}: {e}")
                continue
        
        logger.info(f"Total audit logs migrated: {total_logs}")
    
    def run_migration(self, schema_file: str):
        """Run complete migration process"""
        try:
            self.connect_db()
            
            # Get Excel files
            excel_files = [f for f in os.listdir(self.excel_dir) if f.endswith('.xlsx')]
            logger.info(f"Found {len(excel_files)} Excel files to migrate")
            
            # Execute schema
            logger.info("Creating database schema...")
            # self.execute_schema(schema_file)
            
            # Migrate data
            logger.info("Migrating constituencies and booths...")
            # self.migrate_constituencies_and_booths(excel_files)
            
            logger.info("Migrating users...")
            self.migrate_users(excel_files)
            
            logger.info("Migrating voters...")
            # self.migrate_voters(excel_files)
            
            logger.info("Migrating audit logs...")
            # self.migrate_audit_logs(excel_files)
            
            logger.info("Migration completed successfully!")
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            raise
        finally:
            self.close_db()

def get_db_credentials():
    """Get database credentials from AWS Secrets Manager"""
    secret_name = os.getenv('DB_SECRET_NAME')
    region = os.getenv('AWS_REGION', 'us-east-1')
    
    if not secret_name:
        return {
            'username': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password')
        }
    
    try:
        import boto3
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
        logger.error(f"Failed to retrieve credentials: {e}")
        raise

def main():
    # Database configuration
    credentials = get_db_credentials()
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'voter_management'),
        'user': credentials['username'],
        'password': credentials['password']
    }
    
    # Paths
    excel_dir = os.getenv('EXCEL_DIR', 'app/data/constituency_files')
    schema_file = 'db/postgres_schema.sql'
    
    # Run migration
    migrator = ExcelToPostgresMigrator(db_config, excel_dir)
    migrator.run_migration(schema_file)

if __name__ == "__main__":
    main()