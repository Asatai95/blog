import os
import sys
import time
import traceback
import signal
import django

from django.core.wsgi import get_wsgi_application

os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from .settings import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

"""
一旦、コメントアウトにしてぇおく
app aren't load yet が発生した場合にもとに戻す
"""
# try:
#     django.setup()
#     application = get_wsgi_application()
#     print("without exception")
# except:
#     print('handling WSGI exception')
#     if 'mod_wsgi' in sys.modules:
#         traceback.print_exc()
#         os.kill(os.getpid(), signal.SIGINT)
#         time.sleep(2.5)