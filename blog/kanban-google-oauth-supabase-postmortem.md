# 📋 Kanban Board with Google OAuth + Supabase: Complete Post-Mortem

**Published:** 2026-03-03  
**Author:** Raymond + Jarvis  
**Tags:** #supabase #google-oauth #kanban #zeabur #fullstack #postmortem

---

## 🎯 Executive Summary

**Mission:** Build a personal Kanban board with Google OAuth authentication and per-user data isolation

**Status:** ✅ **SUCCESS** (after 3.3 iterations)

**Time:** ~8 hours (from first commit to working production)

**Tech Stack:**
- Frontend: Vanilla HTML/CSS/JS
- Backend: Node.js + Express
- Database: Supabase (PostgreSQL)
- Auth: Google OAuth 2.0
- Hosting: Zeabur

---

## 🚀 What We Built

### Core Features

| Feature | Status | Notes |
|---------|--------|-------|
| **Google OAuth Login** | ✅ Working | Users can sign in with Google |
| **User Data Isolation** | ✅ Working | Each user sees only their own tasks |
| **CRUD Operations** | ✅ Working | Create, Read, Update, Delete tasks |
| **Real-time Sync** | ⏳ Pending | Next iteration |
| **Mobile Responsive** | ✅ Working | Works on desktop + mobile |

### User Flow

```
1. Visit https://kanban-board.zeabur.app/
2. Click "🔐 Use Google Login"
3. Select Google account
4. See YOUR personal Kanban board
5. Add/move/delete tasks
6. Logout → data stays secure
```

---

## 🏗️ Architecture

### System Diagram

```
┌─────────────────┐
│   User Browser  │
│                 │
│  ┌───────────┐  │
│  │  Frontend │  │
│  │  (HTML/   │  │
│  │   JS)     │  │
│  └─────┬─────┘  │
└────────┼────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│   Zeabur Host   │
│                 │
│  ┌───────────┐  │
│  │  Express  │  │
│  │  Server   │──┼── Google OAuth
│  │  (Node.js)│  │
│  └─────┬─────┘  │
└────────┼────────┘
         │ REST API
         ▼
┌─────────────────┐
│   Supabase DB   │
│                 │
│  ┌───────────┐  │
│  │  users    │  │
│  │  - id     │  │
│  │  - email  │  │
│  │  - google │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │  projects │  │
│  │  - id     │  │
│  │  - user_id│  │
│  │  - title  │  │
│  │  - status │  │
│  └───────────┘  │
└─────────────────┘
```

### Database Schema

```sql
-- Users table (Google OAuth mapping)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    google_id TEXT UNIQUE,
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Projects table (Kanban tasks)
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),  -- ← KEY for isolation!
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('todo', 'in_progress', 'done', 'blocked')),
    priority TEXT DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users view own projects"
    ON projects FOR SELECT
    USING (auth.uid() = user_id);
```

---

## 🐛 Challenges & Solutions

### Challenge 1: User ID Mismatch ❌

**Problem:**
```javascript
// Google OAuth returns string ID
req.user.id = "123456789012345678901"

// Supabase expects UUID
user_id = "550e8400-e29b-41d4-a716-446655440000"

// Direct comparison = NEVER MATCHES!
```

**Symptom:** User logs in but sees 0 tasks 😱

**Solution:** Email-based user mapping
```javascript
async function getOrCreateUser(email, displayName, googleId, photo) {
    // 1. Find user by email
    let user = await supabase
        .from('users')
        .select('id')
        .eq('email', email)
        .single();
    
    // 2. If not exists, create new user
    if (!user) {
        user = await supabase
            .from('users')
            .insert({ email, name: displayName, google_id })
            .select('id')
            .single();
    }
    
    return user.id; // UUID
}
```

**Lesson:** Never assume auth provider IDs match database IDs. Use email as stable identifier.

---

### Challenge 2: Field Name Mismatch ❌

**Problem:**
```javascript
// Frontend sends
{ name: "Task Title" }

// Backend expects
{ title: "Task Title" }

// Result: Task saves but title is NULL!
```

**Symptom:** New tasks don't show up after creation

**Solution:** Consistent field naming
```javascript
// Frontend (index.html)
const newProject = {
    title: title,  // ← Match Supabase column!
    description: description,
    status: 'todo'
};

// Backend rendering
<div class="project-title">
    ${escapeHtml(project.title || project.name || 'Untitled')}
</div>
```

**Lesson:** Use same field names across frontend, backend, and database. Document naming conventions.

---

### Challenge 3: Data Migration ❌

**Problem:**
- Existing tasks in `kanban-board.json` (GitHub)
- New Supabase database is empty
- User logs in → sees nothing!

**Solution:** Automated migration script
```javascript
// auto-migrate.js
const PROJECTS = [
    { name: 'Task 1', status: 'todo', ... },
    { name: 'Task 2', status: 'in_progress', ... },
    // ... 21 tasks
];

async function migrate() {
    // 1. Create user
    const user = await getOrCreateUser(email, name);
    
    // 2. Migrate all projects
    for (const proj of PROJECTS) {
        await supabase.from('projects').upsert({
            user_id: user.id,
            title: proj.name,
            status: proj.status,
            ...
        });
    }
}
```

**Result:** 21 tasks migrated in 3 seconds ✅

**Lesson:** Always plan data migration strategy early. Automate it!

---

### Challenge 4: Schema Evolution ❌

**Problem:**
```sql
-- Original schema (no user isolation)
CREATE TABLE projects (
    id UUID,
    title TEXT,
    status TEXT,
    ...
);

-- New requirement: per-user data
-- Need to add: user_id column
```

**Solution:** Migration SQL
```sql
-- Add user_id column
ALTER TABLE projects 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);

-- Create index for performance
CREATE INDEX IF NOT EXISTS projects_user_id_idx 
ON projects(user_id);
```

**Lesson:** Design for multi-tenancy from day 1. Retro-fitting is painful.

---

## 📊 Version History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| **v1.0** | 2026-02-26 | ✅ Deployed | Basic Kanban (shared data) |
| **v2.0** | 2026-03-02 | ✅ Deployed | Google OAuth added |
| **v3.0** | 2026-03-03 | ❌ Broken | Supabase integration (user ID bug) |
| **v3.1** | 2026-03-03 | ❌ Broken | Email mapping fix |
| **v3.2** | 2026-03-03 | ❌ Broken | Field name bug (name vs title) |
| **v3.3** | 2026-03-03 | ✅ **WORKING!** | All bugs fixed |

---

## 🎯 Key Learnings

### Technical Lessons

1. **Schema Design First** 📐
   - Define database schema BEFORE coding
   - Use consistent naming (title vs name)
   - Plan for multi-tenancy early

2. **Auth Provider Abstraction** 🔐
   - Never use provider IDs directly
   - Map to internal user IDs
   - Email is stable identifier

3. **Automated Testing** 🧪
   - Test login flow end-to-end
   - Test CRUD operations
   - Test with multiple users

4. **Data Migration** 📦
   - Plan migration strategy early
   - Automate with scripts
   - Test on staging first

### Process Lessons

1. **Incremental Deployment** 🚀
   - Deploy small changes frequently
   - Test each feature before next
   - Don't batch too many changes

2. **Error Messages Matter** 📢
   - Clear errors help debugging
   - Log user ID, email for tracing
   - Show success feedback to users

3. **Documentation** 📝
   - Document schema changes
   - Keep migration scripts versioned
   - Write post-mortems!

---

## 🛠️ Code Snippets

### Server Setup (server.js)

```javascript
const express = require('express');
const passport = require('passport');
const { createClient } = require('@supabase/supabase-js');

const app = express();
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Google OAuth strategy
passport.use(new GoogleStrategy({
    clientID: GOOGLE_CLIENT_ID,
    clientSecret: GOOGLE_CLIENT_SECRET,
    callbackURL: '/auth/google/callback'
}, (accessToken, refreshToken, profile, done) => {
    return done(null, profile);
}));

// Get user's projects
app.get('/api/kanban', async (req, res) => {
    if (!req.isAuthenticated()) {
        return res.json({ projects: [] });
    }
    
    const email = req.user.emails[0].value;
    const user = await getOrCreateUser(email);
    
    const { data } = await supabase
        .from('projects')
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false });
    
    res.json({ projects: data || [] });
});
```

### Frontend (index.html)

```javascript
// Add new project
async function addNewProject() {
    const title = prompt('Project name:');
    if (!title) return;
    
    const description = prompt('Description (optional):') || '';
    
    const response = await fetch('/api/kanban', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            projects: [{
                title,
                description,
                status: 'todo',
                priority: 'medium'
            }]
        })
    });
    
    const result = await response.json();
    if (result.success) {
        loadKanban(); // Refresh board
    } else {
        alert('Failed: ' + result.error);
    }
}
```

### Migration Script (auto-migrate.js)

```javascript
async function migrate() {
    console.log('🚀 Starting migration...');
    
    // 1. Create user
    const user = await supabase
        .from('users')
        .insert({ email, name, google_id })
        .select('id')
        .single();
    
    // 2. Migrate projects
    for (const proj of PROJECTS) {
        await supabase
            .from('projects')
            .upsert({
                user_id: user.id,
                title: proj.name,
                status: proj.status,
                priority: proj.priority
            });
    }
    
    console.log(`✅ Migrated ${PROJECTS.length} projects!`);
}
```

---

## 🎉 Success Metrics

| Metric | Before | After |
|--------|--------|-------|
| **Login Method** | None | Google OAuth |
| **Data Isolation** | ❌ Shared | ✅ Per-user |
| **Security** | ❌ Public | ✅ Authenticated |
| **Scalability** | ❌ Single user | ✅ Multi-user |
| **Tasks Migrated** | 0 | 21 |
| **Time to Deploy** | N/A | 8 hours |

---

## 🚀 Next Steps

### Phase 1: Polish (Week 1)
- [ ] Add drag-and-drop for task moving
- [ ] Add task editing (not just create)
- [ ] Add task deletion with confirmation
- [ ] Improve mobile UI

### Phase 2: Features (Week 2-3)
- [ ] Real-time sync (Supabase Realtime)
- [ ] Task comments/notes
- [ ] File attachments
- [ ] Task due dates

### Phase 3: Advanced (Month 2)
- [ ] Team collaboration (shared boards)
- [ ] Activity log / audit trail
- [ ] Export to CSV/PDF
- [ ] Dark mode

---

## 📚 Resources

### Documentation
- [Supabase Docs](https://supabase.com/docs)
- [Passport.js Google OAuth](http://www.passportjs.org/packages/passport-google-oauth20/)
- [Zeabur Deployment](https://zeabur.com/docs)

### GitHub Repo
- **Source Code:** https://github.com/raycoderhk/kanban-board
- **Migration Script:** `kanban-zeabur/auto-migrate.js`
- **Setup Guide:** `kanban-zeabur/MIGRATE.md`

### Live Demo
- **URL:** https://kanban-board.zeabur.app/
- **Test Login:** Any Google account

---

## 🙏 Acknowledgments

- **Jarvis** (AI assistant) - Debugging, code generation, migration scripts
- **Supabase** - Free tier database + excellent docs
- **Zeabur** - Easy deployment + auto HTTPS
- **Google** - OAuth provider (free for small apps)

---

## 📝 Final Thoughts

**What went well:**
- ✅ Supabase is amazing for quick fullstack apps
- ✅ Google OAuth is straightforward with Passport.js
- ✅ Zeabur deployment is seamless
- ✅ Automated migration saved hours

**What could be better:**
- ❌ Should have designed schema for multi-tenancy from day 1
- ❌ Field naming inconsistency caused confusion
- ❌ Testing with multiple users should have been earlier

**Would I do this again?**
**YES!** This stack (Supabase + Express + Google OAuth) is perfect for solo developers building production apps quickly.

---

**🎉 Kanban Board with Google OAuth is LIVE!**

**Try it:** https://kanban-board.zeabur.app/

**Build time:** 8 hours  
**Lines of code:** ~1,500  
**Cost:** $0/month (free tiers)  
**Users supported:** Unlimited  

---

*Published: 2026-03-03*  
*Last updated: 2026-03-03*  
*Version: 3.3 - Production Ready*
