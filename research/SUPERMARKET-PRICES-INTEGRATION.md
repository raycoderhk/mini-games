# 🛒 Consumer Council Supermarket Prices Integration

## Data Source
- **Provider:** Consumer Council (消費者委員會)
- **Portal:** DATA.GOV.HK
- **Dataset:** Online Price Watch
- **URL:** https://data.gov.hk/en-data/dataset/cc-pricewatch-pricewatch
- **Update:** Daily
- **Format:** JSON
- **Cost:** FREE

## Implementation
- Skill: `/workspace/skills/supermarket-prices/`
- Daily cron job fetches data
- SQLite database for storage
- OpenClaw integration for queries

## User Queries
- "今日百佳同惠康邊度平啲？"
- "邊間超市今日可口可樂 1.25L 最平？"
- "Show me discount offers on snacks"

## Status
✅ Skill created, ready for deployment
