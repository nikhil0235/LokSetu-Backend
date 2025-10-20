from app.data.postgres_adapter import PostgresAdapter
from app.models.voter import Voter
from app.utils.logger import logger
from app.services.booth_summary_service import BoothSummaryService

class VoterService:
    def __init__(self, constituency_file=None):
        self.adapter = PostgresAdapter(constituency_file)
        self.booth_summary_service = BoothSummaryService(self.adapter)

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
            if booth_id:
                self.booth_summary_service.update_booth_summary(booth_id)
            logger.info(f"Updated voter {epic_id} and booth summary")
        return result

    def get_booth_summaries(self, booth_ids):
        return self.booth_summary_service.get_booth_summaries(booth_ids)

    def bulk_update_voters(self, user, field_updates, options=None):
        """Bulk update voters with permission validation"""
        options = options or {}
        all_epic_ids = set()
        updated_counts = {}
        
        # Collect all epic IDs to validate permissions
        for field, updates in field_updates.items():
            all_epic_ids.update(updates.keys())
        
        # Get booth IDs for permission check
        affected_booth_ids = self.adapter.get_affected_booth_ids(list(all_epic_ids))
        
        # Validate user has access to all affected booths
        if user['role'] == 'booth_volunteer':
            unauthorized_booths = set(affected_booth_ids) - set(user['assigned_booths'])
            if unauthorized_booths:
                raise ValueError(f"Access denied to booths: {unauthorized_booths}")
        
        # Perform bulk updates for each field
        for field, updates in field_updates.items():
            if updates:  # Skip empty updates
                count = self.adapter.bulk_update_voters_by_field(field, updates, user['user_id'])
                updated_counts[field] = count
                logger.info(f"Bulk updated {count} voters for field '{field}'")
        
        # Refresh booth summaries if requested
        refreshed_booths = []
        if options.get('refresh_booth_summaries', True):
            self.booth_summary_service.refresh_all_summaries(affected_booth_ids)
            refreshed_booths = affected_booth_ids
        
        return {
            'updated_counts': updated_counts,
            'total_voters_affected': len(all_epic_ids),
            'booth_summaries_refreshed': refreshed_booths
        }

    def refresh_booth_summaries(self, booth_ids = None):
        """Refresh all booth summaries"""
        self.booth_summary_service.refresh_all_summaries(booth_ids)
