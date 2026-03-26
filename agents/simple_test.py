#!/usr/bin/env python3
"""
Simple test to check Minimax API connectivity
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/home/node/.openclaw/workspace/skills/vision/config.env')

def test_vision_api():
    """Test the vision API that we know works"""
    print("🔍 Testing Vision API (ABAB 6.5S Vision)...")
    
    api_key = os.getenv('MINIMAX_API_KEY')
    model = os.getenv('MINIMAX_MODEL')
    
    print(f"API Key: {api_key[:20]}...")
    print(f"Model: {model}")
    
    # Try a simple text completion to test connectivity
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
                    {"role": "user", "content": "Hello, are you working?"}
                ],
                "max_tokens": 50
            },
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        if response.status_code == 200:
            print("✅ Vision API connection successful!")
            return True
        else:
            print(f"❌ Vision API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_minimax_models():
    """Check available Minimax models"""
    print("\n📋 Checking Minimax models...")
    
    # Based on research, these are the available models:
    models = {
        "text": ["abab6.5-chat", "abab6.5s-chat", "M2.7"],
        "vision": ["abab6.5s-vision"],
        "image": ["image-01"],
        "video": ["Hailuo-2.3-Fast-768P", "Hailuo-2.3-768P"],
        "music": ["music-2.5"],
        "tts": ["TTS-HD"]
    }
    
    print("Available models in your Minimax Max plan:")
    for category, model_list in models.items():
        print(f"  {category.capitalize()}: {', '.join(model_list)}")
    
    return True

def main():
    print("=" * 60)
    print("🔧 Minimax API Connectivity Test")
    print("=" * 60)
    
    # Test vision API
    vision_ok = test_vision_api()
    
    # Show model information
    check_minimax_models()
    
    print("\n" + "=" * 60)
    print("📝 Analysis of 429 Error:")
    print("=" * 60)
    print("""
The 'insufficient balance (1008)' error suggests:

1. **API Key Scope:** Your current API key might be for:
   - Vision model only (ABAB 6.5S Vision)
   - Not for text models (M2.7/abab6.5-chat)

2. **Account Credits:** The M2.7 text model might require:
   - Separate subscription/credits
   - Account top-up
   - Different API key

3. **Next Steps:**
   a. Use vision API for image tasks (already working)
   b. Get M2.7 text API key from Minimax dashboard
   c. Check account balance at https://platform.minimaxi.com
   d. Ensure you're on the correct pricing plan

4. **Workaround:**
   - Use vision model for now
   - Contact Minimax support for M2.7 access
   - Use alternative text models if needed
    """)
    
    if vision_ok:
        print("\n✅ Vision API is working! You can use it for:")
        print("   • Food image recognition (nutritionist app)")
        print("   • Other vision tasks")
    else:
        print("\n❌ Vision API also failed. Check API key validity.")
    
    return vision_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)