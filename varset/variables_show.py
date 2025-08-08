import requests

url = "https://api.coze.cn/v1/variables"
headers = {
    "Authorization": "",
    "Content-Type": "application/json"
}
params = {
    "bot_id": ""
}

response = requests.get(url, headers=headers, params=params)

# 打印返回结果
# print([item['value'] for item in response.json()['data']['items']])
print({item['keyword']: item['value'] for item in response.json()['data']['items']})