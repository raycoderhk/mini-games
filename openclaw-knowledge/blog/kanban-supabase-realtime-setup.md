# 🚀 Building a Realtime Kanban Board with Supabase + Zeabur

*Published: 2026-02-27 | Tags: #supabase #zeabur #kanban #realtime #nodejs*

---

## 📋 Overview

We recently migrated our Kanban Board from a **static JSON file** to a **realtime database-powered application** using Supabase and Zeabur. This post documents the complete setup process and the troubleshooting journey that got us there.

### Before: Static Architecture
```
Git Push → Zeabur Build (1-2 min) → UI Updates
```
**Problem:** Every change required a git push and 1-2 minute rebuild delay.

### After: Realtime Architecture
```
API Call → Supabase → All connected clients update instantly! ⚡
```
**Result:** Multiple users see changes in real-time, no manual refresh needed.

---

## 🛠️ Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **Database** | Supabase (PostgreSQL) | Free tier, realtime subscriptions, easy setup |
| **Backend** | Node.js + Express | Simple REST API, lightweight |
| **Frontend** | Vanilla JS + Supabase Client | No build step, realtime subscriptions |
| **Deployment** | Zeabur | Auto-deploy from GitHub, free tier |
| **Hosting** | Zeabur Web Service | Global CDN, HTTPS included |

---

## 📁 Project Structure

```
kanban-zeabur/
├── server.js                 # Express API server
├── public/
│   └── index.html            # Frontend UI + Supabase client
├── package.json              # Dependencies
├── supabase-schema.sql       # Database schema
├── .env.example              # Environment template
└── README.md                 # Setup guide
```

---

## 🗄️ Step 1: Supabase Database Setup

### 1.1 Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click **"New Project"**
3. Fill in:
   - **Name:** `kanban-board`
   - **Database Password:** (save this securely!)
   - **Region:** Choose closest to your users

### 1.2 Create Database Schema

Navigate to **SQL Editor** → **New Query** and run:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create boards table
CREATE TABLE IF NOT EXISTS boards (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT NOT NULL DEFAULT 'Main Board',
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create columns table
CREATE TABLE IF NOT EXISTS columns (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  board_id UUID REFERENCES boards(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  "order" INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(board_id, name)
);

-- Create projects table
CREATE TABLE IF NOT EXISTS projects (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  board_id UUID REFERENCES boards(id) ON DELETE CASCADE,
  column_id UUID REFERENCES columns(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL,
  priority TEXT DEFAULT 'medium',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  tags TEXT[],
  notes TEXT[]
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_projects_board_id ON projects(board_id);
CREATE INDEX IF NOT EXISTS idx_projects_column_id ON projects(column_id);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);

-- Enable Row Level Security (RLS)
ALTER TABLE boards ENABLE ROW LEVEL SECURITY;
ALTER TABLE columns ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Create policies (allow all for personal use)
CREATE POLICY "Allow all operations on boards" ON boards
  FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations on columns" ON columns
  FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations on projects" ON projects
  FOR ALL USING (true) WITH CHECK (true);

-- Insert default data
INSERT INTO boards (name, description) VALUES 
  ('Main Board', 'OpenClaw Kanban Board');

-- Enable realtime for all tables
ALTER PUBLICATION supabase_realtime ADD TABLE boards;
ALTER PUBLICATION supabase_realtime ADD TABLE columns;
ALTER PUBLICATION supabase_realtime ADD TABLE projects;
```

### 1.3 Get API Credentials

Go to **Settings** → **API** and copy:

- **Project URL:** `https://[PROJECT_ID].supabase.co`
- **anon/public key:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

⚠️ **Security Note:** The `anon` key is safe to use in frontend code. It's restricted by RLS policies. Never expose your `service_role` key!

---

## 🚀 Step 2: Zeabur Deployment

### 2.1 Push Code to GitHub

```bash
cd kanban-zeabur
git init
git add .
git commit -m "Initial commit: Kanban board with Supabase"
git remote add origin https://github.com/YOUR_USERNAME/kanban-board.git
git push -u origin main
```

### 2.2 Create Zeabur Service

1. Go to [zeabur.com](https://zeabur.com)
2. Click **"New Service"**
3. Select your GitHub repository
4. Choose the `kanban-zeabur` folder (if monorepo)

### 2.3 Add Environment Variables

**⚠️ CRITICAL:** Add each variable **separately** in Zeabur's UI!

| Variable Name | Value | Notes |
|---------------|-------|-------|
| `SUPABASE_URL` | `https://[PROJECT_ID].supabase.co` | No quotes, no trailing slash |
| `SUPABASE_ANON_KEY` | `eyJhbGci...` | Full JWT token, no quotes |
| `PORT` | `8080` | Zeabur default |

**Common Mistake:** Don't paste all variables as one line like a `.env` file. Each variable needs its own row in Zeabur's Variables tab.

**❌ Wrong:**
```
SUPABASE_URL=xxx SUPABASE_ANON_KEY=yyy PORT=8080
```

**✅ Correct:**
```
[SUPABASE_URL]      [https://xxx.supabase.co]
[SUPABASE_ANON_KEY] [eyJhbGciOiJIUzI1NiIs...]
[PORT]              [8080]
```

### 2.4 Auto-Deploy

Zeabur automatically deploys when:
- You push to GitHub
- You add/change environment variables
- You manually trigger redeploy

Wait ~60-90 seconds for deployment to complete.

---

## 🔧 Troubleshooting Journey

Here are the issues we encountered and how we fixed them:

### Issue 1: Missing Environment Variables

**Symptom:**
```
❌ Missing SUPABASE_URL or SUPABASE_ANON_KEY environment variables
error Command failed with exit code 1.
```

**Cause:** Environment variables were added to the wrong Zeabur service (OpenClaw instead of kanban-board).

**Fix:** Each Zeabur service has isolated environment variables. Make sure you're adding them to the correct service.

---

### Issue 2: Malformed Supabase URL

**Symptom:**
```
Error: Invalid supabaseUrl: Provided URL is malformed.
at validateSupabaseUrl (/src/node_modules/@supabase/supabase-js/dist/index.cjs:151:9)
```

**Possible Causes:**

1. **Quotes in value:** `"https://..."` instead of `https://...`
2. **Trailing spaces:** `https://... ` 
3. **Trailing slash:** `https://.../`
4. **Combined variables:** All env vars pasted as one string

**Debug Code Added:**
```javascript
// Log all environment variables
console.log('🔍 Environment variables:');
Object.keys(process.env).forEach(key => {
  if (key.includes('SUPABASE')) {
    const val = process.env[key];
    console.log(`  ${key}: "${val}" (length: ${val?.length})`);
  }
});

// Clean and validate
const supabaseUrl = process.env.SUPABASE_URL
  ?.trim()
  ?.replace(/^["']|["']$/g, '')
  ?.replace(/['"]+/g, '');
```

**Fix:** Delete and re-add variables with exact values (no quotes, no extra characters).

---

### Issue 3: All Variables Combined Into One

**Symptom (from logs):**
```
SUPABASE_URL: "https://xxx.supabase.co SUPABASE_ANON_KEY=eyJ... PORT=8080" (length: 108)
```

**Cause:** All three variables were pasted into a single variable field in Zeabur's UI.

**Fix:** 
1. Delete the combined variable
2. Create three separate variables, one per row
3. Zeabur will auto-redeploy

---

### Issue 4: Tables Don't Exist

**Symptom:**
```
Could not find the table 'public.boards' in the schema cache
```

**Cause:** SQL schema wasn't run in Supabase SQL Editor.

**Fix:** Run the `supabase-schema.sql` script in Supabase Dashboard → SQL Editor.

---

## 📡 Realtime Subscriptions

The magic of Supabase is realtime subscriptions. Here's how we implemented it:

### Frontend Code (index.html)

```javascript
// Initialize Supabase client
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Subscribe to realtime changes
supabase
  .channel('kanban-changes')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'projects'
    },
    (payload) => {
      console.log('🔄 Realtime update:', payload);
      loadBoard(); // Reload board on any change
    }
  )
  .subscribe();
```

**How it works:**
1. Client connects to Supabase Realtime WebSocket
2. Subscribes to changes on the `projects` table
3. Any INSERT, UPDATE, or DELETE triggers the callback
4. UI automatically refreshes with new data

**Benefits:**
- ✅ No polling needed
- ✅ Instant sync across all connected clients
- ✅ Works with multiple users collaborating

---

## 🎯 API Endpoints

Our Express server provides these REST endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/board` | Get full board data |
| `POST` | `/api/projects` | Create new project |
| `PUT` | `/api/projects/:id` | Update project |
| `DELETE` | `/api/projects/:id` | Delete project |
| `GET` | `/health` | Health check |

### Example: Create Project

```bash
curl -X POST https://your-app.zeabur.app/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Feature",
    "description": "Implement realtime sync",
    "status": "todo",
    "priority": "high",
    "tags": ["feature", "realtime"]
  }'
```

---

## 🔐 Security Considerations

### Current Setup (Personal Use)

For personal projects, we use permissive RLS policies:

```sql
CREATE POLICY "Allow all operations on projects" ON projects
  FOR ALL USING (true) WITH CHECK (true);
```

### Production Setup (Multi-User)

For production, implement proper authentication:

```sql
-- Only allow authenticated users to read/write their own data
CREATE POLICY "Users can view own projects" ON projects
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own projects" ON projects
  FOR INSERT WITH CHECK (auth.uid() = user_id);
```

Then use Supabase Auth in your frontend:

```javascript
const { user } = await supabase.auth.getUser();
```

---

## 📊 Performance Tips

1. **Use Indexes:** We added indexes on `board_id`, `column_id`, and `status` for fast lookups.

2. **Limit Realtime Scope:** Only subscribe to tables you need:
   ```javascript
   supabase.channel('kanban-changes').on('postgres_changes', {
     table: 'projects' // Only projects, not all tables
   })
   ```

3. **Debounce UI Updates:** If changes are frequent, debounce the reload:
   ```javascript
   const debouncedReload = debounce(loadBoard, 500);
   ```

---

## 🎉 Results

### Before Migration
- ❌ Manual git push for every change
- ❌ 1-2 minute deployment delay
- ❌ No collaboration support
- ❌ Static data snapshot

### After Migration
- ✅ Instant updates via API
- ✅ Realtime sync across all clients
- ✅ Multi-user collaboration ready
- ✅ Persistent data with full history

---

## 📚 Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Realtime](https://supabase.com/docs/guides/realtime)
- [Zeabur Documentation](https://zeabur.com/docs)
- [Express.js Documentation](https://expressjs.com/)
- [GitHub Repository](https://github.com/raycoderhk/kanban-board)

---

## 🤝 Lessons Learned

1. **Environment Variables Matter:** Zeabur (and most platforms) require each variable separately. Don't paste `.env` file content as one value.

2. **Debug Logging is Essential:** Adding detailed console logs helped us identify that all variables were combined into one.

3. **Test Before Deploy:** Run locally first with a `.env` file to catch issues early.

4. **RLS is Powerful:** Supabase Row Level Security lets you enforce auth at the database level.

5. **Realtime is Game-Changing:** Once you experience instant sync, it's hard to go back to polling.

---

*Have questions? Drop them in #general or reach out on GitHub!*

**Next Post:** Building a Multi-Agent System with OpenClaw 🤖
