from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.schemas.scheme_schema import SchemeCreate, SchemeUpdate, SchemeResponse, SchemeBeneficiaryUpdate
from app.services.scheme_service import SchemeService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=SchemeResponse)
async def create_scheme(
    scheme_data: SchemeCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new scheme (Admin only)"""
    scheme_service = SchemeService()
    scheme = scheme_service.create_scheme(scheme_data.dict(), current_user.user_id)
    return scheme.to_response_dict()

@router.get("/", response_model=List[SchemeResponse])
async def get_all_schemes(
    current_user: User = Depends(get_current_user)
):
    """Get all schemes (Admin only)"""
    scheme_service = SchemeService()
    schemes = scheme_service.get_all_schemes()
    return [scheme.to_response_dict() for scheme in schemes]

@router.get("/{scheme_id}", response_model=SchemeResponse)
async def get_scheme(
    scheme_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get scheme by ID (Admin only)"""
    scheme_service = SchemeService()
    scheme = scheme_service.get_scheme_by_id(scheme_id)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheme not found"
        )
    return scheme.to_response_dict()

@router.put("/{scheme_id}", response_model=SchemeResponse)
async def update_scheme(
    scheme_id: int,
    update_data: SchemeUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update scheme (Admin only)"""
    scheme_service = SchemeService()
    
    # Filter out None values
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    
    scheme = scheme_service.update_scheme(scheme_id, update_dict)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheme not found"
        )
    return scheme.to_response_dict()

@router.delete("/{scheme_id}")
async def delete_scheme(
    scheme_id: int,
    current_user: User = Depends(get_current_user)
):
    """Delete scheme (Admin only)"""
    scheme_service = SchemeService()
    
    if not scheme_service.get_scheme_by_id(scheme_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheme not found"
        )
    
    success = scheme_service.delete_scheme(scheme_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete scheme"
        )
    
    return {"message": "Scheme deleted successfully"}

@router.post("/beneficiaries")
async def update_voter_schemes(
    beneficiary_data: SchemeBeneficiaryUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update voter's scheme beneficiaries (Admin only)"""
    scheme_service = SchemeService()
    
    success = scheme_service.update_voter_schemes(
        beneficiary_data.voter_epic,
        beneficiary_data.scheme_ids,
        current_user
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voter not found or unauthorized"
        )
    
    return {"message": "Voter schemes updated successfully"}

@router.get("/beneficiaries/{scheme_id}")
async def get_scheme_beneficiaries(
    scheme_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get voters assigned to a scheme (Admin only)"""
    scheme_service = SchemeService()
    
    if not scheme_service.get_scheme_by_id(scheme_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheme not found"
        )
    
    beneficiaries = scheme_service.get_scheme_beneficiaries(scheme_id)
    return {
        "scheme_id": scheme_id,
        "beneficiaries": beneficiaries,
        "total_count": len(beneficiaries)
    }

@router.get("/voter/{voter_epic}")
async def get_voter_schemes(
    voter_epic: str,
    current_user: User = Depends(get_current_user)
):
    """Get schemes assigned to a voter (Admin only)"""
    scheme_service = SchemeService()
    
    schemes = scheme_service.get_voter_schemes(voter_epic)
    return {
        "voter_epic": voter_epic,
        "schemes": schemes,
        "total_count": len(schemes)
    }