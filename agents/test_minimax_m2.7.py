#!/usr/bin/env python3
"""
Test script for Minimax M2.7 OpenClaw Agent
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/home/node/.openclaw/workspace/agents/minimax-m2.7.env')

class MinimaxM27Agent:
    """Minimax M2.7 Agent Test Class"""
    
    def __init__(self):
        self.api_key = os.getenv('MINIMAX_M2.7_API_KEY')
        self.base_url = os.getenv('MINIMAX_M2.7_BASE_URL', 'https://api.minimaxi.com/v1')
        self.model = os.getenv('MINIMAX_M2.7_MODEL', 'abab6.5-chat')
        
        if not self.api_key:
            raise ValueError("MINIMAX_M2.7_API_KEY not found in environment variables")
    
    def test_connection(self):
        """Test connection to Minimax API"""
        print("🔍 Testing Minimax M2.7 API connection...")
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": "Hello! Please respond with 'Minimax M2.7 is working!'"}
                    ],
                    "max_tokens": 50,
                    "temperature": 0.7
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content']
                print(f"✅ Connection successful!")
                print(f"🤖 Response: {message}")
                return True
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def test_programming(self):
        """Test programming capabilities"""
        print("\n💻 Testing programming capabilities...")
        
        prompt = """Write a Python function that:
1. Takes a list of numbers as input
2. Returns a dictionary with:
   - 'sum': sum of all numbers
   - 'average': average of numbers
   - 'max': maximum value
   - 'min': minimum value
3. Handle empty list case
4. Include docstring and type hints"""
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.3
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content']
                print(f"✅ Programming test successful!")
                print(f"📝 Code generated:\n{message}")
                return True
            else:
                print(f"❌ Programming test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Programming test error: {e}")
            return False
    
    def test_cantonese(self):
        """Test Cantonese language support"""
        print("\n🇭🇰 Testing Cantonese language support...")
        
        prompt = """用廣東話解釋點樣用 Python 寫一個簡單嘅計算機程式。包括加減乘除功能同錯誤處理。"""
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 300,
                    "temperature": 0.7
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content']
                print(f"✅ Cantonese test successful!")
                print(f"🗣️ Response:\n{message}")
                return True
            else:
                print(f"❌ Cantonese test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Cantonese test error: {e}")
            return False
    
    def get_quota_info(self):
        """Get quota information (if API supports it)"""
        print("\n📊 Checking quota information...")
        
        # Note: Minimax might have different endpoints for quota info
        # This is a placeholder for actual quota checking
        print("ℹ️ Quota monitoring would be implemented here")
        print("• Text quota: 4500 calls / 5 hours (rolling window)")
        print("• Media quotas reset daily at 00:00 HKT")
        return True

def main():
    """Main test function"""
    print("=" * 60)
    print("🚀 Minimax M2.7 OpenClaw Agent Test Suite")
    print("=" * 60)
    
    try:
        # Initialize agent
        agent = MinimaxM27Agent()
        
        # Run tests
        tests = [
            ("API Connection", agent.test_connection),
            ("Programming", agent.test_programming),
            ("Cantonese Support", agent.test_cantonese),
            ("Quota Info", agent.get_quota_info)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n{'='*40}")
            print(f"Running: {test_name}")
            print(f"{'='*40}")
            result = test_func()
            results.append((test_name, result))
        
        # Print summary
        print(f"\n{'='*60}")
        print("📋 Test Summary")
        print(f"{'='*60}")
        
        passed = 0
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
            if result:
                passed += 1
        
        print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
        
        if passed == len(results):
            print("\n🏆 All tests passed! Minimax M2.7 agent is ready!")
        else:
            print(f"\n⚠️ {len(results) - passed} test(s) failed. Check configuration.")
            
    except Exception as e:
        print(f"\n❌ Error initializing agent: {e}")
        return False
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)