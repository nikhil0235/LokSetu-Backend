from app.data.excel_adapter import ExcelAdapter
from app.models.user import User
from app.core.security import verify_password
from app.data.excel_cache import ExcelCache
from app.utils.logger import logger
import os
import glob

class UserService:
    def __init__(self, constituency_file):
        self.adapter = ExcelAdapter(constituency_file)

    def get_user_by_username(self, username: str):
        users = self.adapter.get_users()
        for u in users:
            if u["Username"] == username:
                return User(
                    user_id=u["UserID"],
                    username=u["Username"],
                    role=u["Role"],
                    assigned_scope=self._parse_scope(u["AssignedBoothIDs"]),
                    full_name=u.get("FullName"),
                    phone=u.get("Phone"),
                    email=u.get("Email"),
                    created_by=u.get("Created_by") or u.get("CreatedBy"),
                    assigned_constituencies=self._parse_constituencies(u.get("AssignedConstituencyIDs", ""))
                )
        return None

    def _parse_scope(self, booth_ids_str):
        if booth_ids_str == "ALL":
            return {}
        booth_ids = [x.strip() for x in booth_ids_str.split(",") if x.strip()] if booth_ids_str else []
        return {"booth_ids": booth_ids}
    
    def _parse_constituencies(self, constituency_ids_str):
        if not constituency_ids_str or constituency_ids_str == "ALL":
            return []
        return [x.strip() for x in constituency_ids_str.split(",") if x.strip()]
    
    def authenticate_user(self, username: str, password: str):
        users = self.adapter.get_users()
        for u in users:
            if u["Username"] == username:
                if verify_password(password, u.get("PasswordHash", "")):
                    return self.get_user_by_username(username)
        return None

    def get_users_created_by(self, creator_username: str):
        users = self.adapter.get_users()
        created_users = []
        for u in users:
            if u.get("CreatedBy") == creator_username:
                created_users.append({
                    "user_id": u["UserID"],
                    "username": u["Username"],
                    "full_name": u.get("FullName"),
                    "role": u["Role"],
                    "phone": u.get("Phone"),
                    "email": u.get("Email"),
                    "assigned_booths": self._parse_scope(u["AssignedBoothIDs"]),
                    "assigned_constituencies": self._parse_constituencies(u.get("AssignedConstituencyIDs", ""))
                })
        return created_users

    def get_all_users(self):
        users = self.adapter.get_users()
        all_users = []
        for u in users:
            all_users.append({
                "user_id": u["UserID"],
                "username": u["Username"],
                "full_name": u.get("FullName"),
                "role": u["Role"],
                "phone": u.get("Phone"),
                "email": u.get("Email"),
                "assigned_booths": self._parse_scope(u["AssignedBoothIDs"]),
                "assigned_constituencies": self._parse_constituencies(u.get("AssignedConstituencyIDs", "")),
                "created_by": u.get("CreatedBy"),
                "parent_id": u.get("ParentID")
            })
        return all_users

    def update_user_password(self, username, hashed_password):
        ExcelCache.acquire_write_lock(self.adapter.file_path)
        try:
            ws = self.adapter.ws_users
            headers = [c.value for c in ws[1]]
            username_col = headers.index("Username") + 1
            password_col = headers.index("PasswordHash") + 1

            for row in range(2, ws.max_row + 1):
                if ws.cell(row=row, column=username_col).value == username:
                    ws.cell(row=row, column=password_col, value=hashed_password)
                    self.adapter._save()
                    return True
            return False
        finally:
            ExcelCache.release_write_lock(self.adapter.file_path)
    
    def get_all_constituencies(self):
        # Get data from current Excel file
        voters = self.adapter.get_voters()
        
        if not voters:
            return []
            
        # Get unique constituency data
        constituencies = {}
        for voter in voters:
            const_id = voter.get("ConstituencyID")
            if const_id:
                if const_id not in constituencies:
                    unique_booths = set()
                    blocks = set()
                    panchayats = set()
                    
                    # Count data for this constituency
                    const_voters = [v for v in voters if v.get("ConstituencyID") == const_id]
                    for v in const_voters:
                        if v.get("BoothID"):
                            unique_booths.add(v["BoothID"])
                        if v.get("BlockName"):
                            blocks.add(v["BlockName"])
                        if v.get("PanchayatName"):
                            panchayats.add(v["PanchayatName"])
                    
                    constituencies[const_id] = {
                        "id": const_id,
                        "name": voter.get("ConstituencyName", f"Constituency {const_id}"),
                        "state_name": voter.get("StateName"),
                        "total_voters": len(const_voters),
                        "total_booths": len(unique_booths),
                        "blocks": list(blocks),
                        "panchayats": list(panchayats)
                    }
                    
        return list(constituencies.values())
    
    def get_assigned_constituencies(self, user_id):
        # For admin, return all constituencies like super_admin
        return self.get_all_constituencies()
    
    def get_all_booths(self):
        voters = self.adapter.get_voters()
        booths = {}
        
        for voter in voters:
            if voter.get("BoothID"):
                booth_id = voter["BoothID"]
                if booth_id not in booths:
                    # Count voters in this booth
                    booth_voters = [v for v in voters if v.get("BoothID") == booth_id]
                    booths[booth_id] = {
                        "id": booth_id,
                        "name": voter.get("BoothLocation", f"Booth {booth_id}"),
                        "booth_number": voter.get("BoothNumber", booth_id),
                        "constituency_id": voter.get("ConstituencyID"),
                        "constituency_name": voter.get("ConstituencyName"),
                        "state_name": voter.get("StateName"),
                        "block_name": voter.get("BlockName"),
                        "panchayat_name": voter.get("PanchayatName"),
                        "total_voters": len(booth_voters)
                    }
        
        return list(booths.values())
    
    def get_assigned_booths(self, user_id):
        # For admin, return all booths like super_admin
        return self.get_all_booths()
    
    def get_user_booths(self, assigned_scope):
        if not assigned_scope or not assigned_scope.get("booth_ids"):
            return []
        booth_ids = [int(bid) for bid in assigned_scope["booth_ids"]]
        voters = self.adapter.get_voters()
        booths = set()
        for voter in voters:
            if voter.get("BoothID") in booth_ids and voter.get("BoothLocation"):
                booths.add((voter["BoothID"], voter["BoothLocation"]))
        return [{"id": booth_id, "name": booth_location} for booth_id, booth_location in sorted(booths)]