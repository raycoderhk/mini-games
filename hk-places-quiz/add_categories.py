#!/usr/bin/env python3
import json

# Load quiz data
with open('quiz-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define categories for each question
categories = {
    1: "自然景觀",      # 釣魚翁
    2: "自然景觀",      # 望夫石
    3: "橋樑",          # 鴨脷洲大橋
    4: "建築",          # 馬灣彩虹屋
    5: "海傍景點",      # 黃金海岸
    6: "教育機構",      # 哈羅學校
    7: "歷史建築",      # 美利樓
    8: "交通設施",      # 直升機升降場
    9: "軍事設施",      # 石崗機場
    10: "宗教場所",     # 慈山寺
    11: "水塘",         # 大欖涌水塘
    12: "運動娛樂",     # 石澳高爾夫球場
    13: "海傍景點",     # 星光大道
    14: "水塘",         # 城門水塘
    15: "橋樑"          # 汀九橋
}

# Add category and votes to each question
for question in data['questions']:
    qid = question['id']
    question['category'] = categories.get(qid, "其他")
    question['votes'] = 0  # Initialize votes

# Save updated data
with open('quiz-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Categories and votes added to all questions!")
print(f"Total questions: {len(data['questions'])}")
