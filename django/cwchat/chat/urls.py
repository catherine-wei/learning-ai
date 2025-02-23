from django.urls import path, include
from django.urls import re_path as url

from .views.views import index, chatapi, chat_sessions, session_msgs
from .views.views_3d import CharacterAction, CharacterEmotion

urlpatterns = [
    path('index.html', index, name='chat/index'),
    url(r'^$', index, name='chat/'),
    path('api', chatapi, name='chatapi'),
    path('chatsessions', chat_sessions, name='chatsessions'),
    path('session_msgs', session_msgs, name='session_msgs'),

    path('actions', CharacterAction.character_action_list, name='character_action_list'),
    path('emotions', CharacterEmotion.character_emotion_list, name='character_emotion_list'),

    # path('', include(router.urls)),

    # re_path(r'^$', index, name='chat/index'),
    # path('index.html', index, name='chat/index'),
    # path('index-websocket.html', index_websocket, name='chat/index_websocket'),
    # path('index-javascript.html', index_javascript, name='chat/index_javascript'),
]