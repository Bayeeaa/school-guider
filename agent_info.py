import requests

url = 'https://api.coze.cn/v1/bot/get_online_info'
url_create = 'https://api.coze.cn/v1/bot/create'
params = {
    'bot_id': ''  
}

headers = {
    'Authorization': '',
    'Content-Type': 'application/json'
}

data = {
    "space_id": "",
    "name": "生涯规划师",
    "model_info_config": {
        "model_id": ""
    }
}

response = requests.get(url, headers=headers, params=params)

# 打印响应内容
print(response.json())
