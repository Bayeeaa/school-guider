import requests
import json
import base64 
import os  
from datetime import datetime

base_graphql_url = "https://e.zufe.edu.cn/bus/graphql/news"

current_auth_token = ""
current_session_token = ""
current_id_token_hint = ""

payload_vars = {
    "channelId": "",
    "first": 40, #获取文章的数量
    "offset": 0,
    "title": "",
    "department": "",
}

def upload_txt_to_coze_knowledge(
    access_token,
    dataset_id,
    file_path,
    document_name=None, 
    chunk_strategy=None,
    agw_js_conv_str=True 
):
    api_url = "https://api.coze.cn/open_api/knowledge/document/create"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    if agw_js_conv_str:
        headers["Agw-Js-Conv"] = "str"

    try:
        with open(file_path, "rb") as f: 
            file_content_bytes = f.read()
        file_base64 = base64.b64encode(file_content_bytes).decode('utf-8')
    except FileNotFoundError:
        print(f"ERROR: 文件未找到: {file_path}")
        return None
    except Exception as e:
        print(f"ERROR: 读取或编码文件时出错: {e}")
        return None

    if document_name is None:
        now = datetime.now()
        time_prefix = now.strftime("%Y%m%d_%H%M%S")
        doc_name = os.path.basename(time_prefix + file_path) 
    else:
        doc_name = document_name
    
    file_ext = os.path.splitext(doc_name)[1]
    if file_ext.startswith('.'):
        file_ext = file_ext[1:]
    
    if not file_ext: 
        print(f"WARN: 文件 '{doc_name}' 没有明确的后缀，默认为 'txt'.")
        file_ext = "txt"


    document_base = {
        "name": doc_name,
        "source_info": {
            "file_base64": file_base64,
            "file_type": file_ext 
        }
    }

    if chunk_strategy is None:
        chunk_strategy_payload = {
            "chunk_type": 0
        }
    else:
        chunk_strategy_payload = chunk_strategy

    payload = {
        "dataset_id": str(dataset_id),
        "document_bases": [document_base],
        "chunk_strategy": chunk_strategy_payload,
        "format_type": 0  
    }

    print(f"INFO: Document Base Name: {payload['document_bases'][0]['name']}")
    print(f"INFO: Document Base File Type: {payload['document_bases'][0]['source_info']['file_type']}")
    print(f"INFO: Chunk Strategy: {payload['chunk_strategy']}")

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60) 
        response.raise_for_status()
        
        response_data = response.json()
        print(f"INFO: API 响应状态码 (in json): {response_data.get('code')}")
        print(f"INFO: API 响应消息 (in json): {response_data.get('msg')}")
        
        if response_data.get('code') == 0:
            print("INFO: 文件上传成功！")
            if response_data.get('document_infos'):
                for doc_info in response_data['document_infos']:
                    print(f"  Uploaded Document ID: {doc_info.get('document_id')}, Name: {doc_info.get('name')}, Status: {doc_info.get('status')}")
        else:
            print(f"ERROR: API调用失败。错误码: {response_data.get('code')}, 错误信息: {response_data.get('msg')}")
            if response_data.get('detail', {}).get('logid'):
                print(f"  Log ID: {response_data['detail']['logid']}")
            
        return "*成功将校园资讯添加到知识库"

    except requests.exceptions.HTTPError as http_err:
        print(f"ERROR: HTTP 请求错误: {http_err}")
        print(f"ERROR: 响应内容: {response.text if response else '无响应内容'}")
    except requests.exceptions.RequestException as req_err:
        print(f"ERROR: 请求过程中发生错误: {req_err}")
    except json.JSONDecodeError:
        print(f"ERROR: 无法解析API响应为JSON。响应内容: {response.text if response else '无响应内容'}")
    
    return None


if __name__ == "__main__":
    my_access_token = ""  
    my_dataset_id = ""    
    news_file_path = "news.txt"  
    if not os.path.exists(news_file_path):
        print(f"错误: 新闻文件 '{news_file_path}' 未找到。请先生成该文件。")
    else:
        print("更新news数据")            
        print(f"\n--- 尝试上传文件 '{news_file_path}' 到知识库 '{my_dataset_id}' ---")
        response_upload = upload_txt_to_coze_knowledge(my_access_token, my_dataset_id, news_file_path)