# 🚀 營養師 App 部署指南 (for Jarvis)

**最後更新**: 2026-03-01  
**負責人**: Jarvis (自動化部署 Agent)

---

## 📋 部署檢查清單

### 前置條件
- [ ] 已獲取 Hugging Face API Token
- [ ] 已獲取 Aliyun DashScope API Key
- [ ] Zeabur 帳號已登入
- [ ] 代碼已 commit 到 Git repo

---

## 🛠️ 自動部署流程

### Step 1: 確認配置文件
確保以下文件存在且正確：
```bash
nutritionist-app/
├── zeabur.json          # Zeabur 部署配置
├── server.py            # Python backend entry point
├── index.html           # Frontend UI
├── requirements.txt     # Python 依賴
└── .zeaburignore        # 忽略文件
```

### Step 2: 設置環境變量 (Zeabur Secrets)
在 Zeabur Dashboard 設置以下 secrets：
```bash
HF_API_KEY=<your-huggingface-token>
ALIYUN_API_KEY=<your-aliyun-dashscope-key>
```

**或者用 Zeabur CLI:**
```bash
zeabur env set HF_API_KEY=<your-huggingface-token> -p nutritionist-app
zeabur env set ALIYUN_API_KEY=<your-aliyun-dashscope-key> -p nutritionist-app
```

### Step 3: 部署到 Zeabur

**方法 A: Zeabur CLI (推薦)**
```bash
cd /home/node/.openclaw/workspace/nutritionist-app
zeabur deploy
```

**方法 B: GitHub Auto-Deploy**
1. Commit 並 push 代碼到 GitHub
2. Zeabur 會自動 detect 並 redeploy

**方法 C: Zeabur Dashboard**
1. 去 https://zeabur.com/dashboard
2. 選擇 `nutritionist-app` project
3. 點擊 "Redeploy"

### Step 4: 驗證部署
```bash
# 獲取 Zeabur 部署 URL
DEPLOY_URL=$(zeabur url -p nutritionist-app)

# 測試首頁
curl -s $DEPLOY_URL | head -5

# 測試 API (需要上傳測試圖片)
curl -X POST $DEPLOY_URL/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/jpeg;base64,<test-image-base64>"}'
```

### Step 5: 通知用戶
部署成功後，通知用戶：
- ✅ 部署 URL
- ✅ 測試狀態
- ✅ 環境變量配置確認

---

## 🔧 zeabur.json 配置說明

```json
{
  "$schema": "https://zeabur.com/schema.json",
  "name": "nutritionist-app",
  "description": "AI 食物圖片識別 + 營養分析",
  "region": "hkg",
  "services": [
    {
      "name": "nutritionist-web",
      "type": "python",
      "root": "nutritionist-app",
      "entry": "server.py",
      "port": 8080,
      "include": [
        "index.html",
        "server.py",
        "requirements.txt"
      ],
      "envs": {
        "HF_API_KEY": "{{ secrets.HF_API_KEY }}",
        "ALIYUN_API_KEY": "{{ secrets.ALIYUN_API_KEY }}"
      }
    }
  ]
}
```

**關鍵配置:**
- `type`: 必須係 `"python"` (唔係 `"static"`)
- `entry`: Python server entry point (`server.py`)
- `port`: 服務端口 (`8080`)
- `envs`: 環境變量引用 Zeabur secrets

---

## 🧪 測試清單

部署後驗證以下功能：
- [ ] 首頁正常載入 (http://<zeabur-url>/)
- [ ] 圖片上傳功能正常
- [ ] 食物識別 API 返回結果
- [ ] 營養分析 API 返回結果
- [ ] 錯誤處理正常 (無 API key 時顯示友好錯誤)

---

## 🐛 常見問題

### 問題 1: 部署後顯示 404
**原因**: `zeabur.json` 配置錯誤或 entry point 不對  
**解決**: 確認 `entry` 字段指向正確的 Python 文件

### 問題 2: API 調用失敗
**原因**: 環境變量未設置  
**解決**: 在 Zeabur Dashboard 設置 `HF_API_KEY` 和 `ALIYUN_API_KEY`

### 問題 3: CORS 錯誤
**原因**: 前端無法訪問後端 API  
**解決**: 確認 `server.py` 有設置 CORS headers (已包含)

### 問題 4: 端口衝突
**原因**: Zeabur 分配的端口與配置不符  
**解決**: 使用 `process.env.PORT` 或確認 Zeabur 配置中的 port

---

## 📞 聯絡資訊

如有問題，聯絡：
- **用戶**: Telegram Direct Chat
- **文檔**: `/home/node/.openclaw/workspace/nutritionist-app/README.md`

---

**✨ 部署成功後，記得通知用戶測試！**
