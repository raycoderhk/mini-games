# 🎾 Pickleball 教練認證模擬考試

**版本：** 1.0  
**創建日期：** 2026-03-05  
**狀態：** ✅ 完成

---

## 📋 項目說明

這是一個 Discord Bot，用於測試 Pickleball 教練認證考試的知識。

包含 **30 條模擬試題**，涵蓋：
- 📜 基本規則
- 📊 計分系統
- 🏟️ 場地規格
- 🎯 技術戰術
- 👨‍🏫 教練知識

---

## 🎮 如何使用

### 開始測驗

```
/pickleball start
```

**選項：**
- `num_questions`: 題目數量 (預設 10 題，最多 30 題)

### 查看統計

```
/pickleball status
```

顯示你的：
- 總題目數
- 正確答案
- 準確率
- 最佳成績

### 排行榜

```
/pickleball leaderboard
```

顯示頭 10 名玩家的最佳成績。

---

## 📊 考試範圍

### 1. 基本規則 (Rules)
- 發球規則
- 兩跳規則 (Two-Bounce Rule)
- Kitchen 規則 (非截擊區)
- 犯規情況

### 2. 計分系統 (Scoring)
- 11/15/21 分制
- 發球方得分制
- 分數呼叫順序
- 換邊規則

### 3. 場地規格 (Court)
- 場地尺寸：20' x 44'
- Kitchen 範圍：7 英尺
- 球網高度：34" (中) / 36" (邊)
- 發球區劃分

### 4. 技術戰術 (Technique)
- Dink (網前小球)
- Third Shot Drop
- Erne (繞過 Kitchen)
- ATP (Around The Post)
- Stacking (雙打戰術)
- Soft Game (控球戰術)

### 5. 教練知識 (Coaching)
- 教學優先次序
- 比賽中指導規則
- 雙打溝通
- 初學者常見錯誤

---

## 📂 文件結構

```
pickleball-quiz/
├── bot.py              # Discord Bot 主程式
├── questions.json      # 30 條題目資料庫
├── .env                # Discord Token
├── venv/               # Python 虛擬環境
├── pickleball_quiz.db  # SQLite 資料庫 (自動創建)
└── README.md           # 本文件
```

---

## 🎯 及格標準

| 分數 | 等級 |
|------|------|
| 90-100% | 🏆 優秀 (Excellence) |
| 80-89% | ✅ 良好 (Good) |
| 70-79% | ✔️ 及格 (Pass) |
| <70% | ❌ 未及格 (Fail) |

**及格分數：70%**

---

## 🤖 運行 Bot

### 啟動

```bash
cd /home/node/.openclaw/workspace/pickleball-quiz
./venv/bin/python bot.py
```

### 停止

```bash
pkill -f "python.*bot.py"
```

### 查看日誌

```bash
tail -f /tmp/pickleball_bot.log
```

---

## 📝 題目示例

**題目 1:**
> Pickleball 比賽開始時，發球方有幾多位球員可以發球？
> 
> 🇦 1 位
> 🇧 2 位
> 🇨 只有第一發球方 1 位，之後 2 位
> 🇩 視乎單打定雙打
> 
> **答案：** 🇨

**題目 2:**
> 什麼是「Two-Bounce Rule」（兩跳規則）？
> 
> **答案：** 發球後，接發球方和發球方各必須讓球彈跳一次才能擊球

**題目 3:**
> 「Kitchen」的範圍是？
> 
> **答案：** 距離球網 7 英尺 (2.13m) 的區域

---

## 🔧 自定義題目

編輯 `questions.json` 添加新題目：

```json
{
  "id": 31,
  "category": "rules",
  "question": "你的題目？",
  "options": ["選項 A", "選項 B", "選項 C", "選項 D"],
  "correct": 0,
  "explanation": "解釋為什麼這個答案正確"
}
```

**欄位說明：**
- `id`: 題目編號 (唯一)
- `category`: 類別 (rules/scoring/court/technique/coaching)
- `question`: 題目文字
- `options`: 選項陣列 (2-5 個選項)
- `correct`: 正確答案索引 (0=A, 1=B, 2=C, 3=D)
- `explanation`: 答案解釋

---

## 📊 資料庫結構

**表格：** `scores`

| 欄位 | 類型 | 說明 |
|------|------|------|
| user_id | TEXT | Discord 用戶 ID (主鍵) |
| total_questions | INTEGER | 累計題目數 |
| correct_answers | INTEGER | 累計正確答案 |
| last_score | INTEGER | 最後一次分數 |
| best_score | INTEGER | 最佳分數 |
| last_played | TEXT | 最後測驗時間 |

---

## 🎓 教練認證資源

### 官方認證機構

| 機構 | 網站 |
|------|------|
| IPTPA | https://ipttapickleball.com |
| PPR | https://pprpickleball.com |
| APP | https://appickleball.com |
| Pickleball Canada | https://pickleballcanada.org |

### 學習資源

- **官方規則：** https://pickleball.com/rules
- **戰術教學：** https://pickleballtutorials.com
- **視頻教學：** YouTube "Pickleball Coaching"

---

## 🚀 下一步

- [ ] 添加更多題目 (目標 50+)
- [ ] 增加難度選擇 (初級/中級/高級)
- [ ] 添加計時功能
- [ ] 添加詳細分析報告
- [ ] 支持多人競賽模式

---

**祝你考試順利！** 🎾🏆
