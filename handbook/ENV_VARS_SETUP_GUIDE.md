# OpenClaw 環境變數配置指南

**版本：** 1.0  
**日期：** 2026-03-05  
**安全等級：** ✅ 推薦

---

## 📋 為什麼用 Environment Variables？

### ❌ 直接寫死 Secrets (危險！)
```json
{
  "models": {
    "providers": {
      "aliyun": {
        "apiKey": "sk-xxxxxxxxxxxxx"  // ❌ 危險！
      }
    }
  },
  "channels": {
    "discord": {
      "accounts": {
        "default": {
          "token": "your-discord-bot-token-here"  // ❌ 危險！
        }
      }
    }
  }
}
```

**風險：**
- Git 歷史會永久記錄 secrets
- 分享配置時洩露敏感資料
- 無法在不同環境切換

---

### ✅ 用 Environment Variables (安全！)
```json
{
  "models": {
    "providers": {
      "aliyun": {
        "apiKey": "${ALIYUN_API_KEY}"  // ✅ 安全！
      }
    }
  },
  "channels": {
    "discord": {
      "accounts": {
        "default": {
          "token": "${DISCORD_BOT_TOKEN}"  // ✅ 安全！
        }
      }
    }
  }
}
```

**優勢：**
- Config 文件無敏感資料
- 可以安全分享/commit 到 Git
- 容易切換不同環境 (dev/staging/prod)

---

## 🛠️ 設置步驟

### Step 1: 創建 .env 文件

```bash
# 位置：~/.openclaw/.env
nano ~/.openclaw/.env
```

**內容：**
```bash
# Aliyun (Qwen) API
ALIYUN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# DeepSeek API (如果使用)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# OpenRouter API (如果使用)
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxxxxxx

# Discord Bot Token
DISCORD_BOT_TOKEN=MTQ3NjUwMTI4Nzc0MTk1MjEwMA.xxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxx

# Telegram Bot Token
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Gateway Auth Token
GATEWAY_AUTH_TOKEN=your-gateway-secret-token

# Brave Search API (如果使用)
BRAVE_SEARCH_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
```

---

### Step 2: 修改 openclaw.json

```bash
# 編輯配置文件
nano ~/.openclaw/openclaw.json
```

**替換所有 secrets 為 ${ENV_VAR}：**

```json
{
  "models": {
    "providers": {
      "aliyun": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "${ALIYUN_API_KEY}",
        "api": "openai-completions"
      },
      "deepseek": {
        "baseUrl": "https://api.deepseek.com/v1",
        "apiKey": "${DEEPSEEK_API_KEY}",
        "api": "openai-completions"
      }
    }
  },
  "channels": {
    "discord": {
      "accounts": {
        "default": {
          "token": "${DISCORD_BOT_TOKEN}",
          "groupPolicy": "allowlist",
          "dmPolicy": "allowlist"
        }
      }
    },
    "telegram": {
      "botToken": "${TELEGRAM_BOT_TOKEN}",
      "dmPolicy": "pairing"
    }
  },
  "gateway": {
    "mode": "local",
    "auth": {
      "token": "${GATEWAY_AUTH_TOKEN}"
    }
  }
}
```

---

### Step 3: 創建 .gitignore

```bash
# 位置：~/.openclaw/.gitignore
nano ~/.openclaw/.gitignore
```

**內容：**
```gitignore
# 敏感文件
.env
.env.local
.env.production
*.env

# 備份文件
*.backup.*
*.bak
*.old

# 日誌文件
*.log
logs/

# 臨時文件
tmp/
temp/
*.tmp

# 操作系統文件
.DS_Store
Thumbs.db

# Node.js
node_modules/
npm-debug.log
```

---

### Step 4: 創建 Template (可分享)

```bash
# 創建 template (無實際 secrets)
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.example
```

**編輯 `.example` 文件，添加註釋：**

```json
{
  "_comment": "OpenClaw 配置模板 - 複製此文件為 openclaw.json 並填充環境變數",
  "_version": "1.0",
  "_date": "2026-03-05",
  
  "models": {
    "providers": {
      "aliyun": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "${ALIYUN_API_KEY}",
        "api": "openai-completions",
        "_env_required": "ALIYUN_API_KEY"
      }
    }
  },
  
  "channels": {
    "discord": {
      "accounts": {
        "default": {
          "token": "${DISCORD_BOT_TOKEN}",
          "_env_required": "DISCORD_BOT_TOKEN"
        }
      }
    }
  }
}
```

---

### Step 5: 加載環境變數

**方法 A: 手動加載**
```bash
# 每次啟動前
source ~/.openclaw/.env
openclaw gateway start
```

**方法 B: 自動加載 (推薦)**
```bash
# 編輯 ~/.bashrc 或 ~/.zshrc
echo "source ~/.openclaw/.env" >> ~/.bashrc
source ~/.bashrc
```

**方法 C: 使用 dotenv 工具**
```bash
# 安裝 dotenv-cli
npm install -g dotenv-cli

# 運行 OpenClaw
dotenv -e ~/.openclaw/.env -- openclaw gateway start
```

---

## 📂 最終文件結構

```
~/.openclaw/
├── openclaw.json              # 實際配置 (用 ${ENV_VAR})
├── openclaw.json.example      # Template (可分享)
├── .env                       # Secrets (加入 .gitignore!)
├── .gitignore                 # Git 忽略規則
├── secrets/                   # 可選：額外 secrets 文件
│   └── secrets.json
└── backups/                   # 本地備份
    └── openclaw.json.backup.20260305
```

---

## 🔒 安全檢查清單

### 每次修改後檢查

```bash
# 1. 檢查 .env 是否加入 .gitignore
cat ~/.openclaw/.gitignore | grep ".env"

# 2. 檢查 openclaw.json 有無明文 secrets
grep -E "(sk-|MTQ|Bearer|password)" ~/.openclaw/openclaw.json
# 應該只找到 ${ENV_VAR} 引用

# 3. 檢查 Git 狀態
cd ~/.openclaw
git status
# .env 應該顯示為 untracked (唔應該被 add)

# 4. 測試環境變數是否生效
echo $ALIYUN_API_KEY
# 應該顯示你的 API key (部分)
```

---

## 🚨 緊急情況

### 如果不小心 commit 咗 secrets

```bash
# 1. 立即刪除 Git 歷史中的 secrets
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 2. 強制 push
git push origin main --force

# 3. 更換所有洩露的 secrets
# - 重新生成 API keys
# - 重新生成 Bot tokens
# - 更新 .env 文件

# 4. 通知相關人員 (如果有其他人 access)
```

---

## 💡 最佳實踐

### 1. 本地開發

```bash
# ~/.openclaw/.env (本地)
ALIYUN_API_KEY=sk-dev-xxxxx
DISCORD_BOT_TOKEN=dev-token-xxxxx
```

### 2. 生產環境 (Zeabur VPS)

```bash
# Zeabur Dashboard → Environment Variables
ALIYUN_API_KEY=sk-prod-xxxxx
DISCORD_BOT_TOKEN=prod-token-xxxxx
```

### 3. 團隊分享

```bash
# Git Repo 只包括：
openclaw.json.example    # Template
.gitignore               # 忽略規則
README.md                # 設置說明

# 不包括：
.env                     # Secrets (每個自己設置)
*.backup.*               # 本地備份
```

---

## 📞 故障排除

### 問題：環境變數未生效

```bash
# 檢查 .env 文件路徑
ls -la ~/.openclaw/.env

# 檢查變數名稱是否匹配
cat ~/.openclaw/.env | grep ALIYUN
cat ~/.openclaw/openclaw.json | grep ALIYUN

# 重新加載
source ~/.openclaw/.env
echo $ALIYUN_API_KEY

# 重啟 OpenClaw
openclaw gateway restart
```

### 問題：Git 仍然追蹤 .env

```bash
# 從 Git 移除 (唔刪除文件)
git rm --cached ~/.openclaw/.env

# 確認移除
git status

# Commit
git commit -m "Remove .env from tracking"
```

---

## 📚 相關資源

- [OpenClaw Secrets 文檔](https://docs.openclaw.ai/gateway/secrets)
- [Environment Variables 指南](https://docs.openclaw.ai/help/environment)
- [GitHub Issues #4654](https://github.com/openclaw/openclaw/issues/4654)

---

**Last updated:** 2026-03-05  
**Status:** ✅ Ready to Use
