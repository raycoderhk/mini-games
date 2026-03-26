#!/usr/bin/env python3
"""
Test different Minimax model names
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/home/node/.openclaw/workspace/skills/vision/config.env')

api_key = os.getenv('MINIMAX_API_KEY')

# Try different model names based on research
models_to_test = [
    "abab6.5-chat",           # Text model
    "abab6.5s-chat",          # Text model (smaller)
    "abab6.5",                # Base model
    "abab6.5s",               # Base smaller model
    "abab6.5-vision",         # Alternative vision name
    "abab6.5s-vision",        # Current config
    "abab6.5s-vision-chat",   # Possible full name
    "minimax",                # Generic
    "m2.7",                   # M2.7 model
    "M2.7",                   # M2.7 capitalized
]

print("🔍 Testing Minimax model names...")
print(f"API Key: {api_key[:20]}...")
print()

for model in models_to_test:
    print(f"Testing model: {model:30}", end="")
    
    try:
        response = requests.post(
            "https://api.minimaxi.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [
                    {"role": "user", "content": "Say 'hello' if this model works"}
                ],
                "max_tokens": 20
            },
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ SUCCESS")
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"   Response: {message}")
            break
        elif response.status_code == 400:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            print(f"❌ 400: {error_msg[:50]}")
        elif response.status_code == 429:
            print("❌ 429: Rate limited / Insufficient balance")
        else:
            print(f"❌ {response.status_code}: {response.text[:50]}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)[:50]}")
    
    print()

print("\n" + "="*60)
print("📋 Summary:")
print("="*60)
print("""
Based on the tests, it seems:

1. **API Key Issue:** The API key might be:
   - Invalid or expired
   - For a different service/endpoint
   - Requires account activation

2. **Model Names:** The correct model names might be:
   - Different from what's documented
   - Region-specific
   - Requires specific API version

3. **Next Steps:**
   a. Check Minimax dashboard: https://platform.minimaxi.com
   b. Verify API key is for the correct environment
   c. Contact Minimax support for correct model names
   d. Try using OpenRouter as proxy (if supported)

4. **Immediate Workaround:**
   - Use existing working models (Aliyun Qwen, etc.)
   - Wait for Minimax account setup completion
   - Test with curl to verify API endpoint
""")

# Test with curl command
print("\n🔧 Try this curl command to test:")
print(f"""
curl -X POST https://api.minimaxi.com/v1/chat/completions \\
  -H "Authorization: Bearer {api_key}" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "model": "abab6.5-chat",
    "messages": [{{"role": "user", "content": "Hello"}}],
    "max_tokens": 50
  }}'
""")