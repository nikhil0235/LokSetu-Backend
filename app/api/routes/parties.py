from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.schemas.party_schema import (
    PartyCreate, PartyUpdate, PartyResponse,
    AllianceCreate, AllianceUpdate, AllianceResponse,
    PartyAllianceMapping
)
from app.services.party_service import PartyService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

# Party endpoints
@router.get("/parties", response_model=List[PartyResponse])
async def get_parties(
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_user)
):
    """Get all parties"""
    party_service = PartyService()
    parties = party_service.get_all_parties(is_active)
    return [party.to_dict() for party in parties]

@router.get("/parties/{party_id}", response_model=PartyResponse)
async def get_party(
    party_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get party by ID"""
    party_service = PartyService()
    party = party_service.get_party_by_id(party_id)
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party.to_dict()

@router.post("/parties", response_model=PartyResponse)
async def create_party(
    party_data: PartyCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new party (Admin only)"""
    if current_user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    party_service = PartyService()
    party = party_service.create_party(party_data.dict())
    return party.to_dict()

@router.put("/parties/{party_id}", response_model=PartyResponse)
async def update_party(
    party_id: int,
    update_data: PartyUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update party (Admin only)"""
    if current_user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    party_service = PartyService()
    updates = {k: v for k, v in update_data.dict().items() if v is not None}
    party = party_service.update_party(party_id, updates)
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party.to_dict()

@router.delete("/parties/{party_id}")
async def delete_party(
    party_id: int,
    current_user: User = Depends(get_current_user)
):
    """Delete party (Admin only)"""
    if current_user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    party_service = PartyService()
    if not party_service.get_party_by_id(party_id):
        raise HTTPException(status_code=404, detail="Party not found")
    
    success = party_service.delete_party(party_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete party")
    
    return {"message": "Party deleted successfully"}

# Alliance endpoints
@router.get("/alliances", response_model=List[AllianceResponse])
async def get_alliances(
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_user)
):
    """Get all alliances"""
    party_service = PartyService()
    alliances = party_service.get_all_alliances(is_active)
    return [alliance.to_dict() for alliance in alliances]

@router.get("/alliances/{alliance_id}", response_model=AllianceResponse)
async def get_alliance(
    alliance_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get alliance by ID with member parties"""
    party_service = PartyService()
    alliance = party_service.get_alliance_by_id(alliance_id)
    if not alliance:
        raise HTTPException(status_code=404, detail="Alliance not found")
    return alliance.to_dict()

@router.post("/alliances", response_model=AllianceResponse)
async def create_alliance(
    alliance_data: AllianceCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new alliance (Admin only)"""
    if current_user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    party_service = PartyService()
    alliance = party_service.create_alliance(alliance_data.dict())
    return alliance.to_dict()

@router.put("/alliances/{alliance_id}", response_model=AllianceResponse)
async def update_alliance(
    alliance_id: int,
    update_data: AllianceUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update alliance (Admin only)"""
    if current_user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    party_service = PartyService()
    updates = {k: v for k, v in update_data.dict().items() if v is not None}
    alliance = party_service.update_alliance(alliance_id, updates)
    if not alliance:
        raise HTTPException(status_code=404, detail="Alliance not found")
    return alliance.to_dict()

@router.delete("/alliances/{alliance_id}")
async def delete_alliance(
    alliance_id: int,
    current_user: User = Depends(get_current_user)
):
    """Delete alliance (Admin only)"""
    if current_user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    party_service = PartyService()
    if not party_service.get_alliance_by_id(alliance_id):
        raise HTTPException(status_code=404, detail="Alliance not found")
    
    success = party_service.delete_alliance(alliance_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete alliance")
    
    return {"message": "Alliance deleted successfully"}

@router.post("/party-alliances")
async def map_party_to_alliance(
    mapping: PartyAllianceMapping,
    current_user: User = Depends(get_current_user)
):
    """Map party to alliance (Admin only)"""
    if current_user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    party_service = PartyService()
    
    # Verify party and alliance exist
    if not party_service.get_party_by_id(mapping.party_id):
        raise HTTPException(status_code=404, detail="Party not found")
    if not party_service.get_alliance_by_id(mapping.alliance_id):
        raise HTTPException(status_code=404, detail="Alliance not found")
    
    success = party_service.map_party_to_alliance(
        mapping.party_id, 
        mapping.alliance_id, 
        mapping.joined_date
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to map party to alliance")
    
    return {"message": "Party mapped to alliance successfully"}