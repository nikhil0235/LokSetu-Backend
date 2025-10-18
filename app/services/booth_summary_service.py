from collections import defaultdict
from typing import List, Dict
from app.models.booth_summary import BoothSummary
from app.utils.logger import logger
from datetime import datetime

class BoothSummaryService:
    def __init__(self, excel_adapter):
        self.adapter = excel_adapter
        self._ensure_booth_summary_sheet()

    def _ensure_booth_summary_sheet(self):
        """Create Booth_Summary sheet if it doesn't exist"""
        if "Booth_Summary" not in self.adapter.wb.sheetnames:
            ws = self.adapter.wb.create_sheet("Booth_Summary")
            headers = [
                "BoothID", "ConstituencyID", "TotalVoters", "MaleVoters", 
                "FemaleVoters", "OtherGenderVoters", "VotingPreferenceCounts",
                "ReligionCounts", "CategoryCounts", "EducationCounts", 
                "EmploymentCounts", "AgeGroupCounts", "LastUpdated"
            ]
            ws.append(headers)
            self.adapter._save()

    def calculate_booth_summary(self, booth_id: str) -> BoothSummary:
        """Calculate aggregations for a specific booth"""
        voters = self.adapter.get_voters(booth_ids=[booth_id])
        
        summary = BoothSummary(
            booth_id=booth_id,
            constituency_id=voters[0].get("ConstituencyID") if voters else None
        )
        
        if not voters:
            return summary

        # Basic counts
        summary.total_voters = len(voters)
        summary.male_voters = sum(1 for v in voters if str(v.get("Gender", "")).upper() == "M")
        summary.female_voters = sum(1 for v in voters if str(v.get("Gender", "")).upper() == "F")
        summary.other_gender_voters = summary.total_voters - summary.male_voters - summary.female_voters

        # Aggregation counts
        summary.voting_preference_counts = self._count_field(voters, "VotingPreference")
        summary.religion_counts = self._count_field(voters, "Religion")
        summary.category_counts = self._count_field(voters, "Category")
        summary.education_counts = self._count_field(voters, "EducationLevel")
        summary.employment_counts = self._count_field(voters, "EmploymentStatus")
        summary.age_group_counts = self._count_age_groups(voters)

        return summary

    def _count_field(self, voters: List[Dict], field: str) -> Dict[str, int]:
        """Count occurrences of field values"""
        counts = defaultdict(int)
        for voter in voters:
            value = voter.get(field)
            if value:
                counts[str(value)] += 1
        return dict(counts)

    def _count_age_groups(self, voters: List[Dict]) -> Dict[str, int]:
        """Count voters by age groups"""
        groups = {"18-25": 0, "26-35": 0, "36-50": 0, "51-65": 0, "65+": 0}
        for voter in voters:
            age = voter.get("Age")
            if age:
                try:
                    age = int(age)
                    if 18 <= age <= 25:
                        groups["18-25"] += 1
                    elif 26 <= age <= 35:
                        groups["26-35"] += 1
                    elif 36 <= age <= 50:
                        groups["36-50"] += 1
                    elif 51 <= age <= 65:
                        groups["51-65"] += 1
                    elif age > 65:
                        groups["65+"] += 1
                except ValueError:
                    pass
        return groups

    def update_booth_summary(self, booth_id: str):
        """Update summary for a specific booth"""
        summary = self.calculate_booth_summary(booth_id)
        self._save_booth_summary(summary)
        logger.info(f"Updated booth summary for booth {booth_id}")

    def _save_booth_summary(self, summary: BoothSummary):
        """Save booth summary to Excel"""
        ws = self.adapter.wb["Booth_Summary"]
        headers = [cell.value for cell in ws[1]]
        
        # Find existing row or create new
        booth_row = None
        for row in range(2, ws.max_row + 1):
            if ws.cell(row=row, column=1).value == summary.booth_id:
                booth_row = row
                break
        
        if not booth_row:
            booth_row = ws.max_row + 1
        
        # Update row with summary data
        summary_dict = summary.to_dict()
        for col, header in enumerate(headers, 1):
            ws.cell(row=booth_row, column=col, value=summary_dict.get(header))
        
        self.adapter._save()

    def get_booth_summaries(self, booth_ids: List[str] = None) -> List[BoothSummary]:
        """Get booth summaries with optional filtering"""
        if "Booth_Summary" not in self.adapter.wb.sheetnames:
            return []
        
        ws = self.adapter.wb["Booth_Summary"]
        rows = list(ws.iter_rows(min_row=2, values_only=True))
        headers = [cell.value for cell in ws[1]]
        
        summaries = []
        for row in rows:
            if row[0]:  # BoothID exists
                data = dict(zip(headers, row))
                # print(data)
                if not booth_ids or str(data["BoothID"]) in booth_ids:
                    summaries.append(BoothSummary.from_dict(data))
        
        return summaries

    def refresh_all_summaries(self):
        """Recalculate all booth summaries"""
        voters = self.adapter.get_voters()
        booth_ids = set(v.get("BoothID") for v in voters if v.get("BoothID"))
        for booth_id in booth_ids:
            self.update_booth_summary(str(booth_id))
        
        logger.info(f"Refreshed summaries for {len(booth_ids)} booths")