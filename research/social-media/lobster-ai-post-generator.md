# 🦞 小龍蝦AI Facebook Post 自動生成系統

**分析日期：** 2026-03-22  
**目標：** 自動生成類似「小龍蝦AI」嘅 Facebook post  
**狀態：** 🟡 開發中

---

## 📊 Post 結構分析

### 原文分析

```
最近被"小龙虾AI"刷屏了！它可不是美食，而是科技圈新宠开源智能体OpenClaw，因为图标像红色小龙虾、英文名Claw意为钳子，被网友戏称"小龙虾"，训练它的过程还被叫做"养龙虾"😂

和传统AI最大的区别是：它能让电脑自己操作电脑！全程不用你动手，彻底解放双手！而且它还会自主思考，遇到难题会自己搜索、重试，直到完成任务~

对咱们打工人来说简直是效率神器：
运营岗能让它自动导数据、做表格、发社群；
销售岗可以托付它整理客户资料、发邮件、约会议，把繁琐琐事全交给AI，专心搞核心工作。

普通人也能躺平：规划旅行、处理照片、整理文件、代收快递信息，一句话指令全搞定，手机版也在筹备中～

⚠️不过也要注意：它需要电脑最高权限，有安全风险，大企业多禁止员工使用；运算要付费，成本不低；安装调试也有门槛，对普通人不太友好。

[向右R]但不得不说，小龙虾AI代表了AI新方向——从"被动回答"升级为"主动动手解决问题"，未来或许真的能让我们只下指令，坐等结果！

#小龙虾AI #OpenClaw #AI工具 #打工人必备 #科技新宠 #AI智能体 #openclaw安装 #openclaw教程 #科技 #人工智能[eoi]#
```

---

## 🎯 Post 模板結構

### 1. **標題/開場白**
```
最近被"[主題]AI"刷屏了！它可不是[表面意思]，而是[實際意義]...
```

### 2. **名稱解釋**
```
因为[特徵1]，[特徵2]，被网友戏称"[暱稱]"，训练它的过程还被叫做"[動詞]"
```

### 3. **核心功能**
```
和传统AI最大的区别是：[核心功能1]！[核心功能2]！[核心功能3]！
```

### 4. **應用場景 (打工人)**
```
对咱们打工人来说简直是效率神器：
[崗位1]能让它[功能1]、[功能2]、[功能3]；
[崗位2]可以托付它[功能4]、[功能5]、[功能6]...
```

### 5. **應用場景 (普通人)**
```
普通人也能躺平：[場景1]、[場景2]、[場景3]、[場景4]，一句话指令全搞定...
```

### 6. **注意事項**
```
⚠️不过也要注意：[風險1]；[風險2]；[風險3]...
```

### 7. **總結展望**
```
[轉折詞]但不得不说，[主題]代表了AI新方向——从"[舊模式]"升级为"[新模式]"，未来或许真的能让我们[美好願景]！
```

### 8. **Hashtags**
```
#[主題] #[英文名] #[類型] #[目標用戶] #[定位] #[功能] #[安裝] #[教程] #[領域] #[技術]
```

---

## 🔧 自動生成系統設計

### 系統架構

```
┌─────────────────────────────────────────┐
│          主題數據庫 (JSON)               │
│  - AI 工具列表                          │
│  - 功能模板                             │
│  - 應用場景                             │
│  - 風險警告                             │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         Post 生成器 (Python)             │
│  - 隨機選擇主題                         │
│  - 填充模板                             │
│  - 生成完整 post                        │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│        圖片生成器 (可選)                 │
│  - 創建簡潔圖片                         │
│  - 添加品牌元素                         │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│       自動發布系統 (可選)                │
│  - Facebook API                         │
│  - Discord 通知                         │
└─────────────────────────────────────────┘
```

---

### 數據庫結構

**文件：** `skills/social-media-generator/data/ai-tools-database.json`

```json
{
  "ai_tools": [
    {
      "id": "openclaw",
      "name": "小龍蝦AI",
      "english_name": "OpenClaw",
      "nickname": "小龍蝦",
      "training_verb": "養龍蝦",
      "icon_description": "紅色小龍蝦",
      "meaning": "鉗子",
      "core_features": [
        "能讓電腦自己操作電腦",
        "全程不用你動手，徹底解放雙手",
        "會自主思考，遇到難題會自己搜索、重試，直到完成任務"
      ],
      "professions": [
        {
          "name": "運營崗",
          "tasks": ["自動導數據", "做表格", "發社群"]
        },
        {
          "name": "銷售崗", 
          "tasks": ["整理客戶資料", "發郵件", "約會議"]
        }
      ],
      "common_use_cases": [
        "規劃旅行",
        "處理照片", 
        "整理文件",
        "代收快遞信息"
      ],
      "warnings": [
        "需要電腦最高權限，有安全風險",
        "大企業多禁止員工使用",
        "運算要付費，成本不低",
        "安裝調試也有門檻，對普通人不太友好"
      ],
      "hashtags": [
        "#小龍蝦AI",
        "#OpenClaw", 
        "#AI工具",
        "#打工人必備",
        "#科技新寵",
        "#AI智能體",
        "#openclaw安裝",
        "#openclaw教程", 
        "#科技",
        "#人工智能"
      ]
    }
  ],
  "templates": {
    "opening": [
      "最近被\"{name}\"刷屏了！它可不是{superficial_meaning}，而是{actual_meaning}...",
      "全網都在討論的\"{name}\"到底是什麼？它其實不是{superficial_meaning}，而是{actual_meaning}...",
      "你以為{name}是{superficial_meaning}？錯了！它其實是{actual_meaning}..."
    ],
    "explanation": [
      "因為{icon_description}，英文名{english_name}意為{meaning}，被網友戲稱\"{nickname}\"，訓練它的過程還被叫做\"{training_verb}\"😂",
      "外觀像{icon_description}，名字{english_name}意思是{meaning}，所以大家都叫它\"{nickname}\"，使用它就像\"{training_verb}\"一樣有趣～"
    ],
    "core_features": [
      "和傳統AI最大的區別是：{feature1}！{feature2}！{feature3}！",
      "最厲害的地方在於：{feature1}！{feature2}！再加上{feature3}！"
    ],
    "profession_applications": [
      "對咱們打工人來說簡直是效率神器：\n{profession1}能讓它{task1}、{task2}、{task3}；\n{profession2}可以託付它{task4}、{task5}、{task6}，把繁瑣瑣事全交給AI，專心搞核心工作。",
      "職場人士必備：\n{profession1}可以用來{task1}、{task2}、{task3}；\n{profession2}則能{task4}、{task5}、{task6}，工作效率翻倍！"
    ],
    "common_applications": [
      "普通人也能躺平：{usecase1}、{usecase2}、{usecase3}、{usecase4}，一句話指令全搞定，手機版也在籌備中～",
      "日常生活超實用：{usecase1}、{usecase2}、{usecase3}、{usecase4}，動動嘴就能完成，懶人福音！"
    ],
    "warnings": [
      "⚠️不過也要注意：{warning1}；{warning2}；{warning3}...",
      "🔴使用前請注意：{warning1}；{warning2}；另外{warning3}..."
    ],
    "conclusion": [
      "[向右R]但不得不說，{name}代表了AI新方向——從\"{old_paradigm}\"升級為\"{new_paradigm}\"，未來或許真的能讓我們{vision}！",
      "💡總的來說，{name}開啟了AI新時代：從\"{old_paradigm}\"到\"{new_paradigm}\"，期待未來{vision}！"
    ]
  }
}
```

---

### Post 生成器代碼

**文件：** `skills/social-media-generator/generate-ai-post.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 工具 Facebook Post 自動生成器
模仿「小龍蝦AI」風格
"""

import json
import random
from datetime import datetime
from pathlib import Path

class AIPostGenerator:
    def __init__(self, data_file=None):
        self.base_path = Path(__file__).parent
        self.data_file = data_file or self.base_path / "data" / "ai-tools-database.json"
        
        # 載入數據
        self.load_data()
        
        # 模板變量
        self.template_vars = {
            "old_paradigm": "被動回答",
            "new_paradigm": "主動動手解決問題", 
            "vision": "只下指令，坐等結果",
            "superficial_meaning": "美食"
        }
    
    def load_data(self):
        """載入 AI 工具數據"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def select_random_tool(self):
        """隨機選擇一個 AI 工具"""
        return random.choice(self.data["ai_tools"])
    
    def generate_post(self, tool_id=None):
        """生成完整 post"""
        
        # 選擇工具
        if tool_id:
            tool = next((t for t in self.data["ai_tools"] if t["id"] == tool_id), None)
            if not tool:
                tool = self.select_random_tool()
        else:
            tool = self.select_random_tool()
        
        # 準備變量
        vars = {
            **self.template_vars,
            "name": tool["name"],
            "english_name": tool["english_name"],
            "nickname": tool["nickname"],
            "training_verb": tool["training_verb"],
            "icon_description": tool["icon_description"],
            "meaning": tool["meaning"],
            "actual_meaning": f"科技圈新寵開源智能體{tool['english_name']}"
        }
        
        # 隨機選擇核心功能
        core_features = random.sample(tool["core_features"], 3)
        vars.update({
            "feature1": core_features[0],
            "feature2": core_features[1],
            "feature3": core_features[2]
        })
        
        # 職業應用
        if len(tool["professions"]) >= 2:
            prof1 = tool["professions"][0]
            prof2 = tool["professions"][1]
            vars.update({
                "profession1": prof1["name"],
                "task1": prof1["tasks"][0],
                "task2": prof1["tasks"][1],
                "task3": prof1["tasks"][2],
                "profession2": prof2["name"],
                "task4": prof2["tasks"][0],
                "task5": prof2["tasks"][1],
                "task6": prof2["tasks"][2]
            })
        
        # 普通應用
        usecases = random.sample(tool["common_use_cases"], 4)
        vars.update({
            "usecase1": usecases[0],
            "usecase2": usecases[1],
            "usecase3": usecases[2],
            "usecase4": usecases[3]
        })
        
        # 警告
        warnings = random.sample(tool["warnings"], 3)
        vars.update({
            "warning1": warnings[0],
            "warning2": warnings[1],
            "warning3": warnings[2]
        })
        
        # 生成各部分
        templates = self.data["templates"]
        
        post_parts = [
            self.fill_template(random.choice(templates["opening"]), vars),
            self.fill_template(random.choice(templates["explanation"]), vars),
            "",
            self.fill_template(random.choice(templates["core_features"]), vars),
            "",
            self.fill_template(random.choice(templates["profession_applications"]), vars),
            "",
            self.fill_template(random.choice(templates["common_applications"]), vars),
            "",
            self.fill_template(random.choice(templates["warnings"]), vars),
            "",
            self.fill_template(random.choice(templates["conclusion"]), vars),
            "",
            " ".join(tool["hashtags"])
        ]
        
        return "\n".join(post_parts), tool
    
    def fill_template(self, template, variables):
        """填充模板變量"""
        result = template
        for key, value in variables.items():
            placeholder = "{" + key + "}"
            result = result.replace(placeholder, value)
        return result
    
    def save_post(self, post, tool, output_dir=None):
        """保存生成的 post"""
        if output_dir is None:
            output_dir = self.base_path / "output"
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{tool['id']}_{timestamp}.txt"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"工具: {tool['name']} ({tool['english_name']})\n")
            f.write(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(post)
        
        return filepath
    
    def generate_multiple(self, count=5, tool_id=None):
        """生成多個 post"""
        results = []
        for i in range(count):
            post, tool = self.generate_post(tool_id)
            filepath = self.save_post(post, tool)
            results.append({
                "index": i + 1,
                "tool": tool["name"],
                "filepath": str(filepath),
                "preview": post[:200] + "..."
            })
        return results


def main():
    """主函數"""
    print("🦞 AI 工具 Facebook Post 生成器")
    print("=" * 50)
    
    generator = AIPostGenerator()
    
    # 生成小龍蝦AI post
    print("\n🎯 生成「小龍蝦AI」post...")
    post, tool = generator.generate_post("openclaw")
    
    print(f"\n📝 工具: {tool['name']} ({tool['english_name']})")
    print(f"📁 保存到: {generator.save_post(post, tool)}")
    
    print("\n" + "=" * 50)
    print("📋 生成的 post:")
    print("=" * 50)
    print(post)
    
    # 生成多個示例
    print("\n" + "=" * 50)
    print("🔄 生成 3 個隨機 AI 工具 post...")
    
    results = generator.generate_multiple(3)
    for result in results:
        print(f"\n{result['index']}. {result['tool']}")
        print(f"   文件: {result['filepath']}")
        print(f"   預覽: {result['preview']}")


if __name__ == "__main__":
    main()
```

---

### 擴展數據庫

**更多 AI 工具示例：**

```json
{
  "ai_tools": [
    {
      "id": "midjourney",
      "name": "魔法畫師AI",
      "english_name": "Midjourney",
      "nickname": "魔法畫師",
      "training_verb": "練魔法",
      "icon_description": "魔法杖",
      "meaning": "中途旅程",
      "core_features": [
        "能將文字描述變成精美圖片",
        "支援多種藝術風格",
        "可以無限修改直到滿意"
      ],
      "professions": [
        {
          "name": "設計師",
          "tasks": ["生成概念圖", "創建品牌視覺", "設計海報"]
        },
        {
          "name": "市場營銷",
          "tasks": ["製作社交媒體圖片", "設計廣告素材", "創建視覺內容"]
        }
      ],
      "common_use_cases": [
        "生成個人頭像",
        "創作藝術作品",
        "設計房間裝修",
        "製作生日賀卡"
      ],
      "warnings": [
        "需要 Discord 使用，對新手不友好",
        "生成次數有限制，需要付費訂閱",
        "版權歸屬有爭議",
        "對中文提示詞支援不夠好"
      ],
      "hashtags": [
        "#魔法畫師AI",
        "#Midjourney",
        "#AI繪圖",
        "#設計師必備",
        "#藝術創作",
        "#AI藝術家",
