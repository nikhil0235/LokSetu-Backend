from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class VoterBase(BaseModel):
    ConstituencyID: int
    ConstituencyName: Optional[str]
    StateName: Optional[str]
    BlockName: Optional[str]
    PanchayatName: Optional[str]
    BoothID: int
    BoothNumber: Optional[int]
    BoothLocation: Optional[str]
    PartNo: Optional[str]

    VoterEPIC: str = Field(..., description="Unique voter EPIC ID")
    SerialNoInList: Optional[int]

    Voter_fName: Optional[str]
    Voter_lName: Optional[str]
    Voter_fName_Hin: Optional[str]
    Voter_lName_Hin: Optional[str]

    Relation: Optional[str]
    Guardian_fName: Optional[str]
    Guardian_lName: Optional[str]
    Guardian_fName_Hin: Optional[str]
    Guardian_lName_Hin: Optional[str]

    HouseNo: Optional[Any]
    Gender: Optional[str]
    DOB: Optional[Any]
    Age: Optional[int]

    Mobile: Optional[Any]
    EmailId: Optional[str]

    LastVotedParty: Optional[str]
    VotingPreference: Optional[str]
    CertaintyOfVote: Optional[bool]
    VoteType: Optional[str]
    Availability: Optional[str]

    Religion: Optional[str]
    Category: Optional[str]
    OBCSubtype: Optional[str]
    Caste: Optional[str]
    LanguagePref: Optional[str]

    EducationLevel: Optional[str]
    EmploymentStatus: Optional[str]
    GovtJobType: Optional[str]
    GovtJobGroup: Optional[str]
    JobRole: Optional[str]

    MonthlySalaryRange: Optional[str]
    PrivateJobRole: Optional[str]
    PrivateSalaryRange: Optional[str]

    SelfEmployedService: Optional[str]
    BusinessType: Optional[str]
    BusinessTurnoverRange: Optional[str]
    GigWorkerRole: Optional[str]

    ResidingIn: Optional[str]
    OtherCity: Optional[str]
    PermanentInBihar: Optional[bool]
    Migrated: Optional[bool]
    Feedback: Optional[Dict[str, Any]] = None
    VerificationStatus: Optional[bool]
    CreatedAt: Optional[str]
    UpdatedAt: Optional[str]
    
    # Additional fields
    AdditionalComments: Optional[str] = None
    AddressNotes: Optional[str] = None
    AddressProof: Optional[str] = None
    Area: Optional[str] = None
    BusinessName: Optional[str] = None
    BusinessTypeOther: Optional[str] = None
    CasteOther: Optional[str] = None
    CommunicationLanguage: Optional[str] = None
    CommunityDetails: Optional[str] = None
    CommunityParticipation: Optional[str] = None
    CompanyName: Optional[str] = None
    CropType: Optional[str] = None
    CurrentLocation: Optional[str] = None
    CustomRelationName: Optional[str] = None
    DataConsent: Optional[bool] = None
    DevelopmentSuggestions: Optional[str] = None
    DigitalCreatorCategory: Optional[str] = None
    DigitalCreatorChannelName: Optional[str] = None
    DigitalCreatorContentType: Optional[str] = None
    DigitalCreatorFollowers: Optional[str] = None
    DigitalCreatorIncome: Optional[str] = None
    DigitalCreatorOtherCategory: Optional[str] = None
    DigitalCreatorOtherPlatform: Optional[str] = None
    DigitalCreatorPlatform: Optional[str] = None
    FamilyContactNumber: Optional[str] = None
    FamilyContactPerson: Optional[str] = None
    FamilyHeadId: Optional[str] = None
    FamilyRelation: Optional[str] = None
    FamilyVotesTogether: Optional[bool] = None
    FirstTimeVoter: Optional[bool] = None
    GovtSchemes: Optional[str] = None
    HouseType: Optional[str] = None
    InfluencedByLeaders: Optional[str] = None
    IsPartyWorker: Optional[bool] = None
    IssuesFaced: Optional[str] = None
    LandHolding: Optional[str] = None
    Landmark: Optional[str] = None
    LanguageOther: Optional[str] = None
    MigrationReason: Optional[str] = None
    MlaSatisfaction: Optional[str] = None
    MostImportantIssue: Optional[str] = None
    OtherIssues: Optional[str] = None
    PartyWorkerOtherParty: Optional[str] = None
    PartyWorkerParty: Optional[str] = None
    PinCode: Optional[str] = None
    PostOffice: Optional[str] = None
    SalaryRange: Optional[str] = None
    Street: Optional[str] = None
    UnemploymentReason: Optional[str] = None
    VillageWard: Optional[str] = None
    WorkExperience: Optional[str] = None
    YearsSinceMigration: Optional[int] = None


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
    ConstituencyName: Optional[str] = None
    StateName: Optional[str] = None
    BlockName: Optional[str] = None
    PanchayatName: Optional[str] = None
    BoothNumber: Optional[int] = None
    BoothLocation: Optional[str] = None
    PartNo: Optional[str] = None
    SerialNoInList: Optional[int] = None
    Voter_fName: Optional[str] = None
    Voter_lName: Optional[str] = None
    Voter_fName_Hin: Optional[str] = None
    Voter_lName_Hin: Optional[str] = None
    Relation: Optional[str] = None
    Guardian_fName: Optional[str] = None
    Guardian_lName: Optional[str] = None
    Guardian_fName_Hin: Optional[str] = None
    Guardian_lName_Hin: Optional[str] = None
    HouseNo: Optional[Any] = None
    Gender: Optional[str] = None
    DOB: Optional[Any] = None
    Age: Optional[int] = None
    Mobile: Optional[Any] = None
    EmailId: Optional[str] = None
    LastVotedParty: Optional[str] = None
    VotingPreference: Optional[str] = None
    CertaintyOfVote: Optional[bool] = None
    VoteType: Optional[str] = None
    Availability: Optional[str] = None
    Religion: Optional[str] = None
    Category: Optional[str] = None
    OBCSubtype: Optional[str] = None
    Caste: Optional[str] = None
    LanguagePref: Optional[str] = None
    EducationLevel: Optional[str] = None
    EmploymentStatus: Optional[str] = None
    GovtJobType: Optional[str] = None
    GovtJobGroup: Optional[str] = None
    JobRole: Optional[str] = None
    MonthlySalaryRange: Optional[str] = None
    PrivateJobRole: Optional[str] = None
    PrivateSalaryRange: Optional[str] = None
    SelfEmployedService: Optional[str] = None
    BusinessType: Optional[str] = None
    BusinessTurnoverRange: Optional[str] = None
    GigWorkerRole: Optional[str] = None
    ResidingIn: Optional[str] = None
    OtherCity: Optional[str] = None
    PermanentInBihar: Optional[bool] = None
    Migrated: Optional[bool] = None
    Feedback: Optional[Dict[str, Any]] = None
    VerificationStatus: Optional[bool] = None
    AdditionalComments: Optional[str] = None
    AddressNotes: Optional[str] = None
    AddressProof: Optional[str] = None
    Area: Optional[str] = None
    BusinessName: Optional[str] = None
    BusinessTypeOther: Optional[str] = None
    CasteOther: Optional[str] = None
    CommunicationLanguage: Optional[str] = None
    CommunityDetails: Optional[str] = None
    CommunityParticipation: Optional[str] = None
    CompanyName: Optional[str] = None
    CropType: Optional[str] = None
    CurrentLocation: Optional[str] = None
    CustomRelationName: Optional[str] = None
    DataConsent: Optional[bool] = None
    DevelopmentSuggestions: Optional[str] = None
    DigitalCreatorCategory: Optional[str] = None
    DigitalCreatorChannelName: Optional[str] = None
    DigitalCreatorContentType: Optional[str] = None
    DigitalCreatorFollowers: Optional[str] = None
    DigitalCreatorIncome: Optional[str] = None
    DigitalCreatorOtherCategory: Optional[str] = None
    DigitalCreatorOtherPlatform: Optional[str] = None
    DigitalCreatorPlatform: Optional[str] = None
    FamilyContactNumber: Optional[str] = None
    FamilyContactPerson: Optional[str] = None
    FamilyHeadId: Optional[str] = None
    FamilyRelation: Optional[str] = None
    FamilyVotesTogether: Optional[bool] = None
    FirstTimeVoter: Optional[bool] = None
    GovtSchemes: Optional[str] = None
    HouseType: Optional[str] = None
    InfluencedByLeaders: Optional[str] = None
    IsPartyWorker: Optional[bool] = None
    IssuesFaced: Optional[str] = None
    LandHolding: Optional[str] = None
    Landmark: Optional[str] = None
    LanguageOther: Optional[str] = None
    MigrationReason: Optional[str] = None
    MlaSatisfaction: Optional[str] = None
    MostImportantIssue: Optional[str] = None
    OtherIssues: Optional[str] = None
    PartyWorkerOtherParty: Optional[str] = None
    PartyWorkerParty: Optional[str] = None
    PinCode: Optional[str] = None
    PostOffice: Optional[str] = None
    SalaryRange: Optional[str] = None
    Street: Optional[str] = None
    UnemploymentReason: Optional[str] = None
    VillageWard: Optional[str] = None
    WorkExperience: Optional[str] = None
    YearsSinceMigration: Optional[int] = None


class VoterResponse(VoterBase):
    """
    Full voter response schema returned by the API.
    """
    model_config = {
        "from_attributes": True
    }
