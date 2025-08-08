import requests
import json

params = {
    "conversation_id": ""
}

    
def get_message_ids(conversation_id):
    url = f'https://api.coze.cn/v1/conversation/message/list?conversation_id={conversation_id}'
    headers = {
        'Authorization': '',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers)
    print([i['id'] for i in response.json().get('data', [])])
    return [i['id'] for i in response.json().get('data', [])]

get_message_ids(7500057404197912628)
