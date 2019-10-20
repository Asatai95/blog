from django.urls import path

from . import consumers


app_name = 'chat'


channels_path = [
    path('ws/chat/', consumers.Consumer),
]