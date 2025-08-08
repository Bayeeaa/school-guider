import requests
import base64

file_path = 'D:\\Project\\guider\\news.txt'

with open(file_path, 'rb') as f:
    file_content = f.read()
    encoded_string = base64.b64encode(file_content).decode('utf-8')

print("Base64 编码如下：")
print(encoded_string)

url = 'https://api.coze.cn/v1/files/upload'
headers = {
    'Authorization': '',
}

files = {
    'file': (file_path.split("\\")[-1], file_content)  
}

response = requests.post(url, headers=headers, files=files)

print("上传结果：")
print(response.status_code)
print(response.text)
