from django.urls import path
from django.urls import re_path as url

from .views import index, chat_javascript_get, index_javascript, index_websocket

urlpatterns = [
    path('index.html', index, name='chat/index'),
    path('index-javascript.html', index_javascript, name='chat/index_javascript'),
    url(r'^$', chat_javascript_get, name='chat/'),
    path('api', chat_javascript_get, name='chat/api'),
    # re_path(r'^$', index, name='chat/index'),
    # path('index.html', index, name='chat/index'),
    # path('index-websocket.html', index_websocket, name='chat/index_websocket'),
]