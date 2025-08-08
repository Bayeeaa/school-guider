import requests
import json

url = 'https://api.coze.cn/v3/chat'
headers = {
    'Authorization': '',
    'Content-Type': 'application/json'
}
data = {
    "bot_id": "",
    "user_id": "",
    "stream": False,
    "auto_save_history": True,
    "additional_messages": [
        {
            "role": "user",
            "content": "",
            "content_type": "text"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)

# 打印响应内容
print(response.json())
