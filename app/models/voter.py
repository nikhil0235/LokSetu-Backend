from typing import Optional, Dict

class Voter:
    def __init__(
        self,
        epic_id: str,
        booth_id: int,
        constituency_id: int,
        constituency_name: Optional[str] = None,
        state_name: Optional[str] = None,
        block_name: Optional[str] = None,
        panchayat_name: Optional[str] = None,
        booth_number: Optional[int] = None,
        booth_location: Optional[str] = None,
        part_number: Optional[str] = None,
        serial_no_in_list: Optional[int] = None,
        voter_fname: Optional[str] = None,
        voter_lname: Optional[str] = None,
        voter_fname_hin: Optional[str] = None,
        voter_lname_hin: Optional[str] = None,
        relation: Optional[str] = None,
        guardian_fname: Optional[str] = None,
        guardian_lname: Optional[str] = None,
        guardian_fname_hin: Optional[str] = None,
        guardian_lname_hin: Optional[str] = None,
        house_no: Optional[str] = None,
        gender: Optional[str] = None,
        dob: Optional[str] = None,
        age: Optional[int] = None,
        mobile: Optional[str] = None,
        email_id: Optional[str] = None,
        last_voted_party: Optional[str] = None,
        voting_preference: Optional[str] = None,
        certainty_of_vote: Optional[bool] = None,
        vote_type: Optional[str] = None,
        availability: Optional[str] = None,
        religion: Optional[str] = None,
        category: Optional[str] = None,
        obc_subtype: Optional[str] = None,
        caste: Optional[str] = None,
        language_pref: Optional[str] = None,
        education_level: Optional[str] = None,

        employment_status: Optional[str] = None,
        govt_job_type: Optional[str] = None,
        govt_job_group: Optional[str] = None,
        job_role: Optional[str] = None,
        monthly_salary_range: Optional[str] = None,
        private_job_role: Optional[str] = None,
        private_salary_range: Optional[str] = None,
        self_employed_service: Optional[str] = None,
        business_type: Optional[str] = None,
        business_turnover_range: Optional[str] = None,
        gig_worker_role: Optional[str] = None,

        residing_in: Optional[str] = None,
        other_city: Optional[str] = None,
        permanent_in_bihar: Optional[bool] = None,
        migrated: Optional[bool] = None,
        feedback: Optional[Dict] = None,
        verification_status: Optional[bool] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        # Additional fields
        additional_comments: Optional[str] = None,
        address_notes: Optional[str] = None,
        address_proof: Optional[str] = None,
        area: Optional[str] = None,
        business_name: Optional[str] = None,
        business_type_other: Optional[str] = None,
        caste_other: Optional[str] = None,
        communication_language: Optional[str] = None,
        community_details: Optional[str] = None,
        community_participation: Optional[str] = None,
        company_name: Optional[str] = None,
        crop_type: Optional[str] = None,
        current_location: Optional[str] = None,
        custom_relation_name: Optional[str] = None,
        data_consent: Optional[bool] = None,
        development_suggestions: Optional[str] = None,
        digital_creator_category: Optional[str] = None,
        digital_creator_channel_name: Optional[str] = None,
        digital_creator_content_type: Optional[str] = None,
        digital_creator_followers: Optional[str] = None,
        digital_creator_income: Optional[str] = None,
        digital_creator_other_category: Optional[str] = None,
        digital_creator_other_platform: Optional[str] = None,
        digital_creator_platform: Optional[str] = None,
        family_contact_number: Optional[str] = None,
        family_contact_person: Optional[str] = None,
        family_head_id: Optional[str] = None,
        family_relation: Optional[str] = None,
        family_votes_together: Optional[bool] = None,
        first_time_voter: Optional[bool] = None,
        govt_schemes: Optional[str] = None,
        house_type: Optional[str] = None,
        influenced_by_leaders: Optional[str] = None,
        is_party_worker: Optional[bool] = None,
        issues_faced: Optional[str] = None,
        land_holding: Optional[str] = None,
        landmark: Optional[str] = None,
        language_other: Optional[str] = None,
        migration_reason: Optional[str] = None,
        mla_satisfaction: Optional[str] = None,
        most_important_issue: Optional[str] = None,
        other_issues: Optional[str] = None,
        party_worker_other_party: Optional[str] = None,
        party_worker_party: Optional[str] = None,
        pin_code: Optional[str] = None,
        post_office: Optional[str] = None,
        salary_range: Optional[str] = None,
        street: Optional[str] = None,
        unemployment_reason: Optional[str] = None,
        village_ward: Optional[str] = None,
        work_experience: Optional[str] = None,
        years_since_migration: Optional[int] = None,
        scheme_ids: Optional[str] = None,  # JSON string of scheme IDs
        **kwargs
    ):
        self.epic_id = epic_id
        self.booth_id = booth_id
        self.constituency_id = constituency_id
        self.constituency_name = constituency_name
        self.state_name = state_name
        self.block_name = block_name
        self.panchayat_name = panchayat_name
        self.booth_number = booth_number
        self.booth_location = booth_location
        self.part_number = part_number
        self.serial_no_in_list = serial_no_in_list
        self.voter_fname = voter_fname
        self.voter_lname = voter_lname
        self.voter_fname_hin = voter_fname_hin
        self.voter_lname_hin = voter_lname_hin
        self.relation = relation
        self.guardian_fname = guardian_fname
        self.guardian_lname = guardian_lname
        self.guardian_fname_hin = guardian_fname_hin
        self.guardian_lname_hin = guardian_lname_hin
        self.house_no = house_no
        self.gender = gender
        self.dob = dob
        self.age = age
        self.mobile = mobile
        self.email_id = email_id
        self.last_voted_party = last_voted_party
        self.voting_preference = voting_preference
        self.certainty_of_vote = certainty_of_vote
        self.vote_type = vote_type
        self.availability = availability
        self.religion = religion
        self.category = category
        self.obc_subtype = obc_subtype
        self.caste = caste
        self.language_pref = language_pref
        self.education_level = education_level
        self.employment_status = employment_status
        self.govt_job_type = govt_job_type
        self.govt_job_group = govt_job_group
        self.job_role = job_role
        self.monthly_salary_range = monthly_salary_range
        self.private_job_role = private_job_role
        self.private_salary_range = private_salary_range
        self.self_employed_service = self_employed_service
        self.business_type = business_type
        self.business_turnover_range = business_turnover_range
        self.gig_worker_role = gig_worker_role
        self.residing_in = residing_in
        self.other_city = other_city
        self.permanent_in_bihar = permanent_in_bihar
        self.migrated = migrated
        self.feedback = feedback or {}
        self.verification_status = verification_status
        self.created_at = created_at
        self.updated_at = updated_at
        # Additional fields
        self.additional_comments = additional_comments
        self.address_notes = address_notes
        self.address_proof = address_proof
        self.area = area
        self.business_name = business_name
        self.business_type_other = business_type_other
        self.caste_other = caste_other
        self.communication_language = communication_language
        self.community_details = community_details
        self.community_participation = community_participation
        self.company_name = company_name
        self.crop_type = crop_type
        self.current_location = current_location
        self.custom_relation_name = custom_relation_name
        self.data_consent = data_consent
        self.development_suggestions = development_suggestions
        self.digital_creator_category = digital_creator_category
        self.digital_creator_channel_name = digital_creator_channel_name
        self.digital_creator_content_type = digital_creator_content_type
        self.digital_creator_followers = digital_creator_followers
        self.digital_creator_income = digital_creator_income
        self.digital_creator_other_category = digital_creator_other_category
        self.digital_creator_other_platform = digital_creator_other_platform
        self.digital_creator_platform = digital_creator_platform
        self.family_contact_number = family_contact_number
        self.family_contact_person = family_contact_person
        self.family_head_id = family_head_id
        self.family_relation = family_relation
        self.family_votes_together = family_votes_together
        self.first_time_voter = first_time_voter
        self.govt_schemes = govt_schemes
        self.house_type = house_type
        self.influenced_by_leaders = influenced_by_leaders
        self.is_party_worker = is_party_worker
        self.issues_faced = issues_faced
        self.land_holding = land_holding
        self.landmark = landmark
        self.language_other = language_other
        self.migration_reason = migration_reason
        self.mla_satisfaction = mla_satisfaction
        self.most_important_issue = most_important_issue
        self.other_issues = other_issues
        self.party_worker_other_party = party_worker_other_party
        self.party_worker_party = party_worker_party
        self.pin_code = pin_code
        self.post_office = post_office
        self.salary_range = salary_range
        self.street = street
        self.unemployment_reason = unemployment_reason
        self.village_ward = village_ward
        self.work_experience = work_experience
        self.years_since_migration = years_since_migration
        self.scheme_ids = scheme_ids

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            epic_id=data.get("VoterEPIC"),
            booth_id=data.get("BoothID"),
            constituency_id=data.get("ConstituencyID"),
            constituency_name=data.get("ConstituencyName"),
            state_name=data.get("StateName"),
            block_name=data.get("BlockName"),
            panchayat_name=data.get("PanchayatName"),
            booth_number=data.get("BoothNumber"),
            booth_location=data.get("BoothLocation"),
            part_number = data.get("PartNo"), # added
            serial_no_in_list=data.get("SerialNoInList"),
            voter_fname=data.get("Voter_fName"),
            voter_lname=data.get("Voter_lName"),
            voter_fname_hin=data.get("Voter_fName_Hin"),
            voter_lname_hin=data.get("Voter_lName_Hin"),
            relation=data.get("Relation"),
            guardian_fname=data.get("Guardian_fName"),
            guardian_lname=data.get("Guardian_lName"),
            guardian_fname_hin=data.get("Guardian_fName_Hin"),
            guardian_lname_hin=data.get("Guardian_lName_Hin"),
            house_no=data.get("HouseNo"),
            gender=data.get("Gender"),
            dob=data.get("DOB"),
            age=data.get("Age"),
            mobile=data.get("Mobile"),
            email_id=data.get("EmailId"),
            last_voted_party=data.get("LastVotedParty"),
            voting_preference=data.get("VotingPreference"),
            certainty_of_vote=data.get("CertaintyOfVote"),
            vote_type=data.get("VoteType"),
            availability=data.get("Availability"),
            religion=data.get("Religion"),
            category=data.get("Category"),
            obc_subtype=data.get("OBCSubtype"),
            caste=data.get("Caste"),
            language_pref=data.get("LanguagePref"),
            education_level=data.get("EducationLevel"),
            employment_status=data.get("EmploymentStatus"),
            govt_job_type=data.get("GovtJobType"),
            govt_job_group=data.get("GovtJobGroup"),
            job_role=data.get("JobRole"),
            monthly_salary_range=data.get("MonthlySalaryRange"),
            private_job_role=data.get("PrivateJobRole"),
            private_salary_range=data.get("PrivateSalaryRange"),
            self_employed_service=data.get("SelfEmployedService"),
            business_type=data.get("BusinessType"),
            business_turnover_range=data.get("BusinessTurnoverRange"),
            gig_worker_role=data.get("GigWorkerRole"),
            residing_in=data.get("ResidingIn"),
            other_city = data.get("OtherCity"), #added
            permanent_in_bihar=data.get("PermanentInBihar"), #added
            migrated=data.get("Migrated"), #added
            feedback=data.get("Feedback"),
            verification_status=data.get("VerificationStatus"),
            created_at=data.get("CreatedAt"),
            updated_at=data.get("UpdatedAt"),
            # Additional fields
            additional_comments=data.get("AdditionalComments"),
            address_notes=data.get("AddressNotes"),
            address_proof=data.get("AddressProof"),
            area=data.get("Area"),
            business_name=data.get("BusinessName"),
            business_type_other=data.get("BusinessTypeOther"),
            caste_other=data.get("CasteOther"),
            communication_language=data.get("CommunicationLanguage"),
            community_details=data.get("CommunityDetails"),
            community_participation=data.get("CommunityParticipation"),
            company_name=data.get("CompanyName"),
            crop_type=data.get("CropType"),
            current_location=data.get("CurrentLocation"),
            custom_relation_name=data.get("CustomRelationName"),
            data_consent=data.get("DataConsent"),
            development_suggestions=data.get("DevelopmentSuggestions"),
            digital_creator_category=data.get("DigitalCreatorCategory"),
            digital_creator_channel_name=data.get("DigitalCreatorChannelName"),
            digital_creator_content_type=data.get("DigitalCreatorContentType"),
            digital_creator_followers=data.get("DigitalCreatorFollowers"),
            digital_creator_income=data.get("DigitalCreatorIncome"),
            digital_creator_other_category=data.get("DigitalCreatorOtherCategory"),
            digital_creator_other_platform=data.get("DigitalCreatorOtherPlatform"),
            digital_creator_platform=data.get("DigitalCreatorPlatform"),
            family_contact_number=data.get("FamilyContactNumber"),
            family_contact_person=data.get("FamilyContactPerson"),
            family_head_id=data.get("FamilyHeadId"),
            family_relation=data.get("FamilyRelation"),
            family_votes_together=data.get("FamilyVotesTogether"),
            first_time_voter=data.get("FirstTimeVoter"),
            govt_schemes=data.get("GovtSchemes"),
            house_type=data.get("HouseType"),
            influenced_by_leaders=data.get("InfluencedByLeaders"),
            is_party_worker=data.get("IsPartyWorker"),
            issues_faced=data.get("IssuesFaced"),
            land_holding=data.get("LandHolding"),
            landmark=data.get("Landmark"),
            language_other=data.get("LanguageOther"),
            migration_reason=data.get("MigrationReason"),
            mla_satisfaction=data.get("MlaSatisfaction"),
            most_important_issue=data.get("MostImportantIssue"),
            other_issues=data.get("OtherIssues"),
            party_worker_other_party=data.get("PartyWorkerOtherParty"),
            party_worker_party=data.get("PartyWorkerParty"),
            pin_code=data.get("PinCode"),
            post_office=data.get("PostOffice"),
            salary_range=data.get("SalaryRange"),
            street=data.get("Street"),
            unemployment_reason=data.get("UnemploymentReason"),
            village_ward=data.get("VillageWard"),
            work_experience=data.get("WorkExperience"),
            years_since_migration=data.get("YearsSinceMigration"),
            scheme_ids=data.get("SchemeIds")
        )

    def to_dict(self):
        return {
            "VoterEPIC": self.epic_id,
            "BoothID": self.booth_id,
            "ConstituencyID": self.constituency_id,
            "ConstituencyName": self.constituency_name,
            "StateName": self.state_name,
            "BlockName": self.block_name,
            "PanchayatName": self.panchayat_name,
            "BoothNumber": self.booth_number,
            "BoothLocation": self.booth_location,
            "PartNo": self.part_number,
            "SerialNoInList": self.serial_no_in_list,
            "Voter_fName": self.voter_fname,
            "Voter_lName": self.voter_lname,
            "Voter_fName_Hin": self.voter_fname_hin,
            "Voter_lName_Hin": self.voter_lname_hin,
            "Relation": self.relation,
            "Guardian_fName": self.guardian_fname,
            "Guardian_lName": self.guardian_lname,
            "Guardian_fName_Hin": self.guardian_fname_hin,
            "Guardian_lName_Hin": self.guardian_lname_hin,
            "HouseNo": self.house_no,
            "Gender": self.gender,
            "DOB": self.dob,
            "Age": self.age,
            "Mobile": self.mobile,
            "EmailId": self.email_id,
            "LastVotedParty": self.last_voted_party,
            "VotingPreference": self.voting_preference,
            "CertaintyOfVote": self.certainty_of_vote,
            "VoteType": self.vote_type,
            "Availability": self.availability,
            "Religion": self.religion,
            "Category": self.category,
            "OBCSubtype": self.obc_subtype,
            "Caste": self.caste,
            "LanguagePref": self.language_pref,
            "EducationLevel": self.education_level,
            "EmploymentStatus": self.employment_status,
            "GovtJobType": self.govt_job_type,
            "GovtJobGroup": self.govt_job_group,
            "JobRole": self.job_role,
            "MonthlySalaryRange": self.monthly_salary_range,
            "PrivateJobRole": self.private_job_role,
            "PrivateSalaryRange": self.private_salary_range,
            "SelfEmployedService": self.self_employed_service,
            "BusinessType": self.business_type,
            "BusinessTurnoverRange": self.business_turnover_range,
            "GigWorkerRole": self.gig_worker_role,
            "ResidingIn": self.residing_in,
            "OtherCity": self.other_city,
            "PermanentInBihar": self.permanent_in_bihar,
            "Migrated": self.migrated,
            "Feedback": self.feedback if isinstance(self.feedback, dict) and self.feedback else None,
            "VerificationStatus": self.verification_status,
            "CreatedAt": self.created_at,
            "UpdatedAt": self.updated_at,
            # Additional fields
            "AdditionalComments": self.additional_comments,
            "AddressNotes": self.address_notes,
            "AddressProof": self.address_proof,
            "Area": self.area,
            "BusinessName": self.business_name,
            "BusinessTypeOther": self.business_type_other,
            "CasteOther": self.caste_other,
            "CommunicationLanguage": self.communication_language,
            "CommunityDetails": self.community_details,
            "CommunityParticipation": self.community_participation,
            "CompanyName": self.company_name,
            "CropType": self.crop_type,
            "CurrentLocation": self.current_location,
            "CustomRelationName": self.custom_relation_name,
            "DataConsent": self.data_consent,
            "DevelopmentSuggestions": self.development_suggestions,
            "DigitalCreatorCategory": self.digital_creator_category,
            "DigitalCreatorChannelName": self.digital_creator_channel_name,
            "DigitalCreatorContentType": self.digital_creator_content_type,
            "DigitalCreatorFollowers": self.digital_creator_followers,
            "DigitalCreatorIncome": self.digital_creator_income,
            "DigitalCreatorOtherCategory": self.digital_creator_other_category,
            "DigitalCreatorOtherPlatform": self.digital_creator_other_platform,
            "DigitalCreatorPlatform": self.digital_creator_platform,
            "FamilyContactNumber": self.family_contact_number,
            "FamilyContactPerson": self.family_contact_person,
            "FamilyHeadId": self.family_head_id,
            "FamilyRelation": self.family_relation,
            "FamilyVotesTogether": self.family_votes_together,
            "FirstTimeVoter": self.first_time_voter,
            "GovtSchemes": self.govt_schemes,
            "HouseType": self.house_type,
            "InfluencedByLeaders": self.influenced_by_leaders,
            "IsPartyWorker": self.is_party_worker,
            "IssuesFaced": self.issues_faced,
            "LandHolding": self.land_holding,
            "Landmark": self.landmark,
            "LanguageOther": self.language_other,
            "MigrationReason": self.migration_reason,
            "MlaSatisfaction": self.mla_satisfaction,
            "MostImportantIssue": self.most_important_issue,
            "OtherIssues": self.other_issues,
            "PartyWorkerOtherParty": self.party_worker_other_party,
            "PartyWorkerParty": self.party_worker_party,
            "PinCode": self.pin_code,
            "PostOffice": self.post_office,
            "SalaryRange": self.salary_range,
            "Street": self.street,
            "UnemploymentReason": self.unemployment_reason,
            "VillageWard": self.village_ward,
            "WorkExperience": self.work_experience,
            "YearsSinceMigration": self.years_since_migration,
            "SchemeIds": self.scheme_ids
        }
