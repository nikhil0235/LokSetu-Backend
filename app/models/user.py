from typing import Dict, List, Union

class User:
    def __init__(
        self,
        user_id: int,
        username: str,
        role: str,
        assigned_scope: Dict = None,
        full_name: str = "",
        phone: str = "",
        email: str = None,
        created_by: str = None,
        assigned_constituencies: List[str] = None,
        assigned_blocks: List[str] = None,
        assigned_panchayats: List[str] = None,
        district_id: int = None,
        state_id: int = None,
        party_id: int = None,
        alliance_id: int = None,
        party_name: str = None,
        alliance_name: str = None
    ):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.assigned_scope = assigned_scope or {}
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.created_by = created_by
        self.assigned_constituencies = assigned_constituencies or []
        self.assigned_blocks = assigned_blocks or []
        self.assigned_panchayats = assigned_panchayats or []
        self.district_id = district_id
        self.state_id = state_id
        self.party_id = party_id
        self.alliance_id = alliance_id
        self.party_name = party_name
        self.alliance_name = alliance_name

    def can_access_booth(self, booth_id: Union[str, int]) -> bool:
        if self.role == "super_admin":
            return True
        if self.role == "admin":
            return True  # Admin can access all booths in their constituencies
        if self.role == "booth_boy":
            return str(booth_id) in self.assigned_scope.get("booth_ids", [])
        return False

    def can_access_constituency(self, constituency_id: Union[str, int]) -> bool:
        if self.role == "super_admin":
            return True
        if self.role == "admin":
            return str(constituency_id) in self.assigned_constituencies
        return False

    def can_create_users(self) -> bool:
        return self.role in ["super_admin", "admin"]

    def can_view_user(self, target_user) -> bool:
        if self.role == "super_admin":
            return True
        if self.role == "admin":
            return target_user.created_by == self.username or target_user.username == self.username
        return target_user.username == self.username
