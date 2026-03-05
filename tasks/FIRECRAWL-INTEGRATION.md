# 🔥 Firecrawl Integration - Task Tracking

**Created:** 2026-03-05  
**Priority:** HIGH  
**Status:** IN PROGRESS  
**Owner:** Raymond + Jarvis (Research Agent)

---

## 📋 Overview

Deploy self-hosted Firecrawl on Zeabur for unlimited web scraping capability.

**Why:** Current tools (Tavily, web_fetch) have limitations:
- Tavily: 1000 searches/month limit
- web_fetch: No JavaScript support
- Browserless: 500 min/month limit, overkill for simple scraping

**Firecrawl Benefits:**
- ✅ Unlimited scraping (self-hosted)
- ✅ JavaScript support
- ✅ Markdown extraction
- ✅ No external API costs
- ✅ Data stays in your infrastructure

---

## ✅ Completed

- [x] Researched Firecrawl options (Zeabur vs Cloud)
- [x] Identified Zeabur service deployment as best option
- [x] Found correct Docker image: `ghcr.io/firecrawl/firecrawl:latest`
- [x] Identified PostgreSQL requirement
- [x] Documented environment variables needed

---

## ⏳ In Progress

- [ ] **PostgreSQL Service** - Deploy on Zeabur
- [ ] **Firecrawl Service** - Deploy with correct env vars
- [ ] **Environment Variables:**
  - [ ] `DATABASE_URL=${POSTGRES_CONNECTION_STRING}`
  - [ ] `NUQ_DATABASE_URL=${POSTGRES_CONNECTION_STRING}`
  - [ ] `USE_DB_AUTHENTICATION=false`
- [ ] **Get Internal URL** - From Zeabur dashboard

---

## 🔄 Pending

- [ ] **Backup OpenClaw Config**
  ```bash
  cp /home/node/.openclaw/openclaw.json \
     /home/node/.openclaw/openclaw.json.backup.$(date +%Y%m%d_%H%M%S)
  ```

- [ ] **Update OpenClaw Config**
  ```json
  {
    "tools": {
      "web": {
        "firecrawl": {
          "enabled": true,
          "baseUrl": "http://firecrawl.internal:3002",
          "timeoutSeconds": 30
        }
      }
    }
  }
  ```

- [ ] **Test Firecrawl API**
  ```bash
  curl http://FIRECRAWL_URL/api/scrape \
    -H "Content-Type: application/json" \
    -d '{"url": "https://example.com"}'
  ```

- [ ] **Test via OpenClaw**
  - Scrape static page
  - Scrape dynamic JavaScript site
  - Compare output quality

- [ ] **Create Usage Routing Rules**
  ```
  Static HTML → web_fetch (unlimited)
  Search queries → Tavily (1000/month)
  Dynamic sites → Firecrawl (unlimited)
  Automation → Browserless (500 min/month)
  ```

- [ ] **Document Setup**
  - Write deployment guide
  - Add troubleshooting section
  - Create monitoring script

---

## 📊 Resources

| Resource | URL/Value |
|----------|-----------|
| **Zeabur Project** | `699e998cf134fffc31de75d6` |
| **Firecrawl Image** | `ghcr.io/firecrawl/firecrawl:latest` |
| **Firecrawl Docs** | https://docs.firecrawl.dev |
| **Zeabur Dashboard** | https://zeabur.com |
| **Internal URL** | (pending deployment) |

---

## 🚨 Blockers

| Blocker | Status | Resolution |
|---------|--------|------------|
| PostgreSQL service | ⏳ Pending | Deploy via Zeabur dashboard |
| Environment variables | ⏳ Pending | Add to Firecrawl service |
| Internal URL | ⏳ Pending | Get after deployment |

---

## 📈 Success Criteria

- [ ] Firecrawl service shows "Running" in Zeabur
- [ ] curl test returns successful JSON response
- [ ] OpenClaw can scrape pages via Firecrawl
- [ ] Usage routing working correctly
- [ ] No errors in logs after 24 hours

---

## 🕐 Timeline

| Milestone | Target | Actual |
|-----------|--------|--------|
| Research complete | 2026-03-04 | ✅ 2026-03-04 |
| PostgreSQL deployed | 2026-03-05 | ⏳ Pending |
| Firecrawl deployed | 2026-03-05 | ⏳ Pending |
| OpenClaw integration | 2026-03-05 | ⏳ Pending |
| Testing complete | 2026-03-06 | ⏳ Pending |
| Documentation | 2026-03-06 | ⏳ Pending |

---

## 📝 Notes

- Firecrawl v2+ requires PostgreSQL (not just Redis)
- Zeabur doesn't allow Docker-in-Docker, but supports service deployment
- Use Zeabur's variable reference syntax: `${POSTGRES_CONNECTION_STRING}`
- Keep Firecrawl Cloud API key as backup (500 credits free)

---

**Last Updated:** 2026-03-05  
**Next Action:** Deploy PostgreSQL on Zeabur
