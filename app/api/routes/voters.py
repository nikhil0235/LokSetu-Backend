from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.voter_schema import VoterResponse, VoterUpdate
from app.services.voter_service import VoterService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[VoterResponse])
async def list_voters(
    user: User = Depends(get_current_user)
):
    if user['role'] != "booth_volunteer" :
        raise HTTPException(status_code=404, detail="User does not allowed to fetch voters")
    voter_service = VoterService()
    voters = voter_service.search_voters(user["assigned_booths"])
    return voters

@router.get("/booth/{booth_id}", response_model=List[VoterResponse])
async def list_voters(
    booth_id: int,
    user: User = Depends(get_current_user)
):
    if user['role'] != "booth_volunteer" :
        raise HTTPException(status_code=404, detail="User does not allowed to fetch voters")
    
    voter_service = VoterService()

    if int(booth_id) not in user['assigned_booths'] : 
        raise HTTPException(status_code=404, detail="User does not have access of this booth")

    voters = voter_service.search_voters([booth_id])
    return voters


@router.get("/{epic_id}", response_model=VoterResponse)
async def get_voter(
    epic_id: str
):
    voter_service = VoterService()
    voter = voter_service.get_voter_by_epic(epic_id)
    return voter


@router.patch("/{epic_id}")
async def update_voter(
    epic_id: str,
    payload: VoterUpdate,
    user: User = Depends(get_current_user)
):
    voter_service = VoterService()
    changes = payload.dict(exclude_unset=True)

    if not changes:
        raise HTTPException(status_code=400, detail="No fields to update")

    success = voter_service.update_voter(user, epic_id, changes)
    if not success:
        raise HTTPException(status_code=403, detail="Update failed or access denied")

    return {"message": f"Voter {epic_id} updated successfully", "updated_fields": changes}
