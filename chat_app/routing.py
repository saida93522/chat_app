from django.urls import re_path
from . import consumers
# send data to consumer

websocket_urlpatterns = [
    #w+ is a match a word character. room names.
    #/$ where route ends. anything after /$/ 404 error
    #as_asgi() will instantiate an instance of consumer for each user-connection
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]