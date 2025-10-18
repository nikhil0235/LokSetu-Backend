from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.voter_schema import VoterResponse, VoterUpdate
from app.services.voter_service import VoterService
from app.api.deps import get_current_user, get_constituency_file
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[VoterResponse])
async def list_voters(
    booth_ids: Optional[str] = Query(None, description="Comma-separated booth IDs"),
    constituency_id: Optional[int] = Query(None, description="Filter by constituency"),
    user: User = Depends(get_current_user),
    constituency_file: str = Depends(get_constituency_file)
):
    """
    Get voters accessible to the current user.
    Can filter by booth IDs or constituency.
    """
    voter_service = VoterService(constituency_file)

    # Build scope from user role
    user_scope = user.assigned_scope
    filters = {}


    print(user_scope)
    
    if booth_ids:
        filters["booth_ids"] = [int(x) for x in booth_ids.split(",")]

    voters = voter_service.search_voters(user_scope=user_scope, filters=filters)
    return voters

@router.get("/booth_voters/{booth_id}", response_model=List[VoterResponse])
async def list_voters(
    booth_id: str,
    user: User = Depends(get_current_user),
    constituency_file: str = Depends(get_constituency_file)
):
    """
    Get voters accessible to the current user.
    Can filter by booth IDs or constituency.
    """
    voter_service = VoterService(constituency_file)

    # Build scope from user role
    user_scope = user.assigned_scope
    
    print(user_scope)
    print(str(booth_id))

    if str(booth_id) not in user_scope['booth_ids'] : 
        raise HTTPException(status_code=404, detail="User does not have access of this booth")
    
    user_scope['booth_ids'] = [booth_id]

    voters = voter_service.search_voters(user_scope=user_scope)
    return voters


@router.get("/{epic_id}", response_model=VoterResponse)
async def get_voter(
    epic_id: str,
    user: User = Depends(get_current_user),
    constituency_file: str = Depends(get_constituency_file)
):
    """
    Get a single voter by EPIC ID.
    """
    voter_service = VoterService(constituency_file)
    voters = voter_service.search_voters(user_scope=user.assigned_scope)

    voter = next((v for v in voters if v["VoterEPIC"] == epic_id), None)
    if not voter:
        raise HTTPException(status_code=404, detail="Voter not found or access denied")
    return voter


@router.patch("/{epic_id}")
async def update_voter(
    epic_id: str,
    payload: VoterUpdate,
    user: User = Depends(get_current_user),
    constituency_file: str = Depends(get_constituency_file)
):
    """
    Update a voter partially using EPIC ID.
    Only fields in VoterUpdate schema are allowed.
    """
    voter_service = VoterService(constituency_file)
    changes = payload.dict(exclude_unset=True)

    if not changes:
        raise HTTPException(status_code=400, detail="No fields to update")

    success = voter_service.update_voter(user, epic_id, changes)
    if not success:
        raise HTTPException(status_code=403, detail="Update failed or access denied")

    return {"message": f"Voter {epic_id} updated successfully", "updated_fields": changes}
