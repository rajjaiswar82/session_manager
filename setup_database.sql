-- Database Setup Script for Session Manager Service
-- Run this script to manually create the database and table

-- Create database (run as postgres user)
-- Note: You may need to run this separately before running the rest
-- CREATE DATABASE session_manager;

-- Connect to the database
\c session_manager;

-- Create sessions table
CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    candidate_id INTEGER NOT NULL,
    interviewer_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('active', 'paused', 'completed', 'terminated')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    ended_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_sessions_session_id ON sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_sessions_candidate_id ON sessions(candidate_id);
CREATE INDEX IF NOT EXISTS idx_sessions_interviewer_id ON sessions(interviewer_id);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions(created_at);

-- Create a function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update updated_at on row update
DROP TRIGGER IF EXISTS update_sessions_updated_at ON sessions;
CREATE TRIGGER update_sessions_updated_at
    BEFORE UPDATE ON sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Display table structure
\d sessions;

-- Display indexes
\di sessions*;

-- Success message
SELECT 'Database setup completed successfully!' AS status;
