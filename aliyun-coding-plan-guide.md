# 🚀 Aliyun Coding Plan 訂購指南 (¥40 RMB/月)

## 💰 **計劃詳情**
- **名稱**: 阿里雲編程計劃 (Aliyun Coding Plan)
- **價格**: **¥40 RMB/月** (約 HK$44 / $5.50 USD)
- **API 配額**: Qwen 3.5/4.0 API 調用
- **節省**: 相比市場價 $500+/月，**節省 99%**

---

## 📋 **訂購步驟 (Step-by-Step)**

### **步驟 1: 註冊阿里雲賬戶**
1. 訪問: https://www.alibabacloud.com/
2. 點擊 **"Sign Up"** (右上角)
3. 使用 **國際版** (非中國版)
4. 建議用 **Gmail** 註冊 (避免中國手機號問題)

### **步驟 2: 實名認證**
1. 登入後 → **Account Center** (賬戶中心)
2. 選擇 **Real-name Registration** (實名認證)
3. 需要:
   - 護照/身份證照片
   - 手持證件自拍照
   - 通常 1-2 小時審核

### **步驟 3: 購買 Coding Plan**
1. 訪問: https://www.alibabacloud.com/product/coding-plan
2. 選擇 **"Coding Plan"** (編程計劃)
3. **價格: ¥40 RMB/月** (約 HK$44)
4. 付款方式:
   - ✅ **國際信用卡** (Visa/Mastercard)
   - ✅ **PayPal** (推薦)
   - ❌ 不支援香港本地信用卡

### **步驟 4: 獲取 API Key**
1. 購買後 → **Console** (控制台)
2. 搜索 **"Model Studio"** 或 **"DashScope"**
3. 創建 **API Key**:
   ```
   API Key 格式: sk-xxxxxxxxxxxxxxxxxxxx
   ```
4. 保存到安全地方 (`.env` 文件)

---

## 🔧 **OpenClaw 配置**

### **`.env` 文件配置:**
```bash
# Aliyun Qwen API
ALIYUN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
MODEL_PROVIDER=aliyun
MODEL_NAME=qwen-plus  # 或 qwen-turbo
```

### **測試連接:**
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
  -H "Authorization: Bearer sk-xxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-plus",
    "input": {
      "messages": [{"role": "user", "content": "Hello"}]
    }
  }'
```

---

## 💡 **重要提示**

### **✅ 優點**
1. **價格**: ¥40 RMB/月 (市場最低)
2. **速度**: 香港節點，延遲低
3. **穩定性**: 阿里雲全球基礎設施
4. **模型**: Qwen 3.5/4.0 都可用

### **⚠️ 注意事項**
1. **實名認證** 必須完成才能購買
2. **國際版** 非中國版 (避免支付問題)
3. **API Key** 每月有配額，但足夠個人使用
4. **付款失敗** 可試 PayPal

### **🔒 安全建議**
1. API Key 不要 commit 到 GitHub
2. 使用 `.env` 文件 + `.gitignore`
3. 定期 rotate API Key
4. 監控使用量 (控制台有儀表板)

---

## 📊 **價格對比**

| 供應商 | 價格 | 每月節省 | 備註 |
|--------|------|----------|------|
| **Aliyun Coding Plan** | **¥40 RMB** | - | 你嘅選擇 ✅ |
| OpenAI API | ~$50-100 USD | 節省 95-98% | |
| Anthropic Claude | ~$50-100 USD | 節省 95-98% | |
| 其他雲端 AI | $100-500 USD | 節省 98-99% | |

**每月節省**: **¥40 RMB vs $500 USD = 節省 99%** 🎉

---

## 💬 **分享給 Sheng 的版本 (Cantonese)**

> 喂 Sheng！上次講開個 Aliyun Coding Plan，呢度係詳細步驟：
> 
> **💰 計劃資料**
> - 名稱: 阿里雲編程計劃
> - 價錢: **¥40 RMB/月** (約 HK$44)
> - 內容: Qwen API 調用 (OpenClaw 用緊)
> - 節省: 相比市價 $500+，**慳 99%**
> 
> **📋 訂購步驟**
> 1. **註冊**: https://www.alibabacloud.com/ (用 Gmail)
> 2. **實名認證**: 需要護照/身份證照片 (1-2 小時審核)
> 3. **購買**: https://www.alibabacloud.com/product/coding-plan
> 4. **付款**: ¥40 RMB/月 (PayPal 最簡單)
> 5. **獲取 API Key**: 控制台 → Model Studio → 創建 Key
> 
> **🔧 OpenClaw 配置**
> ```bash
> ALIYUN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
> MODEL_PROVIDER=aliyun
> MODEL_NAME=qwen-plus
> ```
> 
> **⚠️ 注意**
> - 一定要用 **國際版** (唔好中國版)
> - 實名認證必須完成
> - API Key 保存好 (唔好 commit 上 GitHub)
> - 每月配額足夠個人使用
> 
> **💡 建議**
> 1. 先用 **PayPal** 付款 (最簡單)
> 2. 買完試下個 API 先配置 OpenClaw
> 3. 有問題隨時問我！
> 
> 搞掂咗話我知，可以幫你 setup OpenClaw！🚀

---

**發送時間**: 2026-03-22  
**發送者**: Jarvis (OpenClaw Assistant)  
**收件人**: Raymond (raycoderhk@gmail.com)  
**抄送**: Sheng (待提供)