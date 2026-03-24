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

### Media Tracker Suite (Books + Movies + TV Series)
**Completed:** March 18th-19th, 2026  
**Status:** ✅ Production Ready  
**URL:** https://kanban-board.zeabur.app/  
**GitHub:** https://github.com/raycoderhk/kanban-board

**Features:**
- **Book Tracker:** Track reading progress, ratings, notes, purchase links
- **Movie Tracker:** Track movies watched, ratings, director, cast, notes
- **TV Series Tracker:** Track series with seasons/episodes, status, creator, cast
- **Unified Navigation:** All trackers accessible from main Kanban homepage
- **Google OAuth SSO:** Single sign-on across all trackers
- **Search & Filter:** Full-text search + tag cloud filtering
- **Dated Notes:** Add timestamped notes to any item
- **Status Tracking:** Want to Read/Watch, In Progress, Completed, Dropped
- **Cover Images:** Upload custom poster/cover images
- **Responsive Design:** Works on desktop and mobile

**Tech Stack:**
- Frontend: Vanilla HTML/CSS/JavaScript
- Backend: Node.js + Express (Kanban server)
- Storage: JSON files (public/*.json)
- Auth: Google OAuth (reuses Kanban `/api/auth/status`)
- Hosting: Zeabur (auto-deploy from GitHub)
- Cost: $0/month (free tiers)

**Initial Content:**
- **Books:** 6+ books (Economist, National Geographic, AI books, art books)
- **Movies:** 3 movies (Project Hail Mary, 一戰再戰, 50 First Dates)
- **TV Series:** 4 series (Black Mirror, The Bear, Shōgun, 唐宫奇案)

**URLs:**
| Tracker | URL |
|---------|-----|
| Main Kanban | https://kanban-board.zeabur.app/ |
| Books | https://kanban-board.zeabur.app/public/index.html |
| Movies | https://kanban-board.zeabur.app/public/movies.html |
| TV Series | https://kanban-board.zeabur.app/public/series.html |
| Magazine | https://kanban-board.zeabur.app/magazine/ |
| Learning Center | https://kanban-board.zeabur.app/magazine/learning-center/ |

**Key Decisions:**
- JSON storage over Supabase (simpler for personal use, migration task created)
- Public access for trackers (no login required to view)
- OAuth for Learning Center (required for personal progress tracking)
- Single sign-on across all pages
- User can add custom items via "Add" buttons

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

## 📅 Upcoming Events (March - May 2026)

**March 7 (Sat):** Son's school parent day (time TBD)  
**March 8 (Sun):** School field trip (HKUST + Yim Tin Tsai)  
**March 10 (Tue):** Pickleball @ Tsuen Wan Pickledise (19:00-21:00)  
**March 13 (Fri):** 📚 Daughter's History Uniform Test (Revision starts Mar 10)  
**March 14 (Sat):** ✅ Queen Elizabeth School PTA Trip (daughter selected) + Clan Association Dinner
  - Trip: 08:45-16:30, $90/person (subsidized)
  - Itinerary: Dragon fruit farm → Kimchi workshop → Abalone lunch (Flow Shan) → Mural Village  
**March 15 (Sun):** Son's birthday, Maxim's vouchers expire ($250 x 2)  
**March 17 (Tue):** Wedding anniversary @ Ocean Park Marriott  

**May 5 (Tue):** 🏥 **Son** WONG T* Y* medical appointment @ Caritas Medical Centre
  - Department: Ear, Nose and Throat / 耳鼻喉科 (ENT)
  - Time: 10:15 AM
  - Note: After turning 16, transitioning from paediatrics to adult ENT

**May 15 (Fri):** 🏥 Grandma WONG T* M* medical appointment @ Yan Chai Hospital
  - Department: General Surgery (Outpatient)
  - Time: 12:00 PM

**June 3 (Wed):** 🏥 **Son** WONG T* Y* medical appointment @ Princess Margaret Hospital
  - Department: Paediatrics and Adolescent Medicine / 兒童及青少年科
  - Time: 3:15 PM

**September 22 (Tue):** 🏥 Grandma WONG T* M* medical appointment @ Princess Margaret Hospital
  - Department: Urology (泌尿外科)
  - Time: 11:30 AM

**October 28 (Wed):** 🏥 **Son** WONG T* Y* medical appointment @ Caritas Medical Centre
  - Department: Audiology / 聽力學
  - Time: 11:00 AM

## 🏥 Family Health Records

### Grandma WONG T* M* (嫲嫲)
**March 22, 2026 (今日複診):**
- **體重:** 38.4 kg (84.658 lbs)
- **備註:** 今日複診記錄

**Upcoming Appointments:**
1. **May 15, 2026 (Fri) 12:00** - Yan Chai Hospital (General Surgery)
2. **September 22, 2026 (Tue) 11:30** - Princess Margaret Hospital (Urology)

### Son WONG T* Y*
**Upcoming Appointments:**
1. **May 5, 2026 (Tue) 10:15** - Caritas Medical Centre (ENT)
2. **June 3, 2026 (Wed) 15:15** - Princess Margaret Hospital (Paediatrics)
3. **October 28, 2026 (Wed) 11:00** - Caritas Medical Centre (Audiology)

## 🎓 Son's DSE Exams (2026)
**Status:** Critical exam period  
**Oral Exam:** Next week (mid-March)  
**Major Written Exams:** April 2026  

**Academic Profile:**
- **Strong:** Math, M2, ICT (expecting at least 5* in each)
- **Weak:** Chinese (borderline concern)
- **Strategy:** Strong subjects should compensate, Chinese needs attention

**Personal Context:**
- Age: 17 (December born)
- One of the younger/smaller kids in his class
- This can add pressure — comparing himself to older classmates

**Family Context:**
- High-stress period for the family
- Son needs support and quiet study environment
- Parents likely juggling school events + exam prep
- Consider reducing non-urgent notifications during this period

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
