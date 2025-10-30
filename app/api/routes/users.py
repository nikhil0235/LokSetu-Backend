from fastapi import APIRouter, Depends, HTTPException, Path, Form, Body
from typing import List
from app.api.deps import get_current_user
from app.models.user import User
from app.services.user_service import UserService
from app.core.security import hash_password
from app.utils.logger import logger

ROLE_RANK = {
    "super_admin": 1,
    "political_party": 2,
    "district_prabhari": 3,
    "candidate": 4,
    "vidhan_sabha_prabhari": 5,
    "block_prabhari": 6,
    "panchayat_prabhari": 7,
    "booth_volunteer": 8
}

router = APIRouter()

@router.get("/", response_model=List[dict])
async def list_users(
    user: User = Depends(get_current_user)
):
    try:
        service = UserService()
        all_users = service.get_all_users()
        user_booth_ids = set(user.get("assigned_booths", []))
        filtered_users = []
        for u in all_users:
            booth_ids = set(u.get("assigned_booths", ""))
            if (user_booth_ids & booth_ids) and ROLE_RANK[u.get("role")]-ROLE_RANK[user["role"]] == 1:
                filtered_users.append(u)
        
        return filtered_users
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve users. Please try again later.")


@router.post("/")
async def create_user(
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    full_name: str = Form(""),
    phone: str = Form(""),
    email: str = Form(""),
    assigned_booths: str = Form(""),
    assigned_constituencies: str = Form(""),
    assigned_blocks: str = Form(""),
    assigned_panchayats: str = Form(""),
    district_id: int = Form(None),
    state_id: int = Form(None),
    party_id: int = Form(None),
    alliance_id: int = Form(None),
    user: User = Depends(get_current_user)
):
    try:
        logger.info(f"🚀 Creating user: {username}, role: {role}")
        logger.info(f"📋 Form data - booths: {assigned_booths[:100]}..., constituencies: {assigned_constituencies}, party_id: {party_id}")
        
        if ROLE_RANK[user["role"]] > ROLE_RANK[role]:
            logger.error(f"❌ Role validation failed: current user role {user['role']} cannot create {role}")
            raise HTTPException(status_code=403, detail="Cannot create user with higher role than current user")

        service = UserService()
        
        # Check if username exists
        logger.info(f"🔍 Checking if username {username} exists...")
        existing_user = service.get_user_by_username(username)
        if existing_user:
            logger.error(f"❌ Username {username} already exists")
            raise HTTPException(status_code=400, detail="Username already exists")

        # Validate party/alliance constraint
        if party_id and alliance_id:
            logger.error(f"❌ Party/alliance validation failed: party_id={party_id}, alliance_id={alliance_id}")
            raise HTTPException(status_code=400, detail="User cannot belong to both party and alliance")
        
        logger.info(f"✅ Validation passed, creating user via service layer...")
        # Create user via service layer
        created_user = service.create_user(username, role, full_name, phone, email, assigned_booths, assigned_constituencies, hash_password(password), user["user_id"], party_id, alliance_id, assigned_blocks, assigned_panchayats, district_id, state_id)
        
        logger.info(f"✅ User {username} created successfully with ID: {created_user['user_id']}")
        return {
            "message": f"User {username} created successfully with assigned booth ids {assigned_booths} with role {role}",
            "user_id": created_user["user_id"],
            "username": created_user["username"]
        }
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e).lower()
        logger.error(f"💥 Error creating user {username}: {str(e)}")
        logger.error(f"📊 Full error details: {repr(e)}")
        
        # Handle specific constraint violations
        if "unique constraint" in error_msg or "duplicate key" in error_msg:
            if "phone" in error_msg:
                raise HTTPException(status_code=400, detail="This phone number is already registered with another user.")
            elif "email" in error_msg:
                raise HTTPException(status_code=400, detail="This email address is already registered with another user.")
            elif "username" in error_msg:
                raise HTTPException(status_code=400, detail="This username is already taken. Please choose a different one.")
        
        raise HTTPException(status_code=500, detail="Failed to create user. Please try again later.")


@router.patch("/{userId}")
async def update_user(
    userId: int,
    updates: dict = Body(...),
    user: User = Depends(get_current_user)
):
    try:
        service = UserService()
        
        target_user = service.get_user_by_id(userId)
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        current_role = target_user['role']
        if ROLE_RANK[user["role"]] > ROLE_RANK[current_role]:
            raise HTTPException(status_code=403, detail="Only higher roles can update this user")
        
        # Map fields and hash password if needed
        field_mapping = {
            "username": "username",
            "role": "role", 
            "full_name": "full_name",
            "phone": "phone",
            "assigned_booths": "assigned_booths",
            "assigned_constituencies": "assigned_constituencies",
            "assigned_blocks": "assigned_blocks",
            "assigned_panchayats": "assigned_panchayats",
            "email": "email",
            "district_id": "district_id",
            "state_id": "state_id",
            "party_id": "party_id",
            "alliance_id": "alliance_id"
        }
        
        db_updates = {}
        for field, value in updates.items():
            if field in field_mapping and value is not None:
                db_field = field_mapping[field]
                if field == "password":
                    value = hash_password(value)
                db_updates[db_field] = value
        
        if db_updates:
            service.update_user(userId, db_updates)
        
        return {"message": f"User {userId} updated", "success": True}
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e).lower()
        logger.error(f"Error updating user {userId}: {str(e)}")
        
        # Handle specific constraint violations
        if "unique constraint" in error_msg or "duplicate key" in error_msg:
            if "phone" in error_msg:
                raise HTTPException(status_code=400, detail="This phone number is already registered with another user.")
            elif "email" in error_msg:
                raise HTTPException(status_code=400, detail="This email address is already registered with another user.")
            elif "username" in error_msg:
                raise HTTPException(status_code=400, detail="This username is already taken. Please choose a different one.")
        
        raise HTTPException(status_code=500, detail="Failed to update user. Please try again later.")


@router.delete("/{userId}")
async def delete_user(
    userId: int,
    user: User = Depends(get_current_user)
):
    service = UserService()
    
    # Check if user exists and get current role
    target_user = service.get_user_by_id(userId)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_role = target_user['role']
    if ROLE_RANK[user["role"]] >= ROLE_RANK[current_role]:
        raise HTTPException(status_code=403, detail="Only higher roles can delete this user")
    
    service.delete_user(userId)
    
    return {"message": f"User {userId} deleted"}


# @router.get("/assigned-booths")
# async def get_assigned_booths(
#     user: User = Depends(get_current_user)
# ):
#     service = UserService()
    
#     if user.role == "super_admin":
#         # Super admin gets all booths (sample implementation)
#         return service.get_all_booths()
#     elif user.role == "district_prabhari":
#         # District Prabhari gets booths from assigned constituencies only
#         if not user.assigned_constituencies:
#             return []
            
#         # Filter booths by assigned booth IDs if available
#         assigned_booth_ids = user.assigned_scope.get("booth_ids", [])
#         if assigned_booth_ids:
#             # District Prabhari has specific booth assignments
#             import requests
#             all_booths = []
#             try:
#                 for constituency_id in user.assigned_constituencies:
#                     url = "https://gateway-voters.eci.gov.in/api/v1/printing-publish/get-part-list"
#                     payload = {
#                         "stateCd": "S04",
#                         "districtCd": "S0429",
#                         "acNumber": str(constituency_id),
#                         "pageNumber": 0,
#                         "pageSize": 100
#                     }
#                     headers = {
#                         "Accept": "*/*",
#                         "content-type": "application/json",
#                         "platform-type": "ECIWEB"
#                     }
#                     resp = requests.post(url, json=payload, headers=headers)
#                     data = resp.json()
#                     if "payload" in data:
#                         # Filter by assigned booth IDs
#                         filtered_booths = [booth for booth in data["payload"] 
#                                          if str(booth.get("id", booth.get("boothId", ""))) in assigned_booth_ids]
#                         all_booths.extend(filtered_booths)
#                 return all_booths
#             except:
#                 return service.get_user_booths(user.assigned_scope)
#         else:
#             # District Prabhari gets all booths from assigned constituencies
#             import requests
#             all_booths = []
#             try:
#                 for constituency_id in user.assigned_constituencies:
#                     url = "https://gateway-voters.eci.gov.in/api/v1/printing-publish/get-part-list"
#                     payload = {
#                         "stateCd": "S04",
#                         "districtCd": "S0429",
#                         "acNumber": str(constituency_id),
#                         "pageNumber": 0,
#                         "pageSize": 100
#                     }
#                     headers = {
#                         "Accept": "*/*",
#                         "content-type": "application/json",
#                         "platform-type": "ECIWEB"
#                     }
#                     resp = requests.post(url, json=payload, headers=headers)
#                     data = resp.json()
#                     if "payload" in data:
#                         all_booths.extend(data["payload"])
#                 return all_booths
#             except:
#                 return service.get_all_booths()
#     else:  # booth_boy
#         return service.get_user_booths(user.assigned_scope)


# @router.get("/assigned-constituencies")
# async def get_assigned_constituencies(
#     user: User = Depends(get_current_user)
# ):
#     service = UserService()
    
#     if user.role == "super_admin":
#         # Super admin gets all constituencies
#         import requests
#         try:
#             response = requests.get(
#                 "https://gateway-voters.eci.gov.in/api/v1/common/constituencies",
#                 params={"stateCode": "S04"}
#             )
#             return [{
#                 'id': r['acId'],
#                 'name': r['asmblyName'],
#                 'state_name': 'Bihar',
#                 'district_name': r.get('districtCd', ''),
#                 'assembly_number': r['asmblyNo']
#             } for r in response.json()]
#         except:
#             return service.get_all_constituencies()
#     elif user.role == "district_prabhari":
#         # District Prabhari gets only assigned constituencies
#         import requests
#         try:
#             response = requests.get(
#                 "https://gateway-voters.eci.gov.in/api/v1/common/constituencies",
#                 params={"stateCode": "S04"}
#             )
#             all_constituencies = response.json()
#             # Filter by assigned constituency IDs for District Prabhari
#             assigned_ids = [str(cid) for cid in user.assigned_constituencies]
#             filtered = [r for r in all_constituencies if str(r['acId']) in assigned_ids]
#             return [{
#                 'id': r['acId'],
#                 'name': r['asmblyName'],
#                 'state_name': 'Bihar',
#                 'district_name': r.get('districtCd', ''),
#                 'assembly_number': r['asmblyNo']
#             } for r in filtered]
#         except:
#             return service.get_all_constituencies()
#     else:  # booth_boy
#         return []


# @router.get("/test")
# def test_endpoint():
#     logger.info("Test endpoint called")
#     return {"message": "Backend is reachable", "status": "ok"}



