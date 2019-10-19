import os
import sys

from django.urls import path, include, re_path, register_converter
from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
# from .login_session.login_required import *

app_name = 'mysite'

urlpatterns = [
    path('', views.MainView.as_view(), name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('article/<pk>/', views.ArticleInfo.as_view(), name='info'),
    path('search/', views.Search.as_view(), name='search'),
    path('category/<int:id>/', views.Category.as_view(), name='category'),
    path('tags/', views.ALLTags.as_view(), name='all_tags'),
    path('tags/<int:id>/', views.Tags.as_view(), name='tags'),

    # 管理者用のURL
    path('manage/article/create/', login_required(views.ArticleCreate.as_view()), name='create'),
    path('article/create/confirm/', views.ArticleConfirm.as_view(), name='confirm'),
    path('article/create/done/', views.ArticleDone.as_view(), name='done'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)