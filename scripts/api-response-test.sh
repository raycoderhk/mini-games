#!/bin/bash

# OpenClaw API Response Time Test
# 測試 Aliyun Qwen API 響應時間

LOG_FILE="/home/node/.openclaw/workspace/memory/api-response-test.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
HKT_TIME=$(TZ="Asia/Hong_Kong" date '+%Y-%m-%d %H:%M:%S')

echo "========================================" >> $LOG_FILE
echo "Test Start: $HKT_TIME (HKT)" >> $LOG_FILE
echo "========================================" >> $LOG_FILE

# Test count
TEST_COUNT=5

for i in $(seq 1 $TEST_COUNT); do
    START_TIME=$(date +%s%3N)
    
    # Simple test question
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
        -H "Authorization: Bearer $ALIBABA_CLOUD_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "qwen-plus",
            "input": {
                "messages": [
                    {"role": "user", "content": "Say hello in one word"}
                ]
            }
        }' 2>&1)
    
    END_TIME=$(date +%s%3N)
    DURATION=$((END_TIME - START_TIME))
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    
    echo "Test $i: ${DURATION}ms (HTTP: $HTTP_CODE)" >> $LOG_FILE
done

echo "" >> $LOG_FILE
echo "Test Complete: $(TZ="Asia/Hong_Kong" date '+%Y-%m-%d %H:%M:%S')" >> $LOG_FILE
echo "" >> $LOG_FILE
