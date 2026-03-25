# 🥚 爛 Gag 收集所

收集世上最爛嘅 gag，笑到喊出來！

## 🎮 玩法

1. **瀏覽爛 gag** - 訪問 https://gameworld.zeabur.app/gag/
2. **點擊顯示答案** - 每張卡片預設只显示題目，click 先見答案
3. **按出品人 Filter** - 可以睇特定出品人嘅 gag

## 📝 提交方法

### 方法 1：Admin Panel (即時提交) 🔐

1. 訪問 https://gameworld.zeabur.app/gag/admin.html
2. Login:
   - **用戶名:** `mw`
   - **密碼:** `315107`
3. 輸入 GitHub Personal Access Token（第一次需要）
   - 去 https://github.com/settings/tokens
   - 創建一個新 Token，勾選 `repo` scope
   - Copy 個 Token 貼入去
4. 填寫題目、答案、出品人
5. 提交！約 1-2 分鐘後喺網站顯示

### 方法 2：Discord Channel (#gag) 💬

直接 send 去 #gag Channel，格式如下：

```
題目：點解路易十六食自助餐唔使俾錢？
答案：因為自助餐係按人頭收費
出品人：@MW
```

或者簡單格式：

```
點解路易十六食自助餐唔使俾錢？
因為自助餐係按人頭收費
@MW
```

**注意：** Discord 提交需要管理員手動處理或者設置自動 Cron Job

## 📊 數據儲存

- **所有數據儲存喺** `gag/gags.json`
- **自動 Commit 到 GitHub** (Admin Panel)
- **Zeabur 自動部署** (約 2-5 分鐘)

## 🔧 技術細節

### 文件結構

```
mini-games/gag/
├── index.html          # 普通用戶頁面（瀏覽 + 玩）
├── admin.html          # Admin Panel（需要 login + GitHub Token）
├── gags.json           # 數據儲存
├── discord_monitor.py  # Discord 監察腳本（開發中）
└── README.md           # 呢個文件
```

### Admin Panel 認證

- **Login:** 簡單前端驗證 (`mw` / `315107`)
- **GitHub Token:** 用於寫入 `gags.json`
- **Session:** 儲存喺 Browser SessionStorage（關咗 Browser 就消失）

### Discord Monitor

- **腳本:** `discord_monitor.py`
- **功能:** 監察 #gag channel，自動解析並提交
- **狀態:** 開發中（需要 OpenClaw Discord integration）

## 🚀 部署

1. Push 到 GitHub `mini-games` repo
2. Zeabur 自動部署
3. 訪問 https://gameworld.zeabur.app/gag/

## 📝 數據格式

```json
[
  {
    "id": 1234567890,
    "question": "點解雞唔會打機？",
    "answer": "因為佢驚食雞... 🐔",
    "author": "@Raymond",
    "date": "2026-03-21T10:00:00Z"
  }
]
```

## 🔐 安全提示

- **Admin Panel 密碼** 係簡單前端驗證，唔適合高安全需求
- **GitHub Token** 只儲存喺 Browser Session，唔會上傳到任何伺服器
- **生產環境建議:** 使用後端 API + 數據庫

## 🎯 未來改進

- [ ] Discord 自動監察（Cron Job）
- [ ] 點贊/好笑功能
- [ ] 搜尋功能
- [ ] 分類/標籤
- [ ] 每週精選

---

**Enjoy the lams! 😄**
