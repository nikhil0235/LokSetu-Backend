-- PostgreSQL Schema for Voter List Management System
-- Optimized for AWS Aurora PostgreSQL

-- Enable UUID extension for better primary keys
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================
-- CORE ADMINISTRATIVE TABLES
-- =============================================

-- States table
CREATE TABLE states (
    state_id SERIAL PRIMARY KEY,
    state_name VARCHAR(100) NOT NULL UNIQUE,
    state_code VARCHAR(10) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE district (
    district_id SERIAL PRIMARY KEY,
    district_name VARCHAR(100) NOT NULL UNIQUE,
    state_id INTEGER REFERENCES states(state_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Constituencies table
CREATE TABLE constituencies (
    constituency_id INTEGER PRIMARY KEY,
    constituency_name VARCHAR(200) NOT NULL,
    state_id INTEGER REFERENCES states(state_id),
    district_id INTEGER REFERENCES district(district_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Blocks table
CREATE TABLE blocks (
    block_id SERIAL PRIMARY KEY,
    block_name VARCHAR(200) NOT NULL,
    constituency_id INTEGER REFERENCES constituencies(constituency_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Panchayats table
CREATE TABLE panchayats (
    panchayat_id SERIAL PRIMARY KEY,
    panchayat_name VARCHAR(200) NOT NULL,
    block_id INTEGER REFERENCES blocks(block_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Booths table
CREATE TABLE booths (
    booth_id INTEGER PRIMARY KEY,
    booth_number INTEGER,
    booth_location VARCHAR(500),
    constituency_id INTEGER REFERENCES constituencies(constituency_id),
    panchayat_id INTEGER REFERENCES panchayats(panchayat_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- USER MANAGEMENT TABLES
-- =============================================

-- Users table with role-based access
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('super_admin', 'admin', 'booth_boy', 'candidate')),
    full_name VARCHAR(200),
    phone VARCHAR(20),
    email VARCHAR(255),
    created_by INTEGER REFERENCES users(user_id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User constituency assignmentss
CREATE TABLE user_constituencies (
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    constituency_id INTEGER REFERENCES constituencies(constituency_id),
    PRIMARY KEY (user_id, constituency_id)
);

-- User booth assignments
CREATE TABLE user_booths (
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    booth_id INTEGER REFERENCES booths(booth_id),
    PRIMARY KEY (user_id, booth_id)
);

-- =============================================
-- SCHEMES MANAGEMENT
-- =============================================

-- Government schemes table
CREATE TABLE schemes (
    scheme_id SERIAL PRIMARY KEY,
    name VARCHAR(300) NOT NULL,
    description TEXT,
    category VARCHAR(100) DEFAULT 'Other' CHECK (category IN ('Educational', 'Socio', 'Economic', 'Other')),
    created_by INTEGER REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- MAIN VOTERS TABLE
-- =============================================

-- Voters table - core entity
CREATE TABLE voters (
    -- Primary identifiers
    epic_id VARCHAR(20) PRIMARY KEY,
    serial_no_in_list INTEGER,
    part_number VARCHAR(20),
    
    -- Location references
    constituency_id INTEGER REFERENCES constituencies(constituency_id),
    booth_id INTEGER REFERENCES booths(booth_id),
    
    -- Personal information
    voter_fname VARCHAR(200),
    voter_lname VARCHAR(200),
    voter_fname_hin VARCHAR(200),
    voter_lname_hin VARCHAR(200),
    
    -- Guardian information
    relation VARCHAR(50),
    guardian_fname VARCHAR(200),
    guardian_lname VARCHAR(200),
    guardian_fname_hin VARCHAR(200),
    guardian_lname_hin VARCHAR(200),
    
    -- Address
    house_no VARCHAR(100),
    street VARCHAR(200),
    area VARCHAR(200),
    landmark VARCHAR(200),
    village_ward VARCHAR(200),
    pin_code VARCHAR(10),
    post_office VARCHAR(200),
    
    -- Demographics
    gender VARCHAR(20) CHECK (gender IN ('Male', 'Female', 'Other')),
    dob DATE,
    age INTEGER,
    
    -- Contact
    mobile VARCHAR(20),
    email_id VARCHAR(255),
    family_contact_number VARCHAR(20),
    family_contact_person VARCHAR(200),
    
    -- Political preferences
    last_voted_party VARCHAR(100),
    voting_preference VARCHAR(100),
    certainty_of_vote BOOLEAN,
    vote_type VARCHAR(50),
    availability VARCHAR(100),
    first_time_voter BOOLEAN DEFAULT false,
    
    -- Social demographics
    religion VARCHAR(100),
    category VARCHAR(50) CHECK (category IN ('General', 'OBC', 'SC', 'ST', 'Other')),
    obc_subtype VARCHAR(100),
    caste VARCHAR(100),
    caste_other VARCHAR(100),
    
    -- Language preferences
    language_pref VARCHAR(100),
    language_other VARCHAR(100),
    communication_language VARCHAR(100),
    
    -- Education
    education_level VARCHAR(100),
    
    -- Employment details
    employment_status VARCHAR(100),
    govt_job_type VARCHAR(100),
    govt_job_group VARCHAR(100),
    job_role VARCHAR(200),
    monthly_salary_range VARCHAR(100),
    private_job_role VARCHAR(200),
    private_salary_range VARCHAR(100),
    self_employed_service VARCHAR(200),
    business_type VARCHAR(200),
    business_type_other VARCHAR(200),
    business_name VARCHAR(300),
    business_turnover_range VARCHAR(100),
    gig_worker_role VARCHAR(200),
    company_name VARCHAR(300),
    salary_range VARCHAR(100),
    work_experience VARCHAR(200),
    unemployment_reason VARCHAR(300),
    
    -- Agriculture
    land_holding VARCHAR(100),
    crop_type VARCHAR(200),
    
    -- Digital creator fields
    digital_creator_category VARCHAR(100),
    digital_creator_platform VARCHAR(100),
    digital_creator_other_platform VARCHAR(100),
    digital_creator_channel_name VARCHAR(300),
    digital_creator_content_type VARCHAR(200),
    digital_creator_followers VARCHAR(100),
    digital_creator_income VARCHAR(100),
    digital_creator_other_category VARCHAR(200),
    
    -- Location and migration
    residing_in VARCHAR(200),
    current_location VARCHAR(200),
    other_city VARCHAR(200),
    permanent_in_bihar BOOLEAN,
    migrated BOOLEAN DEFAULT false,
    migration_reason VARCHAR(300),
    years_since_migration INTEGER,
    
    -- Family information
    family_head_id VARCHAR(20) REFERENCES voters(epic_id),
    family_relation VARCHAR(100),
    family_votes_together BOOLEAN,
    custom_relation_name VARCHAR(100),
    
    -- Housing
    house_type VARCHAR(100),
    
    -- Political engagement
    is_party_worker BOOLEAN DEFAULT false,
    party_worker_party VARCHAR(100),
    party_worker_other_party VARCHAR(100),
    influenced_by_leaders VARCHAR(300),
    mla_satisfaction VARCHAR(100),
    
    -- Issues and feedback
    most_important_issue VARCHAR(300),
    issues_faced TEXT,
    other_issues TEXT,
    development_suggestions TEXT,
    community_participation VARCHAR(200),
    community_details VARCHAR(300),
    
    -- Government schemes
    govt_schemes TEXT, -- JSON array of scheme names
    
    -- Additional fields
    additional_comments TEXT,
    address_notes TEXT,
    address_proof VARCHAR(200),
    data_consent BOOLEAN DEFAULT false,
    
    -- Verification and audit
    verification_status BOOLEAN DEFAULT false,
    feedback JSONB,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- VOTER-SCHEME RELATIONSHIP
-- =============================================

-- Many-to-many relationship between voters and schemes
CREATE TABLE voter_schemes (
    voter_epic_id VARCHAR(20) REFERENCES voters(epic_id) ON DELETE CASCADE,
    scheme_id INTEGER REFERENCES schemes(scheme_id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by INTEGER REFERENCES users(user_id),
    PRIMARY KEY (voter_epic_id, scheme_id)
);

-- =============================================
-- AUDIT AND TRACKING TABLES
-- =============================================

-- OTP codes table for mobile authentication
CREATE TABLE otp_codes (
    mobile VARCHAR(20) PRIMARY KEY,
    otp VARCHAR(6) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Voter updates audit trail
CREATE TABLE voter_updates (
    update_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    voter_epic_id VARCHAR(20) REFERENCES voters(epic_id),
    user_id INTEGER REFERENCES users(user_id),
    old_values JSONB,
    new_values JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Booth summary statistics
CREATE TABLE booth_summaries (
    booth_id INTEGER PRIMARY KEY REFERENCES booths(booth_id),
    constituency_id INTEGER REFERENCES constituencies(constituency_id),
    total_voters INTEGER DEFAULT 0,
    male_voters INTEGER DEFAULT 0,
    female_voters INTEGER DEFAULT 0,
    other_gender_voters INTEGER DEFAULT 0,
    voting_preference_counts JSONB,
    religion_counts JSONB,
    category_counts JSONB,
    education_counts JSONB,
    employment_counts JSONB,
    age_group_counts JSONB,
    scheme_beneficiaries_counts JSONB,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- INDEXES FOR PERFORMANCE
-- =============================================

-- Primary lookup indexes
CREATE INDEX idx_voters_booth_id ON voters(booth_id);
CREATE INDEX idx_voters_constituency_id ON voters(constituency_id);
CREATE INDEX idx_voters_mobile ON voters(mobile);
CREATE INDEX idx_voters_name ON voters(voter_fname, voter_lname);
CREATE INDEX idx_voters_age ON voters(age);
CREATE INDEX idx_voters_gender ON voters(gender);

-- Political preference indexes
CREATE INDEX idx_voters_voting_preference ON voters(voting_preference);
CREATE INDEX idx_voters_last_voted_party ON voters(last_voted_party);
CREATE INDEX idx_voters_certainty_of_vote ON voters(certainty_of_vote);

-- Demographic indexes
CREATE INDEX idx_voters_religion ON voters(religion);
CREATE INDEX idx_voters_category ON voters(category);
CREATE INDEX idx_voters_education ON voters(education_level);
CREATE INDEX idx_voters_employment ON voters(employment_status);

-- Location indexes
CREATE INDEX idx_voters_residing_in ON voters(residing_in);
CREATE INDEX idx_voters_migrated ON voters(migrated);

-- Audit indexes
CREATE INDEX idx_voter_updates_epic_id ON voter_updates(voter_epic_id);
CREATE INDEX idx_voter_updates_user_id ON voter_updates(user_id);
CREATE INDEX idx_voter_updates_created_at ON voter_updates(created_at);

-- User access indexes
CREATE INDEX idx_user_booths_user_id ON user_booths(user_id);
CREATE INDEX idx_user_constituencies_user_id ON user_constituencies(user_id);

-- Composite indexes for common queries
CREATE INDEX idx_voters_booth_preference ON voters(booth_id, voting_preference);
CREATE INDEX idx_voters_constituency_gender ON voters(constituency_id, gender);
CREATE INDEX idx_voters_booth_age_gender ON voters(booth_id, age, gender);

-- =============================================
-- TRIGGERS FOR AUTO-UPDATES
-- =============================================

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply timestamp triggers
CREATE TRIGGER update_voters_updated_at BEFORE UPDATE ON voters
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_constituencies_updated_at BEFORE UPDATE ON constituencies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_booths_updated_at BEFORE UPDATE ON booths
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_schemes_updated_at BEFORE UPDATE ON schemes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================
-- VIEWS FOR COMMON QUERIES
-- =============================================

-- Complete voter information view
CREATE VIEW voter_details AS
SELECT 
    v.*,
    c.constituency_name,
    s.state_name,
    b.block_name,
    p.panchayat_name,
    bt.booth_number,
    bt.booth_location
FROM voters v
LEFT JOIN constituencies c ON v.constituency_id = c.constituency_id
LEFT JOIN states s ON c.state_id = s.state_id
LEFT JOIN booths bt ON v.booth_id = bt.booth_id
LEFT JOIN panchayats p ON bt.panchayat_id = p.panchayat_id
LEFT JOIN blocks b ON p.block_id = b.block_id;

-- User access view with permissions
CREATE VIEW user_access AS
SELECT 
    u.*,
    COALESCE(
        json_agg(DISTINCT uc.constituency_id) FILTER (WHERE uc.constituency_id IS NOT NULL),
        '[]'::json
    ) as assigned_constituencies,
    COALESCE(
        json_agg(DISTINCT ub.booth_id) FILTER (WHERE ub.booth_id IS NOT NULL),
        '[]'::json
    ) as assigned_booths
FROM users u
LEFT JOIN user_constituencies uc ON u.user_id = uc.user_id
LEFT JOIN user_booths ub ON u.user_id = ub.user_id
WHERE u.is_active = true
GROUP BY u.user_id;

-- =============================================
-- SAMPLE DATA INSERTION
-- =============================================

-- Insert default state
INSERT INTO states (state_name, state_code) VALUES ('Bihar', 'BR') ON CONFLICT DO NOTHING;

-- Insert default admin user (password: admin123)
INSERT INTO users (username, password_hash, role, full_name, is_active) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhM8/LeHxSKL.cpD.nTm6S', 'super_admin', 'System Administrator', true)
ON CONFLICT (username) DO NOTHING;