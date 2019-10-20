import os
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.forms import (
    AuthenticationForm,
)

from django.contrib.auth import get_user_model, password_validation
from mysite.models import (
    Article, User
)

from django.db import models
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary import CloudinaryResource
from cloudinary.forms import CloudinaryFileField
from config.cloudinary_config import *

import requests

import re
import json

from django.core.validators import FileExtensionValidator

from django.contrib import admin

from .views_config.login_session import *

class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class InputForm(forms.Form):
    """ブログ入力フォーム"""

    block = forms.IntegerField(
        label = "構成", initial = 1,
    )

    title = forms.CharField(
           label="タイトル",
           max_length=45,
           widget=forms.TextInput(attrs={'placeholder':'タイトル'}),
    )

    sub_title = forms.CharField(
           label="サブタイトル",
           max_length=45,
           widget=forms.TextInput(attrs={'placeholder':'サブタイトル'}),
    )

    tags = forms.CharField(
           label="タグ名称",
           max_length=45,
           widget=forms.TextInput(attrs={'placeholder':'タグ名称'}),
    )

    category = forms.CharField(
           label="カテゴリ",
           max_length=45,
           widget=forms.TextInput(attrs={'placeholder':'カテゴリー名称'}),
    )

    content = forms.CharField(label='内容', widget=forms.Textarea(attrs={'placeholder':'あさぶろ'}))

    img = CloudinaryJsFileField(
        label = "画像",
    )

    sub_image = CloudinaryJsFileField(
        label = "サムネイル",
    )

    sub_preimage = forms.CharField(
           max_length=45,
    )

    pre_image = forms.CharField(
           max_length=45,
    )

    tmp_file = forms.FileField(
        label = "添付ファイル",
    )

    url_title = forms.CharField(
           label="タイトル",
           max_length=45,
           widget=forms.TextInput(attrs={'placeholder':'タイトル'}),
    )

    url = forms.URLField(
        label = "関連記事",
    )

    class Meta:
        fields = ("block", "title", "sub_title", "tags", "category", "content", "img",
                  "tmp_file", "url", "pre_image", "sub_image", "sub_preimage", "url_title",)

    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        self.fields['pre_image'].widget.attrs['readonly'] = True
        for field in self.fields.values():
            field.required = False
            field.widget.attrs['class'] = 'form-control'
