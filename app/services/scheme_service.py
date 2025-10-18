import pandas as pd
import os
from typing import List, Optional, Dict
from datetime import datetime
import json

from app.models.scheme import Scheme
from app.core.config import settings

class SchemeService:
    def __init__(self):
        self.schemes_file = os.path.join(settings.EXCEL_DIR, "Schemes.xlsx")
        self._ensure_schemes_file()

    def _ensure_schemes_file(self):
        """Create schemes file if it doesn't exist"""
        if not os.path.exists(self.schemes_file):
            df = pd.DataFrame(columns=["SchemeID", "Name", "Description", "Category", "CreatedBy", "CreatedAt", "UpdatedAt"])
            df.to_excel(self.schemes_file, index=False, sheet_name="Schemes")

    def _get_next_scheme_id(self) -> int:
        """Get next available scheme ID"""
        try:
            df = pd.read_excel(self.schemes_file, sheet_name="Schemes")
            if df.empty:
                return 1
            return int(df["SchemeID"].max()) + 1
        except:
            return 1

    def create_scheme(self, scheme_data: dict, created_by: int) -> Scheme:
        """Create a new scheme"""
        scheme_id = self._get_next_scheme_id()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        scheme = Scheme(
            scheme_id=scheme_id,
            name=scheme_data["name"],
            description=scheme_data.get("description"),
            category=scheme_data["category"],
            created_by=created_by,
            created_at=now,
            updated_at=now
        )
        
        # Read existing data
        try:
            df = pd.read_excel(self.schemes_file, sheet_name="Schemes")
        except:
            df = pd.DataFrame()
        
        # Add new scheme
        new_row = pd.DataFrame([scheme.to_dict()])
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Save to Excel
        with pd.ExcelWriter(self.schemes_file, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Schemes")
        
        return scheme

    def get_all_schemes(self) -> List[Scheme]:
        """Get all schemes"""
        try:
            df = pd.read_excel(self.schemes_file, sheet_name="Schemes")
            return [Scheme.from_dict(row.to_dict()) for _, row in df.iterrows()]
        except:
            return []

    def get_scheme_by_id(self, scheme_id: int) -> Optional[Scheme]:
        """Get scheme by ID"""
        try:
            df = pd.read_excel(self.schemes_file, sheet_name="Schemes")
            scheme_row = df[df["SchemeID"] == scheme_id]
            if not scheme_row.empty:
                return Scheme.from_dict(scheme_row.iloc[0].to_dict())
        except:
            pass
        return None

    def update_scheme(self, scheme_id: int, update_data: dict) -> Optional[Scheme]:
        """Update scheme"""
        try:
            df = pd.read_excel(self.schemes_file, sheet_name="Schemes")
            scheme_idx = df[df["SchemeID"] == scheme_id].index
            
            if len(scheme_idx) == 0:
                return None
            
            idx = scheme_idx[0]
            if "name" in update_data:
                df.at[idx, "Name"] = update_data["name"]
            if "description" in update_data:
                df.at[idx, "Description"] = update_data["description"]
            if "category" in update_data:
                df.at[idx, "Category"] = update_data["category"]
            
            df.at[idx, "UpdatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save to Excel
            with pd.ExcelWriter(self.schemes_file, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Schemes")
            
            return Scheme.from_dict(df.iloc[idx].to_dict())
        except:
            return None

    def delete_scheme(self, scheme_id: int) -> bool:
        """Delete scheme and clean up voter references"""
        try:
            df = pd.read_excel(self.schemes_file, sheet_name="Schemes")
            df = df[df["SchemeID"] != scheme_id]
            
            # Save updated schemes
            with pd.ExcelWriter(self.schemes_file, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Schemes")
            
            # Clean up voter scheme references
            self._cleanup_voter_scheme_references(scheme_id)
            
            return True
        except:
            return False

    def _cleanup_voter_scheme_references(self, deleted_scheme_id: int):
        """Remove deleted scheme ID from all voters"""
        from app.services.voter_service import VoterService
        voter_service = VoterService()
        
        # This would need to iterate through all constituency files
        # For now, just handle the main constituency file
        constituency_files = [f for f in os.listdir(settings.EXCEL_DIR) if f.startswith("Constituency_") and f.endswith(".xlsx")]
        
        for file in constituency_files:
            try:
                file_path = os.path.join(settings.EXCEL_DIR, file)
                df = pd.read_excel(file_path, sheet_name="Voters_Data")
                
                # Clean scheme IDs
                for idx, row in df.iterrows():
                    scheme_ids_str = row.get("SchemeIds", "")
                    if scheme_ids_str:
                        try:
                            scheme_ids = json.loads(scheme_ids_str) if scheme_ids_str else []
                            if deleted_scheme_id in scheme_ids:
                                scheme_ids.remove(deleted_scheme_id)
                                df.at[idx, "SchemeIds"] = json.dumps(scheme_ids)
                        except:
                            continue
                
                # Save updated data
                with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                    df.to_excel(writer, index=False, sheet_name="Voters_Data")
            except:
                continue

    def update_voter_schemes(self, voter_epic: str, scheme_ids: List[int], user, constituency_file) -> bool:
        """Update voter's scheme beneficiaries"""
        from app.services.voter_service import VoterService
        voter_service = VoterService(constituency_file)
        
        # Update voter with new scheme IDs using voter service
        update_data = {"SchemeIds": json.dumps(scheme_ids)}
        return voter_service.update_voter(user, voter_epic, update_data)