# from django.http import JsonResponse
# from rest_framework import viewsets
# from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from django.shortcuts import render

from .engine.llm_engine import chat_api
from .engine.utils import new_uuid

from .models import SessionModel, MessageModel, AgentModel
from .serializers import SessionModelSerializer, MessageModelSerializer, AgentModelSerializer

import logging
import json

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    token = request.GET.get("token")
    user_info = get_userinfo_by_token(token=token)
    user_id = user_info.get('user_id')  # 假设get_userinfo_by_token返回一个包含user_id的字典
    print(f"userid={user_id}")

    # 查询SessionModel里属于这个user_id的记录列表
    sessions = SessionModel.objects.filter(user_id=user_id)

    context = {'sessions': sessions}

    return render(request, 'index.html', context)


# class MessageModelViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows MyModel instances to be viewed or edited.
#     """
#     queryset = MessageModel.objects.all()
#     serializer_class = MessageModelSerializer
 
#     @action(detail=True, methods=['post'])
#     def custom_action(self, request, pk=None):
#         """
#         Custom action description.
#         """
#         # 你的自定义动作逻辑
#         return Response({'status': 'custom action executed'})


def chatapi(request):
    token = request.GET.get("token")
    query = request.GET.get("query")
    your_name = request.GET.get("your_name")
    agent_id = request.GET.get("agent_id")
    session_id = request.GET.get("session_id")
    user_id = request.GET.get("user_id")

    # 若user_id为空，根据token找出这个用户是谁
    if user_id == "":
        user_info = get_userinfo_by_token(token=token)
        user_id = user_info.get('user_id')

    print(f"userid={user_id}")

    # 若是没指定跟中个智能体聊天，那就指定为默认的智能体（1）
    if agent_id == "":
        agent_id = "1"
    
    # 如果 session_id为空，就在SessionModel时创建一个新的session
    if session_id == "":
        session_id = new_uuid()
        session = SessionModel(user_id=user_id, agent_id=agent_id, session_id=session_id)
        session.save()

    logger.info("-----------------------------------------------------")
    logger.info(f"token={token}, user_id={user_id}, your_name={your_name}, agent_id={agent_id}, query={query}, session_id={session_id}")
    logger.info("-----------------------------------------------------")

    # 调用chat_api
    response = chat_api(your_name=your_name, query=query)

    # 准备响应数据
    response_data = {
        'user_id': user_id,
        'agent_id': agent_id,
        'session_id': session_id,
        'response': response,
        'code': "200"
    }

    # 保存到数据库
    msg = MessageModel(session_id=session_id, content=query, sender_type=0)
    msg.save()
    msg = MessageModel(session_id=session_id, content=response, sender_type=1)
    msg.save()

    # 返回JSON响应
    return Response(response_data)

def validate_token(token: str, user_id: str):
    '''
    return True, user_info
    '''
    user_info = {}

    if not token:
        return False, user_info
 
    print(f"token={token}")

    try:
        user_info = get_userinfo_by_token(token=token)
        if user_id != "" and user_id != user_info.get('user_id'):
            return False, user_info
        else:
            return True, user_info
    except Exception as e:
        return False, user_info

@api_view(['GET'])
def session_msgs(request):
    '''
    从后端获取会话历史聊天记录
    TODO 只筛选最新的、指定数量的消息
    '''
    token = request.query_params.get('token')
    session_id = request.query_params.get('session_id')
    user_id = request.query_params.get('user_id')
    latest = request.query_params.get('latest')
    if latest == "":
        latest = 5

    # 验证token和用户
    valid, user_info = validate_token(token=token, user_id=user_id)
    if not valid:
        return Response({'error': 'Invalid token or user not found'}, status=HTTP_400_BAD_REQUEST)
    user_id = user_info.get('user_id')
    print(f"token={token}, user_id={user_id}, user_info={user_info}")

    # 验证这个session是不是属于这个user的
    sessions = SessionModel.objects.filter(user_id=user_id, session_id=session_id)
    if not sessions.exists():  # 使用exists()方法更高效，因为它在找到第一个匹配项时就会停止查询
        return Response({'error': 'Invalid session'}, status=HTTP_400_BAD_REQUEST)

    # 筛选指定用户和session的消息列表
    msgs = MessageModel.objects.filter(session_id=session_id).order_by("timestamp")[:latest]
 
    if msgs.exists():  # 使用exists()方法更高效，因为它在找到第一个匹配项时就会停止查询
        response_data = [{'content': obj.content, 'sender_type': obj.sender_type, 'timestamp': obj.timestamp} for obj in msgs]
        status_code = HTTP_200_OK
    print(f"response_data={response_data}")
    return Response(response_data, status=status_code)

@api_view(['GET'])
def chat_sessions(request):
    token = request.query_params.get('token')
    if not token:
        return Response({'error': 'Token is missing'}, status=HTTP_400_BAD_REQUEST)
 
    print(f"token={token}")

    try:
        user_info = get_userinfo_by_token(token=token)
        user_id = user_info.get('user_id')  # 假设get_userinfo_by_token返回一个包含user_id的字典
        print(f"userid={user_id}")
    except Exception as e:
        # 处理令牌验证失败的情况
        return Response({'error': 'Invalid token or user not found'}, status=HTTP_400_BAD_REQUEST)
 
    sessions = SessionModel.objects.filter(user_id=user_id)
 
    if sessions.exists():  # 使用exists()方法更高效，因为它在找到第一个匹配项时就会停止查询
        response_data = [{'value': obj.session_id, 'text': obj.session_id} for obj in sessions]
        status_code = HTTP_200_OK
    else:
        response_data = {
            'user_id': user_id,
            'message': 'Cannot find any chat sessions',  # 使用更清晰的消息字段
            'code': '400'  # 通常，HTTP状态码已经足够表达错误，这里的code字段可能是多余的
        }
        status_code = HTTP_400_BAD_REQUEST  # 或者考虑使用200状态码，但包含一个错误消息，这取决于您的API设计
 
    print(f"response_data={response_data}")

    return Response(response_data, status=status_code)
    
    # token = request.GET.get("token")
    # user_id = get_userinfo_by_token(token=token)
    # response_data = ""

    # print(f"user_id={user_id}")

    # # 查询SessionModel里属于这个user_id的记录列表
    # sessions = SessionModel.objects.filter(user_id=user_id)

    # # 如果返回的数据长度大于0，将他们转换成json
    # if len(sessions) > 0:
    #     response_data = [{'value': obj.session_id, 'text': obj.session_id} for obj in sessions]
    # else:
    #     # 返回chat session列表数据
    #     response_data = {
    #         'user_id': user_id,
    #         'response': 'can not find any chat sessions',
    #         'code': '400'
    #     }

    # print(f"response_data={response_data}")

    # return Response(response_data)

def get_userinfo_by_token(token: str):
    # TODO 整个功能暂时都还没有用户相关实现，暂先写死用user_id为1
    return {"user_id": "1"}














def index_javascript(request):
    token = request.GET.get("token")
    user_id = get_userinfo_by_token(token=token)

    # 查询SessionModel里属于这个user_id的记录列表
    sessions = SessionModel.objects.filter(user_id=user_id)

    context = {'sessions': sessions}

    return render(request, 'index-javascript.html', context)

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
