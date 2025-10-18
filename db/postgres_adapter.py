"""
PostgreSQL Database Adapter
Replaces Excel adapter with PostgreSQL operations
"""

import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from typing import List, Dict, Optional, Any
import json
from datetime import datetime
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class PostgresAdapter:
    def __init__(self, db_config: Dict[str, str]):
        self.db_config = db_config
        self._connection_pool = None
    
    @contextmanager
    def get_connection(self):
        """Get database connection with automatic cleanup"""
        conn = None
        try:
            conn = psycopg2.connect(**self.db_config)
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    # =============================================
    # VOTER OPERATIONS
    # =============================================
    
    def get_voters(self, booth_ids: List[str] = None, constituency_id: int = None, 
                   limit: int = None, offset: int = 0, filters: Dict = None) -> List[Dict]:
        """Get voters with filtering and pagination"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Build query with filters
                where_conditions = []
                params = []
                
                if booth_ids:
                    where_conditions.append("v.booth_id = ANY(%s)")
                    params.append(booth_ids)
                
                if constituency_id:
                    where_conditions.append("v.constituency_id = %s")
                    params.append(constituency_id)
                
                # Additional filters
                if filters:
                    for key, value in filters.items():
                        if value is not None:
                            if key == 'gender':
                                where_conditions.append("v.gender = %s")
                                params.append(value)
                            elif key == 'age_min':
                                where_conditions.append("v.age >= %s")
                                params.append(value)
                            elif key == 'age_max':
                                where_conditions.append("v.age <= %s")
                                params.append(value)
                            elif key == 'voting_preference':
                                where_conditions.append("v.voting_preference = %s")
                                params.append(value)
                            elif key == 'religion':
                                where_conditions.append("v.religion = %s")
                                params.append(value)
                            elif key == 'category':
                                where_conditions.append("v.category = %s")
                                params.append(value)
                            elif key == 'search':
                                where_conditions.append("""
                                    (v.voter_fname ILIKE %s OR v.voter_lname ILIKE %s 
                                     OR v.mobile LIKE %s OR v.epic_id LIKE %s)
                                """)
                                search_term = f"%{value}%"
                                params.extend([search_term, search_term, search_term, search_term])
                
                where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
                
                query = f"""
                    SELECT v.*, c.constituency_name, s.state_name, 
                           bt.booth_number, bt.booth_location
                    FROM voters v
                    LEFT JOIN constituencies c ON v.constituency_id = c.constituency_id
                    LEFT JOIN states s ON c.state_id = s.state_id
                    LEFT JOIN booths bt ON v.booth_id = bt.booth_id
                    {where_clause}
                    ORDER BY v.epic_id
                """
                
                if limit:
                    query += f" LIMIT {limit} OFFSET {offset}"
                
                cur.execute(query, params)
                return [dict(row) for row in cur.fetchall()]
    
    def get_voter_by_epic(self, epic_id: str) -> Optional[Dict]:
        """Get single voter by EPIC ID"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT v.*, c.constituency_name, s.state_name,
                           bt.booth_number, bt.booth_location
                    FROM voters v
                    LEFT JOIN constituencies c ON v.constituency_id = c.constituency_id
                    LEFT JOIN states s ON c.state_id = s.state_id
                    LEFT JOIN booths bt ON v.booth_id = bt.booth_id
                    WHERE v.epic_id = %s
                """, (epic_id,))
                
                result = cur.fetchone()
                return dict(result) if result else None
    
    def update_voter(self, epic_id: str, changes: Dict, user_id: int) -> bool:
        """Update voter information with audit logging"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    # Get current values for audit
                    cur.execute("SELECT * FROM voters WHERE epic_id = %s", (epic_id,))
                    current_voter = cur.fetchone()
                    
                    if not current_voter:
                        return False
                    
                    # Prepare old values for audit
                    old_values = {}
                    for key in changes.keys():
                        if key in current_voter:
                            old_values[key] = current_voter[key]
                    
                    # Build update query
                    set_clauses = []
                    params = []
                    
                    for key, value in changes.items():
                        set_clauses.append(f"{key} = %s")
                        params.append(value)
                    
                    # Add updated_at
                    set_clauses.append("updated_at = CURRENT_TIMESTAMP")
                    params.append(epic_id)
                    
                    update_query = f"""
                        UPDATE voters 
                        SET {', '.join(set_clauses)}
                        WHERE epic_id = %s
                    """
                    
                    cur.execute(update_query, params)
                    
                    # Log the update
                    self._log_voter_update(cur, epic_id, user_id, old_values, changes)
                    
                    conn.commit()
                    return True
                    
                except Exception as e:
                    conn.rollback()
                    logger.error(f"Error updating voter {epic_id}: {e}")
                    raise
    
    def _log_voter_update(self, cursor, epic_id: str, user_id: int, old_values: Dict, new_values: Dict):
        """Log voter update to audit table"""
        cursor.execute("""
            INSERT INTO voter_updates (voter_epic_id, user_id, old_values, new_values)
            VALUES (%s, %s, %s, %s)
        """, (epic_id, user_id, json.dumps(old_values), json.dumps(new_values)))
    
    def get_voter_count(self, booth_ids: List[str] = None, constituency_id: int = None, 
                       filters: Dict = None) -> int:
        """Get total count of voters matching criteria"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                where_conditions = []
                params = []
                
                if booth_ids:
                    where_conditions.append("booth_id = ANY(%s)")
                    params.append(booth_ids)
                
                if constituency_id:
                    where_conditions.append("constituency_id = %s")
                    params.append(constituency_id)
                
                if filters:
                    for key, value in filters.items():
                        if value is not None and key != 'search':
                            where_conditions.append(f"{key} = %s")
                            params.append(value)
                        elif key == 'search' and value:
                            where_conditions.append("""
                                (voter_fname ILIKE %s OR voter_lname ILIKE %s 
                                 OR mobile LIKE %s OR epic_id LIKE %s)
                            """)
                            search_term = f"%{value}%"
                            params.extend([search_term, search_term, search_term, search_term])
                
                where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
                
                cur.execute(f"SELECT COUNT(*) FROM voters {where_clause}", params)
                return cur.fetchone()[0]
    
    # =============================================
    # USER OPERATIONS
    # =============================================
    
    def get_users(self, created_by: str = None) -> List[Dict]:
        """Get users with their permissions"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = """
                    SELECT u.*, 
                           COALESCE(
                               json_agg(DISTINCT uc.constituency_id) FILTER (WHERE uc.constituency_id IS NOT NULL),
                               '[]'::json
                           ) as assigned_constituencies,
                           COALESCE(
                               json_agg(DISTINCT ub.booth_id) FILTER (WHERE ub.booth_id IS NOT NULL),
                               '[]'::json
                           ) as assigned_booths
                    FROM users u
                    LEFT JOIN user_constituencies uc ON u.user_id = uc.user_id
                    LEFT JOIN user_booths ub ON u.user_id = ub.user_id
                    WHERE u.is_active = true
                """
                
                params = []
                if created_by:
                    query += " AND (u.created_by = (SELECT user_id FROM users WHERE username = %s) OR u.username = %s)"
                    params.extend([created_by, created_by])
                
                query += " GROUP BY u.user_id ORDER BY u.user_id"
                
                cur.execute(query, params)
                return [dict(row) for row in cur.fetchall()]
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username with permissions"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT u.*, 
                           COALESCE(
                               json_agg(DISTINCT uc.constituency_id) FILTER (WHERE uc.constituency_id IS NOT NULL),
                               '[]'::json
                           ) as assigned_constituencies,
                           COALESCE(
                               json_agg(DISTINCT ub.booth_id) FILTER (WHERE ub.booth_id IS NOT NULL),
                               '[]'::json
                           ) as assigned_booths
                    FROM users u
                    LEFT JOIN user_constituencies uc ON u.user_id = uc.user_id
                    LEFT JOIN user_booths ub ON u.user_id = ub.user_id
                    WHERE u.username = %s AND u.is_active = true
                    GROUP BY u.user_id
                """, (username,))
                
                result = cur.fetchone()
                return dict(result) if result else None
    
    def create_user(self, user_data: Dict) -> int:
        """Create new user with permissions"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    # Insert user
                    cur.execute("""
                        INSERT INTO users (username, password_hash, role, full_name, phone, email, created_by)
                        VALUES (%(username)s, %(password_hash)s, %(role)s, %(full_name)s, %(phone)s, %(email)s, %(created_by)s)
                        RETURNING user_id
                    """, user_data)
                    
                    user_id = cur.fetchone()[0]
                    
                    # Insert booth assignments
                    if user_data.get('assigned_booth_ids'):
                        booth_values = [(user_id, booth_id) for booth_id in user_data['assigned_booth_ids']]
                        execute_values(
                            cur,
                            "INSERT INTO user_booths (user_id, booth_id) VALUES %s",
                            booth_values
                        )
                    
                    # Insert constituency assignments
                    if user_data.get('assigned_constituency_ids'):
                        const_values = [(user_id, const_id) for const_id in user_data['assigned_constituency_ids']]
                        execute_values(
                            cur,
                            "INSERT INTO user_constituencies (user_id, constituency_id) VALUES %s",
                            const_values
                        )
                    
                    conn.commit()
                    return user_id
                    
                except Exception as e:
                    conn.rollback()
                    logger.error(f"Error creating user: {e}")
                    raise
    
    # =============================================
    # BOOTH AND CONSTITUENCY OPERATIONS
    # =============================================
    
    def get_booths(self, constituency_id: int = None) -> List[Dict]:
        """Get booths with summary statistics"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = """
                    SELECT b.*, c.constituency_name,
                           COALESCE(bs.total_voters, 0) as total_voters,
                           COALESCE(bs.male_voters, 0) as male_voters,
                           COALESCE(bs.female_voters, 0) as female_voters
                    FROM booths b
                    LEFT JOIN constituencies c ON b.constituency_id = c.constituency_id
                    LEFT JOIN booth_summaries bs ON b.booth_id = bs.booth_id
                """
                
                params = []
                if constituency_id:
                    query += " WHERE b.constituency_id = %s"
                    params.append(constituency_id)
                
                query += " ORDER BY b.booth_id"
                
                cur.execute(query, params)
                return [dict(row) for row in cur.fetchall()]
    
    def get_constituencies(self) -> List[Dict]:
        """Get all constituencies"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT c.*, s.state_name,
                           COUNT(b.booth_id) as total_booths,
                           COUNT(v.epic_id) as total_voters
                    FROM constituencies c
                    LEFT JOIN states s ON c.state_id = s.state_id
                    LEFT JOIN booths b ON c.constituency_id = b.constituency_id
                    LEFT JOIN voters v ON c.constituency_id = v.constituency_id
                    GROUP BY c.constituency_id, s.state_name
                    ORDER BY c.constituency_id
                """)
                
                return [dict(row) for row in cur.fetchall()]
    
    # =============================================
    # ANALYTICS AND REPORTING
    # =============================================
    
    def get_booth_summary(self, booth_id: int) -> Dict:
        """Get detailed booth statistics"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Get basic counts
                cur.execute("""
                    SELECT 
                        COUNT(*) as total_voters,
                        COUNT(CASE WHEN gender = 'Male' THEN 1 END) as male_voters,
                        COUNT(CASE WHEN gender = 'Female' THEN 1 END) as female_voters,
                        COUNT(CASE WHEN gender = 'Other' THEN 1 END) as other_gender_voters,
                        AVG(age) as avg_age,
                        COUNT(CASE WHEN voting_preference IS NOT NULL THEN 1 END) as voters_with_preference
                    FROM voters 
                    WHERE booth_id = %s
                """, (booth_id,))
                
                summary = dict(cur.fetchone())
                
                # Get preference distribution
                cur.execute("""
                    SELECT voting_preference, COUNT(*) as count
                    FROM voters 
                    WHERE booth_id = %s AND voting_preference IS NOT NULL
                    GROUP BY voting_preference
                """, (booth_id,))
                
                summary['voting_preferences'] = {row['voting_preference']: row['count'] for row in cur.fetchall()}
                
                # Get religion distribution
                cur.execute("""
                    SELECT religion, COUNT(*) as count
                    FROM voters 
                    WHERE booth_id = %s AND religion IS NOT NULL
                    GROUP BY religion
                """, (booth_id,))
                
                summary['religions'] = {row['religion']: row['count'] for row in cur.fetchall()}
                
                return summary
    
    def update_booth_summary(self, booth_id: int):
        """Update booth summary statistics"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    summary = self.get_booth_summary(booth_id)
                    
                    cur.execute("""
                        INSERT INTO booth_summaries (
                            booth_id, constituency_id, total_voters, male_voters, 
                            female_voters, other_gender_voters, voting_preference_counts,
                            religion_counts, last_updated
                        )
                        SELECT %s, constituency_id, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP
                        FROM booths WHERE booth_id = %s
                        ON CONFLICT (booth_id) DO UPDATE SET
                            total_voters = EXCLUDED.total_voters,
                            male_voters = EXCLUDED.male_voters,
                            female_voters = EXCLUDED.female_voters,
                            other_gender_voters = EXCLUDED.other_gender_voters,
                            voting_preference_counts = EXCLUDED.voting_preference_counts,
                            religion_counts = EXCLUDED.religion_counts,
                            last_updated = CURRENT_TIMESTAMP
                    """, (
                        booth_id,
                        summary['total_voters'],
                        summary['male_voters'],
                        summary['female_voters'],
                        summary['other_gender_voters'],
                        json.dumps(summary['voting_preferences']),
                        json.dumps(summary['religions']),
                        booth_id
                    ))
                    
                    conn.commit()
                    
                except Exception as e:
                    conn.rollback()
                    logger.error(f"Error updating booth summary: {e}")
                    raise