#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多模型測試器 - Multi-Model Tester
測試不同 AI 模型的能力：
1. 文本處理：笑話、創意寫作
2. 圖像理解：食物照片分析
3. 圖像生成：根據 prompt 生成圖片
"""

import os
import json
import time
import base64
from datetime import datetime
from typing import Dict, List, Optional

import urllib.request
import urllib.error

# ============ API 配置 ============
# 阿里雲 DashScope
ALIYUN_API_KEY = os.environ.get("ALIYUN_API_KEY", "")
ALIYUN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# MiniMax Direct API (not via OpenRouter)
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MINIMAX_API_URL = "https://api.minimax.chat/v1/text/chatcompletion_v2"

# ============ 模型列表 ============
TEXT_MODELS = [
    {"id": "qwen-plus", "name": "Qwen Plus", "provider": "aliyun"},
    {"id": "qwen-turbo", "name": "Qwen Turbo", "provider": "aliyun"},
    {"id": "qwen-max", "name": "Qwen Max", "provider": "aliyun"},
    {"id": "MiniMax-01", "name": "MiniMax-01 (Vision)", "provider": "minimax"},
]

VISION_MODELS = [
    {"id": "qwen-plus", "name": "Qwen Plus", "provider": "aliyun"},
    {"id": "qvq-72b-preview", "name": "QVQ-72B (Vision)", "provider": "minimax"},
]

IMAGE_MODELS = [
    {"id": "image-01", "name": "Image-01 (MiniMax)", "provider": "minimax"},
]

# ============ 測試 Prompts ============
TEXT_TESTS = [
    {
        "id": "joke",
        "name": "講笑話",
        "prompt": "請用廣東話講一個關於工程師的笑話",
        "category": "text"
    },
    {
        "id": "creative",
        "name": "創意寫作",
        "prompt": "請用繁體中文寫一首關於夏天的短詩，4-8句",
        "category": "text"
    },
    {
        "id": "summarize",
        "name": "文本摘要",
        "prompt": "請用繁體中文摘要以下內容（50字以內）：人工智能正在改變我們的生活方式和工作模式。從醫療診斷到金融分析，從智能助手到自動駕駛，AI的應用越來越廣泛。",
        "category": "text"
    }
]

# ============ API 調用函數 ============

def call_minimax(model_id: str, messages: list, image_url: str = None) -> Dict:
    """調用 MiniMax Direct API"""
    if not MINIMAX_API_KEY:
        return {
            "success": False,
            "error": "MINIMAX_API_KEY not set",
            "model": model_id,
            "provider": "minimax"
        }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MINIMAX_API_KEY}"
    }
    
    user_content = messages[-1]["content"] if messages else ""
    
    # 構建消息
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": user_content}],
        "max_tokens": 1024
    }
    
    start_time = time.time()
    try:
        req = urllib.request.Request(
            MINIMAX_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        response_time = time.time() - start_time
        
        # MiniMax API response format
        choices = result.get("choices")
        if choices and len(choices) > 0:
            msg = choices[0].get("message", {})
            content = msg.get("content", "")
            return {
                "success": True,
                "content": content,
                "response_time": round(response_time, 2),
                "model": model_id,
                "provider": "minimax"
            }
        else:
            # 沒有 choices，可能是 error
            error_msg = result.get("base_resp", {}).get("error_msg", "Unknown error")
            return {
                "success": False,
                "error": error_msg,
                "response_time": round(response_time, 2),
                "model": model_id,
                "provider": "minimax"
            }
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {
            "success": False,
            "error": f"HTTP {e.code}: {error_body[:200]}",
            "response_time": round(time.time() - start_time, 2),
            "model": model_id,
            "provider": "minimax"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)[:200],
            "response_time": round(time.time() - start_time, 2),
            "model": model_id,
            "provider": "minimax"
        }

def call_aliyun(model_id: str, messages: list, image_url: str = None) -> Dict:
    """調用阿里雲 API"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ALIYUN_API_KEY}"
    }
    
    content = messages[-1]["content"]
    
    # 如果有 image_url，構建視覺消息
    if image_url:
        content = [
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": messages[-1]["content"]}
        ]
    
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 1024,
        "temperature": 0.7
    }
    
    start_time = time.time()
    try:
        req = urllib.request.Request(
            ALIYUN_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        response_time = time.time() - start_time
        
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            return {
                "success": True,
                "content": content,
                "response_time": round(response_time, 2),
                "model": model_id,
                "provider": "aliyun"
            }
        else:
            return {
                "success": False,
                "error": result.get("error_message", "Unknown error"),
                "response_time": round(response_time, 2),
                "model": model_id,
                "provider": "aliyun"
            }
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {
            "success": False,
            "error": f"HTTP {e.code}: {error_body[:200]}",
            "response_time": round(time.time() - start_time, 2),
            "model": model_id,
            "provider": "aliyun"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)[:200],
            "response_time": round(time.time() - start_time, 2),
            "model": model_id,
            "provider": "aliyun"
        }

def call_openrouter(model_id: str, messages: list, image_url: str = None) -> Dict:
    """調用 OpenRouter API (MiniMax, Claude, Gemini等)"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/raycoderhk/nutrition-app",
        "X-Title": "Model Tester"
    }
    
    content = messages[-1]["content"]
    
    # 構建消息
    msg_content = content
    if image_url:
        msg_content = [
            {"type": "image_url", "image_url": {"url": image_url}},
            {"type": "text", "text": content}
        ]
    
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": msg_content}],
        "max_tokens": 1024
    }
    
    start_time = time.time()
    try:
        req = urllib.request.Request(
            OPENROUTER_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        response_time = time.time() - start_time
        
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            return {
                "success": True,
                "content": content,
                "response_time": round(response_time, 2),
                "model": model_id,
                "provider": "openrouter"
            }
        else:
            return {
                "success": False,
                "error": "No response content",
                "response_time": round(response_time, 2),
                "model": model_id,
                "provider": "openrouter"
            }
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {
            "success": False,
            "error": f"HTTP {e.code}: {error_body[:200]}",
            "response_time": round(time.time() - start_time, 2),
            "model": model_id,
            "provider": "openrouter"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)[:200],
            "response_time": round(time.time() - start_time, 2),
            "model": model_id,
            "provider": "openrouter"
        }

def call_model(model_id: str, prompt: str, image_base64: str = None) -> Dict:
    """統一調用介面 - 自動選擇 provider"""
    messages = [{"role": "user", "content": prompt}]
    image_url = None
    
    # 如果有圖片，轉換為 data URL
    if image_base64:
        image_url = f"data:image/jpeg;base64,{image_base64}"
    
    # 選擇 provider
    if model_id.startswith("MiniMax") or model_id.startswith("qvq"):
        return call_minimax(model_id, messages, image_url)
    else:
        return call_aliyun(model_id, messages, image_url)

# ============ 測試函數 ============

def test_text(prompt: str) -> List[Dict]:
    """測試文本處理能力"""
    results = []
    for model in TEXT_MODELS:
        # 檢查 API key
        if model["provider"] == "aliyun" and not ALIYUN_API_KEY:
            results.append({
                "model": model["id"],
                "model_name": model["name"],
                "provider": "aliyun",
                "success": False,
                "error": "ALIYUN_API_KEY not set",
                "response_time": 0
            })
            continue
        if model["provider"] == "minimax" and not MINIMAX_API_KEY:
            results.append({
                "model": model["id"],
                "model_name": model["name"],
                "provider": "minimax",
                "success": False,
                "error": "MINIMAX_API_KEY not set",
                "response_time": 0
            })
            continue
        
        result = call_model(model["id"], prompt)
        results.append({
            "model": model["id"],
            "model_name": model["name"],
            "provider": model["provider"],
            **result
        })
    
    return results

def test_vision(prompt: str, image_base64: str) -> List[Dict]:
    """測試圖像理解能力"""
    results = []
    for model in VISION_MODELS:
        if model["provider"] == "aliyun" and not ALIYUN_API_KEY:
            results.append({
                "model": model["id"],
                "model_name": model["name"],
                "provider": "aliyun",
                "success": False,
                "error": "ALIYUN_API_KEY not set",
                "response_time": 0
            })
            continue
        if model["provider"] == "minimax" and not MINIMAX_API_KEY:
            results.append({
                "model": model["id"],
                "model_name": model["name"],
                "provider": "minimax",
                "success": False,
                "error": "MINIMAX_API_KEY not set",
                "response_time": 0
            })
            continue
        
        result = call_model(model["id"], prompt, image_base64)
        results.append({
            "model": model["id"],
            "model_name": model["name"],
            "provider": model["provider"],
            **result
        })
    
    return results

def test_image_generation(prompt: str) -> List[Dict]:
    """測試圖像生成能力"""
    results = []
    
    # MiniMax Image Generation API
    if not MINIMAX_API_KEY:
        results.append({
            "model": "image-01",
            "model_name": "Image-01 (MiniMax)",
            "provider": "minimax",
            "success": False,
            "error": "MINIMAX_API_KEY not set",
            "response_time": 0
        })
    else:
        result = generate_image_minimax(prompt)
        results.append({
            "model": "image-01",
            "model_name": "Image-01 (MiniMax)",
            "provider": "minimax",
            **result
        })
    
    return results

def generate_image_minimax(prompt: str) -> Dict:
    """MiniMax 圖像生成"""
    if not MINIMAX_API_KEY:
        return {"success": False, "error": "MINIMAX_API_KEY not set"}
    
    url = "https://api.minimax.chat/v1/images_gen"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MINIMAX_API_KEY}"
    }
    
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "num_images": 1,
        "width": 1024,
        "height": 1024
    }
    
    start_time = time.time()
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        response_time = time.time() - start_time
        
        if result.get("image_urls"):
            return {
                "success": True,
                "image_url": result["image_urls"][0],
                "response_time": round(response_time, 2),
                "model": "image-01"
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "response_time": round(response_time, 2)
            }
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {"success": False, "error": f"HTTP {e.code}: {error_body[:200]}", "response_time": 0}
    except Exception as e:
        return {"success": False, "error": str(e)[:200], "response_time": 0}

def run_all_tests(test_type: str, prompt: str = None, image_base64: str = None) -> Dict:
    """運行所有測試"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "test_type": test_type,
        "prompt": prompt,
        "models_tested": 0,
        "successful": 0,
        "failed": 0,
        "results": []
    }
    
    if test_type == "text":
        results["results"] = test_text(prompt or TEXT_TESTS[0]["prompt"])
    elif test_type == "vision":
        if not image_base64:
            return {"success": False, "error": "No image provided for vision test"}
        results["results"] = test_vision(prompt or "請描述這張圖片", image_base64)
    elif test_type == "image":
        results["results"] = test_image_generation(prompt)
    else:
        return {"success": False, "error": f"Unknown test type: {test_type}"}
    
    # 統計
    for r in results["results"]:
        results["models_tested"] += 1
        if r.get("success"):
            results["successful"] += 1
        else:
            results["failed"] += 1
    
    return results

# ============ Flask 路由 ============
def register_routes(app, db_module):
    """註冊測試器路由"""
    
    @app.route('/api/model-test/text', methods=['POST'])
    def test_text_api():
        """測試文本處理"""
        data = request.get_json() or {}
        prompt = data.get('prompt', TEXT_TESTS[0]["prompt"])
        
        results = run_all_tests("text", prompt)
        return jsonify(results)
    
    @app.route('/api/model-test/vision', methods=['POST'])
    def test_vision_api():
        """測試圖像理解"""
        data = request.get_json() or {}
        prompt = data.get('prompt', "請描述這張圖片")
        image = data.get('image', '')
        
        # 移除 data URL 前綴
        if ',' in image:
            image = image.split(',')[1]
        
        results = run_all_tests("vision", prompt, image)
        return jsonify(results)
    
    @app.route('/api/model-test/text-prompts', methods=['GET'])
    def get_text_prompts():
        """獲取可用的文本測試 prompts"""
        return jsonify(TEXT_TESTS)
    
    @app.route('/api/model-test/models', methods=['GET'])
    def get_models():
        """獲取所有可用模型"""
        return jsonify({
            "text_models": TEXT_MODELS,
            "vision_models": VISION_MODELS,
            "image_models": IMAGE_MODELS
        })
    
    @app.route('/api/model-test/providers', methods=['GET'])
    def get_providers():
        """獲取 API 配置狀態"""
        return jsonify({
            "aliyun": {
                "configured": bool(ALIYUN_API_KEY),
                "key_prefix": ALIYUN_API_KEY[:10] + "..." if ALIYUN_API_KEY else None
            },
            "openrouter": {
                "configured": bool(OPENROUTER_API_KEY),
                "key_prefix": OPENROUTER_API_KEY[:10] + "..." if OPENROUTER_API_KEY else None
            }
        })

if __name__ == '__main__':
    # CLI 測試模式
    print("🧪 Multi-Model Tester")
    print(f"Aliyun: {'✅ Configured' if ALIYUN_API_KEY else '❌ Not set'}")
    print(f"OpenRouter: {'✅ Configured' if OPENROUTER_API_KEY else '❌ Not set'}")
    print("\nAvailable tests:")
    print("1. Text processing")
    print("2. Vision (needs image)")
    print("\nExample - Text test:")
    result = run_all_tests("text", "請用廣東話講一個笑話")
    print(json.dumps(result, indent=2, ensure_ascii=False))
