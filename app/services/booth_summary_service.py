import json
from collections import defaultdict
from typing import List, Dict
from app.models.booth_summary import BoothSummary
from app.data.connection import get_db_connection
from app.utils.logger import logger
from datetime import datetime

class BoothSummaryService:
    def __init__(self, adapter):
        self.adapter = adapter

    def calculate_booth_summary(self, booth_id: int) -> BoothSummary:
        """Calculate aggregations for a specific booth"""
        voters = self.adapter.get_voters(booth_ids=[booth_id])
        
        summary = BoothSummary(
            booth_id=booth_id,
            constituency_id=None  # Will be populated from booth table if needed
        )
        
        if not voters:
            return summary

        # Basic counts
        summary.total_voters = len(voters)
        summary.male_voters = sum(1 for v in voters if str(v.get("gender", "")).upper() == "M")
        summary.female_voters = sum(1 for v in voters if str(v.get("gender", "")).upper() == "F")
        summary.other_gender_voters = summary.total_voters - summary.male_voters - summary.female_voters

        # Aggregation counts
        summary.voting_preference_counts = self._count_field(voters, "voting_preference")
        summary.voted_party_counts = self._count_field(voters, "voted_party")
        summary.religion_counts = self._count_field(voters, "religion")
        summary.category_counts = self._count_nested_field(voters, "category", "caste")
        summary.education_counts = self._count_field(voters, "education_level")
        summary.employment_counts = self._count_field(voters, "employment_status")
        summary.age_group_counts = self._count_age_groups(voters)
        summary.complete_voter_count = self._count_complete_voters(voters)
        summary.verified_voter_count = self._count_verified_voters(voters)

        return summary

    def _count_field(self, voters: List[Dict], field: str) -> Dict[str, int]:
        """Count occurrences of field values"""
        counts = defaultdict(int)
        for voter in voters:
            value = voter.get(field)
            if value:
                counts[str(value)] += 1
        return dict(counts)

    def _count_nested_field(self, voters: List[Dict], main_field: str, sub_field: str) -> Dict[str, Dict]:
        """Count occurrences with nested structure: main_field -> sub_field breakdown"""
        nested_counts = defaultdict(lambda: {"total": 0, "breakdown": defaultdict(int)})
        
        for voter in voters:
            main_value = voter.get(main_field)
            sub_value = voter.get(sub_field)
            
            if main_value:
                main_key = str(main_value)
                nested_counts[main_key]["total"] += 1
                
                if sub_value:
                    nested_counts[main_key]["breakdown"][str(sub_value)] += 1
        
        # Convert defaultdict to regular dict
        result = {}
        for main_key, data in nested_counts.items():
            result[main_key] = {
                "total": data["total"],
                "breakdown": dict(data["breakdown"])
            }
        
        return result

    def _count_age_groups(self, voters: List[Dict]) -> Dict[str, int]:
        """Count voters by age groups"""
        groups = {"18-35": 0, "36-55": 0, "56+": 0}
        for voter in voters:
            age = voter.get("age")
            if age:
                try:
                    age = int(age)
                    if 18 <= age <= 35:
                        groups["18-35"] += 1
                    elif 36 <= age <= 55:
                        groups["36-55"] += 1
                    elif age > 56:
                        groups["56+"] += 1
                except ValueError:
                    pass
        return groups

    def _count_complete_voters(self, voters: List[Dict]) -> int:
        """Count voters with caste, category, phone, education"""
        count = 0
        for voter in voters:
            if (voter.get("caste") and voter.get("category") and 
                voter.get("mobile") and voter.get("education_level")):
                count += 1
        return count

    def _count_verified_voters(self, voters: List[Dict]) -> int:
        """Count voters with phone and voting_preference"""
        count = 0
        for voter in voters:
            if voter.get("mobile") and voter.get("voting_preference"):
                count += 1
        return count

    def update_booth_summary(self, booth_id: int):
        """Update summary for a specific booth"""
        summary = self.calculate_booth_summary(booth_id)
        self._save_booth_summary(summary)
        logger.info(f"Updated booth summary for booth {booth_id}")

    def _save_booth_summary(self, summary: BoothSummary):
        """Save booth summary to PostgreSQL"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                """
                INSERT INTO booth_summaries (
                    booth_id, constituency_id, total_voters, male_voters, female_voters, 
                    other_gender_voters, voting_preference_counts, voted_party_counts, religion_counts, 
                    category_counts, education_counts, employment_counts, age_group_counts, 
                    complete_voter_count, verified_voter_count, scheme_beneficiaries_counts
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (booth_id) DO UPDATE SET
                    constituency_id = EXCLUDED.constituency_id,
                    total_voters = EXCLUDED.total_voters,
                    male_voters = EXCLUDED.male_voters,
                    female_voters = EXCLUDED.female_voters,
                    other_gender_voters = EXCLUDED.other_gender_voters,
                    voting_preference_counts = EXCLUDED.voting_preference_counts,
                    voted_party_counts = EXCLUDED.voted_party_counts,
                    religion_counts = EXCLUDED.religion_counts,
                    category_counts = EXCLUDED.category_counts,
                    education_counts = EXCLUDED.education_counts,
                    employment_counts = EXCLUDED.employment_counts,
                    age_group_counts = EXCLUDED.age_group_counts,
                    complete_voter_count = EXCLUDED.complete_voter_count,
                    verified_voter_count = EXCLUDED.verified_voter_count,
                    scheme_beneficiaries_counts = EXCLUDED.scheme_beneficiaries_counts,
                    last_updated = CURRENT_TIMESTAMP
                """,
                (
                    summary.booth_id, summary.constituency_id, summary.total_voters,
                    summary.male_voters, summary.female_voters, summary.other_gender_voters,
                    json.dumps(summary.voting_preference_counts),
                    json.dumps(summary.voted_party_counts),
                    json.dumps(summary.religion_counts),
                    json.dumps(summary.category_counts),
                    json.dumps(summary.education_counts),
                    json.dumps(summary.employment_counts),
                    json.dumps(summary.age_group_counts),
                    summary.complete_voter_count,
                    summary.verified_voter_count,
                    json.dumps(summary.scheme_beneficiaries_counts)
                )
            )
            conn.commit()

    def get_booth_summaries(self, booth_ids: List[int] = None) -> List[BoothSummary]:
        """Get booth summaries with optional filtering"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM booth_summaries WHERE 1=1"
            params = []
            
            if booth_ids:
                query += " AND booth_id = ANY(%s)"
                params.append(booth_ids)
            
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            
            rows = cursor.fetchall()
           
            summaries = []
            for row in rows:
                data = dict(zip(columns, row))
                summaries.append(BoothSummary.from_dict(data))
            
            return summaries

    def refresh_all_summaries(self, booth_ids):
        """Recalculate all booth summaries"""
        for booth_id in booth_ids:
            self.update_booth_summary(booth_id)
        
        logger.info(f"Refreshed summaries for {len(booth_ids)} booths")