from django.http import JsonResponse
from django.shortcuts import render

from .engine.llm_engine import chat_api

import logging
import json

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'index.html')

def index_javascript(request):
    return render(request, 'index-javascript.html')

def chat_javascript_get(request):
    token = request.GET.get("token")
    query = request.GET.get("query")
    your_name = request.GET.get("your_name")

    logger.debug("-----------------------------------------------------")
    logger.debug(f"token={token}, your_name={your_name}, query={query}")
    logger.debug("-----------------------------------------------------")

    # 调用chat_api
    response = chat_api(your_name=your_name, query=query)

    # 准备响应数据
    response_data = {
        'response': response,
        'code': "200"
    }
    
    # 返回JSON响应
    return JsonResponse(response_data)


def index_websocket(request):
    return render(request, 'index-websocket.html')

def chat_javascript_post(request):
    '''
    聊天
    :param request:
    :return:
    '''
    data = json.loads(request.body.decode('utf-8'))

    # 解析url query string 参数
    token = request.GET.get("token")

    logger.debug("-----------------------------------------------------")
    logger.debug(f"token={token}, json={data}")
    logger.debug("-----------------------------------------------------")

    # 解析url query string 参数
    query = data["query"]
    your_name = data["your_name"]

    # 调用chat_api
    response = chat_api(your_name=your_name, query=query)

    return JsonResponse({"response": response, "code": "200"})
