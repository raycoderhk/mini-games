#!/usr/bin/env node
/**
 * Consumer Council Online Price Watch - OpenClaw Skill
 * 
 * Provides functions to search and compare supermarket prices
 * 
 * Usage: 
 *   const skill = require('./supermarket-prices');
 *   const results = await skill.search_product_price('可口可樂');
 */

const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

// Configuration
const CONFIG = {
    DATABASE_PATH: process.env.PRICE_DB_PATH || path.join(__dirname, 'data', 'supermarket_prices.db'),
    SYNONYM_FILE: path.join(__dirname, 'synonyms.json')
};

// Load synonyms
let synonyms = {};
try {
    const synonymData = fs.readFileSync(CONFIG.SYNONYM_FILE, 'utf8');
    synonyms = JSON.parse(synonymData);
} catch (error) {
    console.warn('Warning: Could not load synonyms file, using empty synonyms');
}

// Database connection
let db = null;

function getDb() {
    if (!db) {
        // Ensure data directory exists
        const dbDir = path.dirname(CONFIG.DATABASE_PATH);
        if (!fs.existsSync(dbDir)) {
            fs.mkdirSync(dbDir, { recursive: true });
        }
        db = new Database(CONFIG.DATABASE_PATH);
        db.pragma('journal_mode = WAL');
    }
    return db;
}

/**
 * Expand search keywords using synonym map
 * @param {string} keyword - Original keyword
 * @param {string} type - 'product' or 'store'
 * @returns {string[]} - Array of keywords including synonyms
 */
function expandKeywords(keyword, type = 'product') {
    const results = [keyword.toLowerCase()];
    const synonymMap = type === 'store' ? synonyms.stores : synonyms.products;
    
    if (synonymMap) {
        // Check if keyword matches any synonym group
        for (const [canonical, aliasList] of Object.entries(synonymMap)) {
            if (aliasList.some(alias => alias.toLowerCase() === keyword.toLowerCase())) {
                // Add all aliases from this group
                aliasList.forEach(alias => results.push(alias.toLowerCase()));
                results.push(canonical.toLowerCase());
                break;
            }
        }
    }
    
    return [...new Set(results)]; // Remove duplicates
}

/**
 * Search for product prices across all supermarkets
 * @param {string} keyword - Product name or keyword
 * @param {string} store - Optional store filter
 * @param {number} limit - Max results (default 10)
 * @returns {Promise<Array>} - Array of price results
 */
async function search_product_price(keyword, store = null, limit = 10) {
    const database = getDb();
    
    // Expand keywords with synonyms
    const keywords = expandKeywords(keyword, 'product');
    const likePatterns = keywords.map(k => `%${k}%`);
    
    let query = `
        SELECT 
            product_id,
            product_name,
            product_name_zh,
            brand,
            size,
            category,
            store_name,
            store_name_zh,
            price,
            original_price,
            discount_percent,
            discount_text,
            availability,
            data_date
        FROM product_prices
        WHERE data_date = (SELECT MAX(data_date) FROM product_prices)
        AND (
    `;
    
    // Add OR conditions for each keyword pattern
    const conditions = likePatterns.map(() => 'product_name LIKE ? OR product_name_zh LIKE ?').join(' OR ');
    query += conditions;
    query += ')';
    
    const params = keywords.flatMap(k => [k, k]);
    
    if (store) {
        const storeKeywords = expandKeywords(store, 'store');
        const storePatterns = storeKeywords.map(k => `%${k}%`);
        query += ' AND (store_name LIKE ? OR store_name_zh LIKE ?';
        query += ' OR ' + storePatterns.map(() => 'store_name LIKE ?').join(' OR ') + ')';
        params.push(store, store, ...storeKeywords);
    }
    
    query += ' ORDER BY price ASC LIMIT ?';
    params.push(limit);
    
    const stmt = database.prepare(query);
    const results = stmt.all(...params);
    
    return results.map(row => ({
        productId: row.product_id,
        productName: row.product_name_zh || row.product_name,
        brand: row.brand,
        size: row.size,
        category: row.category,
        store: row.store_name_zh || row.store_name,
        price: row.price,
        originalPrice: row.original_price,
        discountPercent: row.discount_percent,
        discountText: row.discount_text,
        availability: row.availability,
        dataDate: row.data_date
    }));
}

/**
 * Compare prices for a product across different stores
 * @param {string} keyword - Product name or keyword
 * @returns {Promise<Object>} - Comparison results by store
 */
async function compare_stores(keyword) {
    const database = getDb();
    
    // Get all prices for this product
    const prices = await search_product_price(keyword, null, 100);
    
    if (prices.length === 0) {
        return {
            keyword,
            found: false,
            message: `No results found for "${keyword}"`,
            stores: []
        };
    }
    
    // Group by store
    const storePrices = {};
    prices.forEach(item => {
        if (!storePrices[item.store]) {
            storePrices[item.store] = [];
        }
        storePrices[item.store].push(item);
    });
    
    // Calculate cheapest per store
    const comparison = Object.entries(storePrices).map(([store, items]) => {
        const cheapest = items.reduce((min, item) => item.price < min.price ? item : min, items[0]);
        return {
            store,
            cheapestPrice: cheapest.price,
            cheapestItem: cheapest.productName,
            totalItems: items.length,
            priceRange: {
                min: Math.min(...items.map(i => i.price)),
                max: Math.max(...items.map(i => i.price))
            }
        };
    }).sort((a, b) => a.cheapestPrice - b.cheapestPrice);
    
    return {
        keyword,
        found: true,
        cheapestStore: comparison[0],
        mostExpensiveStore: comparison[comparison.length - 1],
        stores: comparison,
        dataDate: prices[0].dataDate
    };
}

/**
 * Get current discount offers and best deals
 * @param {string} category - Optional category filter
 * @param {number} limit - Max results (default 10)
 * @returns {Promise<Array>} - Array of best deals
 */
async function get_best_deals(category = null, limit = 10) {
    const database = getDb();
    
    let query = `
        SELECT 
            product_id,
            product_name,
            product_name_zh,
            brand,
            size,
            category,
            store_name,
            store_name_zh,
            price,
            original_price,
            discount_percent,
            discount_text,
            data_date
        FROM product_prices
        WHERE data_date = (SELECT MAX(data_date) FROM product_prices)
        AND discount_percent IS NOT NULL
        AND discount_percent > 0
    `;
    
    const params = [];
    
    if (category) {
        query += ' AND category LIKE ?';
        params.push(`%${category}%`);
    }
    
    query += ' ORDER BY discount_percent DESC, price ASC LIMIT ?';
    params.push(limit);
    
    const stmt = database.prepare(query);
    const results = stmt.all(...params);
    
    return results.map(row => ({
        productId: row.product_id,
        productName: row.product_name_zh || row.product_name,
        brand: row.brand,
        size: row.size,
        category: row.category,
        store: row.store_name_zh || row.store_name,
        price: row.price,
        originalPrice: row.original_price,
        discountPercent: row.discount_percent,
        discountText: row.discount_text,
        savings: row.original_price - row.price,
        dataDate: row.data_date
    }));
}

/**
 * Get price history for a specific product
 * @param {string} productId - Product ID
 * @param {number} days - Number of days to look back (default 30)
 * @returns {Promise<Array>} - Array of historical prices
 */
async function price_history(productId, days = 30) {
    const database = getDb();
    
    const query = `
        SELECT 
            product_id,
            product_name,
            product_name_zh,
            store_name,
            store_name_zh,
            price,
            data_date
        FROM product_prices
        WHERE product_id = ?
        AND data_date >= date('now', ?)
        ORDER BY data_date DESC
    `;
    
    const stmt = database.prepare(query);
    const results = stmt.all(productId, `-${days} days`);
    
    return results.map(row => ({
        productId: row.product_id,
        productName: row.product_name_zh || row.product_name,
        store: row.store_name_zh || row.store_name,
        price: row.price,
        date: row.data_date
    }));
}

/**
 * Get data freshness info
 * @returns {Promise<Object>} - Data freshness information
 */
async function get_data_freshness() {
    const database = getDb();
    
    const query = `
        SELECT 
            MAX(data_date) as latest_date,
            MIN(data_date) as earliest_date,
            COUNT(DISTINCT data_date) as days_available,
            COUNT(*) as total_records
        FROM product_prices
    `;
    
    const stmt = database.prepare(query);
    const result = stmt.get();
    
    return {
        latestDate: result.latest_date,
        earliestDate: result.earliest_date,
        daysAvailable: result.days_available,
        totalRecords: result.total_records,
        isFresh: result.latest_date === new Date().toISOString().split('T')[0]
    };
}

// Export functions
module.exports = {
    search_product_price,
    compare_stores,
    get_best_deals,
    price_history,
    get_data_freshness,
    expandKeywords,
    getDb
};

// CLI interface for testing
if (require.main === module) {
    const args = process.argv.slice(2);
    const command = args[0];
    
    async function runTest() {
        try {
            if (command === 'search' && args[1]) {
                console.log(`Searching for: ${args[1]}`);
                const results = await search_product_price(args[1]);
                console.log(JSON.stringify(results, null, 2));
            } else if (command === 'compare' && args[1]) {
                console.log(`Comparing stores for: ${args[1]}`);
                const results = await compare_stores(args[1]);
                console.log(JSON.stringify(results, null, 2));
            } else if (command === 'deals') {
                console.log('Getting best deals...');
                const results = await get_best_deals(null, 10);
                console.log(JSON.stringify(results, null, 2));
            } else if (command === 'freshness') {
                console.log('Checking data freshness...');
                const results = await get_data_freshness();
                console.log(JSON.stringify(results, null, 2));
            } else {
                console.log('Usage:');
                console.log('  node supermarket-prices.js search <keyword>');
                console.log('  node supermarket-prices.js compare <keyword>');
                console.log('  node supermarket-prices.js deals');
                console.log('  node supermarket-prices.js freshness');
            }
        } catch (error) {
            console.error('Error:', error.message);
            process.exit(1);
        }
    }
    
    runTest();
}
