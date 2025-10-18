from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.api.deps import get_current_user, get_voter_service
from app.models.user import User
from app.services.voter_service import VoterService
from app.schemas.booth_summary_schema import BoothSummaryResponse
from app.utils.logger import logger

router = APIRouter()

@router.get("/", response_model=List[BoothSummaryResponse])
async def get_booth_summaries(
    current_user: User = Depends(get_current_user),
    voter_service: VoterService = Depends(get_voter_service)
):
    """Get booth summaries based on user access"""
    try:
        summaries = voter_service.get_booth_summaries(current_user["assigned_booths"])
        return [summary.to_response_dict() for summary in summaries]
    except Exception as e:
        logger.error(f"Error fetching booth summaries: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch booth summaries")

@router.post("/refresh")
async def refresh_booth_summaries(
    current_user: User = Depends(get_current_user),
    voter_service: VoterService = Depends(get_voter_service)
):  
    try:
        voter_service.refresh_booth_summaries(current_user["assigned_booths"])
        return {"message": "Booth summaries refreshed successfully"}
    except Exception as e:
        logger.error(f"Error refreshing booth summaries: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh booth summaries")