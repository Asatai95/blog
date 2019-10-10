import os
import sys

from django.urls import path, include, re_path, register_converter
from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'mysite'

urlpatterns = [
    path('article/', views.MainView.as_view(), name='top'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)