from django.urls import path
from . import Consumers

websocket_urlpatterns = [
    path('ws/<str:room_name>/', Consumers.ChatConsumer.as_asgi()),
]