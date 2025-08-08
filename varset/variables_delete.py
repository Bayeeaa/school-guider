import requests
import json

url = 'https://api.coze.cn/v1/variables'

headers = {
    'Authorization': '',
    'Content-Type': 'application/json'
}

payload = {
    "data": [
        {
            "keyword": "major",
        },
        {
            "keyword": "gpa"
        },
        {
            "keyword": "hobby"
        },
        {
            "keyword": "projects"
        }
    ],
    "connector_uid": "",
    "bot_id": ""
}

response = requests.put(url, headers=headers, data=json.dumps(payload))

print(response.status_code)
print(response.text)
