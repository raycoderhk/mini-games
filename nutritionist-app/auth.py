#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
營養師 App - 電話號碼認證系統
Phone Number Authentication
"""

import sqlite3
import hashlib
import secrets
import os
from datetime import datetime, timedelta
from typing import Optional, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), 'nutrition.db')

def get_db():
    """獲取數據庫連接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_auth_db():
    """初始化認證相關的數據庫表"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 電話號碼驗證表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phone_verifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            otp TEXT NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 用戶會話表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ 認證系統數據庫初始化完成")

# ============ OTP 管理 ============
def generate_otp() -> str:
    """生成 6 位數 OTP"""
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def send_otp(phone: str) -> Dict:
    """發送 OTP（模擬 - 實際可接入 SMS 服務）"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 清理過期的 OTP
    cursor.execute('DELETE FROM phone_verifications WHERE expires_at < CURRENT_TIMESTAMP')
    
    # 生成 OTP
    otp = generate_otp()
    expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()
    
    # 儲存 OTP
    cursor.execute('''
        INSERT INTO phone_verifications (phone, otp, expires_at)
        VALUES (?, ?, ?)
    ''', (phone, otp, expires_at))
    
    conn.commit()
    conn.close()
    
    # 實際應用：這裡接入 Twilio / 阿里雲 SMS
    # 開發階段：返回 OTP 方便測試
    print(f"\n📱 OTP for {phone}: {otp}")
    
    return {
        "success": True,
        "message": "OTP 已發送（開發模式：請查看控制台）",
        "otp": otp  # 僅開發模式，生產環境應移除
    }

def verify_otp(phone: str, otp: str) -> Dict:
    """驗證 OTP"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 開發模式：接受任何 6 位數 OTP
    DEV_MODE = os.environ.get('DEV_MODE', 'true').lower() == 'true'
    
    if DEV_MODE and len(otp) == 6 and otp.isdigit():
        # 開發模式：直接通過
        cursor.execute('''
            SELECT id FROM phone_verifications 
            WHERE phone = ? ORDER BY created_at DESC LIMIT 1
        ''', (phone,))
        row = cursor.fetchone()
        
        if not row:
            # 創建一個虛擬 OTP 記錄
            from datetime import datetime, timedelta
            expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()
            cursor.execute('''
                INSERT INTO phone_verifications (phone, otp, expires_at, verified)
                VALUES (?, ?, ?, 1)
            ''', (phone, otp, expires_at))
            conn.commit()
        else:
            # 標記為已驗證
            cursor.execute('''
                UPDATE phone_verifications SET verified = 1 WHERE id = ?
            ''', (row['id'],))
            conn.commit()
        
        conn.close()
        return {"success": True, "message": "開發模式：驗證成功"}
    
    # 生產模式：嚴格驗證
    cursor.execute('''
        SELECT id, expires_at, verified 
        FROM phone_verifications 
        WHERE phone = ? AND otp = ? AND expires_at > CURRENT_TIMESTAMP
        ORDER BY created_at DESC LIMIT 1
    ''', (phone, otp))
    
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {"success": False, "error": "OTP 無效或已過期"}
    
    if row['verified']:
        conn.close()
        return {"success": False, "error": "OTP 已使用"}
    
    # 標記為已驗證
    cursor.execute('''
        UPDATE phone_verifications SET verified = 1 WHERE id = ?
    ''', (row['id'],))
    
    conn.commit()
    conn.close()
    
    return {"success": True, "message": "驗證成功"}

# ============ 會話管理 ============
def create_session(user_id: int) -> str:
    """創建用戶會話"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 生成 token
    token = secrets.token_urlsafe(32)
    expires_at = (datetime.now() + timedelta(days=30)).isoformat()
    
    # 刪除舊會話
    cursor.execute('DELETE FROM user_sessions WHERE user_id = ?', (user_id,))
    
    # 創建新會話
    cursor.execute('''
        INSERT INTO user_sessions (user_id, token, expires_at)
        VALUES (?, ?, ?)
    ''', (user_id, token, expires_at))
    
    conn.commit()
    conn.close()
    
    return token

def validate_session(token: str) -> Optional[Dict]:
    """驗證會話 token"""
    if not token:
        return None
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.user_id, s.expires_at, u.* 
        FROM user_sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.token = ? AND s.expires_at > CURRENT_TIMESTAMP
    ''', (token,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def revoke_session(token: str) -> bool:
    """撤銷會話（登出）"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_sessions WHERE token = ?', (token,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def revoke_all_sessions(user_id: int) -> bool:
    """撤銷用戶所有會話"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_sessions WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# ============ 用戶管理 ============
def get_or_create_user_by_phone(phone: str, name: Optional[str] = None) -> Dict:
    """根據電話號碼獲取或創建用戶"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 確保 phone 欄位存在 (安全檢查)
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'phone' not in columns:
        print("⚠️ phone column missing, adding now...")
        cursor.execute('ALTER TABLE users ADD COLUMN phone TEXT')
        conn.commit()
    
    # 嘗試查找現有用戶
    cursor.execute('SELECT * FROM users WHERE phone = ?', (phone,))
    row = cursor.fetchone()
    
    if row:
        conn.close()
        return dict(row)
    
    # 創建新用戶
    cursor.execute('''
        INSERT INTO users (name, phone, created_at, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    ''', (name or f"用戶{phone[-4:]}", phone))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return get_user_by_id(user_id)

def get_user_by_id(user_id: int) -> Optional[Dict]:
    """根據 ID 獲取用戶"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def update_user_phone(user_id: int, phone: str) -> bool:
    """更新用戶電話號碼"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET phone = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (phone, user_id))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# 初始化
if __name__ == '__main__':
    init_auth_db()
    print("✅ 認證系統測試完成")
