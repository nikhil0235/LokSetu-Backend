import json
from datetime import datetime
from typing import List, Dict, Optional
from app.data.connection import get_db_connection
from app.utils.logger import logger

class PostgresAdapter:
    # Voter table columns (excluding epic_id which cannot be updated)
    VOTER_COLUMNS = {
        'serial_no_in_list', 'voter_fname', 'voter_lname', 'voter_fname_hin', 'voter_lname_hin',
        'relation', 'guardian_fname', 'guardian_lname', 'guardian_fname_hin', 'guardian_lname_hin',
        'house_no', 'street', 'area', 'landmark', 'village_ward', 'pin_code', 'post_office',
        'gender', 'dob', 'age', 'mobile', 'email_id', 'family_contact_number', 'family_contact_person',
        'last_voted_party', 'voting_preference', 'certainty_of_vote', 'vote_type', 'availability',
        'first_time_voter', 'religion', 'category', 'obc_subtype', 'caste', 'caste_other',
        'language_pref', 'language_other', 'communication_language', 'education_level',
        'employment_status', 'govt_job_type', 'govt_job_group', 'job_role', 'monthly_salary_range',
        'private_job_role', 'private_salary_range', 'self_employed_service', 'business_type',
        'business_type_other', 'business_name', 'business_turnover_range', 'gig_worker_role',
        'company_name', 'salary_range', 'work_experience', 'unemployment_reason', 'land_holding',
        'crop_type', 'digital_creator_category', 'digital_creator_platform', 'digital_creator_other_platform',
        'digital_creator_channel_name', 'digital_creator_content_type', 'digital_creator_followers',
        'digital_creator_income', 'digital_creator_other_category', 'residing_in', 'current_location',
        'other_city', 'permanent_in_bihar', 'migrated', 'migration_reason', 'years_since_migration',
        'family_head_id', 'family_relation', 'family_votes_together', 'custom_relation_name',
        'house_type', 'is_party_worker', 'party_worker_party', 'party_worker_other_party',
        'influenced_by_leaders', 'mla_satisfaction', 'most_important_issue', 'issues_faced',
        'other_issues', 'development_suggestions', 'community_participation', 'community_details',
        'govt_schemes', 'additional_comments', 'address_notes', 'address_proof', 'data_consent',
        'verification_status', 'feedback'
    }
    
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
            cursor.execute(
                """
                SELECT u.*, p.party_name, a.alliance_name 
                FROM users u 
                LEFT JOIN parties p ON u.party_id = p.party_id 
                LEFT JOIN alliances a ON u.alliance_id = a.alliance_id
                """
            )
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
            cursor.execute(
                """
                SELECT u.*, p.party_name, a.alliance_name 
                FROM users u 
                LEFT JOIN parties p ON u.party_id = p.party_id 
                LEFT JOIN alliances a ON u.alliance_id = a.alliance_id 
                WHERE u.username = %s
                """, 
                (username,)
            )
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
        username, role, full_name, phone, assigned_booths, password_hash, email, created_by, assigned_constituencies, party_id, alliance_id = user_data
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Insert user
            cursor.execute(
                "INSERT INTO users (username, role, full_name, phone, password_hash, email, created_by, party_id, alliance_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING user_id",
                (username, role, full_name, phone, password_hash, email, created_by, party_id, alliance_id)
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
            return self.get_user_by_id(user_id)
    
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
            cursor.execute(
                """
                SELECT u.*, p.party_name, a.alliance_name 
                FROM users u 
                LEFT JOIN parties p ON u.party_id = p.party_id 
                LEFT JOIN alliances a ON u.alliance_id = a.alliance_id 
                WHERE u.user_id = %s
                """, 
                (user_id,)
            )
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

    def store_otp(self, mobile: str, otp: str, expires_at: datetime):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO otp_codes (mobile, otp, expires_at) VALUES (%s, %s, %s) ON CONFLICT (mobile) DO UPDATE SET otp = EXCLUDED.otp, expires_at = EXCLUDED.expires_at, created_at = CURRENT_TIMESTAMP",
                (mobile, otp, expires_at)
            )
            conn.commit()
    
    def verify_otp(self, mobile: str, otp: str):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT otp, expires_at FROM otp_codes WHERE mobile = %s AND expires_at > %s",
                (mobile, datetime.now())
            )
            result = cursor.fetchone()
            if result and result[0] == otp:
                cursor.execute("DELETE FROM otp_codes WHERE mobile = %s", (mobile,))
                conn.commit()
                return True
            return False
    
    def get_user_by_mobile(self, mobile: str):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT u.*, p.party_name, a.alliance_name 
                FROM users u 
                LEFT JOIN parties p ON u.party_id = p.party_id 
                LEFT JOIN alliances a ON u.alliance_id = a.alliance_id 
                WHERE u.phone = %s
                """, 
                (mobile,)
            )
            row = cursor.fetchone()
            
            if row:
                columns = [desc[0] for desc in cursor.description]
                user = dict(zip(columns, row))
                
                cursor.execute("SELECT booth_id FROM user_booths WHERE user_id = %s", (user['user_id'],))
                user['assigned_booths'] = [r[0] for r in cursor.fetchall()]
                
                cursor.execute("SELECT constituency_id FROM user_constituencies WHERE user_id = %s", (user['user_id'],))
                user['assigned_constituencies'] = [r[0] for r in cursor.fetchall()]
                
                return user
            return None
    
    # Party methods
    def get_parties(self, is_active=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM parties WHERE 1=1"
            params = []
            
            if is_active is not None:
                query += " AND is_active = %s"
                params.append(is_active)
            
            query += " ORDER BY party_name"
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    
    def get_party_by_id(self, party_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM parties WHERE party_id = %s", (party_id,))
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def create_party(self, party_data):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO parties (party_name, party_code, party_symbol, party_type, founded_year, is_active) VALUES (%s, %s, %s, %s, %s, %s) RETURNING party_id",
                (party_data['party_name'], party_data.get('party_code'), party_data.get('party_symbol'), 
                 party_data.get('party_type'), party_data.get('founded_year'), party_data.get('is_active', True))
            )
            party_id = cursor.fetchone()[0]
            conn.commit()
            return self.get_party_by_id(party_id)
    
    def update_party(self, party_id, updates):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            set_clauses = []
            values = []
            
            for field, value in updates.items():
                set_clauses.append(f"{field} = %s")
                values.append(value)
            
            values.append(party_id)
            cursor.execute(f"UPDATE parties SET {', '.join(set_clauses)} WHERE party_id = %s", values)
            conn.commit()
            return self.get_party_by_id(party_id)
    
    def delete_party(self, party_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # First delete party alliance mappings
            cursor.execute("DELETE FROM party_alliances WHERE party_id = %s", (party_id,))
            # Then delete the party
            cursor.execute("DELETE FROM parties WHERE party_id = %s", (party_id,))
            conn.commit()
            return True
    
    # Alliance methods
    def get_alliances(self, is_active=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM alliances WHERE 1=1"
            params = []
            
            if is_active is not None:
                query += " AND is_active = %s"
                params.append(is_active)
            
            query += " ORDER BY alliance_name"
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    
    def get_alliance_by_id(self, alliance_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alliances WHERE alliance_id = %s", (alliance_id,))
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                alliance = dict(zip(columns, row))
                
                # Get alliance parties
                cursor.execute(
                    "SELECT p.* FROM parties p JOIN party_alliances pa ON p.party_id = pa.party_id WHERE pa.alliance_id = %s AND pa.is_current = true",
                    (alliance_id,)
                )
                party_columns = [desc[0] for desc in cursor.description]
                party_rows = cursor.fetchall()
                alliance['parties'] = [dict(zip(party_columns, row)) for row in party_rows]
                
                return alliance
            return None
    
    def create_alliance(self, alliance_data):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO alliances (alliance_name, alliance_code, description, formed_date, is_active) VALUES (%s, %s, %s, %s, %s) RETURNING alliance_id",
                (alliance_data['alliance_name'], alliance_data.get('alliance_code'), alliance_data.get('description'),
                 alliance_data.get('formed_date'), alliance_data.get('is_active', True))
            )
            alliance_id = cursor.fetchone()[0]
            conn.commit()
            return self.get_alliance_by_id(alliance_id)
    
    def update_alliance(self, alliance_id, updates):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            set_clauses = []
            values = []
            
            for field, value in updates.items():
                set_clauses.append(f"{field} = %s")
                values.append(value)
            
            values.append(alliance_id)
            cursor.execute(f"UPDATE alliances SET {', '.join(set_clauses)} WHERE alliance_id = %s", values)
            conn.commit()
            return self.get_alliance_by_id(alliance_id)
    
    def delete_alliance(self, alliance_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # First delete party alliance mappings
            cursor.execute("DELETE FROM party_alliances WHERE alliance_id = %s", (alliance_id,))
            # Then delete the alliance
            cursor.execute("DELETE FROM alliances WHERE alliance_id = %s", (alliance_id,))
            conn.commit()
            return True
    
    def map_party_to_alliance(self, party_id, alliance_id, joined_date=None, is_current=True):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO party_alliances (party_id, alliance_id, joined_date, is_current) VALUES (%s, %s, %s, %s) ON CONFLICT (party_id, alliance_id) DO UPDATE SET joined_date = EXCLUDED.joined_date, is_current = EXCLUDED.is_current",
                (party_id, alliance_id, joined_date, is_current)
            )
            conn.commit()
            return True

    # Scheme methods
    def get_schemes(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM schemes ORDER BY name")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    
    def get_scheme_by_id(self, scheme_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM schemes WHERE scheme_id = %s", (scheme_id,))
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def create_scheme(self, scheme_data):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO schemes (name, description, category, created_by) VALUES (%s, %s, %s, %s) RETURNING scheme_id",
                (scheme_data['name'], scheme_data.get('description'), scheme_data['category'], scheme_data['created_by'])
            )
            scheme_id = cursor.fetchone()[0]
            conn.commit()
            return self.get_scheme_by_id(scheme_id)
    
    def update_scheme(self, scheme_id, updates):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            set_clauses = []
            values = []
            
            for field, value in updates.items():
                set_clauses.append(f"{field} = %s")
                values.append(value)
            
            set_clauses.append("updated_at = CURRENT_TIMESTAMP")
            values.append(scheme_id)
            
            cursor.execute(f"UPDATE schemes SET {', '.join(set_clauses)} WHERE scheme_id = %s", values)
            conn.commit()
            return self.get_scheme_by_id(scheme_id)
    
    def delete_scheme(self, scheme_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Delete scheme (voter_schemes will be deleted automatically due to CASCADE)
            cursor.execute("DELETE FROM schemes WHERE scheme_id = %s", (scheme_id,))
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count > 0
    
    def get_voter_schemes(self, voter_epic_id):
        """Get schemes assigned to a voter"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT s.*, vs.assigned_at, vs.assigned_by 
                FROM schemes s 
                JOIN voter_schemes vs ON s.scheme_id = vs.scheme_id 
                WHERE vs.voter_epic_id = %s
                ORDER BY s.name
                """,
                (voter_epic_id,)
            )
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    
    def update_voter_schemes(self, voter_epic_id, scheme_ids, assigned_by):
        """Update voter's scheme assignments"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Remove existing assignments
            cursor.execute("DELETE FROM voter_schemes WHERE voter_epic_id = %s", (voter_epic_id,))
            
            # Add new assignments
            if scheme_ids:
                for scheme_id in scheme_ids:
                    cursor.execute(
                        "INSERT INTO voter_schemes (voter_epic_id, scheme_id, assigned_by) VALUES (%s, %s, %s)",
                        (voter_epic_id, scheme_id, assigned_by)
                    )
            
            conn.commit()
            return True
    
    def get_scheme_beneficiaries(self, scheme_id):
        """Get voters assigned to a scheme"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT v.epic_id, v.voter_fname, v.voter_lname, vs.assigned_at, vs.assigned_by
                FROM voters v 
                JOIN voter_schemes vs ON v.epic_id = vs.voter_epic_id 
                WHERE vs.scheme_id = %s
                ORDER BY v.voter_fname, v.voter_lname
                """,
                (scheme_id,)
            )
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    def bulk_update_voters_by_field(self, field, updates, user_id, batch_size=1000):
        """Bulk update voters by field with batching for performance"""
        # Validate field
        if field not in self.VOTER_COLUMNS:
            raise ValueError(f"Field '{field}' is not allowed for update")
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            epic_ids = list(updates.keys())
            total_updated = 0
            
            # Process in batches
            for i in range(0, len(epic_ids), batch_size):
                batch_ids = epic_ids[i:i + batch_size]
                batch_updates = {eid: updates[eid] for eid in batch_ids}
                
                # Build CASE-WHEN query
                cases = []
                params = []
                for epic_id, value in batch_updates.items():
                    cases.append("WHEN epic_id = %s THEN %s")
                    params.extend([epic_id, value])
                
                # Add epic_ids for WHERE clause
                params.extend(batch_ids)
                placeholders = ','.join(['%s'] * len(batch_ids))
                
                query = f"""
                UPDATE voters 
                SET {field} = CASE {' '.join(cases)} END,
                    updated_at = CURRENT_TIMESTAMP
                WHERE epic_id IN ({placeholders})
                """
                
                cursor.execute(query, params)
                batch_updated = cursor.rowcount
                total_updated += batch_updated
            
            conn.commit()
            return total_updated

    def get_affected_booth_ids(self, epic_ids):
        """Get booth IDs for given voter epic IDs"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            placeholders = ','.join(['%s'] * len(epic_ids))
            cursor.execute(f"SELECT DISTINCT booth_id FROM voters WHERE epic_id IN ({placeholders})", epic_ids)
            return [row[0] for row in cursor.fetchall()]



    def _log_update(self, epic_id, user_id, old_values, new_values, cursor):
        cursor.execute(
            "INSERT INTO voter_updates (voter_epic_id, user_id, old_values, new_values, created_at) VALUES (%s, %s, %s, %s, %s)",
            (epic_id, user_id, json.dumps(old_values), json.dumps(new_values), datetime.now())
        )