#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
營養師 App Web Server - OpenRouter MiniMax-01 Version
使用 OpenRouter Vision API 進行食物識別 + 營養分析
支援 Zeabur 部署
"""

import os
import json
import base64
import urllib.request
import urllib.error
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

# ============ 配置 ============
PORT = int(os.environ.get("PORT", 8080))
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# 自動載入 .env 文件 (本地開發用)
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

# ============ API 處理 ============
def analyze_food_minimax(image_base64):
    """使用 MiniMax-01 識別食物並分析營養"""
    if not OPENROUTER_API_KEY:
        return {"success": False, "error": "OPENROUTER_API_KEY 未設置"}
    
    # 移除 data:image/jpeg;base64, 前綴
    if ',' in image_base64:
        image_base64 = image_base64.split(',')[1]
    
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
        "calories": 總卡路里，
        "protein": 總蛋白質，
        "carbs": 總碳水，
        "fat": 總脂肪，
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
        "X-Title": "Nutritionist App Web"
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
                            "url": f"data:image/jpeg;base64,{image_base64}"
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
        req = urllib.request.Request(
            OPENROUTER_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        content = result["choices"][0]["message"]["content"]
        
        # 提取 JSON
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            json_str = content[start:end]
            analysis = json.loads(json_str)
            return {"success": True, "data": analysis}
        else:
            return {"success": False, "error": "JSON 解析失敗"}
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"success": False, "error": f"OpenRouter API 錯誤：{e.code} - {error_body}"}
    except Exception as e:
        return {"success": False, "error": f"分析失敗：{str(e)}"}

# ============ Routes ============
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"success": False, "error": "缺少圖片數據"}), 400
        
        image_data = data['image']
        
        # 使用 MiniMax-01 分析
        result = analyze_food_minimax(image_data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "openrouter_configured": bool(OPENROUTER_API_KEY),
        "model": "minimax/minimax-01",
        "version": "2.0 - OpenRouter Vision"
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🥗 營養師 App Server - OpenRouter MiniMax-01")
    print("=" * 60)
    print(f"🌐 服務地址：http://localhost:{PORT}")
    print(f"🔑 OpenRouter API: {'✅' if OPENROUTER_API_KEY else '❌'}")
    print(f"📊 模型：minimax/minimax-01")
    print("=" * 60)
    app.run(host='0.0.0.0', port=PORT, debug=False)
