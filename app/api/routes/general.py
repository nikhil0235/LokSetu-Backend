from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from app.api.deps import get_current_user
from app.models.user import User
from app.data.postgres_adapter import PostgresAdapter

router = APIRouter()
adapter = PostgresAdapter()

@router.get("/states", response_model=List[dict])
async def list_states(
):
    return adapter.get_states() 


@router.get("/districts", response_model=List[dict])
async def list_districts(
    state_id: Optional[int] = Query(None, description="State ID to get districts for")  
):

    return adapter.get_districts(state_id) 


@router.get("/constituencies", response_model=List[dict])
async def list_constituencies(
    state_id: Optional[int] = Query(None, description="State ID to get constituencies for"),
    district_id: Optional[int] = Query(None, description="District ID to get constituencies for")
):

    return adapter.get_constituencies(state_id, district_id)

@router.get("/blocks", response_model=List[dict])
async def list_blocks(
    constituency_id: Optional[int] = Query(None, description="Constituency ID to get blocks for")
):
    return adapter.get_blocks(constituency_id)

@router.get("/panchayats", response_model=List[dict])
async def list_panchayats(
    block_id: Optional[int] = Query(None, description="Block ID to get panchayats for")
):
    return adapter.get_panchayats(block_id)

@router.get("/booths", response_model=List[dict])
async def list_booths(
    constituency_id: Optional[int] = Query(None, description="Constituency ID to get booths for"),
    panchayat_id: Optional[int] = Query(None, description="Panchayat ID to get booths for")
):
    return adapter.get_booths(constituency_id, panchayat_id)

@router.get("/booths-by-blocks", response_model=List[dict])
async def list_booths_by_blocks(
    block_ids: str = Query(..., description="Comma-separated block IDs (e.g., '1,2,3')")
):
    """Get all booths falling under the specified blocks"""
    try:
        # Parse block IDs
        block_id_list = [int(bid.strip()) for bid in block_ids.split(',') if bid.strip()]
        if not block_id_list:
            raise HTTPException(status_code=400, detail="Invalid block_ids parameter")
        
        return adapter.get_booths_by_blocks(block_id_list)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid block_ids format. Use comma-separated integers.")