-- Votes table for HK Places Gallery
CREATE TABLE IF NOT EXISTS votes (
    id BIGSERIAL PRIMARY KEY,
    place_id INTEGER NOT NULL,
    fingerprint TEXT NOT NULL,
    vote_count INTEGER DEFAULT 1,
    voted_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_votes_place_fingerprint ON votes(place_id, fingerprint);
CREATE INDEX IF NOT EXISTS idx_votes_place_id ON votes(place_id);

-- RLS policies (Row Level Security)
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;

-- Anyone can read votes
CREATE POLICY "Anyone can read votes" ON votes
    FOR SELECT USING (true);

-- Anyone can insert votes (with fingerprint)
CREATE POLICY "Anyone can insert votes" ON votes
    FOR INSERT WITH CHECK (true);

-- Functions to get vote count and check cooldown
CREATE OR REPLACE FUNCTION get_vote_count(p_place_id INTEGER)
RETURNS BIGINT AS $$
    SELECT COALESCE(SUM(vote_count), 0)::BIGINT
    FROM votes
    WHERE place_id = p_place_id;
$$ LANGUAGE SQL STABLE;

CREATE OR REPLACE FUNCTION check_vote_cooldown(p_place_id INTEGER, p_fingerprint TEXT)
RETURNS BOOLEAN AS $$
    SELECT (
        SELECT COUNT(*) = 0 OR 
        (NOW() - MAX(voted_at)) > INTERVAL '24 hours'
    FROM votes
    WHERE place_id = p_place_id AND fingerprint = p_fingerprint
    );
$$ LANGUAGE SQL STABLE;

CREATE OR REPLACE FUNCTION cast_vote(p_place_id INTEGER, p_fingerprint TEXT)
RETURNS JSONB AS $$
DECLARE
    can_vote BOOLEAN;
    new_count BIGINT;
BEGIN
    -- Check cooldown
    SELECT check_vote_cooldown(p_place_id, p_fingerprint) INTO can_vote;
    
    IF NOT can_vote THEN
        RETURN jsonb_build_object('success', false, 'cooldown', true, 'message', '24 hour cooldown');
    END IF;
    
    -- Insert vote
    INSERT INTO votes (place_id, fingerprint, vote_count, voted_at)
    VALUES (p_place_id, p_fingerprint, 1, NOW())
    ON CONFLICT (place_id, fingerprint) 
    DO UPDATE SET vote_count = votes.vote_count + 1, voted_at = NOW();
    
    -- Get new count
    SELECT get_vote_count(p_place_id) INTO new_count;
    
    RETURN jsonb_build_object('success', true, 'count', new_count);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_all_vote_counts()
RETURNS TABLE(place_id INTEGER, count BIGINT) AS $$
    SELECT place_id, SUM(vote_count)::BIGINT as count
    FROM votes
    GROUP BY place_id;
$$ LANGUAGE SQL STABLE;
