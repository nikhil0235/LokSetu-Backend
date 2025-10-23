-- Migration script to add voted_party column to voters table
-- Run this script on existing databases to add the new field

-- Add the voted_party column
ALTER TABLE voters ADD COLUMN IF NOT EXISTS voted_party VARCHAR(100);

-- Add index for the new column for better query performance
CREATE INDEX IF NOT EXISTS idx_voters_voted_party ON voters(voted_party);

-- Add voted_party_counts column to booth_summaries table
ALTER TABLE booth_summaries ADD COLUMN IF NOT EXISTS voted_party_counts JSONB;

-- Update the comment to reflect the change
COMMENT ON COLUMN voters.voted_party IS 'Party the voter actually voted for in the election';
COMMENT ON COLUMN booth_summaries.voted_party_counts IS 'Count of voters by actual voted party in JSON format';