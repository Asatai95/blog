
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack

from mysite.chat import routing


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.channels_path,
        )
    ),
    # 'websocket': SessionMiddlewareStack(
    #     URLRouter(
    #         routing.channels_path,
    #     )
    # ),
})

