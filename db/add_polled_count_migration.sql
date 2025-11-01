-- Migration script to add polled_count column to booth_summaries table
-- Run this script on existing databases to add the new field

-- Add the polled_count column
ALTER TABLE booth_summaries ADD COLUMN IF NOT EXISTS polled_count INTEGER DEFAULT 0;

-- Add comment
COMMENT ON COLUMN booth_summaries.polled_count IS 'Number of voters who have actually voted/polled at this booth';