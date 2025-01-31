from django.urls import path, include
from django.urls import re_path as url

from .views import index, chatapi, chat_sessions, session_msgs

urlpatterns = [
    path('index.html', index, name='chat/index'),
    url(r'^$', index, name='chat/'),
    path('api', chatapi, name='chatapi'),
    path('chatsessions', chat_sessions, name='chatsessions'),
    path('session_msgs', session_msgs, name='session_msgs'),

    # path('', include(router.urls)),

    # re_path(r'^$', index, name='chat/index'),
    # path('index.html', index, name='chat/index'),
    # path('index-websocket.html', index_websocket, name='chat/index_websocket'),
    # path('index-javascript.html', index_javascript, name='chat/index_javascript'),
]