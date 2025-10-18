from app.data.postgres_adapter import PostgresAdapter
from app.models.voter import Voter
from app.utils.logger import logger
from app.services.booth_summary_service import BoothSummaryService

class VoterService:
    def __init__(self, constituency_file=None):
        self.adapter = PostgresAdapter(constituency_file)
        # self.booth_summary_service = BoothSummaryService(self.adapter)

    def search_voters(self, booth_ids):
        voters_data = self.adapter.get_voters(booth_ids)
        # Convert to Voter objects
        voters = [Voter.from_dict(v) for v in voters_data]
        return voters

    def get_voter_by_epic(self, epic_id):
        voters_data = self.adapter.get_voters_by_epic(epic_id)
        if voters_data:
            return Voter.from_dict(voters_data[0])
        return None

    def update_voter(self, user, epic_id, changes):  
        result = self.adapter.update_voter(epic_id, changes, user['user_id'])
        if result:
            voter_data = self.adapter.get_voters_by_epic(epic_id)[0]
            booth_id = voter_data["booth_id"]
            # if booth_id:
            #     self.booth_summary_service.update_booth_summary(booth_id)
            print(booth_id)
            logger.info(f" voter {epic_id} and booth summary")
        return result

    def get_booth_summaries(self, user_scope: dict):
        """Get booth summaries based on user access"""
        booth_ids = user_scope.get("booth_ids")
        return self.booth_summary_service.get_booth_summaries(booth_ids)

    def refresh_booth_summaries(self):
        """Refresh all booth summaries"""
        self.booth_summary_service.refresh_all_summaries()
