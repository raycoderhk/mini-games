#!/usr/bin/env node
/**
 * Consumer Council Online Price Watch - Daily Fetcher
 * 
 * Fetches latest price data from DATA.GOV.HK
 * Runs daily via cron at 6:00 AM HKT
 * 
 * Usage: node fetch-prices.js
 */

require('dotenv').config();
const fetch = require('node-fetch');
const fs = require('fs').promises;
const path = require('path');

// Configuration
const CONFIG = {
    // TODO: Replace with actual endpoint from DATA.GOV.HK
    DATA_URL: process.env.PRICEWATCH_DATA_URL || 'https://data.gov.hk/data/dataset/cc-pricewatch/resource/latest.json',
    DATA_DIR: path.join(process.cwd(), 'data'),
    LOG_FILE: path.join(process.cwd(), 'logs', 'fetch-prices.log'),
    RETRY_COUNT: 3,
    RETRY_DELAY: 5000,
    TIMEOUT: 30000
};

// Ensure directories exist
async function ensureDirectories() {
    await fs.mkdir(CONFIG.DATA_DIR, { recursive: true });
    await fs.mkdir(path.dirname(CONFIG.LOG_FILE), { recursive: true });
}

// Logging
function log(message, level = 'INFO') {
    const timestamp = new Date().toISOString();
    const logLine = `[${timestamp}] [${level}] ${message}\n`;
    console.log(logLine.trim());
    fs.appendFile(CONFIG.LOG_FILE, logLine).catch(console.error);
}

// Fetch with retry
async function fetchWithRetry(url, retries = CONFIG.RETRY_COUNT) {
    for (let i = 0; i < retries; i++) {
        try {
            log(`Fetching data (attempt ${i + 1}/${retries})...`);
            const response = await fetch(url, {
                timeout: CONFIG.TIMEOUT,
                headers: {
                    'User-Agent': 'OpenClaw-PriceWatch-Bot/1.0',
                    'Accept': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            log(`Successfully fetched ${Object.keys(data).length || 'unknown'} records`);
            return data;
        } catch (error) {
            log(`Fetch failed: ${error.message}`, 'ERROR');
            if (i === retries - 1) throw error;
            log(`Retrying in ${CONFIG.RETRY_DELAY / 1000} seconds...`);
            await new Promise(resolve => setTimeout(resolve, CONFIG.RETRY_DELAY));
        }
    }
}

// Save data to file
async function saveData(data) {
    const date = new Date().toISOString().split('T')[0];
    const filename = `pricewatch-${date}.json`;
    const filepath = path.join(CONFIG.DATA_DIR, filename);
    
    await fs.writeFile(filepath, JSON.stringify(data, null, 2));
    log(`Data saved to ${filepath}`);
    
    // Also save as latest.json for easy access
    const latestPath = path.join(CONFIG.DATA_DIR, 'latest.json');
    await fs.writeFile(latestPath, JSON.stringify(data, null, 2));
    log(`Latest data saved to ${latestPath}`);
    
    return { filename, filepath, date };
}

// Validate data structure
function validateData(data) {
    if (!data || typeof data !== 'object') {
        throw new Error('Invalid data format: expected object');
    }
    
    // TODO: Add specific validation based on actual schema
    // Expected fields might include:
    // - products: array of product objects
    // - lastUpdated: timestamp
    // - source: data source info
    
    log('Data validation passed');
    return true;
}

// Main function
async function main() {
    log('=== Starting Price Watch Data Fetch ===');
    
    try {
        // Ensure directories exist
        await ensureDirectories();
        
        // Fetch data
        const data = await fetchWithRetry(CONFIG.DATA_URL);
        
        // Validate data
        validateData(data);
        
        // Save data
        const saveResult = await saveData(data);
        
        // Log success
        log('=== Fetch Complete ===');
        log(`Date: ${saveResult.date}`);
        log(`File: ${saveResult.filename}`);
        
        // Exit with success
        process.exit(0);
    } catch (error) {
        log(`=== Fetch Failed ===`, 'ERROR');
        log(`Error: ${error.message}`, 'ERROR');
        log(`Stack: ${error.stack}`, 'ERROR');
        
        // Exit with failure
        process.exit(1);
    }
}

// Run main function
main();
