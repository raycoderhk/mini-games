#!/usr/bin/env python3
import requests
import json

# Test both API keys
api_keys = {
    "new_api_key": "sk-api-xvuTrv5_5d-KmOAbztidMCoRvsxZqivUkWyNd-52GARh24Y_n5icruDncDtcU2urz1RWkWbxgS9QJhPJAG6d3xKMlOWac-hedqiK5rcuu5YFk76GXFdbUk8",
    "vision_api_key": "sk-cp-mqDZwvwYG1u79lQAq_IoECIzYAvT1eBVcSOj3dIvTKcqRbRux_chEqTj1aHbvOtUCZ65CO6xYLSotXR1ocvisRzU4k6Zj1RiCpaf15ioXj5XW3DA1d8T5no"
}

# Test endpoints
endpoints = [
    ("https://api.minimax.chat/v1/text/chatcompletion_v2", "POST"),
    ("https://api.minimaxi.com/v1/text/chatcompletion_v2", "POST"),
    ("https://platform.minimaxi.com/api/v1/text/chatcompletion", "POST"),
]

# Test payload
payload = {
    "model": "abab6.5s-chat",
    "messages": [
        {
            "role": "user",
            "content": "Hello, test if this API key works"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

print("Testing Minimax API keys...")
print("=" * 60)

for key_name, api_key in api_keys.items():
    print(f"\nTesting {key_name}: {api_key[:20]}...")
    
    for endpoint, method in endpoints:
        print(f"\n  Testing endpoint: {endpoint}")
        try:
            if method == "POST":
                response = requests.post(
                    endpoint,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload,
                    timeout=10
                )
            else:
                response = requests.get(
                    endpoint,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    timeout=10
                )
            
            print(f"  Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"  Response: {response.text[:200]}")
            else:
                print(f"  Response: {response.text}")
                
        except Exception as e:
            print(f"  Error: {e}")

print("\n" + "=" * 60)
print("Testing complete.")