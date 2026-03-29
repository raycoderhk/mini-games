-- ============================================
-- HK PLACES GALLERY - VOTES BACKEND SETUP
-- Run this in Supabase SQL Editor
-- ============================================

-- 1. CREATE VOTES TABLE
CREATE TABLE IF NOT EXISTS votes (
    id BIGSERIAL PRIMARY KEY,
    place_id INTEGER NOT NULL,
    fingerprint TEXT NOT NULL,
    vote_count INTEGER DEFAULT 1,
    voted_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. CREATE INDEX FOR FAST LOOKUPS
CREATE INDEX IF NOT EXISTS idx_votes_lookup ON votes(place_id, fingerprint);

-- 3. ENABLE ROW LEVEL SECURITY
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;

-- 4. CREATE POLICIES (allow anyone to read/write)
DROP POLICY IF EXISTS "Anyone can read votes" ON votes;
CREATE POLICY "Anyone can read votes" ON votes FOR SELECT USING (true);

DROP POLICY IF EXISTS "Anyone can insert votes" ON votes;
CREATE POLICY "Anyone can insert votes" ON votes FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Anyone can update votes" ON votes;
CREATE POLICY "Anyone can update votes" ON votes FOR UPDATE USING (true);
