import os
import qianfan

def chat_api(your_name: str, query:str):
    API_KEY = "ZCcK674j19GL54HFtDRTuXqe"
    SECRET_KEY = "lPuu14wS4fiqMYUw4s3GQH4bdhlxcYIu"

    os.environ["QIANFAN_AK"] = API_KEY
    os.environ["QIANFAN_SK"] = SECRET_KEY

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

    return llm_result_text

if __name__ == '__main__':
    API_KEY = "ZCcK674j19GL54HFtDRTuXqe"
    SECRET_KEY = "lPuu14wS4fiqMYUw4s3GQH4bdhlxcYIu"

    os.environ["QIANFAN_AK"] = API_KEY
    os.environ["QIANFAN_SK"] = SECRET_KEY

    chat_api("catherine", "今天吃啥")

