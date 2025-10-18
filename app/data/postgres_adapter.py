import json
from datetime import datetime
from typing import List, Dict, Optional
from app.data.connection import get_db_connection
from app.utils.logger import logger

class PostgresAdapter:
    def __init__(self, constituency_file=None):
        # constituency_file parameter kept for compatibility but not used
        pass

    def get_voters(self, booth_ids=None, constituency_id=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM voters WHERE 1=1"
            params = []
            
            if booth_ids:
                placeholders = ','.join(['%s'] * len(booth_ids))
                query += f" AND booth_id IN ({placeholders})"
                params.extend(booth_ids)
            
            if constituency_id:
                query += " AND constituency_id = %s"
                params.append(constituency_id)

            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            return [dict(zip(columns, row)) for row in rows]
        
    def get_voters_by_epic(self, epic_id=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM voters WHERE 1=1"
            params = []

            if epic_id:
                query += " AND epic_id = %s"
                params.append(epic_id)

            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            return [dict(zip(columns, row)) for row in rows]

    def update_voter(self, epic_id, changes, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get old values for audit
            cursor.execute("SELECT * FROM voters WHERE epic_id = %s", (epic_id,))
            old_row = cursor.fetchone()
            if not old_row:
                return False
            
            columns = [desc[0] for desc in cursor.description]
            old_data = dict(zip(columns, old_row))
            
            # Update voter
            set_clause = ', '.join([f"{key} = %s" for key in changes.keys()])
            values = list(changes.values()) + [epic_id]
            
            cursor.execute(f"UPDATE voters SET {set_clause} WHERE epic_id = %s", values)
            
            # Log update
            old_values = {k: old_data.get(k) for k in changes.keys()}
            self._log_update(epic_id, user_id, old_values, changes, cursor)
            
            conn.commit()
            return True

    def get_users(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            users = []
            for row in rows:
                user = dict(zip(columns, row))
                
                # Get booth assignments
                cursor.execute("SELECT booth_id FROM user_booths WHERE user_id = %s", (user['user_id'],))
                user['assigned_booths'] = [r[0] for r in cursor.fetchall()]
                
                # Get constituency assignments
                cursor.execute("SELECT constituency_id FROM user_constituencies WHERE user_id = %s", (user['user_id'],))
                user['assigned_constituencies'] = [r[0] for r in cursor.fetchall()]
                
                users.append(user)
            
            return users
        
    def get_user_by_username(self, username: str):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()

            if row:
                columns = [desc[0] for desc in cursor.description]
                user = dict(zip(columns, row))
                
                # Get booth assignments
                cursor.execute("SELECT booth_id FROM user_booths WHERE user_id = %s", (user['user_id'],))
                user['assigned_booths'] = [r[0] for r in cursor.fetchall()]
                
                # Get constituency assignments
                cursor.execute("SELECT constituency_id FROM user_constituencies WHERE user_id = %s", (user['user_id'],))
                user['assigned_constituencies'] = [r[0] for r in cursor.fetchall()]
                
                return user
            return None

    def create_user(self, user_data):
        username, role, full_name, phone, assigned_booths, password_hash, email, created_by, assigned_constituencies = user_data
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Insert user
            cursor.execute(
                "INSERT INTO users (username, role, full_name, phone, password_hash, email, created_by) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING user_id",
                (username, role, full_name, phone, password_hash, email, created_by)
            )
            user_id = cursor.fetchone()[0]
            
            # Insert booth assignments
            if assigned_booths:
                if isinstance(assigned_booths, str):
                    booth_ids = [int(b.strip()) for b in assigned_booths.split(',') if b.strip()]
                else:
                    booth_ids = assigned_booths
                for booth_id in booth_ids:
                    cursor.execute(
                        "INSERT INTO user_booths (user_id, booth_id) VALUES (%s, %s)",
                        (user_id, booth_id)
                    )
            
            # Insert constituency assignments
            if assigned_constituencies:
                if isinstance(assigned_constituencies, str):
                    const_ids = [int(c.strip()) for c in assigned_constituencies.split(',') if c.strip()]
                else:
                    const_ids = assigned_constituencies
                for const_id in const_ids:
                    cursor.execute(
                        "INSERT INTO user_constituencies (user_id, constituency_id) VALUES (%s, %s)",
                        (user_id, const_id)
                    )
            
            conn.commit()
            return True
    
    def update_user(self, user_id, updates):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Handle booth and constituency updates separately
            booth_updates = updates.pop('assigned_booths', None)
            const_updates = updates.pop('assigned_constituencies', None)
            # Update main user fields
            if updates:
                set_clauses = []
                values = []
                
                for field, value in updates.items():
                    set_clauses.append(f"{field} = %s")
                    values.append(value)
                
                values.append(user_id)
                cursor.execute(f"UPDATE users SET {', '.join(set_clauses)} WHERE user_id = %s", values)
            
            # Update booth assignments
            if booth_updates is not None:
                cursor.execute("DELETE FROM user_booths WHERE user_id = %s", (user_id,))
                if booth_updates:
                    if isinstance(booth_updates, str):
                        booth_ids = [int(b.strip()) for b in booth_updates.split(',') if b.strip()]
                    else:
                        booth_ids = booth_updates
                    for booth_id in booth_ids:
                        cursor.execute(
                            "INSERT INTO user_booths (user_id, booth_id) VALUES (%s, %s)",
                            (user_id, booth_id)
                        )
            
            # Update constituency assignments
            if const_updates is not None:
                cursor.execute("DELETE FROM user_constituencies WHERE user_id = %s", (user_id,))
                if const_updates:
                    if isinstance(const_updates, str):
                        const_ids = [int(c.strip()) for c in const_updates.split(',') if c.strip()]
                    else:
                        const_ids = const_updates
                    for const_id in const_ids:
                        cursor.execute(
                            "INSERT INTO user_constituencies (user_id, constituency_id) VALUES (%s, %s)",
                            (user_id, const_id)
                        )
            
            conn.commit()
            return True
    
    def delete_user(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Cascade deletes will handle user_booths and user_constituencies
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            conn.commit()
            return True
    
    def get_user_by_id(self, user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            row = cursor.fetchone()
            
            if row:
                columns = [desc[0] for desc in cursor.description]
                user = dict(zip(columns, row))
                
                # Get booth assignments
                cursor.execute("SELECT booth_id FROM user_booths WHERE user_id = %s", (user['user_id'],))
                user['assigned_booths'] = [r[0] for r in cursor.fetchall()]
                
                # Get constituency assignments
                cursor.execute("SELECT constituency_id FROM user_constituencies WHERE user_id = %s", (user['user_id'],))
                user['assigned_constituencies'] = [r[0] for r in cursor.fetchall()]
                
                return user
            return None

    def get_states(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM states ORDER BY state_name")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    
    def get_districts(self, state_id=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM district WHERE 1=1"
            params = []
            
            if state_id:
                query += " AND state_id = %s"
                params.append(state_id)
            
            query += " ORDER BY district_name"
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    
    def get_constituencies(self, state_id=None, district_id=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM constituencies WHERE 1=1"
            params = []
            
            if state_id:
                query += " AND state_id = %s"
                params.append(state_id)
            
            if district_id:
                query += " AND district_id = %s"
                params.append(district_id)
            
            query += " ORDER BY constituency_name"
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    
    def get_blocks(self, constituency_id=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM blocks WHERE 1=1"
            params = []
            
            if constituency_id:
                query += " AND constituency_id = %s"
                params.append(constituency_id)
            
            query += " ORDER BY block_name"
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    
    def get_panchayats(self, block_id=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM panchayats WHERE 1=1"
            params = []
            
            if block_id:
                query += " AND block_id = %s"
                params.append(block_id)
            
            query += " ORDER BY panchayat_name"
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    
    def get_booths(self, constituency_id=None, panchayat_id=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM booths WHERE 1=1"
            params = []
            
            if constituency_id:
                query += " AND constituency_id = %s"
                params.append(constituency_id)
            
            if panchayat_id:
                query += " AND panchayat_id = %s"
                params.append(panchayat_id)
            
            query += " ORDER BY booth_number"
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    def _log_update(self, epic_id, user_id, old_values, new_values, cursor):
        cursor.execute(
            "INSERT INTO voter_updates (voter_epic_id, user_id, old_values, new_values, created_at) VALUES (%s, %s, %s, %s, %s)",
            (epic_id, user_id, json.dumps(old_values), json.dumps(new_values), datetime.now())
        )