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
            epic_id=data.get("epic_id"),
            booth_id=data.get("booth_id"),
            constituency_id=data.get("constituency_id"),
            constituency_name=data.get("constituency_name"),
            state_name=data.get("state_name"),
            block_name=data.get("block_name"),
            panchayat_name=data.get("panchayat_name"),
            booth_number=data.get("booth_number"),
            booth_location=data.get("booth_location"),
            part_number=data.get("part_number"),
            serial_no_in_list=data.get("serial_no_in_list"),
            voter_fname=data.get("voter_fname"),
            voter_lname=data.get("voter_lname"),
            voter_fname_hin=data.get("voter_fname_hin"),
            voter_lname_hin=data.get("voter_lname_hin"),
            relation=data.get("relation"),
            guardian_fname=data.get("guardian_fname"),
            guardian_lname=data.get("guardian_lname"),
            guardian_fname_hin=data.get("guardian_fname_hin"),
            guardian_lname_hin=data.get("guardian_lname_hin"),
            house_no=data.get("house_no"),
            gender=data.get("gender"),
            dob=data.get("dob"),
            age=data.get("age"),
            mobile=data.get("mobile"),
            email_id=data.get("email_id"),
            last_voted_party=data.get("last_voted_party"),
            voting_preference=data.get("voting_preference"),
            certainty_of_vote=data.get("certainty_of_vote"),
            vote_type=data.get("vote_type"),
            availability=data.get("availability"),
            religion=data.get("religion"),
            category=data.get("category"),
            obc_subtype=data.get("obc_subtype"),
            caste=data.get("caste"),
            language_pref=data.get("language_pref"),
            education_level=data.get("education_level"),
            employment_status=data.get("employment_status"),
            govt_job_type=data.get("govt_job_type"),
            govt_job_group=data.get("govt_job_group"),
            job_role=data.get("job_role"),
            monthly_salary_range=data.get("monthly_salary_range"),
            private_job_role=data.get("private_job_role"),
            private_salary_range=data.get("private_salary_range"),
            self_employed_service=data.get("self_employed_service"),
            business_type=data.get("business_type"),
            business_turnover_range=data.get("business_turnover_range"),
            gig_worker_role=data.get("gig_worker_role"),
            residing_in=data.get("residing_in"),
            other_city=data.get("other_city"),
            permanent_in_bihar=data.get("permanent_in_bihar"),
            migrated=data.get("migrated"),
            feedback=data.get("feedback"),
            verification_status=data.get("verification_status"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            additional_comments=data.get("additional_comments"),
            address_notes=data.get("address_notes"),
            address_proof=data.get("address_proof"),
            area=data.get("area"),
            business_name=data.get("business_name"),
            business_type_other=data.get("business_type_other"),
            caste_other=data.get("caste_other"),
            communication_language=data.get("communication_language"),
            community_details=data.get("community_details"),
            community_participation=data.get("community_participation"),
            company_name=data.get("company_name"),
            crop_type=data.get("crop_type"),
            current_location=data.get("current_location"),
            custom_relation_name=data.get("custom_relation_name"),
            data_consent=data.get("data_consent"),
            development_suggestions=data.get("development_suggestions"),
            digital_creator_category=data.get("digital_creator_category"),
            digital_creator_channel_name=data.get("digital_creator_channel_name"),
            digital_creator_content_type=data.get("digital_creator_content_type"),
            digital_creator_followers=data.get("digital_creator_followers"),
            digital_creator_income=data.get("digital_creator_income"),
            digital_creator_other_category=data.get("digital_creator_other_category"),
            digital_creator_other_platform=data.get("digital_creator_other_platform"),
            digital_creator_platform=data.get("digital_creator_platform"),
            family_contact_number=data.get("family_contact_number"),
            family_contact_person=data.get("family_contact_person"),
            family_head_id=data.get("family_head_id"),
            family_relation=data.get("family_relation"),
            family_votes_together=data.get("family_votes_together"),
            first_time_voter=data.get("first_time_voter"),
            govt_schemes=data.get("govt_schemes"),
            house_type=data.get("house_type"),
            influenced_by_leaders=data.get("influenced_by_leaders"),
            is_party_worker=data.get("is_party_worker"),
            issues_faced=data.get("issues_faced"),
            land_holding=data.get("land_holding"),
            landmark=data.get("landmark"),
            language_other=data.get("language_other"),
            migration_reason=data.get("migration_reason"),
            mla_satisfaction=data.get("mla_satisfaction"),
            most_important_issue=data.get("most_important_issue"),
            other_issues=data.get("other_issues"),
            party_worker_other_party=data.get("party_worker_other_party"),
            party_worker_party=data.get("party_worker_party"),
            pin_code=data.get("pin_code"),
            post_office=data.get("post_office"),
            salary_range=data.get("salary_range"),
            street=data.get("street"),
            unemployment_reason=data.get("unemployment_reason"),
            village_ward=data.get("village_ward"),
            work_experience=data.get("work_experience"),
            years_since_migration=data.get("years_since_migration"),
            scheme_ids=data.get("scheme_ids")
        )

    def to_dict(self):
        return {
            "epic_id": self.epic_id,
            "booth_id": self.booth_id,
            "constituency_id": self.constituency_id,
            "constituency_name": self.constituency_name,
            "state_name": self.state_name,
            "block_name": self.block_name,
            "panchayat_name": self.panchayat_name,
            "booth_number": self.booth_number,
            "booth_location": self.booth_location,
            "part_number": self.part_number,
            "serial_no_in_list": self.serial_no_in_list,
            "voter_fname": self.voter_fname,
            "voter_lname": self.voter_lname,
            "voter_fname_hin": self.voter_fname_hin,
            "voter_lname_hin": self.voter_lname_hin,
            "relation": self.relation,
            "guardian_fname": self.guardian_fname,
            "guardian_lname": self.guardian_lname,
            "guardian_fname_hin": self.guardian_fname_hin,
            "guardian_lname_hin": self.guardian_lname_hin,
            "house_no": self.house_no,
            "gender": self.gender,
            "dob": self.dob,
            "age": self.age,
            "mobile": self.mobile,
            "email_id": self.email_id,
            "last_voted_party": self.last_voted_party,
            "voting_preference": self.voting_preference,
            "certainty_of_vote": self.certainty_of_vote,
            "vote_type": self.vote_type,
            "availability": self.availability,
            "religion": self.religion,
            "category": self.category,
            "obc_subtype": self.obc_subtype,
            "caste": self.caste,
            "language_pref": self.language_pref,
            "education_level": self.education_level,
            "employment_status": self.employment_status,
            "govt_job_type": self.govt_job_type,
            "govt_job_group": self.govt_job_group,
            "job_role": self.job_role,
            "monthly_salary_range": self.monthly_salary_range,
            "private_job_role": self.private_job_role,
            "private_salary_range": self.private_salary_range,
            "self_employed_service": self.self_employed_service,
            "business_type": self.business_type,
            "business_turnover_range": self.business_turnover_range,
            "gig_worker_role": self.gig_worker_role,
            "residing_in": self.residing_in,
            "other_city": self.other_city,
            "permanent_in_bihar": self.permanent_in_bihar,
            "migrated": self.migrated,
            "feedback": self.feedback if isinstance(self.feedback, dict) and self.feedback else None,
            "verification_status": self.verification_status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "additional_comments": self.additional_comments,
            "address_notes": self.address_notes,
            "address_proof": self.address_proof,
            "area": self.area,
            "business_name": self.business_name,
            "business_type_other": self.business_type_other,
            "caste_other": self.caste_other,
            "communication_language": self.communication_language,
            "community_details": self.community_details,
            "community_participation": self.community_participation,
            "company_name": self.company_name,
            "crop_type": self.crop_type,
            "current_location": self.current_location,
            "custom_relation_name": self.custom_relation_name,
            "data_consent": self.data_consent,
            "development_suggestions": self.development_suggestions,
            "digital_creator_category": self.digital_creator_category,
            "digital_creator_channel_name": self.digital_creator_channel_name,
            "digital_creator_content_type": self.digital_creator_content_type,
            "digital_creator_followers": self.digital_creator_followers,
            "digital_creator_income": self.digital_creator_income,
            "digital_creator_other_category": self.digital_creator_other_category,
            "digital_creator_other_platform": self.digital_creator_other_platform,
            "digital_creator_platform": self.digital_creator_platform,
            "family_contact_number": self.family_contact_number,
            "family_contact_person": self.family_contact_person,
            "family_head_id": self.family_head_id,
            "family_relation": self.family_relation,
            "family_votes_together": self.family_votes_together,
            "first_time_voter": self.first_time_voter,
            "govt_schemes": self.govt_schemes,
            "house_type": self.house_type,
            "influenced_by_leaders": self.influenced_by_leaders,
            "is_party_worker": self.is_party_worker,
            "issues_faced": self.issues_faced,
            "land_holding": self.land_holding,
            "landmark": self.landmark,
            "language_other": self.language_other,
            "migration_reason": self.migration_reason,
            "mla_satisfaction": self.mla_satisfaction,
            "most_important_issue": self.most_important_issue,
            "other_issues": self.other_issues,
            "party_worker_other_party": self.party_worker_other_party,
            "party_worker_party": self.party_worker_party,
            "pin_code": self.pin_code,
            "post_office": self.post_office,
            "salary_range": self.salary_range,
            "street": self.street,
            "unemployment_reason": self.unemployment_reason,
            "village_ward": self.village_ward,
            "work_experience": self.work_experience,
            "years_since_migration": self.years_since_migration,
            "scheme_ids": self.scheme_ids
        }
