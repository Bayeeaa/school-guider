import requests
import json

url = 'https://api.coze.cn/v3/chat'
headers = {
    'Authorization': '',
    'Content-Type': 'application/json'
}

params = {
    "conversation_id": "7500140307011371023"
}

data = {
    "bot_id": "",
    "user_id": "",
    "stream": False,
    "auto_save_history": True,
    "additional_messages": [
        {
            "role": "user",
            "content": "我有过两次项目经历",
            "content_type": "text"
        }
    ]
}

response = requests.post(url, headers=headers, json=data, params=params)

# 打印响应内容
print(response.json())
