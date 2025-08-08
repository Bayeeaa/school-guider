import requests
import json
import traceback
# time 模块在这里不是必需的，因为我们不做多页循环和延迟

# 你原有的 fetch_news_data 函数，不做修改
def fetch_news_data(base_url, payload_variables, auth_token, session_token, id_token_hint_in_url):
    results = []
    headers = {
        'authority': 'e.zufe.edu.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'authorization': f'Bearer {auth_token}',
        'content-type': 'application/json',
        'origin': 'https://i.zufe.edu.cn',
        'referer': 'https://i.zufe.edu.cn/',
        'sdp-app-session': session_token,
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
    }

    request_payload_json = {
        "query": "query ($channelId: String, $first: Int!, $offset: Float!, $department: String, $read: Boolean, $title: String, $publishDate: String) {\n  publishedArticleIndexService_searchByChannel(channelId: $channelId, first: $first, offset: $offset, department: $department, read: $read, title: $title, publishDate: $publishDate) {\n    edges {\n      node {\n        id\n        articleType\n        createDateTime\n        channelId\n        department\n        endDateTime\n        outLink\n        outLinkUrl\n        startDateTime\n        publishDateTime\n        rePublishDateTime\n        summary\n        title\n        subTitle\n        titleImg\n        top\n        read\n        curChannel {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      page\n      size\n      offset\n      endCursor\n      hasNextPage\n      __typename\n    }\n    uuid\n    totalCount\n    __typename\n  }\n}\n",
        "variables": payload_variables
    }

    request_url_with_token = f"{base_url}?id_token_hint={id_token_hint_in_url}&sf_request_type=fetch"
    # 为了简洁，我移除了之前添加的打印语句，以更贴近“不做修改”的原则
    # print(f"INFO: 正在请求URL: {request_url_with_token}")
    # print(f"INFO: 使用的请求头: {json.dumps(headers, indent=2)}")
    # print(f"INFO: 使用的请求体: {json.dumps(request_payload_json, indent=2, ensure_ascii=False)}")

    try:
        response = requests.post(request_url_with_token, headers=headers, json=request_payload_json, timeout=15)
        # print(f"INFO: 响应状态码: {response.status_code}") # 同样移除
        response.raise_for_status()

        data = response.json()

        if 'errors' in data and data['errors']:
            # print("ERROR: GraphQL查询返回错误:") # 移除
            # for error_item in data['errors']:
            #     print(f"  - Message: {error_item.get('message', '未知GraphQL错误')}")
            return results # 保持原样

        edges = data.get('data', {}).get('publishedArticleIndexService_searchByChannel', {}).get('edges', [])

        if not edges:
            # if 'data' in data and 'publishedArticleIndexService_searchByChannel' in data['data'] and data['data']['publishedArticleIndexService_searchByChannel'].get('totalCount', 0) == 0:
            #     print("INFO: 'edges' 列表为空，但服务器报告总数为0，表示该条件下没有新闻。")
            # else:
            #     print("ERROR: 未能在响应中找到 'edges' 数据，或 'edges' 列表为空。请检查JSON结构或请求是否正确。")
            return results # 保持原样

        # print(f"INFO: 找到 {len(edges)} 条新闻边缘数据。开始提取title和summary...") # 移除
        for i, item in enumerate(edges):
            node = item.get('node', {})
            if node:
                title = node.get('title')
                summary = node.get('summary')

                if title is not None and summary is not None:
                    results.append({
                        'title': title,
                        'summary': summary
                    })
                # else: # 移除警告打印，以求“不做修改”
                #     missing_fields = []
                #     if title is None: missing_fields.append("'title'")
                #     if summary is None: missing_fields.append("'summary'")
                #     node_id = node.get('id', f'在edges中的索引 {i}')
                #     print(f"WARN: 节点 '{node_id}' 中缺少 { ' 和 '.join(missing_fields) }。")
            # else: # 移除警告打印
            #     print(f"WARN: 第 {i+1} 个 'edge' 项中没有有效的 'node' 对象或 'node' 为空。")

    except requests.exceptions.HTTPError as http_err:
        # print(f"ERROR: HTTP请求错误: {http_err}") # 移除
        # if 'response' in locals() and response is not None:
        #     print(f"DEBUG: 响应内容 (前1000字符): {response.text[:1000]}...")
        pass # 保持原有行为，如果之前没有打印，这里就pass
    except requests.exceptions.ConnectionError as conn_err:
        # print(f"ERROR: 网络连接错误: {conn_err}") # 移除
        pass
    except Exception as e:
        # print(f"ERROR: 程序执行过程中发生未知错误: {e}") # 移除
        # print("详细错误追踪信息:")
        # traceback.print_exc()
        pass

    return results

# 新增的函数：将新闻列表保存到文本文件
def save_news_to_file(news_list, filename="news.txt"):
    """将新闻列表保存到文本文件"""
    count = 0
    with open(filename, "w", encoding="utf-8") as f:
        if not news_list: # 处理 news_list 为空的情况
            f.write("未能提取到任何新闻数据。\n")
            print(f"INFO: 未能提取到任何新闻数据，已在 {filename} 中记录。")
            return

        for i, news in enumerate(news_list):
            f.write(f"--- 新闻 {i+1} ---\n")
            f.write(f"标题 (Title): {news.get('title', 'N/A')}\n") # 使用 .get() 增加健壮性
            f.write(f"摘要 (Summary):\n{news.get('summary', 'N/A')}\n\n")
            count += 1
    print(f"INFO: {count} 条新闻已成功保存到 {filename}")


if __name__ == "__main__":
    base_graphql_url = "https://e.zufe.edu.cn/bus/graphql/news"

    current_auth_token = ""
    current_session_token = ""
    current_id_token_hint = ""

    payload_vars = {
        "channelId": "",
        "first": 80, # 保持你原有的设置
        "offset": 0,
        "title": "",
        "department": "",
    }

    # 你原有的调用方式，不做修改
    news_items = fetch_news_data(
        base_graphql_url,
        payload_vars,
        current_auth_token,
        current_session_token,
        current_id_token_hint
    )

    # 在原有打印逻辑之前或之后，添加保存到文件的步骤
    if news_items:
        # 原有的打印到控制台的逻辑
        print(f"\n成功提取到 {len(news_items)} 条新闻：")
        for i, news in enumerate(news_items, 1):
            print(f"\n--- 新闻 {i} ---")
            print(f"标题 (Title): {news['title']}")
            print(f"摘要 (Summary):\n{news['summary']}")
        
        # 新增：保存到文件
            
        save_news_to_file(news_items, "news.txt")

    else:
        # 原有的未提取到数据的打印逻辑
        print("\n未能提取到任何新闻数据，或在提取过程中发生错误。请仔细检查上面的日志输出以了解具体原因。")
        # 新增：即使没有数据，也创建一个文件说明情况
        save_news_to_file([], "news.txt")