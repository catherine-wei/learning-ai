# from rest_framework import viewsets
# from rest_framework.decorators import action
import os
from django.conf import settings
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

class CharacterView:
    
    def default(request):
        token = request.GET.get("token")
        user_info = get_userinfo_by_token(token=token)
        user_id = user_info.get('user_id')  # 假设get_userinfo_by_token返回一个包含user_id的字典
        print(f"userid={user_id}")

        # 查询SessionModel里属于这个user_id的记录列表
        sessions = SessionModel.objects.filter(user_id=user_id)

        context = {'sessions': sessions}

        return render(request, 'default.html', context)

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

class CharacterAction:
    '''character action
    ''' 
    @api_view(['GET'])
    def character_action_list(request):
        # action_list = CharacterActionModel.objects.filter(status=1)
        # serializer = CharacterActionSerializer(action_list, many=True)
        # logger.debug(f"action list: {serializer.data}")
        # return Response({"response": serializer.data, "code": "200"})
        fbx_files = []
        static_dir = settings.STATICFILES_DIRS[0]  # 获取静态文件目录
        static_dir += "/fbx"
        print(f"fbx dir = {static_dir}")
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                if file.endswith('.fbx'):
                    # 构建文件的相对路径
                    relative_path = os.path.join(root, file).replace(static_dir, '').lstrip('/')
                    fbx_files.append(relative_path)
        
        print(f"fbx_files={fbx_files}")
        
        return JsonResponse({'fbx_files': fbx_files})
        
class CharacterEmotion:
    @api_view(['GET'])
    def character_emotion_list(request):
        emotion_arry = ["neutral" , "happy", "angry", "sad", "relaxed", "surprised", "blink", "lookDown", "lookUp", "lookLeft", "lookRight", "blinkLeft", "blinkRight"]
        result_list = [{"name": item, "value": item} for item in emotion_arry]
        print(result_list)

        return Response({"respone":result_list, "code":"200"})
