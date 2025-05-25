from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Example: ws://yourdomain.com/ws/stream/
    re_path(r'ws/stream/$', consumers.StreamConsumer.as_asgi()),
    # You can add more WebSocket routes here
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]