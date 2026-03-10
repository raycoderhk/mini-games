#!/usr/bin/env node
/**
 * Initialize Supermarket Prices Database Schema
 * Run once to create tables
 */

const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const DB_PATH = path.join(__dirname, 'data', 'supermarket_prices.db');

// Ensure data directory exists
const dataDir = path.dirname(DB_PATH);
if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
    console.log('✅ Created data directory');
}

// Create database
const db = new Database(DB_PATH);
console.log('✅ Connected to database:', DB_PATH);

// Enable WAL mode for better performance
db.pragma('journal_mode = WAL');

// Create tables
console.log('📋 Creating tables...');

db.exec(`
    CREATE TABLE IF NOT EXISTS product_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT NOT NULL,
        product_name TEXT NOT NULL,
        product_name_zh TEXT,
        brand TEXT,
        size TEXT,
        category TEXT,
        store_id TEXT NOT NULL,
        store_name TEXT NOT NULL,
        store_name_zh TEXT,
        price REAL NOT NULL,
        original_price REAL,
        discount_percent REAL,
        discount_text TEXT,
        currency TEXT DEFAULT 'HKD',
        availability TEXT DEFAULT 'in_stock',
        source_url TEXT,
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_date DATE NOT NULL,
        UNIQUE(product_id, store_id, data_date)
    )
`);
console.log('✅ Created product_prices table');

db.exec(`
    CREATE TABLE IF NOT EXISTS product_aliases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT NOT NULL,
        alias TEXT NOT NULL,
        alias_type TEXT,
        UNIQUE(product_id, alias)
    )
`);
console.log('✅ Created product_aliases table');

db.exec(`
    CREATE TABLE IF NOT EXISTS stores (
        id TEXT PRIMARY KEY,
        name_en TEXT NOT NULL,
        name_zh TEXT NOT NULL,
        aliases TEXT
    )
`);
console.log('✅ Created stores table');

db.exec(`
    CREATE TABLE IF NOT EXISTS fetch_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fetch_date DATE NOT NULL,
        fetch_time TIME NOT NULL,
        records_fetched INTEGER,
        status TEXT,
        error_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
`);
console.log('✅ Created fetch_log table');

// Create indexes
console.log('📊 Creating indexes...');

db.exec(`CREATE INDEX IF NOT EXISTS idx_product_name ON product_prices(product_name)`);
db.exec(`CREATE INDEX IF NOT EXISTS idx_product_name_zh ON product_prices(product_name_zh)`);
db.exec(`CREATE INDEX IF NOT EXISTS idx_store_name ON product_prices(store_name)`);
db.exec(`CREATE INDEX IF NOT EXISTS idx_category ON product_prices(category)`);
db.exec(`CREATE INDEX IF NOT EXISTS idx_data_date ON product_prices(data_date)`);
db.exec(`CREATE INDEX IF NOT EXISTS idx_price ON product_prices(price)`);
console.log('✅ Created indexes');

// Insert default stores
console.log('🏪 Inserting default stores...');

const stores = [
    ['parks', 'PARKnSHOP', '百佳', '["百佳超級市場","PKS","百佳超市"]'],
    ['wellcome', 'Wellcome', '惠康', '["惠康超級市場","WCM","惠康超市"]'],
    ['7eleven', '7-Eleven', '七仔', '["7-11","柒拾壹","711"]'],
    ['ok', 'OK Convenience', 'OK便利店', '["OK Store","OK"]'],
    ['aeon', 'AEON', '永旺', '["吉之島","JUSCO"]'],
    ['citysuper', 'Citysuper', 'Citysuper', '["citysuper","超級市場"]'],
    ['marketplace', 'Market Place', 'Market Place', '["Market Place by Jasons"]'],
    ['taste', 'Taste', 'Taste', '["TASTE 超市","TASTE"]'],
    ['uselect', 'Uselect', 'Uselect', '["Uselect 超市","U-Select"]'],
    ['crvanguard', 'CR Vanguard', '華潤', '["華潤萬家","Vanguard"]']
];

const insertStore = db.prepare(`
    INSERT OR REPLACE INTO stores (id, name_en, name_zh, aliases)
    VALUES (?, ?, ?, ?)
`);

for (const store of stores) {
    insertStore.run(...store);
}
console.log(`✅ Inserted ${stores.length} stores`);

// Close database
db.close();
console.log('\n✅ Database initialization complete!');
console.log('📊 Database location:', DB_PATH);
console.log('\n📝 Next step: Run fetch-prices.js to populate data');
