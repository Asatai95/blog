from django.apps import AppConfig
import sys
import os
sys.path.append(os.getcwd())

class WebappConfig(AppConfig):
    name = 'mysite'
