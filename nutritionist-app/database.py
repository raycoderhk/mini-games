#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
營養師 App 3.0 - Database Module
SQLite 數據庫存儲用戶資料、餐食記錄、進度追蹤
"""

import sqlite3
import json
import os
from datetime import datetime, date
from typing import Optional, List, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), 'nutrition.db')

def get_db():
    """獲取數據庫連接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化數據庫"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 用戶資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER,
            gender TEXT CHECK(gender IN ('male', 'female', 'other')),
            height_cm REAL,
            weight_kg REAL,
            activity_level TEXT CHECK(activity_level IN ('sedentary', 'light', 'moderate', 'active', 'very_active')),
            goal TEXT CHECK(goal IN ('gain', 'lose', 'maintain')),
            target_weight_kg REAL,
            daily_calories INTEGER,
            daily_protein_g INTEGER,
            daily_carbs_g INTEGER,
            daily_fat_g INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 餐食記錄表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            meal_type TEXT CHECK(meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
            food_items TEXT NOT NULL,
            calories INTEGER,
            protein_g REAL,
            carbs_g REAL,
            fat_g REAL,
            fiber_g REAL,
            image_url TEXT,
            ai_analysis TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # 每日總結表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL UNIQUE,
            total_calories INTEGER,
            total_protein_g REAL,
            total_carbs_g REAL,
            total_fat_g REAL,
            total_fiber_g REAL,
            meal_count INTEGER,
            water_intake_ml INTEGER DEFAULT 0,
            exercise_minutes INTEGER DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # 進度追蹤表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            weight_kg REAL,
            body_fat_percent REAL,
            muscle_mass_kg REAL,
            waist_cm REAL,
            chest_cm REAL,
            hips_cm REAL,
            notes TEXT,
            photo_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ 數據庫初始化完成")

# ============ 用戶管理 ============
def create_user(name: str, email: Optional[str] = None, **kwargs) -> int:
    """創建用戶"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 計算每日營養目標
    age = kwargs.get('age', 30)
    gender = kwargs.get('gender', 'male')
    height = kwargs.get('height_cm', 170)
    weight = kwargs.get('weight_kg', 70)
    activity = kwargs.get('activity_level', 'moderate')
    goal = kwargs.get('goal', 'maintain')
    
    # 計算 BMR (Mifflin-St Jeor)
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # 活動係數
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    tdee = bmr * activity_multipliers.get(activity, 1.55)
    
    # 根據目標調整
    if goal == 'lose':
        tdee *= 0.85  # 減 15%
    elif goal == 'gain':
        tdee *= 1.15  # 加 15%
    
    daily_calories = int(tdee)
    
    # 宏量營養素分配 (蛋白質 30%, 碳水 40%, 脂肪 30%)
    protein = int((daily_calories * 0.3) / 4)
    carbs = int((daily_calories * 0.4) / 4)
    fat = int((daily_calories * 0.3) / 9)
    
    cursor.execute('''
        INSERT INTO users (name, email, age, gender, height_cm, weight_kg, 
                          activity_level, goal, target_weight_kg,
                          daily_calories, daily_protein_g, daily_carbs_g, daily_fat_g)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, age, gender, height, weight, activity, goal,
          kwargs.get('target_weight_kg'), daily_calories, protein, carbs, fat))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return user_id

def get_user(user_id: int = 1) -> Optional[Dict]:
    """獲取用戶資料"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def update_user(user_id: int, **kwargs) -> bool:
    """更新用戶資料"""
    conn = get_db()
    cursor = conn.cursor()
    
    fields = []
    values = []
    for key, value in kwargs.items():
        if key in ['name', 'email', 'age', 'gender', 'height_cm', 'weight_kg',
                   'activity_level', 'goal', 'target_weight_kg',
                   'daily_calories', 'daily_protein_g', 'daily_carbs_g', 'daily_fat_g']:
            fields.append(f"{key} = ?")
            values.append(value)
    
    if not fields:
        return False
    
    fields.append("updated_at = CURRENT_TIMESTAMP")
    values.append(user_id)
    
    cursor.execute(f'UPDATE users SET {", ".join(fields)} WHERE id = ?', values)
    conn.commit()
    conn.close()
    
    return True

# ============ 餐食管理 ============
def add_meal(user_id: int, meal_type: str, food_items: List[Dict], 
             ai_analysis: Optional[str] = None, image_url: Optional[str] = None) -> int:
    """添加餐食記錄"""
    conn = get_db()
    cursor = conn.cursor()
    
    today = date.today().isoformat()
    
    # 計算總營養 (支援嵌套 nutrition 結構和扁平結構)
    def get_nutrition_value(food, key):
        """獲取營養值，支援嵌套和扁平結構"""
        # 先嘗試嵌套結構 (AI API 返回的格式)
        if 'nutrition' in food:
            return food.get('nutrition', {}).get(key, 0)
        # 再嘗試扁平結構 (向後兼容)
        return food.get(key, 0)
    
    total_calories = sum(get_nutrition_value(f, 'calories') for f in food_items)
    total_protein = sum(get_nutrition_value(f, 'protein') for f in food_items)
    total_carbs = sum(get_nutrition_value(f, 'carbs') for f in food_items)
    total_fat = sum(get_nutrition_value(f, 'fat') for f in food_items)
    total_fiber = sum(get_nutrition_value(f, 'fiber') for f in food_items)
    
    food_items_json = json.dumps(food_items, ensure_ascii=False)
    
    cursor.execute('''
        INSERT INTO meals (user_id, date, meal_type, food_items, calories,
                          protein_g, carbs_g, fat_g, fiber_g, image_url, ai_analysis)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, today, meal_type, food_items_json, total_calories,
          total_protein, total_carbs, total_fat, total_fiber, image_url, ai_analysis))
    
    meal_id = cursor.lastrowid
    
    # 更新每日總結
    update_daily_log(conn, user_id, today)
    
    conn.commit()
    conn.close()
    
    return meal_id

def get_meals(user_id: int, date_str: Optional[str] = None) -> List[Dict]:
    """獲取餐食記錄"""
    conn = get_db()
    cursor = conn.cursor()
    
    if date_str:
        cursor.execute('''
            SELECT * FROM meals 
            WHERE user_id = ? AND date = ?
            ORDER BY created_at DESC
        ''', (user_id, date_str))
    else:
        cursor.execute('''
            SELECT * FROM meals 
            WHERE user_id = ? AND date = date('now')
            ORDER BY meal_type, created_at DESC
        ''', (user_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def delete_meal(meal_id: int) -> bool:
    """刪除餐食記錄"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM meals WHERE id = ?', (meal_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# ============ 每日總結 ============
def update_daily_log(conn, user_id: int, date_str: str):
    """更新每日總結"""
    cursor = conn.cursor()
    
    # 計算今日總和
    cursor.execute('''
        SELECT 
            COALESCE(SUM(calories), 0) as total_calories,
            COALESCE(SUM(protein_g), 0) as total_protein,
            COALESCE(SUM(carbs_g), 0) as total_carbs,
            COALESCE(SUM(fat_g), 0) as total_fat,
            COALESCE(SUM(fiber_g), 0) as total_fiber,
            COUNT(*) as meal_count
        FROM meals
        WHERE user_id = ? AND date = ?
    ''', (user_id, date_str))
    
    row = cursor.fetchone()
    
    # 檢查是否已存在
    cursor.execute('SELECT id FROM daily_logs WHERE user_id = ? AND date = ?', (user_id, date_str))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute('''
            UPDATE daily_logs 
            SET total_calories = ?, total_protein_g = ?, total_carbs_g = ?, 
                total_fat_g = ?, total_fiber_g = ?, meal_count = ?
            WHERE user_id = ? AND date = ?
        ''', (row['total_calories'], row['total_protein'], row['total_carbs'],
              row['total_fat'], row['total_fiber'], row['meal_count'], user_id, date_str))
    else:
        cursor.execute('''
            INSERT INTO daily_logs (user_id, date, total_calories, total_protein_g,
                                   total_carbs_g, total_fat_g, total_fiber_g, meal_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, date_str, row['total_calories'], row['total_protein'],
              row['total_carbs'], row['total_fat'], row['total_fiber'], row['meal_count']))

def get_daily_log(user_id: int, date_str: Optional[str] = None) -> Optional[Dict]:
    """獲取每日總結"""
    conn = get_db()
    cursor = conn.cursor()
    
    if not date_str:
        date_str = date.today().isoformat()
    
    cursor.execute('SELECT * FROM daily_logs WHERE user_id = ? AND date = ?', (user_id, date_str))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def get_weekly_summary(user_id: int) -> List[Dict]:
    """獲取每週總結"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM daily_logs 
        WHERE user_id = ? AND date >= date('now', '-7 days')
        ORDER BY date DESC
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ============ 進度追蹤 ============
def add_progress(user_id: int, **kwargs) -> int:
    """添加進度記錄"""
    conn = get_db()
    cursor = conn.cursor()
    
    today = date.today().isoformat()
    
    cursor.execute('''
        INSERT INTO progress (user_id, date, weight_kg, body_fat_percent, 
                             muscle_mass_kg, waist_cm, chest_cm, hips_cm, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, today, kwargs.get('weight_kg'), kwargs.get('body_fat_percent'),
          kwargs.get('muscle_mass_kg'), kwargs.get('waist_cm'), kwargs.get('chest_cm'),
          kwargs.get('hips_cm'), kwargs.get('notes')))
    
    progress_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return progress_id

def get_progress_history(user_id: int, limit: int = 30) -> List[Dict]:
    """獲取進度歷史"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM progress 
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT ?
    ''', (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ============ 統計分析 ============
def get_nutrition_stats(user_id: int, days: int = 7) -> Dict:
    """獲取營養統計"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            AVG(total_calories) as avg_calories,
            AVG(total_protein_g) as avg_protein,
            AVG(total_carbs_g) as avg_carbs,
            AVG(total_fat_g) as avg_fat,
            SUM(total_calories) as total_calories,
            COUNT(*) as days_logged
        FROM daily_logs
        WHERE user_id = ? AND date >= date('now', ? || ' days')
    ''', (user_id, -days))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return {}

# 初始化時調用
if __name__ == '__main__':
    init_db()
    print("✅ 數據庫模塊測試完成")
