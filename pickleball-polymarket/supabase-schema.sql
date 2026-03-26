-- =====================================================
-- Pickleball Polymarket Database Schema
-- For cross-device real-time betting sync
-- =====================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Markets table: one row per market (question)
CREATE TABLE IF NOT EXISTS polymarket_markets (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    market_id       TEXT UNIQUE NOT NULL,  -- e.g. 'pickleball-court-color'
    question        TEXT NOT NULL,
    options         JSONB NOT NULL,         -- e.g. ["Blue","Purple","Green",...]
    revealed        BOOLEAN DEFAULT false,
    winner          TEXT DEFAULT NULL,
    admin_password  TEXT NOT NULL,          -- hashed ideally, plain for now
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Bets table: one row per bettor's bet
CREATE TABLE IF NOT EXISTS polymarket_bets (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    market_id       TEXT NOT NULL,
    bettor_name     TEXT NOT NULL,
    color           TEXT NOT NULL,
    pushups         INTEGER NOT NULL CHECK (pushups >= 1 AND pushups <= 10),
    timestamp       BIGINT NOT NULL,        -- client timestamp millis
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_bets_market ON polymarket_bets(market_id);
CREATE INDEX IF NOT EXISTS idx_bets_color ON polymarket_bets(market_id, color);

-- Row Level Security
ALTER TABLE polymarket_markets ENABLE ROW LEVEL SECURITY;
ALTER TABLE polymarket_bets ENABLE ROW LEVEL SECURITY;

-- Allow public read/write
CREATE POLICY "Allow all on markets" ON polymarket_markets FOR ALL USING (true);
CREATE POLICY "Allow all on bets" ON polymarket_bets FOR ALL USING (true);

-- Grant permissions
GRANT ALL ON ALL TABLES IN SCHEMA public TO PUBLIC;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO PUBLIC;

-- =====================================================
-- Seed the default pickleball market
-- =====================================================
INSERT INTO polymarket_markets (market_id, question, options, admin_password)
VALUES (
    'pickleball-court-color',
    '🏸 新打球場墊係咩顏色？ / What color is the new court mat?',
    '["Blue","Purple","Green","Red","Orange","Pink","White","Yellow","Other"]',
    'pickle2024'
) ON CONFLICT (market_id) DO NOTHING;
