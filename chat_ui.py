import streamlit as st
import requests
import json
import httpx
from dataset.crawlgpa import GetScore
from messageset.message_delete import delete
from messageset.message_detail import get_message_ids
from dataset.kwupload import upload_txt_to_coze_knowledge

API_KEY = ''
BOT_ID = ''
USER_ID = ''
CONVERSATION_ID = ''

CHAT_URL = 'https://api.coze.cn/v3/chat'
HISTORY_URL = f'https://api.coze.cn/v1/conversation/message/list?conversation_id={CONVERSATION_ID}'

my_access_token = ""
my_dataset_id = ""    
news_file_path = "news.txt"  

headers = {
    'Authorization': API_KEY,
    'Content-Type': 'application/json',
}

def get_history():
    try:
        response = requests.post(HISTORY_URL, headers=headers)
        data = response.json()
        if 'data' in data:
            # 按时间排序
            messages = sorted(data['data'], key=lambda x: x['created_at'])
            # 只保留 role 和 content 字段
            return [
                {"role": m.get("role", "system"), "content": m.get("content", "")}
                for m in messages
            ]
        else:
            return []
    except Exception as e:
        return [{'role': 'system', 'content': f'获取历史消息失败: {e}'}]

# 发送消息（非流式）
def send_message(user_input):
    data = {
        "bot_id": BOT_ID,
        "user_id": USER_ID,
        "stream": False,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": user_input,
                "content_type": "text"
            }
        ]
    }
    params = {"conversation_id": CONVERSATION_ID}
    try:
        response = requests.post(CHAT_URL, headers=headers, json=data, params=params)
        if response.status_code == 200 and response.text:
            return response.json()
        else:
            print(response.status_code, response.text)
            return {"error": "API请求失败"}
    except Exception as e:
        return {"error": str(e)}

get_message_ids = get_message_ids(CONVERSATION_ID)
def his_del():
    delete(get_message_ids)

def get_res(payload):  #流式请求
    full_text = ""
    with st.chat_message("assistant", avatar=avatar_m["assistant"]):
        placeholder = st.empty()
        with httpx.stream("POST", CHAT_URL, headers=headers, json=payload, params={"conversation_id": CONVERSATION_ID}, timeout=None) as r:
            cnt = 0
            for line in r.iter_lines():
                if not line:
                    continue
                decoded = line.strip()
                if (decoded[:5] == "event"):
                    if(decoded == "event:conversation.message.completed"): #第二个complite完成前面才是我们需要的content
                        cnt+=1
                if cnt != 2 and decoded.startswith("data:"):
                    data = decoded[5:]
                    try:
                        data_json = json.loads(data)
                        if isinstance(data_json, dict):
                            event = data_json.get("event", "")
                            msg_type = data_json.get("type", "")
                            content = data_json.get("content", "")
                            if event == "conversation.message.delta" or msg_type == "answer":
                                full_text += content
                                placeholder.markdown(full_text)
                    except json.JSONDecodeError:
                        continue
    return full_text

def exc_res(prop):  #请求头配置
    payload = {
        "bot_id": BOT_ID,
        "user_id": USER_ID,
        "stream": True,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": prop,
                "content_type": "text"
            }
        ]
    }
    full_text = get_res(payload)
    st.session_state["messages"].append({"role": "assistant", "content": full_text})

def var_show():
    response = requests.get("https://api.coze.cn/v1/variables", headers=headers, params={"bot_id": "7498231550795186187"})
    var = {item['keyword']: item['value'] for item in response.json()['data']['items']}
    return var

#gpa
def generate_gpa():
    score = GetScore()
    res = score.get_data()
    return res

#school_info



# ========== UI部分 ==========
st.set_page_config(page_title="Coze 聊天室", page_icon="💬",initial_sidebar_state="collapsed")
st.title("智能生涯规划师")

avatar_m = {
    "assistant": "🤖",
    "user": "🧑‍💻",
}
info = ""
with st.sidebar:
    st.subheader("工具栏")
    if st.button("获取个人绩点"):
        res = generate_gpa()
        st.text(res)
    st.button("清空聊天记录",on_click=his_del)
    if st.button("展示变量"):
        var = var_show()
        for key, value in var.items():
            st.text(f"'{key}': '{value}'")
    if st.button("添加校园资讯入知识库"):
        res = upload_txt_to_coze_knowledge(my_access_token,my_dataset_id,news_file_path)
        st.text(res)
    if st.button("展示校园信息"):
        file_path = "news.txt" 
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        st.subheader("校园信息")
        st.text_area("文件内容:", value=content, height=400, disabled=True, key="news_content_area")
                    

        

# 初始化消息历史
if "messages" not in st.session_state:
    history_messages = get_history()
    st.session_state["messages"] = history_messages
    if not st.session_state["messages"]: 
        opening_remark = "你好！我是你的智能生涯规划师，请告诉我您是否有未来规划，我将为您保驾护航！"  #开场白
        st.session_state["messages"].append({"role": "assistant", "content": opening_remark})

# 展示历史消息
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"], avatar=avatar_m.get(msg["role"], "💬")).write(msg["content"])

# 聊天输入区
if prompt := st.chat_input("请输入你的消息："):
    st.chat_message("user", avatar=avatar_m["user"]).write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})
    exc_res(prompt)
    
