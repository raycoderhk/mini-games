#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
營養師 App Web Server (Flask Version for Zeabur)
提供 API 接口調用 Hugging Face + Aliyun AI
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
HF_TOKEN = os.environ.get("HF_API_KEY", "")
ALIYUN_API_KEY = os.environ.get("ALIYUN_API_KEY", "")

MODEL_ID = "google/siglip-so400m-patch14-384"
HF_API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
ALIYUN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# ============ API 處理 ============
def recognize_food(image_data):
    """識別食物圖片 (Hugging Face API)"""
    if not HF_TOKEN:
        return {"success": False, "error": "HF_API_KEY 未設置"}
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/octet-stream"
    }
    
    try:
        req = urllib.request.Request(HF_API_URL, data=image_data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        if isinstance(result, list):
            return {"success": True, "foods": [item.get("label", "") for item in result[:5]]}
        return {"success": True, "foods": [str(result)]}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HF API 錯誤：{e.code} - {e.reason}"}
    except Exception as e:
        return {"success": False, "error": f"識別失敗：{str(e)}"}

def analyze_nutrition(food_items):
    """分析營養成分 (Aliyun Qwen API)"""
    if not ALIYUN_API_KEY:
        return {"success": False, "error": "ALIYUN_API_KEY 未設置"}
    
    prompt = f"請分析以下食物的營養成分：{', '.join(food_items)}，以 JSON 格式返回營養信息（卡路里、蛋白質、碳水化合物、脂肪）"
    headers = {"Authorization": f"Bearer {ALIYUN_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "qwen-plus",
        "messages": [
            {"role": "system", "content": "你是專業營養師，請以 JSON 格式返回營養數據"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        req = urllib.request.Request(ALIYUN_API_URL, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        content = result["choices"][0]["message"]["content"]
        start, end = content.find("{"), content.rfind("}") + 1
        if start >= 0 and end > start:
            return {"success": True, "data": json.loads(content[start:end])}
        return {"success": False, "error": "JSON 解析失敗"}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"Aliyun API 錯誤：{e.code}"}
    except Exception as e:
        return {"success": False, "error": f"營養分析失敗：{str(e)}"}

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
        
        image_base64 = data['image']
        if ',' in image_base64:
            image_base64 = image_base64.split(',')[1]
        
        image_data = base64.b64decode(image_base64)
        
        # 1. 識別食物
        recognition = recognize_food(image_data)
        if not recognition.get('success'):
            return jsonify(recognition), 500
        
        # 2. 營養分析
        nutrition = analyze_nutrition(recognition['foods'])
        
        return jsonify({
            "success": True,
            "foods": recognition['foods'],
            "nutrition": nutrition
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "hf_configured": bool(HF_TOKEN),
        "aliyun_configured": bool(ALIYUN_API_KEY)
    })

if __name__ == '__main__':
    print(f"🥗 營養師 App Server - http://localhost:{PORT}")
    print(f"📊 HF API 配置：{'✅' if HF_TOKEN else '❌'}")
    print(f"📊 Aliyun API 配置：{'✅' if ALIYUN_API_KEY else '❌'}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
