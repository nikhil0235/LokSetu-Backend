-- Migration script to add user blocks and panchayats assignment tables
-- Run this script on existing databases to add the new tables

-- Create user_blocks junction table
CREATE TABLE IF NOT EXISTS user_blocks (
    user_id INTEGER NOT NULL,
    block_id INTEGER NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, block_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (block_id) REFERENCES blocks(block_id) ON DELETE CASCADE
);

-- Create user_panchayats junction table
CREATE TABLE IF NOT EXISTS user_panchayats (
    user_id INTEGER NOT NULL,
    panchayat_id INTEGER NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, panchayat_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (panchayat_id) REFERENCES panchayats(panchayat_id) ON DELETE CASCADE
);

-- Add indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_blocks_user_id ON user_blocks(user_id);
CREATE INDEX IF NOT EXISTS idx_user_blocks_block_id ON user_blocks(block_id);
CREATE INDEX IF NOT EXISTS idx_user_panchayats_user_id ON user_panchayats(user_id);
CREATE INDEX IF NOT EXISTS idx_user_panchayats_panchayat_id ON user_panchayats(panchayat_id);

-- Add comments
COMMENT ON TABLE user_blocks IS 'Junction table for user block assignments';
COMMENT ON TABLE user_panchayats IS 'Junction table for user panchayat assignments';