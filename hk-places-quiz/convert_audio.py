#!/usr/bin/env python3
"""
MOV 轉 MP3 自動轉換工具
專為 HK Places Quiz 語音導航設計
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

def check_ffmpeg():
    """檢查 FFmpeg 是否可用"""
    try:
        result = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg 已安裝:", result.stdout.strip())
            return True
        else:
            print("❌ FFmpeg 未安裝")
            return False
    except Exception as e:
        print(f"❌ 檢查 FFmpeg 時出錯: {e}")
        return False

def convert_mov_to_mp3(mov_path, mp3_path=None):
    """
    將 MOV 檔案轉換為 MP3
    
    Args:
        mov_path: 輸入 MOV 檔案路徑
        mp3_path: 輸出 MP3 檔案路徑（如為 None，自動生成）
    
    Returns:
        tuple: (成功與否, 輸出檔案路徑, 錯誤訊息)
    """
    if not os.path.exists(mov_path):
        return False, None, f"檔案不存在: {mov_path}"
    
    if mp3_path is None:
        # 自動生成 MP3 檔案名
        base_name = os.path.splitext(mov_path)[0]
        mp3_path = base_name + ".mp3"
    
    print(f"🎬 轉換中: {mov_path} → {mp3_path}")
    
    try:
        # FFmpeg 命令：提取音頻，最高品質
        cmd = [
            "ffmpeg",
            "-i", mov_path,      # 輸入檔案
            "-q:a", "0",         # 最高音質（VBR）
            "-map", "a",         # 只提取音頻軌道
            "-y",                # 覆蓋現有檔案
            mp3_path
        ]
        
        print(f"📝 執行命令: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30  # 30秒超時
        )
        
        if result.returncode == 0:
            if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 0:
                file_size = os.path.getsize(mp3_path)
                print(f"✅ 轉換成功！檔案大小: {file_size:,} 字節")
                return True, mp3_path, None
            else:
                return False, None, "轉換後檔案不存在或為空"
        else:
            error_msg = f"FFmpeg 錯誤:\n{result.stderr}"
            print(f"❌ {error_msg}")
            return False, None, error_msg
            
    except subprocess.TimeoutExpired:
        return False, None, "轉換超時（超過30秒）"
    except Exception as e:
        return False, None, f"轉換過程出錯: {e}"

def update_quiz_audio(question_id, audio_path):
    """
    更新 quiz-data.json 中的 audio 欄位
    
    Args:
        question_id: 題目 ID
        audio_path: 音頻檔案路徑（相對路徑）
    
    Returns:
        bool: 更新是否成功
    """
    quiz_file = "quiz-data.json"
    
    if not os.path.exists(quiz_file):
        print(f"❌ 找不到 {quiz_file}")
        return False
    
    try:
        with open(quiz_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated = False
        for q in data['questions']:
            if q['id'] == question_id:
                old_audio = q.get('audio', '無')
                q['audio'] = audio_path
                updated = True
                print(f"✅ 更新 Q{question_id}: audio = {audio_path}")
                print(f"   舊值: {old_audio}")
                break
        
        if updated:
            with open(quiz_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ 已儲存 {quiz_file}")
            return True
        else:
            print(f"❌ 找不到 Q{question_id}")
            return False
            
    except Exception as e:
        print(f"❌ 更新 JSON 時出錯: {e}")
        return False

def process_ting_kau_bridge():
    """處理汀九橋語音導航"""
    print("=" * 50)
    print("🎯 處理汀九橋語音導航")
    print("=" * 50)
    
    # 檢查 FFmpeg
    if not check_ffmpeg():
        print("請先安裝 FFmpeg: apt-get install -y ffmpeg")
        return False
    
    # 檔案路徑
    mov_file = "assets/audio/ting-kau-bridge.mov"
    mp3_file = "assets/audio/ting-kau-bridge.mp3"
    
    if not os.path.exists(mov_file):
        print(f"❌ 找不到原始檔案: {mov_file}")
        return False
    
    # 轉換 MOV 為 MP3
    success, output_path, error = convert_mov_to_mp3(mov_file, mp3_file)
    
    if not success:
        print(f"❌ 轉換失敗: {error}")
        return False
    
    # 更新 quiz-data.json
    if not update_quiz_audio(15, mp3_file):  # Q15 = 汀九橋
        return False
    
    print("\n" + "=" * 50)
    print("🎉 汀九橋語音導航處理完成！")
    print("=" * 50)
    print(f"📁 原始檔案: {mov_file}")
    print(f"🎵 音頻檔案: {mp3_file}")
    print(f"📊 檔案大小: {os.path.getsize(mp3_file):,} 字節")
    print(f"🔗 Audio 欄位: assets/audio/ting-kau-bridge.mp3")
    print("\n✅ 請硬刷新頁面測試：Ctrl+Shift+R")
    
    return True

def batch_convert_directory(directory="assets/audio"):
    """批次轉換目錄中所有 MOV 檔案"""
    print(f"🔄 批次轉換目錄: {directory}")
    
    if not os.path.exists(directory):
        print(f"❌ 目錄不存在: {directory}")
        return
    
    mov_files = list(Path(directory).glob("*.mov"))
    
    if not mov_files:
        print("✅ 目錄中沒有 MOV 檔案")
        return
    
    print(f"📁 找到 {len(mov_files)} 個 MOV 檔案")
    
    for mov_file in mov_files:
        print(f"\n🔧 處理: {mov_file.name}")
        mp3_file = mov_file.with_suffix('.mp3')
        
        # 如果 MP3 已存在，跳過
        if mp3_file.exists():
            print(f"   ⏭️ MP3 已存在，跳過")
            continue
        
        success, output_path, error = convert_mov_to_mp3(str(mov_file), str(mp3_file))
        
        if success:
            print(f"   ✅ 轉換成功: {mp3_file.name}")
        else:
            print(f"   ❌ 轉換失敗: {error}")

if __name__ == "__main__":
    print("🎵 MOV 轉 MP3 轉換工具")
    print("專為 HK Places Quiz 語音導航設計")
    print("=" * 50)
    
    # 檢查參數
    if len(sys.argv) > 1:
        if sys.argv[1] == "batch":
            batch_convert_directory()
        elif sys.argv[1] == "check":
            check_ffmpeg()
        else:
            print(f"❌ 未知參數: {sys.argv[1]}")
            print("用法:")
            print("  python3 convert_audio.py          # 處理汀九橋")
            print("  python3 convert_audio.py batch    # 批次轉換目錄")
            print("  python3 convert_audio.py check    # 檢查 FFmpeg")
    else:
        # 默認處理汀九橋
        process_ting_kau_bridge()