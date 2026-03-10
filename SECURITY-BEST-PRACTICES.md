# 🔐 Security Best Practices

## ⚠️ NEVER Commit to Git

- ❌ API keys (`sk-...`, `pk-...`)
- ❌ `.env` files
- ❌ Memory files (may contain secrets)
- ❌ Passwords or tokens
- ❌ Database URLs with credentials

## ✅ Always Use

- ✅ Environment variables (`.env` - gitignored)
- ✅ Password managers (1Password, Bitwarden)
- ✅ GitHub Secrets for CI/CD

## If You Expose a Secret

1. **Rotate immediately** - Generate new key, revoke old
2. **Remove from git** - Use BFG or git filter-branch
3. **Check exposure** - Search GitHub for your key

## Gitignore Rules

```
# NEVER commit
.env
memory/
*.log
*.db
```

---
**Incident:** 2026-03-10 - GitHub blocked push due to API keys in memory files  
**Action:** Removed memory/ from git, added to .gitignore
