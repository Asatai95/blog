import os
import sys
import django
# from channels.asgi import get_channel_layer
from channels.routing import get_default_application

import config

sys.path.append(os.getcwd())

from .settings import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()
application = get_default_application()