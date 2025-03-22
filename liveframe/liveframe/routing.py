from django.urls import path
from .consumers import VideoConsumer

websocket_urlpatterns = [
    path('ws/video_feed/', VideoConsumer.as_asgi()),
]
