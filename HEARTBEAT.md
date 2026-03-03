# HEARTBEAT.md

Check for pending notifications, cron job results, and system events.
If nothing needs attention, reply HEARTBEAT_OK.

## Sleep Time Management
**睡眠時間**: 23:00-08:00 HKT (15:00-00:00 UTC)
**睡眠期間**: 減少通知
**例外**: 緊急提醒(<2 小時)、系統錯誤、用戶請求
**恢復**: 08:00 HKT 恢復正常通知

## 即將到來的事件
**今日 (3 月 1 日 星期日)**
• 已完成：Hugging Face Token 申請
• 已完成：營養師 App 配置 + 測試成功

**下星期六 (3 月 7 日)**
• 兒子學校家長日 (時間未定，需確認)

**下週日 (3 月 8 日)**
• 08:15-18:00 HKT - 學校旅行 (科大及西貢鹽田梓)

**3 月 10 日 (星期二)**
• 19:00-21:00 HKT - 匹克球 (Tsuen Wan Pickledise)
  - 朋友：Pulley (預計 19:10 到場，因泊車安排)
  - 泊車：19:00 準時到場 (場所有泊車優惠)

**3 月 13 日 (星期五)**
• 午餐 - 朋友 Chris (時間/地點待定)

**3 月 14 日 (星期六)**
• 學校旅行 (去流浮山) + 同鄉會晚宴 (需確認時間)

**3 月 15 日 (星期日)**
• 兒子生日
• Maxim's 現金券 $250 x 2 到期 (盆菜購買)

**3 月 17 日 (星期二)**
• 結婚周年紀念日 (海洋公園萬豪酒店 Membership 套餐 + spa)

## 待辦事項
**Maxim's 現金券**
• $250 電子現金券 × 2 (盆菜購買)
• 適用：美心皇宮
• 需在 3 月 15 日前使用或送給朋友
• ❓ 需確認：是否指定信用卡購買？有無使用限制？

**需確認事項**
1. 兒子學校家長日 (3 月 7 日) - 確認時間
2. 3 月 14 日活動 - 確認流浮山學校旅行和同鄉會晚宴時間

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
