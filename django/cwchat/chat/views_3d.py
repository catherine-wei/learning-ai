# from rest_framework import viewsets
# from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from django.shortcuts import render



from .engine.llm_engine import chat_api
from .engine.utils import new_uuid
from .views import get_userinfo_by_token

from .models import SessionModel, MessageModel, AgentModel
from .serializers import SessionModelSerializer, MessageModelSerializer, AgentModelSerializer

import logging
import json

logger = logging.getLogger(__name__)




def test_3vrm(request):
    token = request.GET.get("token")
    user_info = get_userinfo_by_token(token=token)
    user_id = user_info.get('user_id')  # 假设get_userinfo_by_token返回一个包含user_id的字典
    print(f"userid={user_id}")

    # 查询SessionModel里属于这个user_id的记录列表
    sessions = SessionModel.objects.filter(user_id=user_id)

    context = {'sessions': sessions}

    return render(request, 'test-3vrm.html', context)

# Create your views here.
def test3vrm(request):
    token = request.GET.get("token")
    user_info = get_userinfo_by_token(token=token)
    user_id = user_info.get('user_id')  # 假设get_userinfo_by_token返回一个包含user_id的字典
    print(f"userid={user_id}")

    # 查询SessionModel里属于这个user_id的记录列表
    sessions = SessionModel.objects.filter(user_id=user_id)

    context = {'sessions': sessions}

    return render(request, 'test3vrm.html', context)

def test3d(request):
    token = request.GET.get("token")
    user_info = get_userinfo_by_token(token=token)
    user_id = user_info.get('user_id')  # 假设get_userinfo_by_token返回一个包含user_id的字典
    print(f"userid={user_id}")

    # 查询SessionModel里属于这个user_id的记录列表
    sessions = SessionModel.objects.filter(user_id=user_id)

    context = {'sessions': sessions}

    return render(request, 'test3d.html', context)
