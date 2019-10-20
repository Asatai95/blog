from config import *
import os
import sys

from django import *
from django.contrib.messages import *
from django.contrib import *

from django.db import models

from django.db.backends.mysql.base import DatabaseWrapper

import cloudinary
import cloudinary.uploader
import cloudinary.api

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_NAME = os.path.basename(BASE_DIR)
SECRET_KEY = '75c6@w6i1c=xsb$($_117$zk-v!@n*5r9(@tgcj+n=jj+ff*g!'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mysite.apps.WebappConfig',
    'config',
    "mysite.templatetags",
]
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 3600 * 24,
    },
    # "file_resubmit": {
    #     'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #     "LOCATION": '/tmp/file_resubmit/'
    # },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'config.session_config.SessionMiddleware.SessionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# sessionの有効期限更新月は変更するかも
SESSION_COOKIE_AGE = 3600 * 24 * 30 * 365 #1年単位
SESSION_COOKIE_NAME = "asablog"
SESSION_SAVE_EVERY_REQUEST = True
# パスワード再設定リンクの有効期限
PASSWORD_RESET_TIMEOUT_DAYS = 1
sys.path.append(os.getcwd())
ROOT_URLCONF = 'config.urls'
TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, "templates")],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.static',
                    "mysite.templatetags.context_processors.common",
                ],
            },
        },
    ]
LOGIN_URL = 'apps:login'
LOGIN_REDIRECT_URL = 'apps:top'
LOGOUT_URL = 'apps:logout'

WSGI_APPLICATION = 'config.wsgi.application'
# sys.path.append(os.getcwd())
# ASGI_APPLICATION = 'mysite.routing.application'
# if 'test' in sys.argv:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'testsqldb',
#             'USER': 'root',
#             'PASSWORD': 'password',
#             'OPTIONS': {
#                 'charset': 'utf8mb4',
#             },
#             'TEST': {
#                 'NAME': 'test_roomii_sample',
#             }
#         }
#     }
# else:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': 'blog',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
TIME_ZONE = 'Asia/Tokyo'
LANGUAGE_CODE = 'ja'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
AUTH_USER_MODEL = 'mysite.User'


cloudinary.config(
    cloud_name = 'db5nsevmi',
    api_key = '881246414241688',
    api_secret = 'Z_eIAX_pTKF5JHFxl2KrOoWqLz8'
)

# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
SESSION_SAVE_EVERY_REQUEST = True

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
# 下記のコードのちに消す可能性あり
coverage = [
            '--with-coverage',
            '--cover-package=foo,bar',
        ]