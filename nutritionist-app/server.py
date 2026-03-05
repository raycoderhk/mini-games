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
import auth as auth_module

app = Flask(__name__, static_folder='.')

# ============ 錯誤處理 ============
@app.errorhandler(Exception)
def handle_exception(e):
    """全局錯誤處理 - 返回 JSON 而非 HTML"""
    import traceback
    print(f"❌ Global error: {e}")
    traceback.print_exc()
    return jsonify({
        "success": False,
        "error": f"伺服器錯誤：{str(e)}"
    }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "找不到資源"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "error": "伺服器內部錯誤"}), 500

# ============ 配置 ============
PORT = int(os.environ.get("PORT", 8080))
# 使用阿里雲 DashScope API (Coding Plan)
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
DASHSCOPE_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

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

# 初始化數據庫 (必須在 auth 之前)
db.init_db()

# 初始化認證系統 (確保 users 表已存在)
auth_module.init_auth_db()

# ============ 圖片壓縮 ============
def compress_image_base64(image_base64, max_size=800, quality=80):
    """壓縮圖片以減少 API 請求大小和時間 (可選 - 依賴 PIL)"""
    try:
        import base64
        from PIL import Image
        import io
        
        if ',' in image_base64:
            image_base64 = image_base64.split(',')[1]
        
        image_data = base64.b64decode(image_base64)
        img = Image.open(io.BytesIO(image_data))
        
        # 轉換為 RGB (移除 alpha channel)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        # 縮放圖片
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # 壓縮並重新編碼
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        
        compressed_base64 = base64.b64encode(output.getvalue()).decode('utf-8')
        return compressed_base64
    except ImportError:
        # PIL 未安裝，跳過壓縮
        print("⚠️ PIL 未安裝，跳過圖片壓縮")
        if ',' in image_base64:
            return image_base64.split(',')[1]
        return image_base64
    except Exception as e:
        print(f"圖片壓縮失敗：{e}")
        if ',' in image_base64:
            return image_base64.split(',')[1]
        return image_base64  # 返回原圖

# ============ AI 分析 ============
def analyze_food_minimax(image_base64):
    """使用阿里雲 Qwen-VL 識別食物並分析營養"""
    if not DASHSCOPE_API_KEY:
        return {"success": False, "error": "DASHSCOPE_API_KEY 未設置"}
    
    # 壓縮圖片
    image_base64 = compress_image_base64(image_base64)
    
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
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 使用 Qwen-VL-Max (阿里雲最強視覺模型)
    payload = {
        "model": "qwen-vl-max",
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
            DASHSCOPE_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        # MiniMax-01 需要較長時間，設置 90 秒超時
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        content = result["choices"][0]["message"]["content"]
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            return {"success": True, "data": json.loads(content[start:end])}
        return {"success": False, "error": "JSON 解析失敗"}
            
    except urllib.error.URLError as e:
        if "timed out" in str(e).lower():
            return {"success": False, "error": "AI 分析超時，請重試或縮小圖片"}
        return {"success": False, "error": f"網絡錯誤：{e}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============ API Routes ============

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/test')
def test():
    """Simple test endpoint to verify server is responding"""
    return jsonify({
        "status": "ok",
        "message": "Server is running!",
        "timestamp": "2026-03-03T09:20:00Z"
    })

# ============ 認證 API ============
@app.route('/api/auth/send-otp', methods=['POST'])
def send_otp():
    """發送 OTP 到電話號碼"""
    data = request.get_json()
    if not data or not data.get('phone'):
        return jsonify({"success": False, "error": "缺少電話號碼"}), 400
    
    phone = data['phone']
    
    # 驗證電話格式（簡單驗證）
    if len(phone) < 8 or not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
        return jsonify({"success": False, "error": "電話號碼格式無效"}), 400
    
    result = auth_module.send_otp(phone)
    return jsonify(result)

@app.route('/api/auth/verify-otp', methods=['POST'])
def verify_otp():
    """驗證 OTP 並登入"""
    try:
        data = request.get_json()
        if not data or not data.get('phone') or not data.get('otp'):
            return jsonify({"success": False, "error": "缺少電話號碼或 OTP"}), 400
        
        phone = data['phone']
        otp = data['otp']
        name = data.get('name')
        
        print(f"🔐 Verifying OTP for {phone}: {otp}")
        
        # 驗證 OTP
        verify_result = auth_module.verify_otp(phone, otp)
        print(f"📋 OTP result: {verify_result}")
        
        if not verify_result['success']:
            return jsonify(verify_result), 400
        
        # 獲取或創建用戶
        user = auth_module.get_or_create_user_by_phone(phone, name)
        print(f"👤 User: {user}")
        
        # 創建會話
        token = auth_module.create_session(user['id'])
        
        return jsonify({
            "success": True,
            "message": "登入成功",
            "token": token,
            "user": {
                "id": user['id'],
                "name": user['name'],
                "phone": user['phone'],
                "email": user.get('email')
            }
        })
    except Exception as e:
        print(f"❌ verify_otp error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": f"伺服器錯誤：{str(e)}"}), 500

@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    """獲取當前登入用戶"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not token:
        return jsonify({"success": False, "error": "未登入"}), 401
    
    user = auth_module.validate_session(token)
    if not user:
        return jsonify({"success": False, "error": "會話無效或已過期"}), 401
    
    return jsonify({
        "success": True,
        "user": {
            "id": user['id'],
            "name": user['name'],
            "phone": user.get('phone'),
            "email": user.get('email'),
            "age": user.get('age'),
            "gender": user.get('gender'),
            "height_cm": user.get('height_cm'),
            "weight_kg": user.get('weight_kg'),
            "activity_level": user.get('activity_level'),
            "goal": user.get('goal'),
            "daily_calories": user.get('daily_calories'),
            "daily_protein_g": user.get('daily_protein_g'),
            "daily_carbs_g": user.get('daily_carbs_g'),
            "daily_fat_g": user.get('daily_fat_g')
        }
    })

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """登出"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not token:
        return jsonify({"success": False, "error": "未登入"}), 401
    
    auth_module.revoke_session(token)
    return jsonify({"success": True, "message": "已登出"})

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
        "dashscope_configured": bool(DASHSCOPE_API_KEY),
        "model": "qwen-vl-max",
        "provider": "Aliyun DashScope",
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
