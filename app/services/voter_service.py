from app.data.excel_adapter import ExcelAdapter
from app.models.voter import Voter
from app.utils.logger import logger
from app.services.booth_summary_service import BoothSummaryService

class VoterService:
    def __init__(self, constituency_file):
        self.adapter = ExcelAdapter(constituency_file)
        self.booth_summary_service = BoothSummaryService(self.adapter)

    def search_voters(self, user_scope: dict, filters: dict = None):
        voters_data = self.adapter.get_voters(
            booth_ids=user_scope.get("booth_ids"),
            # constituency_id=user_scope.get("constituency_id")
        )
        # Convert to Voter objects
        voters = [Voter.from_dict(v) for v in voters_data]

        # Apply additional filters
        if filters:
            for key, value in filters.items():
                voters = [v for v in voters if str(getattr(v, key, "")).lower() == str(value).lower()]

        logger.info(f"Fetched {len(voters)} voters with expanded schema")
        return [v.to_dict() for v in voters]

    def update_voter(self, user, epic_id, changes):
        # Verify access to the voter
        allowed_voters = self.adapter.get_voters(
            booth_ids=user.assigned_scope.get("booth_ids"),
            constituency_id=user.assigned_scope.get("constituency_id")
        )
        voter_data = next((v for v in allowed_voters if v["VoterEPIC"] == epic_id), None)
        if not voter_data:
            logger.warning(f"Unauthorized voter update attempt by {user.username}")
            return False

        result = self.adapter.update_voter(epic_id, changes, user.user_id)
        if result:
            # Update booth summary after voter change
            booth_id = voter_data.get("BoothID")
            if booth_id:
                self.booth_summary_service.update_booth_summary(booth_id)
            logger.info(f"Updated voter {epic_id} and booth summary")
        return result

    def get_booth_summaries(self, user_scope: dict):
        """Get booth summaries based on user access"""
        booth_ids = user_scope.get("booth_ids")
        return self.booth_summary_service.get_booth_summaries(booth_ids)

    def refresh_booth_summaries(self):
        """Refresh all booth summaries"""
        self.booth_summary_service.refresh_all_summaries()
