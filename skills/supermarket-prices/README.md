# 🛒 Consumer Council Price Watch Skill

## Overview

OpenClaw skill for comparing supermarket prices across Hong Kong using Consumer Council's Online Price Watch data from DATA.GOV.HK.

## Features

- ✅ Search product prices across all supermarkets
- ✅ Compare prices between stores (百佳 vs 惠康 vs 7-Eleven etc.)
- ✅ Get best deals and discount offers
- ✅ Track price history
- ✅ Cantonese/English synonym support
- ✅ Daily automatic data updates

## Installation

### 1. Install Dependencies

```bash
cd /home/node/.openclaw/skills/supermarket-prices
npm install
```

### 2. Set Up Database

```bash
# Create data directory
mkdir -p data

# Initialize database (schema will be created on first run)
```

### 3. Configure Environment

Create `.env` file:

```bash
# Data source URL (update with actual endpoint from DATA.GOV.HK)
PRICEWATCH_DATA_URL=https://data.gov.hk/data/dataset/cc-pricewatch/resource/latest.json

# Database path
PRICE_DB_PATH=/home/node/.openclaw/skills/supermarket-prices/data/supermarket_prices.db
```

### 4. Set Up Daily Cron Job

```bash
crontab -e

# Add this line (runs daily at 6 AM HKT)
0 6 * * * cd /home/node/.openclaw/skills/supermarket-prices && node fetch-prices.js >> logs/fetch.log 2>&1
```

### 5. Add to OpenClaw Config

Edit `/home/node/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "supermarket-prices": {
      "enabled": true,
      "path": "./skills/supermarket-prices",
      "tools": [
        "search_product_price",
        "compare_stores",
        "get_best_deals",
        "price_history"
      ]
    }
  }
}
```

## Usage

### CLI Testing

```bash
# Search for product
node supermarket-prices.js search "可口可樂"

# Compare stores
node supermarket-prices.js compare "公仔麵"

# Get best deals
node supermarket-prices.js deals

# Check data freshness
node supermarket-prices.js freshness
```

### OpenClaw Integration

Once configured in OpenClaw, users can ask:

```
User: "今日百佳同惠康邊度平啲？"
Agent: [Calls compare_stores API]
Response: "今日惠康平啲！可口可樂 1.25L 惠康 $8.5，百佳 $9.8..."

User: "邊間超市今日可口可樂 1.25L 最平？"
Agent: [Calls search_product_price API]
Response: "今日最平係 7-Eleven，$7.9！第二平係惠康 $8.5..."

User: "Show me discount offers on snacks"
Agent: [Calls get_best_deals API]
Response: "Top deals today: 1. Lay's Chips -30% at PARKnSHOP..."
```

## API Reference

### `search_product_price(keyword, store?, limit?)`

Search for product prices across supermarkets.

**Parameters:**
- `keyword` (string, required): Product name or keyword
- `store` (string, optional): Filter by specific store
- `limit` (number, default 10): Max results

**Returns:** Array of price results

### `compare_stores(keyword)`

Compare prices for a product across different stores.

**Parameters:**
- `keyword` (string, required): Product name

**Returns:** Comparison object with cheapest/most expensive stores

### `get_best_deals(category?, limit?)`

Get current discount offers and best deals.

**Parameters:**
- `category` (string, optional): Product category filter
- `limit` (number, default 10): Max results

**Returns:** Array of best deals with discount info

### `price_history(productId, days?)`

Get price history for a specific product.

**Parameters:**
- `productId` (string, required): Product ID
- `days` (number, default 30): Days to look back

**Returns:** Array of historical prices

### `get_data_freshness()`

Check data freshness and coverage.

**Returns:** Object with latest date, record count, freshness status

## Data Source

- **Provider:** Consumer Council (消費者委員會)
- **Portal:** DATA.GOV.HK
- **Dataset:** Online Price Watch
- **URL:** https://data.gov.hk/en-data/dataset/cc-pricewatch-pricewatch
- **Update Frequency:** Daily
- **License:** Open Data (check specific terms)

## Supported Stores

- 百佳 (PARKnSHOP)
- 惠康 (Wellcome)
- 7-Eleven (七仔)
- OK便利店
- AEON (永旺)
- Citysuper
- Market Place
- Taste
- Uselect
- 華潤 (CR Vanguard)

## Supported Languages

- 🇭🇰 Cantonese (繁體中文)
- 🇬🇧 English
- 🇨🇳 Simplified Chinese (partial)

## Synonym Support

The skill includes extensive synonym mapping for:
- Store names (e.g., 百佳 = PARKnSHOP = PKS)
- Product names (e.g., 可樂 = 可口可樂 = Coca-Cola = Coke)
- Categories (e.g., 飲品 = Drinks = 飲料)

See `synonyms.json` for full list.

## Troubleshooting

### No Results Found

1. Check data freshness: `node supermarket-prices.js freshness`
2. Try different keywords or synonyms
3. Verify database has data: `sqlite3 data/supermarket_prices.db "SELECT COUNT(*) FROM product_prices;"`

### Fetch Fails

1. Check DATA.GOV.HK endpoint URL
2. Verify network connectivity
3. Check logs: `cat logs/fetch.log`
4. Update endpoint if DATA.GOV.HK changed URL

### Database Errors

1. Delete and recreate: `rm data/supermarket_prices.db`
2. Run fetch again to repopulate
3. Check disk space

## Development

### Add New Synonyms

Edit `synonyms.json`:

```json
{
  "stores": {
    "新超市": ["New Store", "新超市", "NS"]
  }
}
```

### Test New Features

```bash
npm test
```

## License

MIT License - See LICENSE file

## Attribution

Data Source: Consumer Council Online Price Watch  
URL: https://data.gov.hk/en-data/dataset/cc-pricewatch-pricewatch

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-10  
**Author:** OpenClaw Research Agent
