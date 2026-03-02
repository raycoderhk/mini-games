#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
營養師 App - 使用 Aliyun Qwen-VL 識別食物 + 營養分析
單一 API 搞掂圖片識別 + 營養分析！
"""

import urllib.request
import urllib.error
import json
import base64
import os
import sys
from datetime import datetime

# ============ 配置 ============
ALIYUN_API_KEY = os.environ.get("ALIYUN_API_KEY", "sk-sp-8eec812bc72d47c3866d388cef6372f8")
ALIYUN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# ============ Qwen-VL 圖片分析 ============
def analyze_food_image(image_path):
    """使用 Qwen-VL 識別食物並分析營養"""
    print("\n🔍 使用 Qwen-VL 分析食物圖片...")
    
    # 轉換圖片為 Base64
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    print(f"✅ 圖片載入成功 ({len(image_data)} bytes)")
    
    # Qwen-VL Prompt
    prompt = """請分析這張食物圖片：

1. 識別圖片中的所有食物（列出食物名稱）
2. 分析每種食物的營養成分（卡路里、蛋白質、碳水化合物、脂肪、纖維）
3. 計算總營養含量
4. 提供 2-3 條健康建議

請以 JSON 格式返回：
{
    "foods": ["食物 1", "食物 2", ...],
    "nutrition": {
        "foods": [
            {"name": "食物名", "calories": 數字，"protein": 數字，"carbs": 數字，"fat": 數字，"fiber": 數字}
        ],
        "total": {"calories": 總卡路里，"protein": 總蛋白質，"carbs": 總碳水，"fat": 總脂肪，"fiber": 總纖維}
    },
    "health_tips": ["建議 1", "建議 2", "建議 3"]
}

只返回 JSON，不要其他文字。"""

    headers = {
        "Authorization": f"Bearer {ALIYUN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Qwen-VL 需要特殊格式
    payload = {
        "model": "qwen-vl-plus",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"image": f"data:image/jpeg;base64,{image_data}"},
                    {"text": prompt}
                ]
            }
        ]
    }
    
    try:
        print("\n📡 調用 Aliyun Qwen-VL API...")
        req = urllib.request.Request(
            ALIYUN_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        content = result["choices"][0]["message"]["content"]
        print(f"✅ API 調用成功！")
        
        # 提取 JSON
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            json_str = content[start:end]
            analysis = json.loads(json_str)
            return {"success": True, "data": analysis}
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
    print(f"\n🍽️ 識別到的食物：{', '.join(foods)}")
    
    # 營養成分
    nutrition = data.get("nutrition", {})
    if nutrition:
        print("\n📈 營養成分:")
        
        # 每種食物
        for food in nutrition.get("foods", []):
            print(f"\n  {food.get('name', 'N/A')}:")
            print(f"    🔥 卡路里：{food.get('calories', 0)} kcal")
            print(f"    💪 蛋白質：{food.get('protein', 0)}g")
            print(f"    🍚 碳水化合物：{food.get('carbs', 0)}g")
            print(f"    🥑 脂肪：{food.get('fat', 0)}g")
            print(f"    🌾 纖維：{food.get('fiber', 0)}g")
        
        # 總計
        total = nutrition.get("total", {})
        if total:
            print("\n📊 總計:")
            print(f"  🔥 卡路里：{total.get('calories', 0)} kcal")
            print(f"  💪 蛋白質：{total.get('protein', 0)}g")
            print(f"  🍚 碳水化合物：{total.get('carbs', 0)}g")
            print(f"  🥑 脂肪：{total.get('fat', 0)}g")
            print(f"  🌾 纖維：{total.get('fiber', 0)}g")
    
    # 健康建議
    health_tips = data.get("health_tips", [])
    if health_tips:
        print("\n💡 健康建議:")
        for i, tip in enumerate(health_tips, 1):
            print(f"  {i}. {tip}")
    
    print("\n" + "=" * 60)

# ============ 主函數 ============
def main():
    print("=" * 60)
    print("🥗 營養師 App - Aliyun Qwen-VL")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n使用方法：python3 nutritionist_qwen_vl.py <圖片路徑>")
        return 1
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"\n❌ 錯誤：找不到圖片 '{image_path}'")
        return 1
    
    # 分析圖片
    result = analyze_food_image(image_path)
    
    if not result.get("success"):
        print(f"\n❌ 分析失敗：{result.get('error')}")
        return 1
    
    # 顯示結果
    display_result(result)
    
    # 保存報告
    report_file = f"nutrition_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 🥗 營養分析報告\n\n")
        f.write(f"**生成時間：** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"## 🍽️ 識別到的食物\n\n")
        for food in result['data'].get('foods', []):
            f.write(f"- {food}\n")
        f.write(f"\n## 📊 營養成分\n\n```json\n")
        f.write(json.dumps(result['data'].get('nutrition', {}), indent=2, ensure_ascii=False))
        f.write(f"\n```\n\n## 💡 健康建議\n\n")
        for tip in result['data'].get('health_tips', []):
            f.write(f"- {tip}\n")
    
    print(f"\n✅ 報告已保存：{report_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
