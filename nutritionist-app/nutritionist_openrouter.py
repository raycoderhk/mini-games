#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
營養師 App - OpenRouter Vision + Aliyun Nutrition
使用 MiniMax-01 (OpenRouter Free) 識別食物圖片
使用 Qwen3.5-Plus (Aliyun Coding Plan) 分析營養

優點：
- MiniMax-01: 免費視覺識別，準確度高
- Qwen3.5-Plus: 專業營養分析，中文優化
- 雙模型協作，發揮各自優勢
"""

import urllib.request
import urllib.error
import json
import base64
import os
import sys
from datetime import datetime

# ============ 配置 ============
# OpenRouter API (MiniMax-01 for Vision)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Aliyun API (Qwen3.5-Plus for Nutrition Analysis)
ALIYUN_API_KEY = os.environ.get("ALIYUN_API_KEY", "")
ALIYUN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# ============ 食物識別 (OpenRouter + MiniMax-01) ============
def recognize_food_openrouter(image_path):
    """使用 OpenRouter MiniMax-01 識別食物圖片"""
    print("\n🔍 使用 MiniMax-01 (OpenRouter) 識別食物...")
    
    # 轉換圖片為 Base64
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    print(f"✅ 圖片載入成功 ({len(image_data)} bytes)")
    
    # MiniMax-01 Prompt
    prompt = """請仔細分析這張食物圖片，識別圖片中的所有食物。

請以 JSON 格式返回：
{
    "foods": [
        {"name": "食物名稱（中文）", "confidence": 0.95, "description": "簡單描述"},
        ...
    ],
    "image_quality": "good/medium/poor",
    "notes": "任何需要註意的事項"
}

只返回 JSON，不要其他文字。"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/raycoderhk/nutritionist-app",
        "X-Title": "Nutritionist App"
    }
    
    # MiniMax-01 支援 vision
    payload = {
        "model": "minimax/minimax-01",
        "max_tokens": 2048,  # 限制 token 用量避免 402 錯誤
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
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        content = result["choices"][0]["message"]["content"]
        print(f"✅ OpenRouter API 調用成功！")
        
        # 提取 JSON
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            json_str = content[start:end]
            recognition = json.loads(json_str)
            return {"success": True, "data": recognition, "model": "MiniMax-01"}
        else:
            return {"success": False, "error": "JSON 解析失敗", "raw": content}
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"success": False, "error": f"HTTP {e.code}: {e.reason} - {error_body}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============ 營養分析 (Aliyun Qwen3.5-Plus) ============
def analyze_nutrition(food_items):
    """使用 Qwen3.5-Plus 分析食物營養成分"""
    print("\n📊 使用 Qwen3.5-Plus (Aliyun) 分析營養成分...")
    
    foods_str = ", ".join([f.get("name", "") for f in food_items])
    
    prompt = f"""你是一位專業營養師。請分析以下食物的營養成分：

{foods_str}

請以 JSON 格式返回詳細營養信息：
{{
    "foods": [
        {{
            "name": "食物名稱",
            "serving_size": "份量（克）",
            "calories": 數字（千卡）,
            "protein": 數字（克）,
            "carbs": 數字（克）,
            "fat": 數字（克）,
            "fiber": 數字（克）,
            "sodium": 數字（毫克）,
            "vitamins": ["維生素 A", "維生素 C", ...]
        }}
    ],
    "total": {{
        "calories": 總卡路里,
        "protein": 總蛋白質,
        "carbs": 總碳水,
        "fat": 總脂肪,
        "fiber": 總纖維
    }},
    "health_tips": [
        "建議 1",
        "建議 2",
        "建議 3"
    ],
    "meal_rating": "優秀/良好/普通/需注意"
}}

只返回 JSON，不要其他文字。"""

    headers = {
        "Authorization": f"Bearer {ALIYUN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen3.5-plus",
        "messages": [
            {"role": "system", "content": "你是一位專業營養師，提供準確的營養分析和健康建議。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        print("\n📡 調用 Aliyun Qwen3.5-Plus API...")
        req = urllib.request.Request(
            ALIYUN_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        content = result["choices"][0]["message"]["content"]
        print(f"✅ Aliyun API 調用成功！")
        
        # 提取 JSON
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            json_str = content[start:end]
            nutrition = json.loads(json_str)
            return {"success": True, "data": nutrition}
        else:
            return {"success": False, "error": "JSON 解析失敗", "raw": content}
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"success": False, "error": f"HTTP {e.code}: {e.reason} - {error_body}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============ 顯示結果 ============
def display_result(recognition, nutrition):
    """顯示完整分析結果"""
    print("\n" + "=" * 60)
    print("📊 完整分析結果")
    print("=" * 60)
    
    # 食物識別
    rec_data = recognition.get("data", {})
    foods = rec_data.get("foods", [])
    
    print(f"\n🍽️ 識別到的食物 ({len(foods)} 項):")
    for food in foods:
        name = food.get("name", "未知")
        confidence_raw = food.get("confidence", 0)
        # 處理 confidence 可能是 string 或數字
        try:
            confidence = float(confidence_raw) * 100 if isinstance(confidence_raw, (int, float)) else float(confidence_raw.replace('%', '')) if isinstance(confidence_raw, str) else 0
        except:
            confidence = 0
        desc = food.get("description", "")
        print(f"  • {name} ({confidence:.0f}% 信心) - {desc}")
    
    # 營養成分
    nutr_data = nutrition.get("data", {})
    if nutr_data:
        print("\n📈 營養成分:")
        
        # 每種食物
        for food in nutr_data.get("foods", []):
            print(f"\n  {food.get('name', 'N/A')} ({food.get('serving_size', '未知份量')}):")
            print(f"    🔥 卡路里：{food.get('calories', 0)} kcal")
            print(f"    💪 蛋白質：{food.get('protein', 0)}g")
            print(f"    🍚 碳水化合物：{food.get('carbs', 0)}g")
            print(f"    🥑 脂肪：{food.get('fat', 0)}g")
            print(f"    🌾 纖維：{food.get('fiber', 0)}g")
            print(f"    🧂 鈉：{food.get('sodium', 0)}mg")
        
        # 總計
        total = nutr_data.get("total", {})
        if total:
            print("\n📊 總計:")
            print(f"  🔥 卡路里：{total.get('calories', 0)} kcal")
            print(f"  💪 蛋白質：{total.get('protein', 0)}g")
            print(f"  🍚 碳水化合物：{total.get('carbs', 0)}g")
            print(f"  🥑 脂肪：{total.get('fat', 0)}g")
            print(f"  🌾 纖維：{total.get('fiber', 0)}g")
        
        # 餐食評分
        rating = nutr_data.get("meal_rating", "未知")
        print(f"\n⭐ 餐食評分：{rating}")
    
    # 健康建議
    health_tips = nutr_data.get("health_tips", [])
    if health_tips:
        print("\n💡 健康建議:")
        for i, tip in enumerate(health_tips, 1):
            print(f"  {i}. {tip}")
    
    print("\n" + "=" * 60)

# ============ 保存報告 ============
def save_report(recognition, nutrition, image_path):
    """保存分析報告為 Markdown"""
    report_file = f"nutrition_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    rec_data = recognition.get("data", {})
    nutr_data = nutrition.get("data", {})
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 🥗 營養分析報告\n\n")
        f.write(f"**生成時間：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**圖片：** `{image_path}`\n\n")
        f.write(f"**識別模型：** MiniMax-01 (OpenRouter)\n")
        f.write(f"**分析模型：** Qwen3.5-Plus (Aliyun)\n\n")
        
        # 食物列表
        f.write(f"## 🍽️ 識別到的食物\n\n")
        for food in rec_data.get('foods', []):
            confidence = food.get('confidence', 0) * 100
            f.write(f"- **{food.get('name', '未知')}** ({confidence:.0f}%)\n")
            if food.get('description'):
                f.write(f"  - {food.get('description')}\n")
        f.write("\n")
        
        # 營養成分
        f.write(f"## 📊 營養成分\n\n")
        f.write("### 每種食物\n\n")
        for food in nutr_data.get('foods', []):
            f.write(f"#### {food.get('name', 'N/A')} ({food.get('serving_size', '未知份量')})\n\n")
            f.write(f"| 營養素 | 含量 |\n")
            f.write(f"|--------|------|\n")
            f.write(f"| 🔥 卡路里 | {food.get('calories', 0)} kcal |\n")
            f.write(f"| 💪 蛋白質 | {food.get('protein', 0)}g |\n")
            f.write(f"| 🍚 碳水 | {food.get('carbs', 0)}g |\n")
            f.write(f"| 🥑 脂肪 | {food.get('fat', 0)}g |\n")
            f.write(f"| 🌾 纖維 | {food.get('fiber', 0)}g |\n")
            f.write(f"| 🧂 鈉 | {food.get('sodium', 0)}mg |\n\n")
        
        # 總計
        total = nutr_data.get('total', {})
        if total:
            f.write("### 總計\n\n")
            f.write(f"| 營養素 | 總量 |\n")
            f.write(f"|--------|------|\n")
            f.write(f"| 🔥 卡路里 | {total.get('calories', 0)} kcal |\n")
            f.write(f"| 💪 蛋白質 | {total.get('protein', 0)}g |\n")
            f.write(f"| 🍚 碳水 | {total.get('carbs', 0)}g |\n")
            f.write(f"| 🥑 脂肪 | {total.get('fat', 0)}g |\n")
            f.write(f"| 🌾 纖維 | {total.get('fiber', 0)}g |\n\n")
        
        # 評分
        rating = nutr_data.get('meal_rating', '未知')
        f.write(f"### ⭐ 餐食評分：{rating}\n\n")
        
        # 健康建議
        f.write(f"## 💡 健康建議\n\n")
        for i, tip in enumerate(nutr_data.get('health_tips', []), 1):
            f.write(f"{i}. {tip}\n")
    
    return report_file

# ============ 主函數 ============
def main():
    print("=" * 60)
    print("🥗 營養師 App - OpenRouter Vision + Aliyun Nutrition")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n使用方法：python3 nutritionist_openrouter.py <圖片路徑>")
        print("\n環境變數設定:")
        print("  export OPENROUTER_API_KEY='sk-or-...'")
        print("  export ALIYUN_API_KEY='sk-...'")
        return 1
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"\n❌ 錯誤：找不到圖片 '{image_path}'")
        return 1
    
    # 檢查 API Keys
    if not OPENROUTER_API_KEY:
        print("\n⚠️ 警告：OPENROUTER_API_KEY 未設定")
        print("請執行：export OPENROUTER_API_KEY='sk-or-...'")
        return 1
    
    if not ALIYUN_API_KEY:
        print("\n⚠️ 警告：ALIYUN_API_KEY 未設定")
        print("請執行：export ALIYUN_API_KEY='sk-...'")
        return 1
    
    # 1. 識別食物 (OpenRouter MiniMax-01)
    recognition_result = recognize_food_openrouter(image_path)
    
    if not recognition_result.get("success"):
        print(f"\n❌ 食物識別失敗：{recognition_result.get('error')}")
        return 1
    
    foods = recognition_result['data'].get("foods", [])
    
    if not foods:
        print("\n❌ 無法識別食物")
        return 1
    
    print(f"\n✅ 識別成功：{len(foods)} 種食物")
    
    # 2. 營養分析 (Aliyun Qwen3.5-Plus)
    nutrition_result = analyze_nutrition(foods)
    
    if not nutrition_result.get("success"):
        print(f"\n⚠️ 營養分析失敗：{nutrition_result.get('error')}")
        # 仍然顯示識別結果
        display_result(recognition_result, {"success": True, "data": {}})
        return 1
    
    # 3. 顯示結果
    display_result(recognition_result, nutrition_result)
    
    # 4. 保存報告
    report_file = save_report(recognition_result, nutrition_result, image_path)
    print(f"\n✅ 報告已保存：{report_file}")
    
    print("\n🎉 分析完成！")
    return 0

if __name__ == "__main__":
    sys.exit(main())
