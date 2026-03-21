# 🎯 香港地標猜猜猜 - HK Places Quiz

## 遊戲簡介
一個簡單嘅香港地標猜謎遊戲，玩家睇相揀答案，答完每題會有小知識。

## 文件結構
```
quiz/
├── index.html          # 遊戲主頁面
├── quiz-data.json      # 題目數據
├── assets/             # 圖片文件
│   ├── fisherman.jpg          # 釣魚翁
│   ├── waiting-wife.jpg       # 望夫石
│   └── ap-lei-chau-bridge.jpg # 鴨脷洲大橋
└── README.md           # 本文檔
```

## 如何添加新題目

### 1. 準備圖片
- 將圖片放入 `assets/` 文件夾
- 建議命名：`[地點英文名].jpg`（小寫，連字符分隔）
- 建議尺寸：寬 800-1200px，保持合理文件大小 (<500KB)

### 2. 編輯 quiz-data.json
在 `questions` 陣列中添加新題目：

```json
{
  "id": 4,
  "image": "assets/your-image.jpg",
  "correctAnswer": "正確答案",
  "options": [
    "正確答案",
    "錯誤選項 1",
    "錯誤選項 2",
    "錯誤選項 3"
  ],
  "hint": "提示（可選）",
  "fact": "關於呢個地方嘅小知識"
}
```

### 3. 測試
- 打開 `quiz/index.html` 測試新題目
- 確保圖片正確顯示
- 檢查答案選項是否正確

## 遊戲設定

在 `quiz-data.json` 的 `settings` 中可以調整：

```json
"settings": {
  "passingScore": 2,        // 合格需要答對的題數
  "timePerQuestion": 15,    // 每題作答時間（秒）- 未來功能
  "showFactAfterAnswer": true  // 答完顯示小知識
}
```

## 現有題目

| # | 地點 | 類型 | 難度 |
|---|------|------|------|
| 1 | 釣魚翁 | 行山徑 | 🟡 中 |
| 2 | 望夫石 | 傳說地標 | 🟢 易 |
| 3 | 鴨脷洲大橋 | 基建 | 🟢 易 |

## 未來擴充想法

### 題目分類
- 🏞️ 行山系（三尖、九徑等）
- 🏛️ 地標系（望夫石、大佛等）
- 🌉 基建系（橋樑、隧道等）
- 🏙️ 維港系（天際線、建築物等）

### 遊戲模式
- 計時模式（限時答題）
- 生存模式（答錯出局）
- 學習模式（無限時，答完顯示詳細資料）

### 功能增強
- 計分排行榜（Local Storage 或後端）
- 分享成績（生成圖片或文字）
- 多語言支持（廣東話/英文/普通話）
- 提示系統（可以使用 hint）

## 訪問 URL

**本地開發：**
```
http://localhost:3000/magazine/learning-center/quiz/
```

**生產環境（Zeabur）：**
```
https://kanban-board.zeabur.app/magazine/learning-center/quiz/
```

## 技術細節

- **純前端：** 無需後端，JSON 數據 + HTML/CSS/JS
- **響應式設計：** 支持手機/平板/桌面
- **無須登入：** 任何人都可以玩
- **輕量級：** 無外部依賴

---

**最後更新：** 2026-03-12
**題目數量：** 3 題
**貢獻者：** Raymond + Gym 師兄
