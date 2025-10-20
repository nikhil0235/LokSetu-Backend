from app.data.postgres_adapter import PostgresAdapter
from app.models.party import Party, Alliance
from app.utils.logger import logger
from typing import List, Optional

class PartyService:
    def __init__(self):
        self.adapter = PostgresAdapter()
    
    def get_all_parties(self, is_active: Optional[bool] = None) -> List[Party]:
        parties_data = self.adapter.get_parties(is_active)
        return [Party.from_dict(party) for party in parties_data]
    
    def get_party_by_id(self, party_id: int) -> Optional[Party]:
        party_data = self.adapter.get_party_by_id(party_id)
        if party_data:
            return Party.from_dict(party_data)
        return None
    
    def create_party(self, party_data: dict) -> Party:
        created_party = self.adapter.create_party(party_data)
        logger.info(f"Created party: {created_party['party_name']}")
        return Party.from_dict(created_party)
    
    def update_party(self, party_id: int, updates: dict) -> Optional[Party]:
        updated_party = self.adapter.update_party(party_id, updates)
        if updated_party:
            logger.info(f"Updated party ID: {party_id}")
            return Party.from_dict(updated_party)
        return None
    
    def delete_party(self, party_id: int) -> bool:
        success = self.adapter.delete_party(party_id)
        if success:
            logger.info(f"Deleted party ID: {party_id}")
        return success
    
    def get_all_alliances(self, is_active: Optional[bool] = None) -> List[Alliance]:
        alliances_data = self.adapter.get_alliances(is_active)
        alliances = []
        for alliance_data in alliances_data:
            alliance = Alliance.from_dict(alliance_data)
            # Get alliance parties
            full_alliance = self.adapter.get_alliance_by_id(alliance.alliance_id)
            if full_alliance and full_alliance.get('parties'):
                alliance.parties = [Party.from_dict(party) for party in full_alliance['parties']]
            alliances.append(alliance)
        return alliances
    
    def get_alliance_by_id(self, alliance_id: int) -> Optional[Alliance]:
        alliance_data = self.adapter.get_alliance_by_id(alliance_id)
        if alliance_data:
            alliance = Alliance.from_dict(alliance_data)
            if alliance_data.get('parties'):
                alliance.parties = [Party.from_dict(party) for party in alliance_data['parties']]
            return alliance
        return None
    
    def create_alliance(self, alliance_data: dict) -> Alliance:
        created_alliance = self.adapter.create_alliance(alliance_data)
        logger.info(f"Created alliance: {created_alliance['alliance_name']}")
        return Alliance.from_dict(created_alliance)
    
    def update_alliance(self, alliance_id: int, updates: dict) -> Optional[Alliance]:
        updated_alliance = self.adapter.update_alliance(alliance_id, updates)
        if updated_alliance:
            logger.info(f"Updated alliance ID: {alliance_id}")
            alliance = Alliance.from_dict(updated_alliance)
            if updated_alliance.get('parties'):
                alliance.parties = [Party.from_dict(party) for party in updated_alliance['parties']]
            return alliance
        return None
    
    def delete_alliance(self, alliance_id: int) -> bool:
        success = self.adapter.delete_alliance(alliance_id)
        if success:
            logger.info(f"Deleted alliance ID: {alliance_id}")
        return success
    
    def map_party_to_alliance(self, party_id: int, alliance_id: int, joined_date=None) -> bool:
        success = self.adapter.map_party_to_alliance(party_id, alliance_id, joined_date)
        if success:
            logger.info(f"Mapped party {party_id} to alliance {alliance_id}")
        return success