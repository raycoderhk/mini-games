#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
營養師 App - OpenRouter MiniMax-01 ONLY
單一模型搞掂食物識別 + 營養分析！
使用 MiniMax-01 (OpenRouter) 視覺識別 + 營養分析

優點:
- 單一 API 調用
- 免費額度 (OpenRouter)
- 無須 Aliyun Key
"""

import urllib.request
import urllib.error
import json
import base64
import os
import sys
from datetime import datetime

# ============ 配置 ============
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ============ MiniMax-01 完整分析 ============
def analyze_food_miniMax(image_path):
    """使用 MiniMax-01 一次性完成食物識別 + 營養分析"""
    print("\n🔍 使用 MiniMax-01 (OpenRouter) 分析食物圖片...")
    
    # 轉換圖片為 Base64
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    print(f"✅ 圖片載入成功 ({len(image_data)} bytes)")
    
    # 完整 Prompt (識別 + 營養分析)
    prompt = """請詳細分析這張食物圖片：

## 任務
1. **識別食物**: 列出圖片中所有可見的食物
2. **營養分析**: 分析每種食物的營養成分
3. **健康建議**: 提供 2-3 條健康飲食建議

## 返回格式 (JSON)
{
    "foods": [
        {
            "name": "食物名稱（中文）",
            "confidence": 0.95,
            "description": "簡單描述",
            "nutrition": {
                "serving_size": "份量（克）",
                "calories": 數字（千卡）,
                "protein": 數字（克）,
                "carbs": 數字（克）,
                "fat": 數字（克）,
                "fiber": 數字（克）
            }
        }
    ],
    "total_nutrition": {
        "calories": 總卡路里,
        "protein": 總蛋白質,
        "carbs": 總碳水,
        "fat": 總脂肪,
        "fiber": 總纖維
    },
    "health_tips": [
        "建議 1",
        "建議 2",
        "建議 3"
    ],
    "meal_rating": "優秀/良好/普通/需注意"
}

只返回 JSON，不要其他文字。"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/raycoderhk/nutritionist-app",
        "X-Title": "Nutritionist App"
    }
    
    payload = {
        "model": "minimax/minimax-01",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    try:
        print("\n📡 調用 OpenRouter MiniMax-01 API...")
        req = urllib.request.Request(
            OPENROUTER_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        content = result["choices"][0]["message"]["content"]
        print(f"✅ OpenRouter API 調用成功！")
        
        # 提取 JSON
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            json_str = content[start:end]
            analysis = json.loads(json_str)
            return {"success": True, "data": analysis, "model": "MiniMax-01"}
        else:
            return {"success": False, "error": "JSON 解析失敗", "raw": content}
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"success": False, "error": f"HTTP {e.code}: {e.reason} - {error_body}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============ 顯示結果 ============
def display_result(analysis):
    """顯示分析結果"""
    print("\n" + "=" * 60)
    print("📊 分析結果")
    print("=" * 60)
    
    data = analysis.get("data", {})
    
    # 食物列表
    foods = data.get("foods", [])
    print(f"\n🍽️ 識別到的食物 ({len(foods)} 項):")
    for food in foods:
        name = food.get("name", "未知")
        confidence_raw = food.get("confidence", 0)
        try:
            confidence = float(confidence_raw) * 100 if isinstance(confidence_raw, (int, float)) else float(str(confidence_raw).replace('%', '')) if isinstance(confidence_raw, str) else 0
        except:
            confidence = 0
        desc = food.get("description", "")
        print(f"  • {name} ({confidence:.0f}% 信心)")
        if desc:
            print(f"    → {desc}")
    
    # 營養成分
    total = data.get("total_nutrition", {})
    if total:
        print("\n📊 總營養含量:")
        print(f"  🔥 卡路里：{total.get('calories', 0)} kcal")
        print(f"  💪 蛋白質：{total.get('protein', 0)}g")
        print(f"  🍚 碳水化合物：{total.get('carbs', 0)}g")
        print(f"  🥑 脂肪：{total.get('fat', 0)}g")
        print(f"  🌾 纖維：{total.get('fiber', 0)}g")
    
    # 每種食物的詳細營養
    print("\n📈 每種食物營養成分:")
    for food in foods:
        name = food.get("name", "未知")
        nutrition = food.get("nutrition", {})
        if nutrition:
            print(f"\n  {name}:")
            print(f"    份量：{nutrition.get('serving_size', '未知')}")
            print(f"    🔥 卡路里：{nutrition.get('calories', 0)} kcal")
            print(f"    💪 蛋白質：{nutrition.get('protein', 0)}g")
            print(f"    🍚 碳水：{nutrition.get('carbs', 0)}g")
            print(f"    🥑 脂肪：{nutrition.get('fat', 0)}g")
            print(f"    🌾 纖維：{nutrition.get('fiber', 0)}g")
    
    # 評分
    rating = data.get("meal_rating", "")
    if rating:
        print(f"\n⭐ 餐食評分：{rating}")
    
    # 健康建議
    health_tips = data.get("health_tips", [])
    if health_tips:
        print("\n💡 健康建議:")
        for i, tip in enumerate(health_tips, 1):
            print(f"  {i}. {tip}")
    
    print("\n" + "=" * 60)

# ============ 保存報告 ============
def save_report(analysis, image_path):
    """保存分析報告"""
    report_file = f"nutrition_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    data = analysis.get("data", {})
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 🥗 營養分析報告 (MiniMax-01)\n\n")
        f.write(f"**生成時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**圖片**: `{image_path}`\n")
        f.write(f"**模型**: MiniMax-01 (OpenRouter)\n\n")
        
        # 食物列表
        f.write("## 🍽️ 識別到的食物\n\n")
        for food in data.get('foods', []):
            f.write(f"- **{food.get('name', '未知')}**\n")
            if food.get('description'):
                f.write(f"  - {food.get('description')}\n")
        f.write("\n")
        
        # 總營養
        total = data.get('total_nutrition', {})
        if total:
            f.write("## 📊 總營養含量\n\n")
            f.write(f"| 營養素 | 含量 |\n")
            f.write(f"|--------|------|\n")
            f.write(f"| 🔥 卡路里 | {total.get('calories', 0)} kcal |\n")
            f.write(f"| 💪 蛋白質 | {total.get('protein', 0)}g |\n")
            f.write(f"| 🍚 碳水 | {total.get('carbs', 0)}g |\n")
            f.write(f"| 🥑 脂肪 | {total.get('fat', 0)}g |\n")
            f.write(f"| 🌾 纖維 | {total.get('fiber', 0)}g |\n\n")
        
        # 評分
        if data.get('meal_rating'):
            f.write(f"## ⭐ 餐食評分：{data.get('meal_rating')}\n\n")
        
        # 健康建議
        f.write("## 💡 健康建議\n\n")
        for i, tip in enumerate(data.get('health_tips', []), 1):
            f.write(f"{i}. {tip}\n")
    
    return report_file

# ============ 主函數 ============
def main():
    print("=" * 60)
    print("🥗 營養師 App - MiniMax-01 ONLY (OpenRouter)")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n使用方法：python3 nutritionist_openrouter_only.py <圖片路徑>")
        print("\n環境變數:")
        print("  export OPENROUTER_API_KEY='sk-or-...'")
        return 1
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"\n❌ 錯誤：找不到圖片 '{image_path}'")
        return 1
    
    if not OPENROUTER_API_KEY:
        print("\n❌ 錯誤：OPENROUTER_API_KEY 未設定")
        print("請執行：export OPENROUTER_API_KEY='sk-or-...'")
        return 1
    
    # 分析圖片
    result = analyze_food_miniMax(image_path)
    
    if not result.get("success"):
        print(f"\n❌ 分析失敗：{result.get('error')}")
        return 1
    
    # 顯示結果
    display_result(result)
    
    # 保存報告
    report_file = save_report(result, image_path)
    print(f"\n✅ 報告已保存：{report_file}")
    
    print("\n🎉 分析完成！")
    return 0

if __name__ == "__main__":
    sys.exit(main())
