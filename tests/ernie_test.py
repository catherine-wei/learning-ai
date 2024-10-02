import os
import requests
import json
import qianfan

def chat_api(your_name: str, query:str):
    
    llm = qianfan.ChatCompletion()

    messages = []
    # prompt
    # prompt = "you are a helpful assistant"
    # messages.append({'role': 'system', 'content': prompt})
    # # TODO Knowledge Base(知识库) mode to be implemented
    # messages.append({"role": "system", "content": oddmeta_server_kb})
    # history

    # user message
    messages.append({'role': 'user', 'content': your_name + "说：" + query})

    response = llm.do(endpoint="eb-instant", messages=messages, stream=True)

    llm_result_text = ""
    for r in response:
        print(r["body"]["result"])
        llm_result_text = llm_result_text + r["body"]["result"]

    print(f"response={llm_result_text}")

def chat_http(your_name: str, query:str):
        
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token=" + get_access_token()

    messages = []
    # prompt
    # prompt = "you are a helpful assistant"
    # messages.append({'role': 'system', 'content': prompt})
    # # TODO Knowledge Base(知识库) mode to be implemented
    # messages.append({"role": "system", "content": oddmeta_server_kb})
    # history

    # user message
    messages.append({'role': 'user', 'content': your_name + "说：" + query})
    chunk_size = 50
    json_payload = {
        "messages" : messages,
        "temperature": 0.7,
        "max_output_tokens": chunk_size
    }

    payload = json.dumps(json_payload)
    headers = { 'Content-Type': 'application/json' }
    
    print(f"payload={payload}")

    # r = requests.request("POST", url, headers=headers, data=payload, stream=True)
    r = requests.get(url, headers=headers, data=payload, stream=True)

    # if r.encoding is None:
    #     r.encoding = 'utf-8'

    # Check if the request was successful
    if r.status_code == 200:
        for chunk in r.iter_content(chunk_size=128):
            print(f"chunk={chunk}")

    # chunks = []

    # for chunk in r.iter_content(chunk_size):
    #     chunks.append(chunk)

    # response_data = b''.join(chunks)
    # print(f"response_data={response_data}")

    # j = json.loads(response_data)
    # print(j["result"])
    print("adfasdf")

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    API_KEY = "ZCcK674j19GL54HFtDRTuXqe"
    SECRET_KEY = "lPuu14wS4fiqMYUw4s3GQH4bdhlxcYIu"
    os.environ["QIANFAN_AK"] = API_KEY
    os.environ["QIANFAN_SK"] = SECRET_KEY

    # chat_http("catherine", "今天吃啥")
    chat_api("catherine", "今天吃啥")

