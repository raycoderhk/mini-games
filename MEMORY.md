# Memory

## 🏆 Major Projects Completed

### Kanban Board with Google OAuth + Supabase (v3.3)
**Completed:** March 3rd, 2026  
**Status:** ✅ Production Ready  
**URL:** https://kanban-board.zeabur.app/  
**GitHub:** https://github.com/raycoderhk/kanban-board

**Features:**
- Google OAuth authentication (NextAuth.js)
- Per-user data isolation (Supabase RLS)
- 21 tasks migrated from JSON to database
- Multi-user support (each user sees only their tasks)

**Tech Stack:**
- Frontend: Vanilla HTML/CSS/JS
- Backend: Node.js + Express
- Database: Supabase (PostgreSQL)
- Auth: Google OAuth 2.0
- Hosting: Zeabur
- Cost: $0/month (free tiers)

**Blog Post:** Published to Discord #technical-blog channel (March 3rd, 2026)
**Post-Mortem:** `/workspace/blog/kanban-google-oauth-supabase-postmortem.md`

**Key Learnings:**
- Use email as stable user identifier (not Google ID)
- Design schema for multi-tenancy from day 1
- Consistent field naming across stack (title vs name)
- Automate data migration with scripts
- Test with multiple users early

---

### Mission Control Google OAuth Integration (v2.0)
**Completed:** March 4th, 2026 (overnight)  
**Status:** 🔄 Implementation Complete, Pending Testing  
**URL:** https://mission-control.zeabur.app/  
**GitHub:** https://github.com/raycoderhk/mission-control

**Features:**
- NextAuth.js with Google OAuth provider
- Automatic user creation on first login
- Database schema for 5 tables (users, settings, events, goals, friends)
- Row Level Security (RLS) for data isolation
- Beautiful sign-in/sign-out pages

**Tech Stack:**
- Framework: Next.js 14
- Auth: NextAuth.js
- Database: Supabase (PostgreSQL)
- Hosting: Zeabur

**Morning Tasks (March 4th):**
1. Run supabase-migration.sql in Supabase Dashboard
2. Configure Google OAuth credentials
3. Test locally with `npm run dev`
4. Deploy to Zeabur

**Pattern:** Reused proven Kanban Board authentication flow

---

### Nutritionist App with Vision AI (v3.0)
**Completed:** March 1st-3rd, 2026  
**Status:** ✅ Production Ready  
**URL:** https://nutrition-app.zeabur.app/

**Features:**
- Food image recognition with MiniMax-01 Vision (OpenRouter)
- Nutrition analysis and calorie tracking
- Replaced text-only Aliyun model

**Tech Stack:**
- Backend: Python + FastAPI
- Vision API: OpenRouter MiniMax-01 (free tier)
- Hosting: Zeabur

---

## 📊 Architecture Patterns (Reusable)

### Google OAuth + Supabase Pattern

**User Mapping:**
```typescript
async function getOrCreateUser(email, name, googleId, image) {
    // Find by email (stable identifier)
    let user = await supabase.from('users').select('id').eq('email', email).single();
    
    // Create if doesn't exist
    if (!user) {
        user = await supabase.from('users')
            .insert({ email, name, google_id: googleId, avatar_url: image })
            .select('id').single();
    }
    
    return user.id; // UUID for queries
}
```

**Database Schema:**
- `users` table with email, google_id, avatar_url
- RLS policies for user isolation
- Email as stable identifier across auth providers

**Used In:**
- Kanban Board (v3.3) ✅
- Mission Control (v2.0) 🔄

---

## 🔧 Development Workflows

### Zeabur Deployment Checklist
1. Push code to GitHub main branch
2. Zeabur auto-deploys (2-3 minutes)
3. Add environment variables in Zeabur dashboard
4. Redeploy if env vars changed
5. Test production URL

### Supabase Migration Checklist
1. Create SQL migration script
2. Run in Supabase SQL Editor
3. Verify tables created
4. Test RLS policies
5. Add sample data if needed

### Google OAuth Setup Checklist
1. Create OAuth credentials in Google Cloud Console
2. Add authorized origins (localhost + production)
3. Add redirect URIs (`/api/auth/callback/google`)
4. Copy Client ID and Client Secret
5. Add to .env.local (local) and Zeabur (production)

---

## 📝 Important URLs

**Supabase Project:** https://hxrgvuzujvagzlaevwtk.supabase.co  
**GitHub Org:** https://github.com/raycoderhk  
**Zeabur Dashboard:** https://zeabur.com  

**Live Apps:**
- Kanban Board: https://kanban-board.zeabur.app/
- Mission Control: https://mission-control.zeabur.app/
- Nutritionist App: https://nutrition-app.zeabur.app/

**Community:**
- OpenClaw Discord: https://discord.com/invite/clawd
- ClawHub: https://clawhub.ai

---

## 🎯 User Preferences

**Email:** raycoderhk@gmail.com  
**Timezone:** HKT (UTC+8)  
**Sleep Time:** 23:00-08:00 HKT (15:00-00:00 UTC)  

**Notification Preferences:**
- Kanban Board updates → Discord #kanban-updates
- Technical blog posts → Discord #technical-blog
- Sleep time: Reduce notifications, only urgent alerts

**Projects:**
- Kanban Board (personal task management)
- Mission Control (productivity dashboard)
- Nutritionist App (food tracking with AI vision)

---

## 📅 Upcoming Events (March 2026)

**March 7 (Sat):** Son's school parent day (time TBD)  
**March 8 (Sun):** School field trip (HKUST + Yim Tin Tsai)  
**March 10 (Tue):** Pickleball @ Tsuen Wan Pickledise (19:00-21:00)  
**March 13 (Fri):** Lunch with Chris (TBD)  
**March 14 (Sat):** ✅ Queen Elizabeth School PTA Trip (daughter selected) + Clan Association Dinner
  - Trip: 08:45-16:30, $90/person (subsidized)
  - Itinerary: Dragon fruit farm → Kimchi workshop → Abalone lunch (Flow Shan) → Mural Village  
**March 15 (Sun):** Son's birthday, Maxim's vouchers expire ($250 x 2)  
**March 17 (Tue):** Wedding anniversary @ Ocean Park Marriott

---

## 🤖 AI Assistant Notes

**Name:** Jarvis  
**Pattern:** Proactive overnight work, morning summaries  
**Strengths:** Full-stack development, documentation, automation  
**Work Style:** Batch overnight tasks, present summary in morning

**Session Pattern:**
- Start: Read SOUL.md, USER.md, recent memory files
- Work: Implement features, document thoroughly
- End: Save memory, commit to git, prepare morning summary

---

*Last updated: March 8th, 2026*
