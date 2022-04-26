from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
import chat_app.routing

#inspects the type of connection 
application = ProtocolTypeRouter(
    {
    #  if type of connect is websocket,chat handler
    'websocket':AuthMiddlewareStack(
        # populate the connection’s scope with a reference to the currently authenticated user
        URLRouter(
            chat_app.routing.websocket_urlpatterns
        )
    )
})