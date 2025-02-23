"""
ASGI config for cwchat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cwchat.settings')

from chat.routing import websocket_urlpatterns
from chat.mainservice.messages.chat_live_message import ChatLiveMsgTask
from chat.mainservice.messages.chat_final_message import ChatHistoryTask
from chat.engine.live.live_message_connecter import LiveConnecterTask,live_connecter_main
from chat.mainservice.schedule.scheduled_tasks import run_scheduled_tasks, scheduled_action
# from chat.omagent.agent_service import oddmeta_agent_start

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator


live_connecter_main()
run_scheduled_tasks(1, scheduled_action)
ChatLiveMsgTask.start()
ChatHistoryTask.start()
LiveConnecterTask.start()
# oddmeta_agent_start()

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # 配置WebSocket协议
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})