# 🔐 Supabase RLS Security Fix - Custom JWT Approach (v2.0)

**Document Version:** 2.0  
**Created:** 2026-03-18  
**Author:** Jarvis (OpenClaw Assistant)  
**Review Status:** ✅ Validated by Independent LLM  
**Status:** Ready for Implementation  

---

## 🚨 Why v1.0 Was Flawed

### ❌ Original Approach: `current_setting()` RPC

```sql
-- FLAWED: Connection pooling breaks this
CREATE FUNCTION set_current_user(user_google_id TEXT)
RETURNS void AS $$
    PERFORM set_config('app.current_google_id', user_google_id, true);
$$ LANGUAGE plpgsql;
```

**Problem:** Supabase's connection pooling causes:
- **Transaction-local:** Setting lost after RPC completes → RLS fails
- **Session-local:** Setting persists in connection pool → **DATA LEAK!**

**Verdict:** **CRITICAL SECURITY FLAW** - Do not use!

---

## ✅ Correct Approach: Custom JWT

### Overview

```
┌─────────────────┐
│   User Login    │
│  (Google OAuth) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Backend Server │
│  (Passport.js/  │
│   NextAuth)     │
└────────┬────────┘
         │
         │ 1. Extract google_id from OAuth profile
         ▼
┌─────────────────┐
│   Mint Custom   │
│      JWT        │
│ (HS256 signed)  │
└────────┬────────┘
         │
         │ 2. Return JWT to frontend
         ▼
┌─────────────────┐
│    Frontend     │
│   (Browser)     │
└────────┬────────┘
         │
         │ 3. Initialize Supabase client with JWT
         ▼
┌─────────────────┐
│  Supabase API   │
│  (PostgREST)    │
└────────┬────────┘
         │
         │ 4. RLS evaluates auth.jwt() ->> 'sub'
         ▼
┌─────────────────┐
│  User sees ONLY │
│   their data    │
└─────────────────┘
```

---

## 🛠️ Implementation Plan

### Step 1: Get Supabase JWT_SECRET

**Location:** Supabase Dashboard → Project Settings → API

```bash
# You need this from Supabase Dashboard:
SUPABASE_JWT_SECRET=your-jwt-secret-here

# IMPORTANT: This is DIFFERENT from SUPABASE_ANON_KEY
# ANON_KEY: For public operations
# JWT_SECRET: For signing custom tokens
```

**Action Required:** 
- [ ] Login to Supabase Dashboard
- [ ] Go to: https://app.supabase.com/project/hxrgvuzujvagzlaevwtk/settings/api
- [ ] Copy "JWT Secret" (service role key)
- [ ] Add to all server environments (see Step 4)

---

### Step 2: Install JWT Signing Library

#### Kanban Board (Express)

```bash
cd kanban-zeabur
npm install jose
```

#### Mission Control (Next.js)

```bash
cd mission-control
npm install jose
```

**Why `jose`?** 
- Lightweight JWT library
- Works in Node.js and Edge runtimes
- Recommended by Supabase docs

---

### Step 3: Create JWT Minting Function

#### Kanban Board (Passport.js)

**File:** `kanban-zeabur/lib/jwt.js`

```javascript
import { SignJWT } from 'jose';

const JWT_SECRET = new TextEncoder().encode(process.env.SUPABASE_JWT_SECRET);

/**
 * Mint custom JWT for Supabase RLS
 * @param {string} googleId - User's Google ID from OAuth
 * @returns {Promise<string>} JWT token
 */
export async function mintSupabaseJwt(googleId) {
    const jwt = await new SignJWT({ 
        // Custom claims
        google_id: googleId 
    })
        .setProtectedHeader({ alg: 'HS256' })
        .setSubject(googleId)
        .setIssuedAt()
        .setExpirationTime('24h') // Token expires in 24 hours
        .sign(JWT_SECRET);
    
    return jwt;
}
```

#### Mission Control (NextAuth)

**File:** `mission-control/lib/supabase-jwt.js`

```typescript
import { SignJWT } from 'jose';

const JWT_SECRET = new TextEncoder().encode(process.env.SUPABASE_JWT_SECRET!);

export async function mintSupabaseJwt(googleId: string): Promise<string> {
    const jwt = await new SignJWT({ 
        google_id: googleId 
    })
        .setProtectedHeader({ alg: 'HS256' })
        .setSubject(googleId)
        .setIssuedAt()
        .setExpirationTime('24h')
        .sign(JWT_SECRET);
    
    return jwt;
}
```

---

### Step 4: Add JWT_SECRET to Environment

#### Kanban Board (Zeabur)

**File:** `kanban-zeabur/.env` (local)
```env
SUPABASE_URL=https://hxrgvuzujvagzlaevwtk.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_JWT_SECRET=<get-from-supabase-dashboard>
```

**Zeabur Dashboard:**
1. Go to: https://zeabur.com/dashboard
2. Select: kanban-board
3. Settings → Environment Variables
4. Add: `SUPABASE_JWT_SECRET`
5. Redeploy

---

#### Mission Control (Zeabur)

**File:** `mission-control/.env.local` (local)
```env
SUPABASE_URL=https://hxrgvuzujvagzlaevwtk.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_JWT_SECRET=<get-from-supabase-dashboard>
```

**Zeabur Dashboard:**
1. Go to: https://zeabur.com/dashboard
2. Select: mission-control
3. Settings → Environment Variables
4. Add: `SUPABASE_JWT_SECRET`
5. Redeploy

---

### Step 5: Update OAuth Flow

#### Kanban Board (Passport.js)

**File:** `kanban-zeabur/server.js`

```javascript
import { mintSupabaseJwt } from './lib/jwt.js';

passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: process.env.GOOGLE_CALLBACK_URL
}, async (accessToken, refreshToken, profile, done) => {
    try {
        // 1. Get or create user in database
        const user = await getOrCreateUser(profile);
        
        // 2. Mint custom JWT for Supabase RLS
        const supabaseJwt = await mintSupabaseJwt(profile.id);
        
        // 3. Attach JWT to user session
        user.supabaseJwt = supabaseJwt;
        
        return done(null, user);
    } catch (error) {
        return done(error);
    }
}));

// Session serialization
passport.serializeUser((user, done) => {
    done(null, {
        id: user.id,
        supabaseJwt: user.supabaseJwt // Include JWT in session
    });
});
```

**Update API Routes:**

```javascript
// BEFORE (insecure - manual filtering)
app.get('/api/kanban', ensureAuthenticated, async (req, res) => {
    const { data: projects, error } = await supabase
        .from('projects')
        .select('*')
        .eq('user_id', req.user.id); // Manual filtering
    
    res.json({ projects });
});

// AFTER (secure - RLS handles filtering)
app.get('/api/kanban', ensureAuthenticated, async (req, res) => {
    // Create Supabase client with user's JWT
    const supabase = createClient(
        process.env.SUPABASE_URL,
        process.env.SUPABASE_ANON_KEY,
        {
            global: {
                headers: {
                    Authorization: `Bearer ${req.user.supabaseJwt}`
                }
            }
        }
    );
    
    // RLS automatically filters to user's data
    const { data: projects, error } = await supabase
        .from('projects')
        .select('*');
    
    if (error) throw error;
    res.json({ projects });
});
```

---

#### Mission Control (NextAuth)

**File:** `mission-control/app/api/auth/[...nextauth]/route.ts`

```typescript
import { mintSupabaseJwt } from '@/lib/supabase-jwt';

export const authOptions = {
    providers: [GoogleProvider({
        clientId: process.env.GOOGLE_CLIENT_ID!,
        clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    })],
    callbacks: {
        async signIn({ user, account, profile }) {
            if (account?.provider === 'google') {
                // 1. Mint custom JWT for Supabase RLS
                const supabaseJwt = await mintSupabaseJwt(profile.sub!);
                
                // 2. Save to database
                const { data, error } = await supabase
                    .from('mc_users')
                    .upsert({
                        google_id: profile.sub,
                        email: user.email,
                        name: user.name,
                        avatar_url: user.image,
                        updated_at: new Date().toISOString()
                    }, {
                        onConflict: 'google_id'
                    });
                
                if (error) {
                    console.error('User creation failed:', error);
                    return false;
                }
                
                // 3. Store JWT in user record for later use
                // (or pass via session token)
            }
            return true;
        },
        async session({ session, token }) {
            // Store JWT in session for API calls
            if (token.supabaseJwt) {
                session.supabaseJwt = token.supabaseJwt;
            }
            return session;
        },
        async jwt({ token, user, account, profile }) {
            if (account?.provider === 'google' && profile?.sub) {
                // Mint JWT on sign-in
                token.supabaseJwt = await mintSupabaseJwt(profile.sub);
            }
            return token;
        }
    }
}
```

**Update API Routes:**

```typescript
// app/api/events/route.ts
import { auth } from '@/app/api/auth/[...nextauth]/route';
import { createClient } from '@supabase/supabase-js';

export async function GET(request: Request) {
    const session = await auth();
    
    if (!session?.supabaseJwt) {
        return Response.json({ error: 'Unauthorized' }, { status: 401 });
    }
    
    // Create Supabase client with user's JWT
    const supabase = createClient(
        process.env.SUPABASE_URL!,
        process.env.SUPABASE_ANON_KEY!,
        {
            global: {
                headers: {
                    Authorization: `Bearer ${session.supabaseJwt}`
                }
            }
        }
    );
    
    // RLS automatically filters to user's data
    const { data: events, error } = await supabase
        .from('events')
        .select('*');
    
    if (error) {
        return Response.json({ error: error.message }, { status: 500 });
    }
    
    return Response.json({ events });
}
```

---

### Step 6: Update RLS Policies

**File:** `supabase-migration-secure-rls-v2.sql`

```sql
-- ============================================
-- mc_users Table - Secure RLS with auth.jwt()
-- ============================================

-- Drop old insecure policies
DROP POLICY IF EXISTS "Allow anonymous insert" ON mc_users;
DROP POLICY IF EXISTS "Users read own profile" ON mc_users;
DROP POLICY IF EXISTS "Users update own profile" ON mc_users;

-- Enable RLS
ALTER TABLE mc_users ENABLE ROW LEVEL SECURITY;

-- Policy 1: Allow INSERT (for OAuth sign-up)
-- User can only insert with their own google_id (from JWT)
CREATE POLICY "Allow user creation"
    ON mc_users FOR INSERT
    WITH CHECK (
        google_id = auth.jwt() ->> 'sub'
    );

-- Policy 2: Users can SELECT their own profile ONLY
CREATE POLICY "Users read own profile"
    ON mc_users FOR SELECT
    USING (
        google_id = auth.jwt() ->> 'sub'
    );

-- Policy 3: Users can UPDATE their own profile ONLY
CREATE POLICY "Users update own profile"
    ON mc_users FOR UPDATE
    USING (
        google_id = auth.jwt() ->> 'sub'
    )
    WITH CHECK (
        google_id = auth.jwt() ->> 'sub'
    );

-- ============================================
-- tasks Table - Secure RLS with auth.jwt()
-- ============================================

-- Drop old policies
DROP POLICY IF EXISTS "Users can view own tasks" ON tasks;
DROP POLICY IF EXISTS "Users can insert own tasks" ON tasks;
DROP POLICY IF EXISTS "Users can update own tasks" ON tasks;
DROP POLICY IF EXISTS "Users can delete own tasks" ON tasks;

-- Enable RLS
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Policy: Users can SELECT tasks where user_id matches JWT sub
CREATE POLICY "Users view own tasks"
    ON tasks FOR SELECT
    USING (
        user_id::text = auth.jwt() ->> 'sub'
    );

-- Policy: Users can INSERT tasks with their own user_id
CREATE POLICY "Users insert own tasks"
    ON tasks FOR INSERT
    WITH CHECK (
        user_id::text = auth.jwt() ->> 'sub'
    );

-- Policy: Users can UPDATE their own tasks
CREATE POLICY "Users update own tasks"
    ON tasks FOR UPDATE
    USING (
        user_id::text = auth.jwt() ->> 'sub'
    )
    WITH CHECK (
        user_id::text = auth.jwt() ->> 'sub'
    );

-- Policy: Users can DELETE their own tasks
CREATE POLICY "Users delete own tasks"
    ON tasks FOR DELETE
    USING (
        user_id::text = auth.jwt() ->> 'sub'
    );

-- ============================================
-- Apply same pattern to ALL tables
-- ============================================

-- events table
ALTER TABLE events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users view own events"
    ON events FOR SELECT
    USING (user_id::text = auth.jwt() ->> 'sub');

CREATE POLICY "Users insert own events"
    ON events FOR INSERT
    WITH CHECK (user_id::text = auth.jwt() ->> 'sub');

CREATE POLICY "Users update own events"
    ON events FOR UPDATE
    USING (user_id::text = auth.jwt() ->> 'sub')
    WITH CHECK (user_id::text = auth.jwt() ->> 'sub');

CREATE POLICY "Users delete own events"
    ON events FOR DELETE
    USING (user_id::text = auth.jwt() ->> 'sub');

-- Repeat for: settings, goals, friends, etc.
```

---

### Step 7: Testing Checklist

#### Pre-Deployment Tests

```markdown
## JWT Minting
- [ ] `mintSupabaseJwt()` generates valid JWT
- [ ] JWT contains correct `sub` claim (google_id)
- [ ] JWT signed with correct algorithm (HS256)
- [ ] JWT expires after 24 hours

## RLS Policies
- [ ] User can SELECT own data
- [ ] User CANNOT SELECT other user's data
- [ ] User can INSERT with own google_id
- [ ] User CANNOT INSERT with other google_id
- [ ] User can UPDATE own data
- [ ] User CANNOT UPDATE other user's data
- [ ] User can DELETE own data
- [ ] User CANNOT DELETE other user's data

## OAuth Flow
- [ ] Google OAuth login completes successfully
- [ ] JWT minted during OAuth callback
- [ ] JWT stored in session
- [ ] JWT passed to Supabase client
- [ ] User sees their own data after login

## Security Tests
- [ ] User A cannot read User B's data (SQL injection test)
- [ ] User A cannot update User B's data
- [ ] User A cannot delete User B's data
- [ ] Unauthenticated requests blocked
- [ ] Expired JWT rejected
- [ ] Tampered JWT rejected
```

#### Test Scripts

```javascript
// Test JWT minting
import { mintSupabaseJwt } from './lib/jwt.js';

const jwt = await mintSupabaseJwt('test-google-id-123');
console.log('JWT:', jwt);

// Decode and verify
import { jwtVerify } from 'jose';
const { payload } = await jwtVerify(jwt, JWT_SECRET);
console.log('Payload:', payload);
// Should show: { sub: 'test-google-id-123', google_id: 'test-google-id-123' }
```

```sql
-- Test RLS with custom JWT (in Supabase SQL Editor)

-- Set custom JWT header
-- Note: This is for testing only - real JWT comes from client
SELECT set_config('request.jwt.claims', 
    '{"sub": "user-a-google-id"}', 
    true);

-- Test SELECT policy
SELECT * FROM mc_users WHERE google_id = 'user-a-google-id';
-- Should return: 1 row

SELECT * FROM mc_users WHERE google_id = 'user-b-google-id';
-- Should return: 0 rows (blocked by RLS)
```

---

## 📊 Comparison: v1.0 vs v2.0

| Aspect | v1.0 (current_setting) | v2.0 (Custom JWT) |
|--------|----------------------|-------------------|
| **Connection Pooling** | ❌ Breaks | ✅ Works correctly |
| **Data Leak Risk** | 🔴 HIGH | ✅ ZERO |
| **Supabase Support** | ❌ Anti-pattern | ✅ Official pattern |
| **RLS Syntax** | `current_setting()` | `auth.jwt() ->> 'sub'` |
| **Token Persistence** | ❌ Lost after RPC | ✅ Persists in client |
| **Security** | ❌ Vulnerable | ✅ Cryptographically secure |
| **Complexity** | 🟡 Medium | 🟢 Low |
| **Maintenance** | ❌ Custom solution | ✅ Standard library |

---

## 📁 Files to Create/Modify

| File | Application | Action | Effort |
|------|-------------|--------|--------|
| `lib/jwt.js` | Kanban Board | Create | 15 min |
| `lib/supabase-jwt.ts` | Mission Control | Create | 15 min |
| `server.js` | Kanban Board | Update OAuth + API | 30 min |
| `app/api/auth/[...nextauth]/route.ts` | Mission Control | Update NextAuth | 30 min |
| `app/api/*/route.ts` | Mission Control | Update API routes | 30 min |
| `supabase-migration-secure-rls-v2.sql` | All | Run in Supabase | 15 min |
| `.env` files | All | Add JWT_SECRET | 10 min |
| Zeabur env vars | All | Add JWT_SECRET | 10 min |

**Total Estimated Effort:** 2-3 hours

---

## 🔑 Required Environment Variables

Add to ALL server environments:

```env
# Get from: https://app.supabase.com/project/hxrgvuzujvagzlaevwtk/settings/api
SUPABASE_JWT_SECRET=<your-jwt-secret-here>

# IMPORTANT: Keep this SECRET!
# Do NOT commit to Git
# Do NOT share publicly
```

---

## ⚠️ Security Notes

### JWT_SECRET Handling

```bash
# ✅ DO: Store in environment variables
export SUPABASE_JWT_SECRET="your-secret"

# ✅ DO: Use secrets management (Zeabur, Vercel, etc.)

# ❌ DON'T: Commit to Git
git add .env  # NO!

# ❌ DON'T: Log or expose
console.log(process.env.SUPABASE_JWT_SECRET)  # NO!

# ❌ DON'T: Share in chat/email
"Hey, here's the JWT secret: abc123..."  # NO!
```

### Token Expiration

- **Default:** 24 hours
- **Recommendation:** Match session duration
- **Refresh:** Mint new JWT on each OAuth refresh

---

## 🎯 Success Criteria

### Functional
- ✅ OAuth login works
- ✅ JWT minted successfully
- ✅ User sees their own data
- ✅ User can create/update/delete their data
- ✅ No 500 errors in logs

### Security
- ✅ Users CANNOT see other users' data
- ✅ Supabase Security Advisor: 0 errors
- ✅ No RLS violations in logs
- ✅ JWT_SECRET not exposed

### Performance
- ✅ JWT minting < 10ms
- ✅ No significant overhead
- ✅ Page load < 2 seconds

---

## 🔄 Rollback Plan

If issues occur:

```sql
-- EMERGENCY: Disable RLS
ALTER TABLE mc_users DISABLE ROW LEVEL SECURITY;
ALTER TABLE tasks DISABLE ROW LEVEL SECURITY;

-- Restore old (insecure) policies
DROP POLICY IF EXISTS "Allow user creation" ON mc_users;
CREATE POLICY "Allow anonymous insert"
    ON mc_users FOR INSERT
    WITH CHECK (true);
```

```bash
# Revert code changes
git revert HEAD
git push origin main
```

---

## 📞 Resources

- [Supabase Third-Party Auth Overview](https://supabase.com/docs/guides/auth/third-party/overview)
- [Custom JWTs with Supabase](https://supabase.com/docs/guides/auth/auth-jwt)
- [jose Library Documentation](https://github.com/panva/jose)
- [NextAuth.js Custom JWT](https://next-auth.js.org/configuration/options#jwt)

---

**Status:** ✅ Ready for Implementation  
**Next Step:** Get JWT_SECRET from Supabase Dashboard → Implement

---

*Last Updated: 2026-03-18*  
*Author: Jarvis (OpenClaw Assistant)*  
*Review Status: Validated by Independent LLM*
