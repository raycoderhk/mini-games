# 🌊 《啓示路：樂土之門》Discord Bot

基於鄧紫棋科幻小說《啓示路》的互動文字冒險遊戲

---

## 📖 遊戲簡介

玩家將扮演女主角**歌莉雅**，在虛擬世界「樂土」中探索自我、尋找真相、邂逅愛情。
你的每個選擇都會影響三個隱藏數值，最終解鎖 **6 個不同結局**。

### 核心數值
- ❤️ **愛情值** - 影響與愛凡的關係發展
- 🔍 **真相值** - 影響揭露秘密的程度
- 🌐 **樂土值** - 影響對虛擬世界的信任

---

## 🚀 快速部署

### 1. 前置條件

- Python 3.8+
- Discord Developer Account
- 一個 Discord Server

### 2. 創建 Discord Bot

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications)
2. 點擊 "New Application"，命名為 "啓示路遊戲 Bot"
3. 進入 "Bot" 頁面，點擊 "Reset Token"，複製 Token
4. 進入 "OAuth2" → "URL Generator"
   - Scopes: 勾選 `bot` 和 `applications.commands`
   - Bot Permissions: 勾選 `Send Messages`, `Embed Links`, `Use Slash Commands`
5. 複製生成的 URL，在瀏覽器打開，邀請 Bot 到你的 Server

### 3. 設置環境變量

```bash
# Linux/Mac
export DISCORD_TOKEN=你的_BOT_TOKEN

# Windows (PowerShell)
$env:DISCORD_TOKEN="你的_BOT_TOKEN"

# 或者創建 .env 文件
echo "DISCORD_TOKEN=你的_BOT_TOKEN" > .env
```

### 4. 安裝依賴

```bash
cd revelation-game
pip install -r requirements.txt
```

### 5. 運行 Bot

```bash
python bot.py
```

看到以下訊息表示成功：
```
啓示路遊戲 Bot 已登入！
已同步 X 個命令
```

---

## 🎮 遊戲命令

| 命令 | 描述 |
|------|------|
| `/revelation start` | 開始新遊戲 |
| `/revelation continue` | 繼續遊戲 |
| `/revelation status` | 查看角色狀態 |
| `/revelation reset` | 重置進度 |
| `/help` | 顯示幫助信息 |

---

## 📁 項目結構

```
revelation-game/
├── bot.py                 # Discord Bot 主程序
├── requirements.txt       # Python 依賴
├── players.db            # SQLite 數據庫 (自動生成)
├── scripts/
│   ├── chapter_1.json    # 第一章劇本
│   ├── chapter_2.json    # 第二章劇本 (待開發)
│   └── ...
└── README.md             # 本文件
```

---

## 📝 劇本格式

每個章節是一個 JSON 文件，格式如下：

```json
{
  "chapter": 1,
  "title": "章節標題",
  "scenes": [
    {
      "id": "scene_0",
      "text": "場景描述文字...",
      "choices": [
        {
          "emoji": "1️⃣",
          "text": "選擇文字",
          "next": "scene_1",
          "effects": {"love": 1, "truth": 0, "afterland": 0}
        }
      ]
    }
  ]
}
```

---

## 🎯 開發計劃

### 已完成
- ✅ 第一章劇本 (5 個場景，10+ 選擇)
- ✅ Discord Bot 基礎框架
- ✅ 進度儲存系統
- ✅ 數值追蹤系統

### 待開發
- [ ] 第二章至第七章劇本
- [ ] 多重結局系統
- [ ] 成就系統
- [ ] 漂流瓶多人互動
- [ ] 排行榜
- [ ] AI 生成對話 (可選)

---

## 🔧 自定義

### 修改數值影響

在 `scripts/chapter_X.json` 中修改 `effects`：

```json
"effects": {
  "love": 2,      // 愛情值變化 (-5 到 5)
  "truth": 1,     // 真相值變化
  "afterland": 0  // 樂土值變化
}
```

### 添加新場景

在劇本 JSON 中添加新 scene：

```json
{
  "id": "scene_new",
  "text": "新場景文字...",
  "choices": [...]
}
```

### 修改結局條件

在 `bot.py` 中添加結局判斷邏輯：

```python
def check_ending(scores):
    if scores['love'] > 10 and scores['afterland'] > 10:
        return "樂土永恆"
    elif scores['love'] > 10 and scores['truth'] > 10:
        return "現實擁抱"
    # ... 其他結局
```

---

## 🐛 常見問題

### Bot 沒有回應命令？
- 確保 Bot 有足夠權限
- 檢查命令是否已同步 (重啟 Bot)
- 確保在正確的 Server 中使用

### 進度沒有儲存？
- 檢查 `players.db` 文件是否存在
- 確保 Bot 有寫入權限

### 劇本載入失敗？
- 檢查 JSON 格式是否正確
- 確保文件編碼為 UTF-8

---

## 📞 支援

如有問題或建議，歡迎在 Discord 社群反饋！

---

## 🙏 鳴謝

- 原著：鄧紫棋《啓示路》
- 靈感來源：Choose Your Own Adventure 系列
- 技術支持：Discord.py 社群

---

## 📄 許可證

本項目僅供學習交流使用，請勿用於商業用途。
原著版權歸鄧紫棋及出版社所有。
