from fastapi import APIRouter, Depends, HTTPException, Path, Form, Body
from typing import List
from app.api.deps import get_current_user, get_constituency_file
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
    user: User = Depends(get_current_user),
    constituency_file: str = Depends(get_constituency_file)
):
    service = UserService(constituency_file)
    all_users = service.adapter.get_users()

    # filtered_users = [user for user in all_users if user.get("Created_by") == user.username]

    user_booth_ids = set(user.assigned_scope.get("booth_ids", []))

    filtered_users = []
    for u in all_users:
        assigned_str = u.get("AssignedBoothIDs", "")
        booth_ids = set(
            bid.strip()
            for bid in assigned_str.split(",")
            if bid.strip()
        )

        # Keep user if there is at least one booth overlap
        if (user_booth_ids & booth_ids) and ROLE_RANK[u.get("Role")]-ROLE_RANK[user.role] == 1:
            filtered_users.append(u)
    
    return filtered_users


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
    user: User = Depends(get_current_user),
    constituency_file: str = Depends(get_constituency_file)
):
    
    if ROLE_RANK[user.role] > ROLE_RANK[role]:
        raise HTTPException(status_code=403, detail="Cannot create user with higher role than current user")

    service = UserService(constituency_file)
    ws = service.adapter.ws_users

    for row in ws.iter_rows(min_row=2, values_only=True):
        existing_username = row[1]
        if existing_username == username:
            raise HTTPException(status_code=200, detail="Username already exists")

    # Get headers to ensure correct column order
    headers = [cell.value for cell in service.adapter.ws_users[1]]
    
    # Create user data in correct order
    user_data = [None] * len(headers)
    user_data[headers.index("UserID")] = service.adapter.ws_users.max_row
    user_data[headers.index("Username")] = username
    user_data[headers.index("Role")] = role
    user_data[headers.index("FullName")] = full_name
    user_data[headers.index("Phone")] = phone
    user_data[headers.index("AssignedBoothIDs")] = assigned_booths
    user_data[headers.index("PasswordHash")] = hash_password(password)
    user_data[headers.index("Email")] = email
    user_data[headers.index("Created_by")] = user.username
    user_data[headers.index("AssignedConstituencyIDs")] = assigned_constituencies
    
    # Find ParentID column if it exists
    if "ParentID" in headers:
        user_data[headers.index("ParentID")] = user.user_id
    
    ws.append(user_data)
    service.adapter._save()
    return {"message": f"User {username} created successfully with assigned booth ids {assigned_booths} with role {role}"}


@router.patch("/{userId}")
async def update_user(
    userId: int,
    updates: dict = Body(...),
    user: User = Depends(get_current_user),
    constituency_file: str = Depends(get_constituency_file)
):
    logger.info(f"Updating user {userId} with updates: {updates}")
    logger.info(f"Current user role: {user.role}")

    service = UserService(constituency_file)
    ws = service.adapter.ws_users
    headers = [c.value for c in ws[1]]
    userid_col = headers.index("UserID") + 1
    role_col = headers.index("role") + 1

    for row in range(2, ws.max_row + 1):
        if ws.cell(row=row, column=userid_col).value == userId:
            if ROLE_RANK[user.role] < ROLE_RANK[ws.cell(row=row, column=role_col).value]:
                raise HTTPException(status_code=403, detail="Only higher roles can update this user")
            
            field_mapping = {
                "username": "Username",
                "role": "Role", 
                "full_name": "FullName",
                "phone": "Phone",
                "assigned_booths": "AssignedBoothIDs",
                "assigned_constituencies": "AssignedConstituencyIDs",
                "email": "Email",
                "password": "PasswordHash"
            }
            
            for field, value in updates.items():
                if field in field_mapping and value is not None:
                    excel_field = field_mapping[field]
                    if field == "password":
                        value = hash_password(value)
                    col = headers.index(excel_field) + 1
                    ws.cell(row=row, column=col, value=value)
                    logger.info(f"Updated {excel_field} to {value}")
            
            service.adapter._save()
            logger.info(f"Successfully updated user {userId}")
            return {"message": f"User {userId} updated", "success": True}
    
    logger.warning(f"User {userId} not found")
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{userId}")
async def delete_user(
    userId: int,
    user: User = Depends(get_current_user),
    constituency_file: str = Depends(get_constituency_file)
):

    service = UserService(constituency_file)
    ws = service.adapter.ws_users
    headers = [c.value for c in ws[1]]
    userid_col = headers.index("UserID") + 1
    role_col = headers.index("role") + 1

    for row in range(2, ws.max_row + 1):
        if ws.cell(row=row, column=userid_col).value == userId:
            if ROLE_RANK[user.role] < ROLE_RANK[ws.cell(row=row, column=role_col).value]:
                raise HTTPException(status_code=403, detail="Only higher roles can delete this user")
            ws.delete_rows(row, 1)
            service.adapter._save()
            return {"message": f"User {userId} deleted"}
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/assigned-booths")
async def get_assigned_booths(
    user: User = Depends(get_current_user),
    constituency_file: str = Depends(get_constituency_file)
):
    service = UserService(constituency_file)
    
    if user.role == "super_admin":
        # Super admin gets all booths (sample implementation)
        return service.get_all_booths()
    elif user.role == "district_prabhari":
        # District Prabhari gets booths from assigned constituencies only
        if not user.assigned_constituencies:
            return []
            
        # Filter booths by assigned booth IDs if available
        assigned_booth_ids = user.assigned_scope.get("booth_ids", [])
        if assigned_booth_ids:
            # District Prabhari has specific booth assignments
            import requests
            all_booths = []
            try:
                for constituency_id in user.assigned_constituencies:
                    url = "https://gateway-voters.eci.gov.in/api/v1/printing-publish/get-part-list"
                    payload = {
                        "stateCd": "S04",
                        "districtCd": "S0429",
                        "acNumber": str(constituency_id),
                        "pageNumber": 0,
                        "pageSize": 100
                    }
                    headers = {
                        "Accept": "*/*",
                        "content-type": "application/json",
                        "platform-type": "ECIWEB"
                    }
                    resp = requests.post(url, json=payload, headers=headers)
                    data = resp.json()
                    if "payload" in data:
                        # Filter by assigned booth IDs
                        filtered_booths = [booth for booth in data["payload"] 
                                         if str(booth.get("id", booth.get("boothId", ""))) in assigned_booth_ids]
                        all_booths.extend(filtered_booths)
                return all_booths
            except:
                return service.get_user_booths(user.assigned_scope)
        else:
            # District Prabhari gets all booths from assigned constituencies
            import requests
            all_booths = []
            try:
                for constituency_id in user.assigned_constituencies:
                    url = "https://gateway-voters.eci.gov.in/api/v1/printing-publish/get-part-list"
                    payload = {
                        "stateCd": "S04",
                        "districtCd": "S0429",
                        "acNumber": str(constituency_id),
                        "pageNumber": 0,
                        "pageSize": 100
                    }
                    headers = {
                        "Accept": "*/*",
                        "content-type": "application/json",
                        "platform-type": "ECIWEB"
                    }
                    resp = requests.post(url, json=payload, headers=headers)
                    data = resp.json()
                    if "payload" in data:
                        all_booths.extend(data["payload"])
                return all_booths
            except:
                return service.get_all_booths()
    else:  # booth_boy
        return service.get_user_booths(user.assigned_scope)


@router.get("/assigned-constituencies")
async def get_assigned_constituencies(
    user: User = Depends(get_current_user),
    constituency_file: str = Depends(get_constituency_file)
):
    service = UserService(constituency_file)
    
    if user.role == "super_admin":
        # Super admin gets all constituencies
        import requests
        try:
            response = requests.get(
                "https://gateway-voters.eci.gov.in/api/v1/common/constituencies",
                params={"stateCode": "S04"}
            )
            return [{
                'id': r['acId'],
                'name': r['asmblyName'],
                'state_name': 'Bihar',
                'district_name': r.get('districtCd', ''),
                'assembly_number': r['asmblyNo']
            } for r in response.json()]
        except:
            return service.get_all_constituencies()
    elif user.role == "district_prabhari":
        # District Prabhari gets only assigned constituencies
        import requests
        try:
            response = requests.get(
                "https://gateway-voters.eci.gov.in/api/v1/common/constituencies",
                params={"stateCode": "S04"}
            )
            all_constituencies = response.json()
            # Filter by assigned constituency IDs for District Prabhari
            assigned_ids = [str(cid) for cid in user.assigned_constituencies]
            filtered = [r for r in all_constituencies if str(r['acId']) in assigned_ids]
            return [{
                'id': r['acId'],
                'name': r['asmblyName'],
                'state_name': 'Bihar',
                'district_name': r.get('districtCd', ''),
                'assembly_number': r['asmblyNo']
            } for r in filtered]
        except:
            return service.get_all_constituencies()
    else:  # booth_boy
        return []


@router.get("/test")
def test_endpoint():
    logger.info("Test endpoint called")
    return {"message": "Backend is reachable", "status": "ok"}



