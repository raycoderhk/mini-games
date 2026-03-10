#!/bin/bash
# Consumer Council Online Price Watch - Daily Fetch
# Run this manually or via systemd timer until cron is available
# 
# For now, run daily: ./daily-fetch.sh

cd /home/node/.openclaw/workspace/skills/supermarket-prices

echo "[$(date)] Starting daily price fetch..." >> logs/fetch.log
node fetch-prices.js >> logs/fetch.log 2>&1
echo "[$(date)] Fetch complete" >> logs/fetch.log
