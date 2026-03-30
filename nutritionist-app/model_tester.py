#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里雲模型測試器 - Aliyun Model Tester
測試不同 Qwen 模型 (turbo/plus/max) 的輸出質量、速度、成本
"""

import os
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List
import urllib.request
import urllib.error

# 阿里雲 API 配置
ALIYUN_API_KEY = os.environ.get("ALIYUN_API_KEY", "")
ALIYUN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

# 測試的模型列表
MODELS = [
    {"id": "qwen-turbo", "name": "Qwen Turbo", "cost_per_1k": 0.002},
    {"id": "qwen-plus", "name": "Qwen Plus", "cost_per_1k": 0.004},
    {"id": "qwen-max", "name": "Qwen Max", "cost_per_1k": 0.012},
]

# 測試 prompts
TEST_PROMPTS = [
    {
        "category": "代碼生成",
        "prompt": "寫一個 Python 函數，計算斐波那契數列的第 n 項"
    },
    {
        "category": "文本摘要",
        "prompt": "摘要以下內容：人工智能是當今科技發展的重要方向，它正在改變我們的生活和工作方式。從自動駕駛到醫療診斷，從智能助手到金融分析，AI 的應用範圍越來越廣泛。然而，人工智能的發展也帶來了挑戰，包括就業影響、隱私問題和倫理考量。"
    },
    {
        "category": "問題回答",
        "prompt": "為什麼天空是藍色的？請用簡單的語言解釋。"
    },
    {
        "category": "翻譯",
        "prompt": "將以下中文翻譯成英文：「今天天氣真好，我們一起去公園散步吧。」"
    },
    {
        "category": "創意寫作",
        "prompt": "寫一首關於春天的短詩，4-8 句。"
    }
]

def call_aliyun_model(model_id: str, prompt: str) -> Dict:
    """調用阿里雲 Qwen 模型 API"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ALIYUN_API_KEY}"
    }
    
    payload = {
        "model": model_id,
        "input": {
            "messages": [
                {
                    "role": "system",
                    "content": "你是一個有幫助的助手。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        "parameters": {
            "max_tokens": 1024,
            "temperature": 0.7,
            "top_p": 0.8
        }
    }
    
    start_time = time.time()
    
    try:
        req = urllib.request.Request(
            ALIYUN_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        end_time = time.time()
        response_time = end_time - start_time
        
        # 提取回應內容
        output = result.get("output", {})
        choices = output.get("choices", [])
        message = choices[0].get("message", {}) if choices else {}
        content = message.get("content", "")
        
        # 提取 token 用量
        usage = result.get("usage", {})
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)
        total_tokens = input_tokens + output_tokens
        
        # 計算成本
        cost = (total_tokens / 1000) * next(
            (m["cost_per_1k"] for m in MODELS if m["id"] == model_id), 0
        )
        
        return {
            "success": True,
            "content": content,
            "response_time": round(response_time, 2),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cost": round(cost, 6),
            "model": model_id
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "model": model_id,
            "response_time": 0
        }

def run_model_test(model_id: str, prompt: str) -> Dict:
    """運行單個模型測試"""
    result = call_aliyun_model(model_id, prompt)
    return result

def run_all_models_test(prompt: str) -> List[Dict]:
    """對所有模型運行同一個 prompt 測試"""
    results = []
    
    for model in MODELS:
        print(f"🧪 測試 {model['name']}...")
        result = run_model_test(model["id"], prompt)
        result["model_name"] = model["name"]
        results.append(result)
    
    return results

def run_full_test_suite() -> Dict:
    """運行完整的測試套件"""
    all_results = []
    
    for test_prompt in TEST_PROMPTS:
        print(f"\n📝 測試類別：{test_prompt['category']}")
        print(f"Prompt: {test_prompt['prompt'][:50]}...")
        
        results = run_all_models_test(test_prompt["prompt"])
        
        all_results.append({
            "category": test_prompt["category"],
            "prompt": test_prompt["prompt"],
            "results": results
        })
    
    # 生成總結報告
    summary = generate_summary(all_results)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "tests": all_results,
        "summary": summary
    }

def generate_summary(all_results: List[Dict]) -> Dict:
    """生成測試總結"""
    model_stats = {}
    
    for test in all_results:
        for result in test["results"]:
            if not result.get("success"):
                continue
                
            model_id = result["model"]
            if model_id not in model_stats:
                model_stats[model_id] = {
                    "model_name": result.get("model_name", model_id),
                    "total_tests": 0,
                    "successful_tests": 0,
                    "total_time": 0,
                    "total_tokens": 0,
                    "total_cost": 0
                }
            
            stats = model_stats[model_id]
            stats["total_tests"] += 1
            stats["successful_tests"] += 1
            stats["total_time"] += result.get("response_time", 0)
            stats["total_tokens"] += result.get("total_tokens", 0)
            stats["total_cost"] += result.get("cost", 0)
    
    # 計算平均值
    summary = []
    for model_id, stats in model_stats.items():
        if stats["successful_tests"] > 0:
            summary.append({
                "model_id": model_id,
                "model_name": stats["model_name"],
                "avg_response_time": round(stats["total_time"] / stats["successful_tests"], 2),
                "avg_tokens": round(stats["total_tokens"] / stats["successful_tests"], 1),
                "total_cost": round(stats["total_cost"], 4),
                "success_rate": 100
            })
    
    # 按響應時間排序
    summary.sort(key=lambda x: x["avg_response_time"])
    
    return {
        "model_comparison": summary,
        "fastest_model": summary[0]["model_id"] if summary else None,
        "cheapest_model": min(summary, key=lambda x: x["total_cost"])["model_id"] if summary else None
    }

# Flask 路由輔助函數
def get_tester_results_from_db(db_module):
    """從數據庫獲取測試結果"""
    conn = db_module.get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM model_test_results 
        ORDER BY created_at DESC 
        LIMIT 10
    ''')
    
    rows = cursor.fetchall()
    results = [dict(row) for row in rows]
    conn.close()
    
    return results

def save_test_results_to_db(db_module, test_results: Dict):
    """保存測試結果到數據庫"""
    conn = db_module.get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO model_test_results (test_data, created_at)
        VALUES (?, ?)
    ''', (json.dumps(test_results), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # 測試運行
    if not ALIYUN_API_KEY:
        print("❌ 請設置 ALIYUN_API_KEY 環境變量")
    else:
        print("🚀 開始運行模型測試...")
        results = run_full_test_suite()
        print("\n✅ 測試完成！")
        print(json.dumps(results, indent=2, ensure_ascii=False))
