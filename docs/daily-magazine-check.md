# 📰 每日雜誌更新檢查 | Daily Magazine Check

**目的:** 檢查最新一期雜誌是否出版，並添加到 Archive

---

## 📅 檢查時間

**每日 Heartbeat 自動檢查** (08:00 HKT)

---

## 📚 檢查清單

### 1. Bloomberg Businessweek
**出版頻率:** 每週一  
**官方網址:** https://www.bloomberg.com/businessweek  
**最新期數:** 2026-03-01 (March 1, 2026)  
**下一期預計:** 2026-03-08 (March 8, 2026)

**檢查步驟:**
1. 訪問 Bloomberg Businessweek 首頁
2. 查看最新一期日期
3. 如果有新一期 → 創建新 issue 目錄
4. 添加文章連結 (Cover + Gen Alpha + Business + World + Lifestyle)
5. 創建 ESL Vocab 頁面

**狀態:** ✅ 進行中 (8/19 vocab pages)

---

### 2. The Economist
**出版頻率:** 每週四  
**官方網址:** https://www.economist.com  
**最新期數:** 2026-03-14 (March 14, 2026)  
**下一期預計:** 2026-03-21 (March 21, 2026)

**檢查步驟:**
1. 訪問 Economist 首頁
2. 查看最新一期日期
3. 如果有新一期 → 創建新 issue 目錄
4. 添加文章連結 (Leaders, Britain, World, Business, Tech...)
5. 創建 ESL Vocab 頁面

**狀態:** ✅ 進行中 (3 issues, 227 articles, 18 vocab pages)

---

### 3. HKEJ 信報
**出版頻率:** 每週一至六  
**官方網址:** https://www.hkej.com  
**最新期數:** 2026-03-12 (March 12, 2026)  
**下一期預計:** 2026-03-13 (March 13, 2026)

**檢查步驟:**
1. 訪問 HKEJ 首頁
2. 查看今日要聞
3. 如果有新內容 → 更新 issue 目錄
4. 添加文章連結 (要聞 + 時事評論)
5. 創建 ESL Vocab 頁面

**狀態:** ✅ 進行中 (1 issue, 10 articles)

---

### 4. National Geographic
**出版頻率:** 每月  
**官方網址:** https://www.nationalgeographic.com/magazine  
**最新期數:** 2026-03 (March 2026)  
**下一期預計:** 2026-04 (April 2026)

**檢查步驟:**
1. 訪問 Nat Geo Magazine 首頁
2. 查看最新一期月份
3. 如果有新一期 → 創建新 issue 目錄
4. 添加文章連結 (Cover Story + Features + Explorer)
5. 創建 ESL Vocab 頁面

**狀態:** ✅ 進行中 (3 issues, 16 articles, 4 vocab pages)

---

## 🔧 自動化腳本

### 檢查腳本位置
```
/workspace/scripts/check-magazine-updates.py
```

### 腳本功能
1. 訪問各雜誌官方網站
2. 檢測最新期數日期
3. 與本地最新期數比較
4. 如果有更新 → 發送 Discord 通知
5. 自動創建 issue 目錄結構

### 運行方式
```bash
# 手動運行
python3 /workspace/scripts/check-magazine-updates.py

# Cron 自動運行 (每日 08:00 HKT)
0 0 * * * python3 /workspace/scripts/check-magazine-updates.py
```

---

## 📝 添加新期數流程

### Step 1: 確認新期數
- [ ] 訪問官方網站確認出版日期
- [ ] 記錄期數日期 (e.g., 2026-03-08)
- [ ] 記錄文章數量

### Step 2: 創建目錄結構
```bash
mkdir -p /workspace/magazine/bloomberg/2026-03-08
```

### Step 3: 創建 index.html
- [ ] 複製上一期結構
- [ ] 更新日期和期數
- [ ] 添加文章連結 (Original + Archive.ph)
- [ ] 添加 Cover Image (如有)

### Step 4: 創建 Vocab 頁面
- [ ] 選擇重點文章 (5-10 篇)
- [ ] 創建 vocab-*.html 頁面
- [ ] 添加 10 個詞彙 + 3 道測驗題
- [ ] 添加預生成 AI 解釋

### Step 5: 更新主頁
- [ ] 更新 magazine/index.html
- [ ] 添加新 issue card
- [ ] 更新統計數據

### Step 6: Commit & Deploy
```bash
git add -A
git commit -m "feat: Add [Magazine] [Date] issue ([X] articles)"
git push mini-games main
```

---

## 📊 當前狀態總覽

| Magazine | Latest Issue | Next Issue | Status | Vocab Pages |
|----------|--------------|------------|--------|-------------|
| **Bloomberg** | 2026-03-01 | 2026-03-08 | 🟡 In Progress | 8/19 |
| **Economist** | 2026-03-14 | 2026-03-21 | 🟢 Complete | 18/∞ |
| **HKEJ** | 2026-03-12 | 2026-03-13 | 🟡 In Progress | 0/∞ |
| **Nat Geo** | 2026-03 | 2026-04 | 🟢 Complete | 4/∞ |

---

## 🔔 通知設置

### Discord 通知
**Channel:** #magazine-updates  
**Trigger:** 檢測到新期數  
**格式:**
```
📰 New Magazine Issue Detected!

**Magazine:** [Name]
**Issue Date:** [Date]
**Articles:** [Count]
**Status:** Ready for processing

[Link to official site]
```

### Heartbeat 檢查
**時間:** 每日 08:00 HKT  
**任務:** 檢查 4 本雜誌  
**輸出:** memory/magazine-check-YYYY-MM-DD.md

---

## 📝 備註

1. **Bloomberg:** 每週一出版，重點關注 Cover Story + Business
2. **Economist:** 每週四出版，重點關注 Leaders + World + Business
3. **HKEJ:** 每週一至六，重點關注要聞 (10 篇)
4. **Nat Geo:** 每月出版，重點關注 Cover Story + Features

---

*Last updated: 2026-03-16*  
*Next check: 2026-03-17 08:00 HKT*
