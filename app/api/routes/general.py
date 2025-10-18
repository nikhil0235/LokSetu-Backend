from fastapi import APIRouter, Depends, Query, HTTPException, Path, Form
from typing import List
from app.api.deps import get_current_user, get_constituency_file
from app.models.user import User
import requests

router = APIRouter()

@router.get("/states", response_model=List[dict])
async def list_states(
    user: User = Depends(get_current_user)
):
    if user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Only admins can get information")

    response = requests.get("https://gateway-voters.eci.gov.in/api/v1/common/states")
    state_data = [{'stateId': r['stateId'], 'stateCd': r['stateCd'], 'stateName': r['stateName'], 'stateNameHindi': r['stateNameHindi']} for r in response.json()]
    return state_data 


@router.get("/districts", response_model=List[dict])
async def list_districts(
    user: User = Depends(get_current_user),
    state_id: str = Form(..., description="State ID to get districts for")  
):
    if user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Only admins can get information")

    response = requests.get(f"https://gateway-voters.eci.gov.in/api/v1/common/districts/{state_id}")
    district_data = [{'state': r['state'], 'districtNo': r['districtNo'], 'districtCd': r['districtCd'], 'districtValue': r['districtValue'], 'districtValueHindi': r['districtValueHindi']} for r in response.json()]
    return district_data 


@router.get("/assembly", response_model=List[dict])
async def list_assemblies(
    user: User = Depends(get_current_user),
    state_id: str = Query(..., description="State ID to get assemblies for")  
):
    if user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Only admins can get information")

    response = requests.get(
        "https://gateway-voters.eci.gov.in/api/v1/common/constituencies",
        params={"stateCode": state_id}
    )

    assembly_data = [
        {
            'stateCd': r['stateCd'],
            'districtCd': r['districtCd'],
            'asmblyName': r['asmblyName'],
            'asmblyNameL1': r['asmblyNameL1'],
            'asmblyNo': r['asmblyNo'],
            'acId': r['acId']
        }
        for r in response.json()
    ]
    return assembly_data

@router.get("/booths", response_model=List[dict])
async def list_booths(
    user: dict = Depends(get_current_user),
    state_id: str = Query(..., description="State ID to get districts for"),  
    district_id: str = Query(..., description="District ID to get districts for"),
    assembly_id: str = Query(..., description="Assembly ID to get districts for")
):
    if user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Only admins can get information")

    url = "https://gateway-voters.eci.gov.in/api/v1/printing-publish/get-part-list"
    payload = {
        "stateCd": state_id,
        "districtCd": district_id,
        "acNumber": assembly_id,
        "pageNumber": 0,
        "pageSize": 10
    }
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Origin": "https://voters.eci.gov.in",
        "User-Agent": "Mozilla/5.0",
        "applicationname": "VSP",
        "channelidobo": "VSP",
        "content-type": "application/json",
        "platform-type": "ECIWEB",
    }

    resp = requests.post(url, json=payload, headers=headers)

    # Safety check in case API response is missing 'payload'
    data = resp.json()
    if "payload" not in data:
        raise HTTPException(status_code=502, detail="Invalid response from ECI API")

    return data["payload"]