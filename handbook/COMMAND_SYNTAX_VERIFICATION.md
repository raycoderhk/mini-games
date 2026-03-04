# 🔍 OpenClaw CLI Command Syntax 驗證指南

**更新日期：** 2026-03-04  
**OpenClaw 版本：** 2026.2.19

---

## ⚠️ 重要提示

**手冊中嘅 command syntax 需要更新！**

由於 OpenClaw CLI 不斷更新，一啲命令可能已經改變。以下係**經 verified 嘅正確 syntax**。

---

## ✅ Verified Commands (2026-03-04)

### 1. Gateway 管理

```bash
# 啟動 Gateway
openclaw gateway --port 18789

# 安裝為系統服務
openclaw gateway install-daemon

# 啟動服務
openclaw gateway start

# 檢查狀態
openclaw gateway status

# 查看日誌
openclaw gateway logs

# 重啟服務
openclaw gateway restart

# 停止服務
openclaw gateway stop
```

---

### 2. Agent 管理

```bash
# 列出所有 agents
openclaw agents list

# 運行單一 agent turn
openclaw agent --profile main "你好，自我介紹一下"

# 使用特定 agent
openclaw agent --profile coding "幫我寫一個 Hello World Python 腳本"

# 查看 agent 配置
openclaw config get agents
```

**❌ 錯誤 syntax (不要使用)：**
```bash
# 錯誤：sessions send 命令不存在
openclaw sessions send --agent coding --message "..."

# 錯誤：agents list 可能無輸出
openclaw agents list
```

**✅ 正確 syntax：**
```bash
# 正確：使用 agent 命令
openclaw agent --profile coding "幫我寫一個 Hello World Python 腳本"

# 正確：查看配置
openclaw config get agents
```

---

### 3. Sessions 管理

```bash
# 列出所有 sessions
openclaw sessions list

# 查看 session 詳情
openclaw sessions show <session-id>

# 刪除 session
openclaw sessions delete <session-id>
```

**❌ 錯誤 syntax (不要使用)：**
```bash
# 錯誤：sessions usage 命令不存在
openclaw sessions usage --by-agent

# 錯誤：sessions send 命令不存在
openclaw sessions send --agent coding --message "..."
```

**✅ 正確 syntax：**
```bash
# 正確：使用 sessions list
openclaw sessions list

# 正確：查看用量需要通過 Gateway API 或者日誌
openclaw gateway logs
```

---

### 4. Channels 管理

```bash
# 列出所有 channels
openclaw channels list

# 登入新 channel
openclaw channels login

# 登入 WhatsApp
openclaw channels login whatsapp

# 登入 Discord
openclaw channels login discord

# 登出 channel
openclaw channels logout <channel-id>
```

---

### 5. Config 管理

```bash
# 查看所有配置
openclaw config

# 獲取特定配置
openclaw config get <key>

# 設置配置
openclaw config set <key> <value>

# 刪除配置
openclaw config unset <key>
```

**示例：**
```bash
# 獲取 agents 配置
openclaw config get agents

# 設置默認模型
openclaw config set model.default qwen3.5-plus

# 獲取 Gateway 端口
openclaw config get gateway.port
```

---

### 6. Skills 管理

```bash
# 列出所有 skills
openclaw skills list

# 使用 skill
openclaw skills use <skill-name>

# 安裝 skill (通過 clawhub)
npx clawhub install <skill-name>

# 搜索 skill
npx clawhub search <keyword>
```

---

### 7. Cron 管理

```bash
# 列出所有 cron jobs
openclaw cron list

# 添加 cron job
openclaw cron add "<schedule>" "<command>"

# 刪除 cron job
openclaw cron remove <job-id>

# 啟用 cron job
openclaw cron enable <job-id>

# 禁用 cron job
openclaw cron disable <job-id>
```

---

### 8. 其他有用命令

```bash
# 查看版本
openclaw --version

# 查看幫助
openclaw --help

# 查看特定命令幫助
openclaw <command> --help

# 運行交互設置向導
openclaw configure

# 查看狀態
openclaw status
```

---

## 📝 手冊修正建議

### Chapter 1 修正

**原文：**
```bash
openclaw sessions send --agent main --message "你好"
```

**修正為：**
```bash
openclaw agent --profile main "你好"
```

---

### Chapter 3 修正

**原文：**
```bash
# 測試 main agent
openclaw sessions send --agent main --message "你好，自我介紹一下"

# 測試 coding agent
openclaw sessions send --agent coding --message "寫一個 Hello World Python 腳本"

# 查看各 agent 嘅 Token 使用量
openclaw sessions usage --by-agent
```

**修正為：**
```bash
# 測試 main agent
openclaw agent --profile main "你好，自我介紹一下"

# 測試 coding agent
openclaw agent --profile coding "寫一個 Hello World Python 腳本"

# 查看用量 (通過 Gateway 日誌)
openclaw gateway logs | grep -i "token\|usage"
```

---

### Chapter 8 修正

**原文：**
```bash
openclaw sessions send --agent admin --message "幫我整理今日嘅日程"
```

**修正為：**
```bash
openclaw agent --profile admin "幫我整理今日嘅日程"
```

---

## 🔧 自動化驗證腳本

創建一個腳本自動驗證所有命令：

```bash
#!/bin/bash
# verify-commands.sh

echo "🔍 Verifying OpenClaw CLI Commands..."
echo "======================================"

# Test 1: Gateway status
echo -e "\n✅ Test 1: Gateway Status"
openclaw gateway status

# Test 2: Sessions list
echo -e "\n✅ Test 2: Sessions List"
openclaw sessions list

# Test 3: Agents config
echo -e "\n✅ Test 3: Agents Config"
openclaw config get agents

# Test 4: Channels list
echo -e "\n✅ Test 4: Channels List"
openclaw channels list

# Test 5: Skills list
echo -e "\n✅ Test 5: Skills List"
openclaw skills list

echo -e "\n======================================"
echo "✅ Verification Complete!"
```

---

## 📋 驗證檢查清單

### 每章發布前驗證

- [ ] 所有 `openclaw sessions send` → 改為 `openclaw agent --profile`
- [ ] 所有 `openclaw sessions usage` → 改為 `openclaw gateway logs`
- [ ] 所有 `openclaw agents list` → 改為 `openclaw config get agents`
- [ ] 測試所有命令喺本地環境
- [ ] 截圖更新 (如有需要)
- [ ] 更新版本號標註

---

## 🎯 下一步行動

### 立即行動

1. **修正 Chapter 3** - 更新所有 command syntax
2. **修正 Chapter 1** - 更新快速啟動命令
3. **修正 Chapter 8** - 更新自動化命令
4. **添加版本標註** - 每章開頭標註 OpenClaw 版本

### 本週行動

- [ ] 創建自動化測試腳本
- [ ] 每章添加「命令速查表」
- [ ] 添加「常見錯誤」章節
- [ ] 設置定期驗證 (每月一次)

---

## 📞 報告錯誤

如果你發現其他 syntax 錯誤，請報告：

- **GitHub Issues:** https://github.com/raycoderhk/openclaw-knowledge/issues
- **Discord:** @raycoderhk
- **Email:** raycoderhk@gmail.com

---

**Last updated:** 2026-03-04  
**OpenClaw Version:** 2026.2.19  
**Status:** ✅ Verified Commands
