from django.urls import path
from ChatApp import consumers


websocket_urlpatterns = [
    path('ws/wsc/<str:group_name>/', consumers.MyWebsocketConsumer.as_asgi()),
    path('ws/awsc/<str:group_name>/', consumers.MyAsyncWebsocketConsumer.as_asgi()),
]