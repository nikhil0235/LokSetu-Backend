-- Migration script to add party-wise count columns to booth_summaries table
-- Run this script on existing databases to add the new columns

-- Add party_wise_gender_counts column
ALTER TABLE booth_summaries ADD COLUMN IF NOT EXISTS party_wise_gender_counts JSONB;

-- Add party_wise_age_group_counts column
ALTER TABLE booth_summaries ADD COLUMN IF NOT EXISTS party_wise_age_group_counts JSONB;

-- Add party_wise_category_counts column
ALTER TABLE booth_summaries ADD COLUMN IF NOT EXISTS party_wise_category_counts JSONB;

-- Add comments
COMMENT ON COLUMN booth_summaries.party_wise_gender_counts IS 'Gender distribution by party in JSON format';
COMMENT ON COLUMN booth_summaries.party_wise_age_group_counts IS 'Age group distribution by party in JSON format';
COMMENT ON COLUMN booth_summaries.party_wise_category_counts IS 'Category distribution by party in JSON format';