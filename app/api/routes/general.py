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