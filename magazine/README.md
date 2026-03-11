# 📚 Magazine Archive - 使用指南

## ⚠️ 重要聲明

本存檔系統嘅**頁面結構同連結格式**已準備妥當，但由於 The Economist 網站有 Paywall 限制，部分**文章標題為示例數據**。

---

## 🔗 Archive.ph 連結公式

### 基本格式

```
https://archive.ph/[原始 Economist URL]
```

### 示例

| 類型 | 原始 URL | Archive.ph 連結 |
|------|----------|----------------|
| 封面故事 | `https://www.economist.com/weeklyedition/2026-03-07` | `https://archive.ph/https://www.economist.com/weeklyedition/2026-03-07` |
| Leaders | `https://www.economist.com/leaders/2026/03/05/donald-trump-must-stop-soon` | `https://archive.ph/https://www.economist.com/leaders/2026/03/05/donald-trump-must-stop-soon` |
| Briefing | `https://www.economist.com/briefing/2026/03/05/an-ai-disaster-is-getting-ever-closer` | `https://archive.ph/https://www.economist.com/briefing/2026/03/05/an-ai-disaster-is-getting-ever-closer` |
| World | `https://www.economist.com/china/2026/03/02/chinas-ice-cold-calculus-over-iran` | `https://archive.ph/https://www.economist.com/china/2026/03/02/chinas-ice-cold-calculus-over-iran` |
| Finance | `https://www.economist.com/finance-and-economics/2026/03/03/the-nightmare-war-scenario-is-becoming-reality-in-energy-markets` | `https://archive.ph/https://www.economist.com/finance-and-economics/2026/03/03/the-nightmare-war-scenario-is-becoming-reality-in-energy-markets` |

---

## 📝 如何更新真實文章數據

### 步驟 1️⃣：獲取真實文章 URL

訪問 The Economist 官方網站：
```
https://www.economist.com/weeklyedition/2026-03-14
```

複製每篇文章嘅真實連結。

### 步驟 2️⃣：編輯 HTML 文件

打開對應期號嘅 HTML 文件（例如 `magazine/economist/2026-03-14/index.html`）

找到文章表格部分：
```html
<tbody>
    <tr>
        <td>1</td>
        <td><strong>文章標題</strong><br><small>副標題</small></td>
        <td><span class="category leaders">Leaders</span></td>
        <td class="links">
            <a href="https://www.economist.com/..." class="original" target="_blank">Original</a>
            <a href="https://archive.ph/https://www.economist.com/..." class="archive" target="_blank">Archive.ph</a>
        </td>
    </tr>
</tbody>
```

### 步驟 3️⃣：替換真實數據

將示例標題同 URL 替換為真實數據。

### 步驟 4️⃣：提交更新

```bash
git add magazine/
git commit -m "fix: Update Economist 2026-03-14 with real article data"
git push
```

---

## 🏷️ 文章分類標籤

| 分類 | CSS Class | 顏色 |
|------|-----------|------|
| Leaders | `category leaders` | 🔴 紅 |
| Briefing | `category briefing` | 🔵 藍 |
| World | `category world` | 🟢 綠 |
| Business | `category business` | 🟠 橙 |
| Finance | `category finance` | 🟣 紫 |
| Technology | `category tech` | 🔷 青 |
| Culture | `category culture` | 🟣 粉 |

---

## 📋 文章 URL 格式規律

The Economist 文章 URL 通常遵循以下格式：

```
https://www.economist.com/[section]/[year]/[month]/[day]/[article-slug]
```

### Section 列表

| Section | URL 路徑 |
|---------|----------|
| Leaders | `/leaders/` |
| Briefing | `/briefing/` |
| China | `/china/` |
| United States | `/united-states/` |
| Europe | `/europe/` |
| Middle East & Africa | `/middle-east-and-africa/` |
| The Americas | `/the-americas/` |
| Asia | `/asia/` |
| Finance and Economics | `/finance-and-economics/` |
| Business | `/business/` |
| Science and Technology | `/science-and-technology/` |
| Culture | `/culture/` |
| The World This Week | `/the-world-this-week/` |
| Economic Indicators | `/economic-and-financial-indicators/` |

---

## 📅 期號文件結構

```
magazine/
├── index.html                          # 雜誌列表
└── economist/
    ├── index.html                      # Economist 期號列表
    ├── 2026-03-01/
    │   └── index.html                  # March 1 期號文章目錄
    ├── 2026-03-07/
    │   └── index.html                  # March 7 期號文章目錄
    └── 2026-03-14/
        └── index.html                  # March 14 期號文章目錄
```

---

## 🔍 驗證真實數據

### 方法 1️⃣：直接訪問 Economist 官網
```
https://www.economist.com/weeklyedition/2026-03-14
```

### 方法 2️⃣：使用 Archive.ph 搜索
```
https://archive.ph/
```
輸入 Economist URL 搜索是否有存檔。

### 方法 3️⃣：Google 搜索
```
site:economist.com "2026-03-14"
```

---

## 🛠️ 工具

### Bookmarklet 解鎖 Paywall

將以下連結拖曳到書籤欄：

```javascript
javascript:(function(){window.open('https://archive.ph/'+window.location.href);})();
```

點擊即可在當前頁面打開 Archive.ph 版本。

---

## ❓ 常見問題

### Q: 點解部分標題係示例數據？
A: The Economist 網站有 Paywall 限制，無法直接抓取真實內容。歡迎用戶提供真實數據更新。

### Q: Archive.ph 連結點樣用？
A: 將 Economist 官方 URL 加在 `https://archive.ph/` 後面即可。

### Q: 點樣貢獻真實數據？
A: 歡迎透過 GitHub Issue 或 Pull Request 提供真實文章標題同 URL。

---

## 📞 聯絡

如有疑問或想貢獻數據，請聯絡：
- GitHub: https://github.com/raycoderhk/mini-games
- Discord: OpenClaw Community

---

**最後更新：** 2026-03-11  
**版本：** 1.0
