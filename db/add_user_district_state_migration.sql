-- Migration script to add district_id and state_id columns to users table
-- Run this script on existing databases to add the new columns

-- Add district_id column to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS district_id INTEGER;

-- Add state_id column to users table  
ALTER TABLE users ADD COLUMN IF NOT EXISTS state_id INTEGER;

-- Add foreign key constraints
ALTER TABLE users ADD CONSTRAINT IF NOT EXISTS fk_users_district 
    FOREIGN KEY (district_id) REFERENCES district(district_id) ON DELETE SET NULL;

ALTER TABLE users ADD CONSTRAINT IF NOT EXISTS fk_users_state 
    FOREIGN KEY (state_id) REFERENCES states(state_id) ON DELETE SET NULL;

-- Add indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_district_id ON users(district_id);
CREATE INDEX IF NOT EXISTS idx_users_state_id ON users(state_id);

-- Add comments
COMMENT ON COLUMN users.district_id IS 'Reference to district table';
COMMENT ON COLUMN users.state_id IS 'Reference to states table';