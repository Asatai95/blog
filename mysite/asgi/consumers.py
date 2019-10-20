import os
from django import *
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from mysite.models import Article, Fab, ArticleLive, Chat_room, Company
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.auth import login
import asyncio
from django.contrib.auth import get_user_model, authenticate
from channels.generic.http import AsyncHttpConsumer

from channels.auth import login

import json

from django.conf import settings
from django.db import models

import requests

import re

from config.settings import *

import cloudinary
import cloudinary.uploader
import cloudinary.api

from cloudinary.forms import cl_init_js_callbacks


class Consumer(AsyncWebsocketConsumer):

    model = Chat_room

    async def connect(self):

        self.user = self.scope["user"]

        self.room_group_name = 'chat_%s' % self.user
        await self.channel_layer.group_add (
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard (
            self.room_group_name,
            self.channel_name
        )