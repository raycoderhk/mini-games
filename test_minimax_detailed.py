#!/usr/bin/env python3
import requests
import json

api_key = "sk-api-xvuTrv5_5d-KmOAbztidMCoRvsxZqivUkWyNd-52GARh24Y_n5icruDncDtcU2urz1RWkWbxgS9QJhPJAG6d3xKMlOWac-hedqiK5rcuu5YFk76GXFdbUk8"

endpoint = "https://api.minimaxi.com/v1/text/chatcompletion_v2"

# Test with different models
models_to_test = [
    "abab6-chat",
    "abab6.5s-chat", 
    "abab6.5s-vision",
    "abab6.5",
    "abab6.5s",
    "m2.7",
    "m2.7-chat"
]

print("Testing different Minimax models with the new API key...")
print("=" * 60)

for model in models_to_test:
    print(f"\nTesting model: {model}")
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": "Hello, test if this API key works"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 10  # Very short to minimize cost
    }
    
    try:
        response = requests.post(
            endpoint,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=10
        )
        
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  Response keys: {list(data.keys())}")
                
                if "base_resp" in data:
                    base_resp = data["base_resp"]
                    print(f"  base_resp: {base_resp}")
                    
                    if "status_msg" in base_resp:
                        print(f"  Status Message: {base_resp['status_msg']}")
                    
                    if "status_code" in base_resp:
                        print(f"  Status Code (internal): {base_resp['status_code']}")
                        
                elif "error" in data:
                    print(f"  Error: {data['error']}")
                else:
                    print(f"  Full response: {json.dumps(data, indent=2)[:300]}")
                    
            except json.JSONDecodeError:
                print(f"  Response (text): {response.text[:200]}")
        else:
            print(f"  Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "=" * 60)
print("Testing complete.")