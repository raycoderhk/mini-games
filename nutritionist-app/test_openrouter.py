#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 OpenRouter MiniMax-01 Vision API
"""

import urllib.request
import urllib.error
import json
import base64
import os
import sys

# ============ 配置 ============
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ============ 測試 ============
def test_vision_api(image_path):
    """測試 MiniMax-01 Vision API"""
    print("=" * 60)
    print("🧪 OpenRouter MiniMax-01 Vision API 測試")
    print("=" * 60)
    
    if not OPENROUTER_API_KEY:
        print("\n❌ 錯誤：OPENROUTER_API_KEY 未設定")
        print("請執行：export OPENROUTER_API_KEY='sk-or-...'")
        return False
    
    if not os.path.exists(image_path):
        print(f"\n❌ 錯誤：找不到圖片 '{image_path}'")
        return False
    
    # 轉換圖片為 Base64
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    print(f"\n✅ 圖片載入成功：{image_path}")
    print(f"   大小：{len(image_data)} bytes")
    
    # 簡單 Prompt
    prompt = "這是什麼食物？請用中文回答。"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/raycoderhk/nutritionist-app",
        "X-Title": "Nutritionist App Test"
    }
    
    payload = {
        "model": "minimax/minimax-01",
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
        print("\n📡 調用 OpenRouter API...")
        req = urllib.request.Request(
            OPENROUTER_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        content = result["choices"][0]["message"]["content"]
        
        print("\n✅ API 調用成功！")
        print("\n📝 識別結果:")
        print("-" * 60)
        print(content)
        print("-" * 60)
        
        # 顯示用量
        if "usage" in result:
            usage = result["usage"]
            print(f"\n📊 Token 用量:")
            print(f"   Prompt: {usage.get('prompt_tokens', 0)}")
            print(f"   Completion: {usage.get('completion_tokens', 0)}")
            print(f"   Total: {usage.get('total_tokens', 0)}")
        
        return True
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"\n❌ HTTP {e.code}: {e.reason}")
        print(f"   {error_body}")
        return False
    except Exception as e:
        print(f"\n❌ 錯誤：{e}")
        return False

# ============ 主函數 ============
def main():
    if len(sys.argv) < 2:
        print("\n使用方法：python3 test_openrouter.py <圖片路徑>")
        print("\n範例:")
        print("  python3 test_openrouter.py lobster.jpg")
        return 1
    
    image_path = sys.argv[1]
    success = test_vision_api(image_path)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
