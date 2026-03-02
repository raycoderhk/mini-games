# 🚀 營養師 App - Zeabur 部署指南

**最後更新**: 2026-03-01  
**版本**: Flask Version (Zeabur Compatible)

---

## ⚡ 快速部署 (3 步)

### Step 1: 設置環境變量

在 **Zeabur Dashboard** 設置以下 secrets：

1. 去 https://zeabur.com/dashboard
2. 選擇 `nutritionist-app` project
3. 點擊 **Variables** / **Environment**
4. 添加兩個變量：

| 變量名 | 值 |
|--------|-----|
| `HF_API_KEY` | 你的 Hugging Face Token |
| `ALIYUN_API_KEY` | 你的 Aliyun DashScope Key |

---

### Step 2: 重新部署

**方法 A: Zeabur Dashboard (推薦)**
1. 去 https://zeabur.com/dashboard
2. 選擇 `nutritionist-app`
3. 點擊 **Redeploy** 按鈕
4. 等待部署完成（約 1-2 分鐘）

**方法 B: GitHub Auto-Deploy**
```bash
# Commit 並 push 更新
cd /home/node/.openclaw/workspace
git add nutritionist-app/
git commit -m "fix: Flask version for Zeabur deployment"
git push
```
Zeabur 會自動 detect 並 redeploy。

---

### Step 3: 驗證部署

**測試健康檢查:**
```bash
curl https://<your-zeabur-url>.zeabur.app/health
```

**預期結果:**
```json
{
  "status": "ok",
  "hf_configured": true,
  "aliyun_configured": true
}
```

如果顯示 `false`，表示環境變量未正確設置！

**測試首頁:**
```bash
curl https://<your-zeabur-url>.zeabur.app/
```

---

## 🧪 功能測試

1. 打開 Zeabur 提供的 URL
2. 上傳一張食物圖片
3. 點擊「開始分析」
4. 應該看到：
   - 🍽️ 識別到的食物名稱
   - 📊 營養分析數據

---

## 🐛 常見問題

### ❌ 顯示 "HF_API_KEY 未設置"
**原因**: Zeabur 環境變量未配置  
**解決**: 在 Zeabur Dashboard → Variables 添加 `HF_API_KEY`

### ❌ 顯示 "Aliyun API 錯誤：401"
**原因**: Aliyun API Key 無效  
**解決**: 檢查 Key 是否正確，確認有足夠餘額

### ❌ 頁面無法載入 (404/502)
**原因**: 部署失敗  
**解決**: 
1. 檢查 Zeabur Deploy Logs
2. 確認 `requirements.txt` 有 `flask`
3. 確認 `server.py` 在正確位置

### ❌ CORS 錯誤
**原因**: 前端無法訪問 API  
**解決**: Flask 已自動處理 CORS，檢查是否用錯 URL

---

## 📁 文件結構

```
nutritionist-app/
├── server.py            # Flask backend (entry point)
├── index.html           # Frontend UI
├── requirements.txt     # Flask dependency
├── zeabur.json          # Zeabur config
├── .zeaburignore        # Ignore rules
└── ZEABUR_DEPLOY.md     # 呢個文件
```

---

## 🔑 獲取 API Keys

### Hugging Face Token
1. 去 https://huggingface.co/settings/tokens
2. 點擊 "New token"
3. 選擇 "Read" 權限
4. Copy token

### Aliyun DashScope Key
1. 去 https://dashscope.console.aliyun.com/
2. 登入阿里雲帳號
3. 去 API Key Management
4. Copy Key

---

## 📞 需要幫助？

檢查部署日誌：
- Zeabur Dashboard → Deployments → View Logs

或者聯絡用戶（Telegram Direct Chat）。

---

**✨ 部署成功後，記得測試健康檢查 endpoint!**
