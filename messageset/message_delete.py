import requests
from .message_detail import get_message_ids

url = "https://api.coze.cn/v1/conversation/message/delete"
params = {
    "conversation_id": "",
    "message_id": ""
}

headers = {
    "Authorization": "",
    "Content-Type": "application/json"
}

conversation_id = params["conversation_id"]
message_ids = get_message_ids(conversation_id)

def delete(message_ids):
    for message_id in message_ids:
        params = {
            "conversation_id": conversation_id,
            "message_id": message_id
        }
        response = requests.post(url, headers=headers, params=params)
        print(f"删除消息 {message_id} 状态码: {response.status_code}, 返回: {response.text}")

delete(message_ids)