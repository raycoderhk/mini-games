# 🎮 原版 Pixel Office 功能分析

**來源：** https://github.com/xmanrui/OpenClaw-bot-review  
**文件：** `app/pixel-office/page.tsx` (3,500+ 行) + `lib/pixel-office/` (多個核心模組)

---

## 📊 核心功能清單

### 1. 渲染引擎 (Engine)

**文件：** `lib/pixel-office/engine/`

| 功能 | 說明 | 複雜度 |
|------|------|--------|
| **OfficeState** | 辦公室狀態管理 | ⭐⭐⭐⭐⭐ |
| **Renderer** | Canvas 渲染引擎 | ⭐⭐⭐⭐⭐ |
| **Characters** | 角色動畫系統 | ⭐⭐⭐⭐⭐ |
| **Matrix Effect** | 黑客帝國風格代碼雨 | ⭐⭐⭐⭐ |
| **Pathfinding** | A* 尋路算法 | ⭐⭐⭐⭐⭐ |

**代碼量：** 約 2,000+ 行

---

### 2. 編輯器系統 (Editor)

**文件：** `lib/pixel-office/editor/`

| 功能 | 說明 |
|------|------|
| **編輯工具欄** | 選擇、放置、旋轉家具 |
| **地形編輯** | 地板、牆壁、擴建辦公室 |
| **撤銷/重做** | 操作歷史記錄 |
| **保存/載入** | 本地存儲佈局 |

**UI 組件：**
- `EditorToolbar.tsx` - 工具選擇
- `EditActionBar.tsx` - 操作按鈕

---

### 3. 家具系統 (Furniture)

**文件：** `lib/pixel-office/layout/furnitureCatalog.ts`

**家具類型：** 30+ 種

| 類別 | 家具 |
|------|------|
| **Desks** | 書桌、木桌 (橫/直) |
| **Chairs** | 椅子、旋轉椅、長凳 |
| **Storage** | 書架、文件櫃 |
| **Decor** | 植物、白板、時鐘、畫作 |
| **Electronics** | 電腦、伺服器、相機 |
| **Misc** | 飲水機、雪櫃、梳化 |

**功能：**
- 旋轉 (4 個方向)
- 開/關狀態 (燈、電腦)
- 可放置喺枱面 (相機、電話、咖啡杯)
- 牆壁家具 (畫、白板)

---

### 4. 角色系統 (Characters)

**文件：** `lib/pixel-office/engine/characters.ts`

**角色狀態：**
```typescript
enum CharacterState {
  IDLE = 'idle',
  WALKING = 'walking',
  SITTING = 'sitting',
  STANDING_UP = 'standing_up',
  INTERACTING = 'interacting'
}
```

**功能：**
- **自動尋路** - A* 算法搵最短路徑
- **狀態機** - Idle → Walking → Sitting → Standing
- **動畫幀** - 4 幀行走出動畫
- **碰撞檢測** - 唔會行過家具
- **互動點** - 喺枱前低、喺白板前寫字

**角色數量：** 每個 Agent 一個角色  
**外觀：** 5 種顏色 × 多種髮型/衣服 (可自定義)

---

### 5. 音效系統 (Audio)

**文件：** `lib/pixel-office/notificationSound.ts`

**功能：**
- **背景音樂** - Lo-fi 風格循環播放
- **音效**：
  - 坐下聲
  - 完成工作聲
  - 提示聲
- **靜音控制** - 開關音效
- **自動解鎖** - 用戶點擊後先播放

---

### 6. 數據可視化 (Stats)

**功能：**
- **貢獻圖** - GitHub 風格热力圖
- **Sparkline** - 小型趨勢圖表
- **Agent 卡片**：
  - Session 數量
  - Token 用量
  - 平均響應時間
  - 最後活躍時間

**API 調用：**
- `/api/agent-activity` - Agent 活動數據
- `/api/stats-all` - 綜合統計
- `/api/activity-heatmap` - 热力圖數據

---

### 7. 多語言 (i18n)

**文件：** `lib/i18n/`

**支持語言：**
- 繁體中文 (zh-TW)
- 簡體中文 (zh)
- 英文 (en)

**翻譯內容：**
- UI 文字
- 工具提示
- 通知消息
- 家具名稱

---

### 8. 特殊效果 (Effects)

| 效果 | 說明 |
|------|------|
| **Matrix Code** | 隨機浮現代碼片段 (工程師文化) |
| **SRE Blackwords** | 運維術語浮現 (「先止血」、「降載執行」) |
| **Photo Comments** | 相冊評論浮現 |
| **Lobster Rage** | 🦞 憤怒龍蝦 (彩蛋) |
| **Floating Text** | Agent 頭上浮現文字 |

---

### 9. 佈局系統 (Layout)

**文件：** `lib/pixel-office/layout/`

**功能：**
- **Tile-based** - 網格化佈局 (16x16 像素/格)
- **擴建系統** - 可以向 4 個方向擴建辦公室
- **序列化** - Save/Load 佈局 (JSON)
- **遷移** - 版本升級自動遷移舊佈局

**佈局數據結構：**
```typescript
interface OfficeLayout {
  version: number
  cols: number
  rows: number
  tiles: TileType[]      // 地板/牆壁/空白
  furniture: Furniture[] // 家具列表
  floorColor: FloorColor // 地板顏色主題
}
```

---

### 10. Agent 橋接 (Agent Bridge)

**文件：** `lib/pixel-office/agentBridge.ts`

**功能：**
- **同步 Agent 到辦公室** - 每個 Agent 一個角色
- **活動追蹤** - 根據 Agent 活動改變角色狀態
- **忙/閒狀態**：
  - 忙：坐喺枱前打緊字
  - 閒：喺辦公室行來行去

**API 整合：**
- 讀取 `~/.openclaw/openclaw.json`
- 同步 Agents/Models/Platforms

---

## 🎨 視覺風格

### 像素藝術 (Pixel Art)

**風格：** 16-bit 復古風  
**調色板：** 自定義 (深藍/紫色為主)  
**精細度：** 每個角色 16x16 像素 × 4 幀動畫

### 家具精靈 (Sprites)

**來源：**
1. **手繪精靈** - 原創像素畫
2. **Tileset** - 使用開源像素素材包

**加載方式：**
- PNG 文件 → Base64 → 渲染到 Canvas

---

## ⚙️ 技術架構

### 前端 (React + Canvas)

```
app/pixel-office/page.tsx (3,500 行)
├── Canvas 渲染 (requestAnimationFrame)
├── React State (useState, useEffect)
├── 事件處理 (mouse/touch/keyboard)
└── 組件組合 (EditorToolbar, AgentCard, etc.)
```

### 後端 (Next.js API Routes)

```
app/api/pixel-office/
├── layout/route.ts    - 佈局 Save/Load
├── tracks/route.ts    - 角色軌跡
├── idle-rank/route.ts - 閒置排名
├── contributions/route.ts - 貢獻數據
└── version/route.ts   - 版本檢查
```

### 核心引擎 (TypeScript)

```
lib/pixel-office/
├── engine/           - 渲染引擎
├── editor/           - 編輯器
├── layout/           - 佈局系統
├── sprites/          - 精靈數據
├── bugs/             - 彩蛋系統
└── types.ts          - 類型定義
```

---

## 📈 性能優化

| 優化 | 說明 |
|------|------|
| **Canvas 分層** | 背景/角色/UI 分層渲染 |
| **幀率控制** | Desktop 60FPS / Mobile 30FPS |
| **精靈批處理** | 合併相同精靈減少 draw 調用 |
| **事件防抖** | Mouse/Touch 事件節流 |
| **數據輪詢** | 10 秒刷新 Gateway, 1 秒刷新 Agent |

---

## 🎮 用戶交互

### 鼠标操作 (Desktop)

| 操作 | 功能 |
|------|------|
| **左鍵點擊** | 選擇/放置家具 |
| **右鍵點擊** | 旋轉/移除家具 |
| **拖拽** | 平移視圖 |
| **滾輪** | 縮放 (0.5x - 6x) |

### 觸控操作 (Mobile)

| 操作 | 功能 |
|------|------|
| **單指拖拽** | 平移視圖 |
| **雙指捏合** | 縮放 |
| **長按** | 顯示操作菜單 |

---

## 🔧 自定義能力

### 可配置項

| 配置 | 說明 |
|------|------|
| **辦公室大小** | 最小 10x10, 最大 100x100 |
| **地板顏色** | 5 種主題 |
| **角色外觀** | 5 種顏色 × 多款髮型 |
| **家具佈局** | 完全自由放置 |
| **音效開關** | 開/關背景音樂/音效 |

### 擴展點

| 擴展 | 說明 |
|------|------|
| **新家具** | 添加 PNG + Catalog Entry |
| **新角色** | 添加 Sprite Sheet |
| **新效果** | 添加 Effect Renderer |
| **新語言** | 添加 i18n JSON |

---

## 📊 代碼量統計

| 模組 | 文件數 | 代碼行數 |
|------|--------|---------|
| **Page Component** | 1 | 3,500 |
| **Engine** | 5 | 1,200 |
| **Editor** | 4 | 800 |
| **Layout** | 4 | 600 |
| **Sprites** | 3 | 400 |
| **API Routes** | 6 | 300 |
| **Components** | 8 | 1,000 |
| **Utils** | 10 | 500 |
| **總計** | **41** | **8,300+** |

---

## 🎯 我嘅精簡版 vs 原版

### 精簡版 (我而家做嘅)

**代碼量：** ~150 行  
**功能：**
- ✅ 基本 Canvas 渲染
- ✅ 角色移動 (隨機 + 碰撞)
- ✅ 簡單像素角色 (單色方塊 + 眼)
- ✅ 辦公室佈景 (地板 + 枱)
- ❌ 無編輯器
- ❌ 無家具系統
- ❌ 無尋路算法
- ❌ 無音效
- ❌ 無動畫幀 (靜止)
- ❌ 無數據可視化

### 原版

**代碼量：** 8,300+ 行  
**功能：** 上面列嘅所有嘢

---

## 💡 建議方案

### 選項 A: 保留精簡版 + 逐步增強

**優點：**
- 快速上線 (已經做好)
- 代碼簡單易維護
- 可以逐步添加功能

**缺點：**
- 美觀度一般
- 功能有限

**增強路線圖：**
1. 添加動畫幀 (4 幀行走)
2. 添加簡單家具 (枱 + 椅)
3. 添加尋路 (簡單版 A*)
4. 添加音效
5. 添加編輯器 (簡化版)

---

### 選項 B: 完整整合原版

**方法 1: iframe 嵌入**
```html
<iframe src="https://openclaw-bot-review.vercel.app/pixel-office" 
        style="width: 100%; height: 600px; border: none;">
</iframe>
```

**優點：**
- 完整功能
- 唔使自己維護

**缺點：**
- 需要部署原版
- iframe 可能有跨域問題

---

**方法 2: 複製核心代碼**

**步驟：**
1. 複製 `lib/pixel-office/` 到 kanban-zeabur
2. 複製 `app/pixel-office/page.tsx` 改為 HTML/JS
3. 複製 API Routes
4. 複製精靈圖片

**優點：**
- 完整功能
- 自己控制

**缺點：**
- 代碼量大 (8,300+ 行)
- 需要大量適配工作 (React → Vanilla JS)
- 維護成本高

---

### 選項 C: 混合方案 (推薦)

**核心思路：**
- **精簡版做預覽** - 快速載入，基本動畫
- **完整版做可選** - 點擊「進入完整辦公室」先載入

**實現：**
```html
<!-- 精簡版 (默認) -->
<div id="pixelOfficeLite">...</div>

<!-- 完整版 (按需載入) -->
<button onclick="loadFullPixelOffice()">🎮 進入完整辦公室</button>
<div id="pixelOfficeFull" style="display:none;">
  <iframe src="/pixel-office-full.html"></iframe>
</div>
```

---

## 🎯 你點揀？

| 選項 | 時間 | 功能 | 美觀 | 推薦度 |
|------|------|------|------|--------|
| **A: 精簡版 + 增強** | 1-2 小時/功能 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **B1: iframe 嵌入** | 10 分鐘 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **B2: 完整複製** | 10-20 小時 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **C: 混合方案** | 1 小時 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

**你鍾意邊個方案？我可以即刻幫你實現！** 🦞🎮
