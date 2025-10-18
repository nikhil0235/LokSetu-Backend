from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import datetime

class VoterBase(BaseModel):
    constituency_id: int
    constituency_name: Optional[str]
    state_name: Optional[str]
    block_name: Optional[str]
    panchayat_name: Optional[str]
    booth_id: int
    booth_number: Optional[int]
    booth_location: Optional[str]
    part_number: Optional[str]

    epic_id: str = Field(..., description="Unique voter EPIC ID")
    serial_no_in_list: Optional[int]

    voter_fname: Optional[str]
    voter_lname: Optional[str]
    voter_fname_hin: Optional[str]
    voter_lname_hin: Optional[str]

    relation: Optional[str]
    guardian_fname: Optional[str]
    guardian_lname: Optional[str]
    guardian_fname_hin: Optional[str]
    guardian_lname_hin: Optional[str]

    house_no: Optional[Any]
    gender: Optional[str]
    dob: Optional[Any]
    age: Optional[int]

    mobile: Optional[Any]
    email_id: Optional[str]

    last_voted_party: Optional[str]
    voting_preference: Optional[str]
    certainty_of_vote: Optional[bool]
    vote_type: Optional[str]
    availability: Optional[str]

    religion: Optional[str]
    category: Optional[str]
    obc_subtype: Optional[str]
    caste: Optional[str]
    language_pref: Optional[str]

    education_level: Optional[str]
    employment_status: Optional[str]
    govt_job_type: Optional[str]
    govt_job_group: Optional[str]
    job_role: Optional[str]

    monthly_salary_range: Optional[str]
    private_job_role: Optional[str]
    private_salary_range: Optional[str]

    self_employed_service: Optional[str]
    business_type: Optional[str]
    business_turnover_range: Optional[str]
    gig_worker_role: Optional[str]

    residing_in: Optional[str]
    other_city: Optional[str]
    permanent_in_bihar: Optional[bool]
    migrated: Optional[bool]
    feedback: Optional[Dict[str, Any]] = None
    verification_status: Optional[bool]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    
    # Additional fields
    additional_comments: Optional[str] = None
    address_notes: Optional[str] = None
    address_proof: Optional[str] = None
    area: Optional[str] = None
    business_name: Optional[str] = None
    business_type_other: Optional[str] = None
    caste_other: Optional[str] = None
    communication_language: Optional[str] = None
    community_details: Optional[str] = None
    community_participation: Optional[str] = None
    company_name: Optional[str] = None
    crop_type: Optional[str] = None
    current_location: Optional[str] = None
    custom_relation_name: Optional[str] = None
    data_consent: Optional[bool] = None
    development_suggestions: Optional[str] = None
    digital_creator_category: Optional[str] = None
    digital_creator_channel_name: Optional[str] = None
    digital_creator_content_type: Optional[str] = None
    digital_creator_followers: Optional[str] = None
    digital_creator_income: Optional[str] = None
    digital_creator_other_category: Optional[str] = None
    digital_creator_other_platform: Optional[str] = None
    digital_creator_platform: Optional[str] = None
    family_contact_number: Optional[str] = None
    family_contact_person: Optional[str] = None
    family_head_id: Optional[str] = None
    family_relation: Optional[str] = None
    family_votes_together: Optional[bool] = None
    first_time_voter: Optional[bool] = None
    govt_schemes: Optional[str] = None
    house_type: Optional[str] = None
    influenced_by_leaders: Optional[str] = None
    is_party_worker: Optional[bool] = None
    issues_faced: Optional[str] = None
    land_holding: Optional[str] = None
    landmark: Optional[str] = None
    language_other: Optional[str] = None
    migration_reason: Optional[str] = None
    mla_satisfaction: Optional[str] = None
    most_important_issue: Optional[str] = None
    other_issues: Optional[str] = None
    party_worker_other_party: Optional[str] = None
    party_worker_party: Optional[str] = None
    pin_code: Optional[str] = None
    post_office: Optional[str] = None
    salary_range: Optional[str] = None
    street: Optional[str] = None
    unemployment_reason: Optional[str] = None
    village_ward: Optional[str] = None
    work_experience: Optional[str] = None
    years_since_migration: Optional[int] = None


class VoterCreate(VoterBase):
    """
    Schema for creating a new voter.
    Requires minimum fields.
    """
    pass


class VoterUpdate(BaseModel):
    """
    Schema for updating an existing voter.
    Fields are optional since partial updates are allowed.
    """
    constituency_name: Optional[str] = None
    state_name: Optional[str] = None
    block_name: Optional[str] = None
    panchayat_name: Optional[str] = None
    booth_number: Optional[int] = None
    booth_location: Optional[str] = None
    part_number: Optional[str] = None
    serial_no_in_list: Optional[int] = None
    voter_fname: Optional[str] = None
    voter_lname: Optional[str] = None
    voter_fname_hin: Optional[str] = None
    voter_lname_hin: Optional[str] = None
    relation: Optional[str] = None
    guardian_fname: Optional[str] = None
    guardian_lname: Optional[str] = None
    guardian_fname_hin: Optional[str] = None
    guardian_lname_hin: Optional[str] = None
    house_no: Optional[Any] = None
    gender: Optional[str] = None
    dob: Optional[Any] = None
    age: Optional[int] = None
    mobile: Optional[Any] = None
    email_id: Optional[str] = None
    last_voted_party: Optional[str] = None
    voting_preference: Optional[str] = None
    certainty_of_vote: Optional[bool] = None
    vote_type: Optional[str] = None
    availability: Optional[str] = None
    religion: Optional[str] = None
    category: Optional[str] = None
    obc_subtype: Optional[str] = None
    caste: Optional[str] = None
    language_pref: Optional[str] = None
    education_level: Optional[str] = None
    employment_status: Optional[str] = None
    govt_job_type: Optional[str] = None
    govt_job_group: Optional[str] = None
    job_role: Optional[str] = None
    monthly_salary_range: Optional[str] = None
    private_job_role: Optional[str] = None
    private_salary_range: Optional[str] = None
    self_employed_service: Optional[str] = None
    business_type: Optional[str] = None
    business_turnover_range: Optional[str] = None
    gig_worker_role: Optional[str] = None
    residing_in: Optional[str] = None
    other_city: Optional[str] = None
    permanent_in_bihar: Optional[bool] = None
    migrated: Optional[bool] = None
    feedback: Optional[Dict[str, Any]] = None
    verification_status: Optional[bool] = None
    additional_comments: Optional[str] = None
    address_notes: Optional[str] = None
    address_proof: Optional[str] = None
    area: Optional[str] = None
    business_name: Optional[str] = None
    business_type_other: Optional[str] = None
    caste_other: Optional[str] = None
    communication_language: Optional[str] = None
    community_details: Optional[str] = None
    community_participation: Optional[str] = None
    company_name: Optional[str] = None
    crop_type: Optional[str] = None
    current_location: Optional[str] = None
    custom_relation_name: Optional[str] = None
    data_consent: Optional[bool] = None
    development_suggestions: Optional[str] = None
    digital_creator_category: Optional[str] = None
    digital_creator_channel_name: Optional[str] = None
    digital_creator_content_type: Optional[str] = None
    digital_creator_followers: Optional[str] = None
    digital_creator_income: Optional[str] = None
    digital_creator_other_category: Optional[str] = None
    digital_creator_other_platform: Optional[str] = None
    digital_creator_platform: Optional[str] = None
    family_contact_number: Optional[str] = None
    family_contact_person: Optional[str] = None
    family_head_id: Optional[str] = None
    family_relation: Optional[str] = None
    family_votes_together: Optional[bool] = None
    first_time_voter: Optional[bool] = None
    govt_schemes: Optional[str] = None
    house_type: Optional[str] = None
    influenced_by_leaders: Optional[str] = None
    is_party_worker: Optional[bool] = None
    issues_faced: Optional[str] = None
    land_holding: Optional[str] = None
    landmark: Optional[str] = None
    language_other: Optional[str] = None
    migration_reason: Optional[str] = None
    mla_satisfaction: Optional[str] = None
    most_important_issue: Optional[str] = None
    other_issues: Optional[str] = None
    party_worker_other_party: Optional[str] = None
    party_worker_party: Optional[str] = None
    pin_code: Optional[str] = None
    post_office: Optional[str] = None
    salary_range: Optional[str] = None
    street: Optional[str] = None
    unemployment_reason: Optional[str] = None
    village_ward: Optional[str] = None
    work_experience: Optional[str] = None
    years_since_migration: Optional[int] = None

class VoterResponse(VoterBase):
    """
    Full voter response schema returned by the API.
    """
    model_config = {
        "from_attributes": True
    }
