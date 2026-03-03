#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
營養師 App 3.0 - Personal Nutrition Advisor
使用 OpenRouter MiniMax-01 Vision + SQLite 數據庫
追蹤餐食、營養、進度
"""

import os
import json
import base64
import urllib.request
import urllib.error
from datetime import datetime, date
from flask import Flask, request, jsonify, send_from_directory

# 導入數據庫模塊
import database as db

app = Flask(__name__, static_folder='.')

# ============ 配置 ============
PORT = int(os.environ.get("PORT", 8080))
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# 自動載入 .env 文件
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

# 初始化數據庫
db.init_db()

# ============ AI 分析 ============
def analyze_food_minimax(image_base64):
    """使用 MiniMax-01 識別食物並分析營養"""
    if not OPENROUTER_API_KEY:
        return {"success": False, "error": "OPENROUTER_API_KEY 未設置"}
    
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
                "calories": 數字,
                "protein": 數字,
                "carbs": 數字,
                "fat": 數字,
                "fiber": 數字
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
    "health_tips": ["建議 1", "建議 2", "建議 3"],
    "meal_rating": "優秀/良好/普通/需注意"
}

只返回 JSON，不要其他文字。"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/raycoderhk/2048-game",
        "X-Title": "Nutritionist App 3.0"
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
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                    },
                    {"type": "text", "text": prompt}
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
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            return {"success": True, "data": json.loads(content[start:end])}
        return {"success": False, "error": "JSON 解析失敗"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============ API Routes ============

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 用戶管理
@app.route('/api/user', methods=['GET'])
def get_user():
    """獲取用戶資料"""
    user_id = request.args.get('id', 1, type=int)
    user = db.get_user(user_id)
    if user:
        return jsonify({"success": True, "data": user})
    return jsonify({"success": False, "error": "用戶不存在"}), 404

@app.route('/api/user', methods=['POST'])
def create_user():
    """創建用戶"""
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"success": False, "error": "缺少姓名"}), 400
    
    try:
        user_id = db.create_user(
            name=data['name'],
            email=data.get('email'),
            age=data.get('age', 30),
            gender=data.get('gender', 'male'),
            height_cm=data.get('height_cm', 170),
            weight_kg=data.get('weight_kg', 70),
            activity_level=data.get('activity_level', 'moderate'),
            goal=data.get('goal', 'maintain'),
            target_weight_kg=data.get('target_weight_kg')
        )
        return jsonify({"success": True, "user_id": user_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/user', methods=['PUT'])
def update_user():
    """更新用戶資料"""
    data = request.get_json()
    user_id = data.get('id', 1)
    
    if not data:
        return jsonify({"success": False, "error": "缺少數據"}), 400
    
    update_fields = {k: v for k, v in data.items() 
                     if k not in ['id'] and v is not None}
    
    if db.update_user(user_id, **update_fields):
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "更新失敗"}), 500

# 餐食管理
@app.route('/api/meals', methods=['GET'])
def get_meals():
    """獲取餐食記錄"""
    user_id = request.args.get('user_id', 1, type=int)
    date_str = request.args.get('date')
    meals = db.get_meals(user_id, date_str)
    return jsonify({"success": True, "meals": meals})

@app.route('/api/meals', methods=['POST'])
def add_meal():
    """添加餐食記錄"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "缺少數據"}), 400
    
    user_id = data.get('user_id', 1)
    meal_type = data.get('meal_type', 'lunch')
    food_items = data.get('food_items', [])
    ai_analysis = data.get('ai_analysis')
    
    try:
        meal_id = db.add_meal(user_id, meal_type, food_items, ai_analysis)
        return jsonify({"success": True, "meal_id": meal_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/meals/<int:meal_id>', methods=['DELETE'])
def delete_meal(meal_id):
    """刪除餐食記錄"""
    if db.delete_meal(meal_id):
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "刪除失敗"}), 404

# AI 分析
@app.route('/api/analyze', methods=['POST'])
def analyze():
    """AI 分析食物圖片"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"success": False, "error": "缺少圖片數據"}), 400
        
        result = analyze_food_minimax(data['image'])
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 每日總結
@app.route('/api/daily', methods=['GET'])
def get_daily():
    """獲取每日總結"""
    user_id = request.args.get('user_id', 1, type=int)
    date_str = request.args.get('date')
    
    daily_log = db.get_daily_log(user_id, date_str)
    user = db.get_user(user_id)
    
    if not daily_log:
        daily_log = {
            'total_calories': 0,
            'total_protein_g': 0,
            'total_carbs_g': 0,
            'total_fat_g': 0,
            'meal_count': 0
        }
    
    # 計算目標完成度
    progress = {}
    if user:
        progress = {
            'calories': daily_log['total_calories'] / user['daily_calories'] * 100 if user['daily_calories'] else 0,
            'protein': daily_log['total_protein_g'] / user['daily_protein_g'] * 100 if user['daily_protein_g'] else 0,
            'carbs': daily_log['total_carbs_g'] / user['daily_carbs_g'] * 100 if user['daily_carbs_g'] else 0,
            'fat': daily_log['total_fat_g'] / user['daily_fat_g'] * 100 if user['daily_fat_g'] else 0
        }
    
    return jsonify({
        "success": True,
        "daily": daily_log,
        "progress": progress,
        "goals": {
            'calories': user['daily_calories'] if user else 2000,
            'protein': user['daily_protein_g'] if user else 150,
            'carbs': user['daily_carbs_g'] if user else 250,
            'fat': user['daily_fat_g'] if user else 65
        }
    })

# 每週總結
@app.route('/api/weekly', methods=['GET'])
def get_weekly():
    """獲取每週總結"""
    user_id = request.args.get('user_id', 1, type=int)
    weekly = db.get_weekly_summary(user_id)
    stats = db.get_nutrition_stats(user_id)
    return jsonify({"success": True, "weekly": weekly, "stats": stats})

# 進度追蹤
@app.route('/api/progress', methods=['GET'])
def get_progress():
    """獲取進度歷史"""
    user_id = request.args.get('user_id', 1, type=int)
    limit = request.args.get('limit', 30, type=int)
    progress = db.get_progress_history(user_id, limit)
    return jsonify({"success": True, "progress": progress})

@app.route('/api/progress', methods=['POST'])
def add_progress():
    """添加進度記錄"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "缺少數據"}), 400
    
    user_id = data.get('user_id', 1)
    
    try:
        progress_id = db.add_progress(user_id, **data)
        return jsonify({"success": True, "progress_id": progress_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 健康檢查
@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "openrouter_configured": bool(OPENROUTER_API_KEY),
        "model": "minimax/minimax-01",
        "version": "3.0 - Personal Nutrition Advisor",
        "database": "SQLite initialized"
    })

@app.route('/api/reset', methods=['POST'])
def reset_data():
    """重置用戶數據（測試用）"""
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM meals WHERE user_id = ?', (1,))
        cursor.execute('DELETE FROM daily_logs WHERE user_id = ?', (1,))
        cursor.execute('DELETE FROM progress WHERE user_id = ?', (1,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "數據已重置"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🥗 營養師 App 3.0 - Personal Nutrition Advisor")
    print("=" * 60)
    print(f"🌐 服務地址：http://localhost:{PORT}")
    print(f"🔑 OpenRouter API: {'✅' if OPENROUTER_API_KEY else '❌'}")
    print(f"📊 模型：minimax/minimax-01")
    print(f"💾 數據庫：SQLite (nutrition.db)")
    print("=" * 60)
    app.run(host='0.0.0.0', port=PORT, debug=False)
