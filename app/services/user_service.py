from app.data.postgres_adapter import PostgresAdapter
from app.models.user import User
from app.core.security import verify_password
from app.data.excel_cache import ExcelCache
from app.utils.logger import logger

class UserService:
    def __init__(self, constituency_file=None):
        self.adapter = PostgresAdapter(constituency_file)

    def get_user_by_username(self, username: str):
        return self.adapter.get_user_by_username(username)
    
    def authenticate_user(self, username: str, password: str):
        user = self.adapter.get_user_by_username(username)
        if user != None and user["username"] == username:
            if verify_password(password, user.get("password_hash", "")):
                return user
        return None
    
    def get_user_by_mobile(self, mobile: str):
        return self.adapter.get_user_by_mobile(mobile)

    def get_users_created_by(self, creator_username: str):
        users = self.adapter.get_users()
        created_users = []
        for u in users:
            if u.get("created_by") == creator_username:
                created_users.append({
                    "user_id": u["user_id"],
                    "username": u["username"],
                    "full_name": u.get("full_name"),
                    "role": u["role"],
                    "phone": u.get("phone"),
                    "email": u.get("email"),
                    "assigned_booths": u["assigned_booths"],
                    "assigned_constituencies": u.get("assigned_constituencies", "")
                })
        return created_users

    def get_all_users(self):
        users = self.adapter.get_users()
        all_users = []
        for u in users:
            all_users.append({
                "user_id": u["user_id"],
                "username": u["username"],
                "full_name": u.get("full_name"),
                "role": u["role"],
                "phone": u.get("phone"),
                "email": u.get("email"),
                "assigned_booths": u["assigned_booths"],
                "assigned_constituencies": u.get("assigned_constituencies", ""),
                "created_by": u.get("created_by")
            })
        return all_users

    def create_user(self, username, role, full_name, phone, email, assigned_booths, assigned_constituencies, password_hash, created_by):
        user_data = (username, role, full_name, phone, assigned_booths, password_hash, email, created_by, assigned_constituencies)
        return self.adapter.create_user(user_data)
    
    def update_user(self, user_id, updates):
        return self.adapter.update_user(user_id, updates)
    
    def delete_user(self, user_id):
        return self.adapter.delete_user(user_id)
    
    def get_user_by_id(self, user_id):
        return self.adapter.get_user_by_id(user_id)
    
    def update_user_password(self, username, hashed_password):
        user = self.get_user_by_username(username)
        if user:
            return self.adapter.update_user(user['user_id'], {'password_hash': hashed_password})
        return False
    
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
    
