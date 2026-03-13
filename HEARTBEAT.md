# HEARTBEAT.md

Check for pending notifications, cron job results, and system events.
If nothing needs attention, reply HEARTBEAT_OK.

## Sleep Time Management
**睡眠時間**: 23:00-08:00 HKT (15:00-00:00 UTC)
**睡眠期間**: 減少通知
**例外**: 緊急提醒(<2 小時)、系統錯誤、用戶請求
**恢復**: 08:00 HKT 恢復正常通知

## 即將到來的事件
**今日 (3 月 12 日 星期四)** ⭐
• 19:00 HKT - [Family] 晚餐 @ TST
  - 朋友：Poke / Vincent / Sam

**3 月 13 日 (星期五)**
• 11:00-13:00 HKT - [Raymond] 匹克球 @ Pickleland
• ~13:00 HKT - [Raymond] 午餐 - 匹克球朋友 (after pickleball)

**3 月 14 日 (星期六)** ✅ 已報名成功
• [Family] 伊利沙伯中學 PTA 新春親子旅行 (已中籤)
  - 集合：08:45 (待定地點)
  - 解散：16:30
  - 團費：$90/人 (已資助)
  - 行程：火龍果農莊 → 韓式泡菜工作坊 → 流浮山鮑魚海鮮午宴 → 海味街 → 錦田壁畫村
  - 聯絡：2380 9621
• 18:30 HKT - [Family] 同鄉會晚宴 @North Point (Tentative)

**3 月 15 日 (星期日)**
• [Son] 兒子生日 🎂
• [Family] 慶祝活動: board game

**3 月 17 日 (星期二)** 💕
• [Family] 結婚周年紀念日 (深圳)
  - 11:00 深圳灣文化廣場展覽
  - 食 + 按摩
• [Family] 🏛️ 深圳灣文化廣場展覽 (Anniversary) @ 11:00
  - 📍 深圳市南山區科苑南路 2516 號
  - 🚇 地鐵 13 號線「人才公園站」B1 出口
  - 🖼️ 必睇：《我心歸處》+《匠作中國》+《一個世紀的椅子》

**3 月 26 日 (星期四)** 📚
• 08:15-09:00 [Daughter UT] 中文
• 09:45-10:15 [Daughter UT] CES

**3 月 27 日 (星期五)** 📚
• 08:15-09:00 [Daughter UT] 英文
• 09:45-10:15 [Daughter UT] 地理

**3 月 30 日 (星期一)** 📚
• 08:15-09:00 [Daughter UT] 數學
• 09:45-10:15 [Daughter UT] 歷史

**3 月 31 日 (星期二)** 📚
• 08:15-09:00 [Daughter UT] 科學
• 09:45-10:15 [Daughter UT] 中國歷史

**已完成 (Past Events):**
• Hugging Face Token 申請
• 營養師 App 配置 + 測試成功
• 匹克球 (Pickledise) - 3/6
• 家庭晚餐 - 3/6
• 兒子學校家長日 - 3/7
• 學校旅行 (科大及鹽田梓) - 3/8
• Maxim's 現金券 $250 x 2 - ✅ 已使用
• 匹克球 (Pulley) - 3/10

## 待辦事項
**需確認事項**
1. 3 月 13 日午餐 with 匹克球朋友 - 確認地點
2. 3 月 14 日同鄉會晚宴 - 確認 (Tentative 18:30 @North Point)
3. Lunch with Chris - Reschedule to next week

**🔴 今日待辦 (3 月 12 日)**
4. ⚠️ **預約深圳灣文化廣場** - 微信小程式「深圳灣文化廣場 DBAY」
   - 日期：3 月 17 日 (星期二) 11:00 時段
   - 人數：2 人 (夫婦)
   - 截止：今日內完成預約

**✅ 已完成**
• Hugging Face Token 申請 - ✅ Done (3 月 1 日)
• 營養師 App 配置 - ✅ Done (proj-020, 測試成功!)
• 晨報系統升級 (web_fetch) - ✅ Done (3 月 1 日)
• Brave Search API Key - ⏳ Optional (web_fetch 已 work)

## 通知偏好
**Kanban Updates**
• 每當 Kanban Board 有更新時，在此 Discord Channel (#kanban-updates) 通知用戶
• 包括：新項目、狀態變更、項目完成

## Heartbeat Tasks

### Google Calendar Sync (每次 Heartbeat 檢查)
**目標:** 自動同步 HEARTBEAT.md 事件到 Google Calendar  
**頻率:** 每次 Heartbeat (約 30 分鐘)  
**位置:** `skills/google-calendar/sync_calendar.py`

**檢查項目:**
1. 讀取 HEARTBEAT.md 即將到來的事件
2. 同步到 Google Calendar (避免重複)
3. 用戶可在 iPhone Google Calendar App 查看

**設置狀態:**
- [ ] 安裝依賴：`pip3 install -r requirements.txt`
- [ ] OAuth 認證：`python3 auth.py`
- [ ] 測試同步：`python3 sync_calendar.py`
- [ ] 啟用自動同步

---

### Daily OpenClaw Community Engagement (每日檢查)
**目標：** 每日參與 OpenClaw Discord 社區
**檢查項目：**
1. 是否已登入 Discord: https://discord.com/invite/clawd
2. 分享今日進度/心得（#general 或 #showcase 頻道）
3. 睇下有無新問題可以幫手解答
4. 檢查 ClawHub 有新 skills 未：https://clawhub.ai
5. 如果有問題，開 thread 問（唔好自己困死）

**今日可以分享嘅話題：**
- [ ] 新安裝咗邊個 skill？
- [ ] 整咗咩新項目？（Kanban/Mission Control/Nutritionist App）
- [ ] 遇到咩問題需要幫手？
- [ ] 有無咩 tips 可以分享畀其他用戶？

**注意：** 睡眠時間 (23:00-08:00 HKT) 唔好打擾社區

### Email Monitoring (每 30 分鐘檢查 - 日間時段)
**位置:** Gmail (raycoderhk.openclaw@gmail.com)  
**檢查頻率:** 每 30 分鐘 (日間 08:00-23:00 HKT)  
**睡眠時段:** 23:00-08:00 HKT (只記錄，不通知，除非緊急)  
**檢查項目:**
1. 新未讀電郵數量
2. 識別緊急/重要電郵 (安全警告、付款通知、活動邀請等)
3. 分析並總結新電郵內容
4. 如有行動項目，自動加入 Kanban Board
5. 發送通知到 #email Discord 頻道

**通知規則:**
- 🔴 **URGENT (紅色)** - 安全警告、API 洩露、賬戶風險 → 立即通知 + 加入 Kanban (urgent priority)
- 🟠 **HIGH (橙色)** - 付款通知、賬單、<48 小時活動 → 通知 + 加入 Kanban (high priority)
- 🟡 **MEDIUM (黃色)** - 一般查詢、會議邀請 → 通知 + 可選加入 Kanban
- 🟢 **LOW (綠色)** - Newsletter、推廣、收據 → 只記錄，不加入 Kanban
- 😴 **睡眠時段** - 除非 URGENT，否則累積到 08:00 HKT 一次過通知

**Discord 通知格式:**
```
## 📬 Email Summary - [時間]

**New Emails:** X unread

### 🔴 URGENT (需立即處理)
- [Email Subject](link) - Brief description
  **Action:** [Kanban proj-XXX created]

### 🟠 HIGH Priority
- [Email Subject](link)

### 🟡 Normal
- [Email Subject](link)

---
**Next Check:** [時間]
```

**Kanban 自動創建:**
- 檢測到 action items → 自動創建 Kanban task
- 根據郵件類型設置 priority (urgent/high/medium)
- 在 notes 中記錄郵件 ID 和內容摘要
- 標籤：`email`, `auto-added`, `[類型]`

---

### Kanban Board Monitoring (每次 Heartbeat 檢查)
**位置:** `workspace/kanban-board.json`
**檢查項目:**
1. 讀取 `kanban-board.json` 的 `meta.updated` 時間戳
2. 與上次檢查的時間比較 (`memory/kanban-last-checked.json`)
3. 如果有更新:
   - 比較項目數量變化
   - 識別新項目、狀態變更、完成的項目
   - 發送更新通知到 #kanban-updates Discord 頻道
   - 更新 `memory/kanban-last-checked.json`

**通知格式範例:**
```
## 📊 Kanban Board Updated

**Changes detected:**
- ✅ New project completed: [Project Name]
- 🔄 Status change: [Project] (todo → in_progress)
- ➕ New project added: [Project Name]

**Current Stats:**
- Total: X projects
- In Progress: Y
- Done: Z
```

**不通知的情況:**
- 沒有更新 (meta.updated 未變化)
- 睡眠時間 (23:00-08:00 HKT)，除非緊急

### Memory State File
**位置:** `memory/kanban-last-checked.json`
**格式:**
```json
{
  "lastChecked": "2026-03-01T14:00:00Z",
  "lastUpdated": "2026-03-01T09:30:00Z",
  "projectCount": 19,
  "lastChange": "proj-018 status changed to in_progress"
}
```

---

### 📊 API Response Time Monitoring (24 小時自動測試)
**目標:** 自動記錄 Aliyun Qwen API 唔同時段嘅響應速度  
**頻率:** 每小時一次 (24 小時共 24 次測試)  
**位置:** `memory/api-response-test.md`  
**匯報:** 每次測試後即時通知用戶

**測試時間表 (HKT):**
| 測試 # | 時間 | 時段 |
|--------|------|------|
| 1 | 08:00 | 清晨 |
| 2 | 09:00 | 上午 |
| 3 | 10:00 | 上午 |
| 4 | 11:00 | 上午 |
| 5 | 12:00 | 中午 |
| 6 | 13:00 | 下午 |
| 7 | 14:00 | 下午 |
| 8 | 15:00 | 下午 |
| 9 | 16:00 | 傍晚 |
| 10 | 17:00 | 傍晚 |
| 11 | 18:00 | 晚間峰值開始 ⚠️ |
| 12 | 19:00 | 晚間峰值 ⚠️ |
| 13 | 20:00 | 晚間峰值高峰 ⚠️ |
| 14 | 21:00 | 晚間 ⚠️ |
| 15 | 22:00 | 深夜 |
| 16 | 23:00 | 深夜 |
| 17 | 00:00 | 午夜 |
| 18 | 01:00 | 凌晨 |
| 19 | 02:00 | 凌晨 |
| 20 | 03:00 | 凌晨 |
| 21 | 04:00 | 凌晨 |
| 22 | 05:00 | 清晨 |
| 23 | 06:00 | 清晨 |
| 24 | 07:00+1 | 清晨 +1 |

**測試方法:**
1. 運行 `session_status` 命令
2. 記錄響應時間 (秒)
3. 記錄到 `memory/api-response-test.md`
4. 標記時段 (快速/正常/慢)

**記錄格式:**
```markdown
### 📊 Test #X - [時段] (HH:MM HKT, March DD)
| Metric | Value |
|--------|-------|
| **Time** | YYYY-MM-DD HH:MM HKT |
| **Response Time** | X.X seconds |
| **Status** | ✅ Success / ❌ Failed |
| **Notes** | 快速 / 正常 / 慢 |
```

**報告時間:**
- **每日 08:00 HKT** - 發送 24 小時總結報告
- **發現異常 (>10 秒)** - 即時通知

**狀態追蹤:**
```json
// memory/api-test-state.json
{
  "lastTest": "2026-03-13T07:50:00+08:00",
  "nextTest": "2026-03-13T10:00:00+08:00",
  "testCount": 1,
  "avgResponseTime": 2.5,
  "slowestPeriod": null
}
```
