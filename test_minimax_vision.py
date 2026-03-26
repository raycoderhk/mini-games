#!/usr/bin/env python3
import requests
import json
import base64

# Test the Token Plan Key with vision endpoint
token_plan_key = "sk-cp-mqDZwvwYG1u79lQAq_IoECIzYAvT1eBVcSOj3dIvTKcqRbRux_chEqTj1aHbvOtUCZ65CO6xYLSotXR1ocvisRzU4k6Zj1RiCpaf15ioXj5XW3DA1d8T5no"

# Create a simple test image (1x1 pixel black PNG)
# Base64 encoded 1x1 black PNG
test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

print("Testing Token Plan Key with vision endpoint...")
print("=" * 60)

# Try vision completion endpoint
vision_endpoint = "https://api.minimaxi.com/v1/text/chatcompletion_v2"

payload = {
    "model": "abab6.5s-vision",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{test_image_base64}"
                    }
                }
            ]
        }
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

try:
    response = requests.post(
        vision_endpoint,
        headers={
            "Authorization": f"Bearer {token_plan_key}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            
            if "base_resp" in data:
                base_resp = data["base_resp"]
                print(f"base_resp: {base_resp}")
                
                if "status_msg" in base_resp:
                    print(f"Status Message: {base_resp['status_msg']}")
                    
                if "status_code" in base_resp:
                    print(f"Status Code (internal): {base_resp['status_code']}")
                    
            elif "choices" in data and data["choices"]:
                print(f"Success! Response: {data['choices'][0]}")
            else:
                print(f"Full response: {json.dumps(data, indent=2)[:500]}")
                
        except json.JSONDecodeError:
            print(f"Response (text): {response.text[:500]}")
    else:
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Testing complete.")