#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
數據庫遷移腳本
Database Migration Script

Run this ONCE to add the phone column to users table:
    python3 migrate.py
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'nutrition.db')

def get_db():
    """獲取數據庫連接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def migrate():
    """執行數據庫遷移"""
    print("=" * 60)
    print("🔧 數據庫遷移 - Database Migration")
    print("=" * 60)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 檢查 users 表結構
    print("\n📋 檢查 users 表結構...")
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"當前欄位：{columns}")
    
    # 添加 phone 欄位
    if 'phone' not in columns:
        print("\n🔧 添加 phone 欄位...")
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN phone TEXT')
            conn.commit()
            print("✅ phone 欄位添加成功！")
        except sqlite3.OperationalError as e:
            print(f"❌ 添加失敗：{e}")
    else:
        print("\n✅ phone 欄位已存在，無需遷移")
    
    # 檢查 auth 相關表
    print("\n📋 檢查認證相關表...")
    
    # phone_verifications
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='phone_verifications'")
    if cursor.fetchone():
        print("✅ phone_verifications 表已存在")
    else:
        print("🔧 創建 phone_verifications 表...")
        cursor.execute('''
            CREATE TABLE phone_verifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT NOT NULL,
                otp TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                verified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        print("✅ phone_verifications 表創建成功")
    
    # user_sessions
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_sessions'")
    if cursor.fetchone():
        print("✅ user_sessions 表已存在")
    else:
        print("🔧 創建 user_sessions 表...")
        cursor.execute('''
            CREATE TABLE user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()
        print("✅ user_sessions 表創建成功")
    
    # 顯示統計
    print("\n📊 數據庫統計:")
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"用戶總數：{user_count}")
    
    cursor.execute("SELECT COUNT(*) FROM phone_verifications")
    otp_count = cursor.fetchone()[0]
    print(f"OTP 記錄：{otp_count}")
    
    cursor.execute("SELECT COUNT(*) FROM user_sessions")
    session_count = cursor.fetchone()[0]
    print(f"會話記錄：{session_count}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ 數據庫遷移完成！")
    print("=" * 60)

if __name__ == '__main__':
    migrate()
