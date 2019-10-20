import os
from PIL import Image
from django import *
from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView, ListView, TemplateView
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render, resolve_url, render_to_response, get_object_or_404
from django.views.generic.edit import UpdateView
from django.views import View, generic
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
import hashlib
import hmac
# import secrets
import random
from django.utils.encoding import force_bytes


from multiprocessing import Process
import time

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView,
)

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from django.db import models
from django.db.models import Q, Count, Max
from .models import (
    User, Article, Content, References, TagsInfo, CategoryInfo,
)
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.contrib.auth import logout

from .forms import (
    LoginForm, InputForm,
)

import operator
from functools import reduce

from datetime import datetime, timedelta

import requests
import re
import numpy as np
import regex

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pure_pagination.mixins import PaginationMixin

from config.settings import *

Get_user = get_user_model()
ArticleMain = Article.objects.all()

from django.utils.safestring import mark_safe
import json

import cloudinary
import cloudinary.uploader
import cloudinary.api

from cloudinary.forms import cl_init_js_callbacks

from collections import Counter, defaultdict

"""
グローバル
"""
def TagstableInfo(self , tags_table):
    tmp_tag = []
    if tags_table.first():
        for x in tags_table:
            for y in Article.objects.all():
                if x.id == y.tags:
                    tmp_tag.append(x.name)
        count_tag = dict(Counter(tmp_tag))
    else:
        count_tag = None

    return count_tag

def CategorytableInfo(self, category_table):
    tmp_category = []
    if category_table.first():
        for x in category_table:
            for y in Article.objects.all():
                if x.id == y.category:
                    tmp_category.append(x.name)
        count_category_tag = dict(Counter(tmp_category))
    else:
        count_category_tag = None

    return count_category_tag

"""
ログイン機能
"""
class Login(LoginView):

    form_class = LoginForm
    template_name = 'register/login.html'

"""
ログアウト機能
"""
class Logout(LoginRequiredMixin, LogoutView):

    def get(self, request, *args, **kwargs):
        return redirect("apps:logout")

"""
トップ画面
"""
class MainView(generic.ListView):
    template_name = "apps/index.html"
    model = Article

    def get(self, request, *args, **kwargs):

        table = self.model.objects.all().order_by("-created_at")
        tmp_date = []
        for x in table:
            tmp_date.append({"id": x.id , "date": x.created_at})
        today = datetime.today()
        for y in tmp_date:
            date = today.date() - y["date"].date()
            if date.days == 0:
                y.update({"day": "today"})
            else:
                y.update({"day": date.days})
        tags = TagsInfo.objects.all()
        count_tag = TagstableInfo(self, tags)

        category_table = CategoryInfo.objects.all()
        count_category_tag = CategorytableInfo(self, category_table)

        return render(self.request, self.template_name, {"table": table, "date": tmp_date, "tags": tags, "count_tag": count_tag, "category_table": category_table, "count_category_tag": count_category_tag})

"""
記事詳細
"""
class ArticleInfo(generic.DetailView):
    template_name = "apps/info.html"
    model = Article

    def get(self, request, *args, **kwargs):

        pk = self.kwargs.get("pk")
        try:
            table = self.model.objects.get(pk = pk)
        except:
            return redirect("apps:top")

        tmp_date = []
        tmp_date.append({"id": table.id, "date": table.created_at})
        today = datetime.today()
        for x in tmp_date:
            date = today.date() - x["date"].date()
            if date.days == 0:
                x.update({"day": "today"})
            else:
                x.update({"day": date.days})

        content = Content.objects.filter(article_id = table.id)
        if not content.first():
            return redirect("apps:top")

        tmp_content_id = []
        for x in content:
            tmp_content_id.append(x.block)

        content_id = list(set(tmp_content_id))

        references = References.objects.filter(article_id = table.id)

        tags = TagsInfo.objects.all()
        count_tag = TagstableInfo(self, tags)

        category_table = CategoryInfo.objects.all()
        count_category_tag = CategorytableInfo(self, category_table)

        return render(request, self.template_name, {"info": table, "date": tmp_date, "content": content, "content_id": content_id, "category_table": category_table,
                                                    "references": references, "tags": tags, "count_tag": count_tag, "count_category_tag": count_category_tag} )

"""
検索機能
"""
class Search(generic.ListView):
    template_name = "apps/index.html"
    model = Article

    def get(self, request, *args, **kwargs):
        return redirect("apps:top")

    def post(self, request, *args, **kwargs):

        search = self.request.POST.get("search")
        table = self.model.objects.filter(title__icontains=search)
        if not table.first():
            table = self.model.objects.all().order_by("-created_at")

        tmp_date = []
        for x in table:
            tmp_date.append({"id": x.id , "date": x.created_at})
        today = datetime.today()
        for y in tmp_date:
            date = today.date() - y["date"].date()
            if date.days == 0:
                y.update({"day": "today"})
            else:
                y.update({"day": date.days})

        tags = TagsInfo.objects.all()
        count_tag = TagstableInfo(self, tags)

        category_table = CategoryInfo.objects.all()
        count_category_tag = CategorytableInfo(self, category_table)

        return render(self.request, self.template_name, {"table": table, "date": tmp_date, "tags": tags, "count_tag": count_tag,
                                                         "category_table": category_table, "count_category_tag": count_category_tag})

"""
カテゴリー検索（表示画面のレイアウトはトップ画面と一緒）
"""
class Category(generic.ListView):
    template_name = "apps/index.html"
    model = Article

    def get(self, request, *args, **kwargs):

        id = self.kwargs.get("id")
        print(id)
        table = self.model.objects.filter(category=id)
        if not table.first():
            return redirect("apps:top")

        tmp_date = []
        for x in table:
            tmp_date.append({"id": x.id , "date": x.created_at})
        today = datetime.today()
        for y in tmp_date:
            date = today.date() - y["date"].date()
            if date.days == 0:
                y.update({"day": "today"})
            else:
                y.update({"day": date.days})

        tags = TagsInfo.objects.all()
        count_tag = TagstableInfo(self, tags)

        category_table = CategoryInfo.objects.all()
        count_category_tag = CategorytableInfo(self, category_table)

        return render(self.request, self.template_name, {"table": table, "date": tmp_date, "tags": tags, "count_tag": count_tag, "category_id": id,
                                                         "category_table": category_table, "count_category_tag": count_category_tag})
"""
登録中のタグ情報を表示
"""
class ALLTags(generic.ListView):
    template_name = "apps/all_tags.html"
    model = Article

    def get(self, request, *args, **kwargs):

        table = self.model.objects.all().order_by("-created_at")
        if not table.first():
            return redirect("apps:top")

        tmp_date = []
        for x in table:
            tmp_date.append({"id": x.id , "date": x.created_at})
        today = datetime.today()
        for y in tmp_date:
            date = today.date() - y["date"].date()
            if date.days == 0:
                y.update({"day": "today"})
            else:
                y.update({"day": date.days})

        tags = TagsInfo.objects.all()
        count_tag = TagstableInfo(self, tags)

        category_table = CategoryInfo.objects.all()
        count_category_tag = CategorytableInfo(self, category_table)

        return render(self.request, self.template_name, {"table": table, "date": tmp_date, "tags": tags, "count_tag": count_tag, "all_tags": "all_tags",
                                                         "category_table": category_table, "count_category_tag": count_category_tag})

"""
タグ検索（表示画面のレイアウトはトップ画面と一緒）
"""
class Tags(generic.ListView):
    template_name = "apps/index.html"
    model = Article

    def get(self, request, *args, **kwargs):

        id = self.kwargs.get("id")
        table = self.model.objects.filter(tags=id)
        if not table.first():
            return redirect("apps:top")

        tmp_date = []
        for x in table:
            tmp_date.append({"id": x.id , "date": x.created_at})
        today = datetime.today()
        for y in tmp_date:
            date = today.date() - y["date"].date()
            if date.days == 0:
                y.update({"day": "today"})
            else:
                y.update({"day": date.days})

        tags = TagsInfo.objects.all()
        count_tag = TagstableInfo(self, tags)

        category_table = CategoryInfo.objects.all()
        count_category_tag = CategorytableInfo(self, category_table)

        return render(self.request, self.template_name, {"table": table, "date": tmp_date, "tags": tags, "count_tag": count_tag, "tags_id": id,
                                                         "category_table": category_table, "count_category_tag": count_category_tag})

"""
記事情報入力画面
"""
class ArticleCreate(generic.FormView):
    template_name = "register/insert.html"
    model = Article
    form_class = InputForm

    def get(self, request, *args, **kwargs):

        tags_table = TagsInfo.objects.all()
        count_tag = TagstableInfo(self, tags_table)

        category_table = CategoryInfo.objects.all()
        count_category_tag = CategorytableInfo(self, category_table)

        content = Content.objects.all()

        return render(self.request, self.template_name, {"form": self.form_class, "tags": tags_table, "category_table": category_table, "content": content,
                                                         "count_category_tag": count_category_tag, "count_tag": count_tag})

    def form_valid(self, form):

        category = self.request.POST.getlist("category")
        if len(category) <= 1:
            category = None
        tags = self.request.POST.getlist("tags")
        if len(tags) <= 1:
            tags = None
        block_id = self.request.POST.getlist("block")
        block_count = len(block_id)
        sub_title = self.request.POST.getlist("sub_title")
        content = self.request.POST.getlist("content")
        image = self.request.POST.getlist("image")
        tmp_file = self.request.POST.getlist("tmp_file")
        url = self.request.POST.getlist("url")
        tags_table = TagsInfo.objects.all()
        count_tag = TagstableInfo(self, tags_table)

        category_table = CategoryInfo.objects.all()
        count_category_tag = CategorytableInfo(self, category_table)

        tmp_block = []
        for x in range(0, block_count):
            try:
                tmp_block.append({
                    "block": block_id[x], "sub_title": sub_title[x], "content": content[x], "image": image[x]
                })
            except:
                pass

        return render(self.request, "register/insert_confirm.html", {"form": form, "block_id": block_id , "tmp_block": tmp_block, "url": url, "count_tag": count_tag, "category_table": category_table,
                                                                     "tmp_file": tmp_file, "category": category, "tags_form": tags, "tags":tags_table, "count_category_tag": count_category_tag})

"""
記事情報入力確認画面
"""
class ArticleConfirm(generic.FormView):

    model = Article
    form_class = InputForm

    def form_valid(self, form):

        tmp_category_list = []
        category = self.request.POST.getlist("category")
        for x in category:
            if x != "":
                tmp_category_list.append(x)
        category = tmp_category_list
        tmp_tags_list = []
        tags = self.request.POST.getlist("tags")
        for x in tags:
            if x != "":
                tmp_tags_list.append(x)
        tags = tmp_tags_list
        block = self.request.POST.getlist("block")
        block_count = len(block)
        sub_title = self.request.POST.getlist("sub_title")
        content = self.request.POST.getlist("content")
        image = self.request.POST.getlist("pre_image")
        tmp_file = self.request.POST.getlist("tmp_file")
        url = self.request.POST.getlist("url")

        tags_table = TagsInfo.objects.all()
        count_tag = TagstableInfo(self, tags_table)

        category_table = CategoryInfo.objects.all()
        count_category_tag = CategorytableInfo(self, category_table)

        tmp_block = []
        for x in range(0, block_count):
            try:
                tmp_block.append({
                    "block": block[x], "sub_title": sub_title[x], "content": content[x], "image": image[x]
                })
            except:
                pass

        return render(self.request, "register/confirm.html", {"form": form, "block_id": block , "tmp_block": tmp_block, "url": url, "count_tag": count_tag, "category_table": category_table,
                                                         "tmp_file": tmp_file, "category": category, "tags_form": tags, "tags":tags_table, "count_category_tag": count_category_tag})


    def form_invalid(self, form):

        category = self.request.POST.getlist("category")
        tags = self.request.POST.getlist("tags")
        block = self.request.POST.getlist("block")
        block_count = len(block)
        sub_title = self.request.POST.getlist("sub_title")
        content = self.request.POST.getlist("content")
        image = self.request.POST.getlist("pre_image")
        tmp_file = self.request.POST.getlist("tmp_file")
        url = self.request.POST.getlist("url")

        tags_table = TagsInfo.objects.all()
        count_tag = TagstableInfo(self, tags_table)

        category_table = CategoryInfo.objects.all()
        count_category_tag = CategorytableInfo(self, category_table)

        tmp_block = []
        for x in range(0, block_count):
            try:
                tmp_block.append({
                    "block": block[x], "sub_title": sub_title[x], "content": content[x], "image": image[x]
                })
            except:
                pass

        return render(self.request, "register/insert.html", {"form": form, "block_id": block , "tmp_block": tmp_block, "url": url, "count_tag": count_tag, "category_table": category_table,
                                                         "tmp_file": tmp_file, "category": category, "tags_form": tags, "tags":tags_table, "count_category_tag": count_category_tag})

class ArticleDone(generic.FormView):
    model = Article
    form_class = InputForm

    def form_valid(self, form):

        block = self.request.POST.getlist("block")
        category = self.request.POST.getlist("category")
        for z in category:
            if not CategoryInfo.objects.filter(name = z).first():
                category_id = CategoryInfo.objects.create(
                    name = z
                )
                category = category_id.id
            else:
                category = CategoryInfo.objects.filter(name = z).first().id

        tags = self.request.POST.getlist("tags")
        for z in tags:
            if not TagsInfo.objects.filter(name = z).first():
                tags_id = TagsInfo.objects.create(
                    name = z
                )
                tags = tags_id.id
            else:
                tags = TagsInfo.objects.filter(name = z).first().id
        main_title = self.request.POST.get("title")
        print(main_title)
        sub_image = self.request.POST.get("sub_image")
        article_table = Article.objects.create(
            title = main_title, image = sub_image, tags = tags, category = category,
        )
        print(article_table.id)

        sub_title = self.request.POST.getlist("sub_title")
        print(sub_title)
        content = self.request.POST.getlist("content")
        print(content)
        image = self.request.POST.getlist("image")
        print(image)
        tmp_file = self.request.POST.getlist("tmp_file")
        url = self.request.POST.getlist("url")

        tmp_content = []
        for x in range(0, len(block)):
            tmp_content.append({
                "block": block[x], "sub_title": sub_title[x], "content": content[x], "image": image[x],
            })
        for y in tmp_content:
            content = Content.objects.create(
                article_id = article_table.id, block = y["block"], sub_title = y["sub_title"], content = y["content"], image = y["image"],
            )
        for z in url:
            if z is not None or z != "":
                References.objects.create(
                    article_id = article_table.id, title=None, link=z, tmpfile=None
                )
        for t in tmp_file:
            if t is not None or z != "":
                References.objects.create(
                    article_id = article_table.id, title=None, tmpfile=t, link=None
                )

        messages.success(self.request, "記事の内容を投稿しました！！")
        return redirect("apps:top")

"""
投稿を削除
"""

class ArticleDelete(generic.ListView):
    model = Article

    def get(self, request, *args, **kwargs):
        return redirect("apps:top")

    def post(self, request, *args, **kwargs):

        article_id = self.request.POST.get("id")
        print(article_id)
        article_id = int(article_id)

        self.model.objects.filter(id = article_id).update(
            delete_flag = True,
        )

        Content.objects.filter(article_id = article_id).update(
            delete_flag = True,
        )

        References.objects.filter(article_id = article_id).update(
            delete_flag = True,
        )

        d = {
            "article_id": article_id,
        }
        messages.success(self.request, "記事の内容を削除しました！！")
        return JsonResponse(d)

"""
投稿を復活
"""

class ArticleRecovery(generic.ListView):
    model = Article

    def get(self, request, *args, **kwargs):
        return redirect("apps:top")

    def post(self, request, *args, **kwargs):

        article_id = int(self.request.POST.get("id"))
        print(article_id)
        print(type(article_id))
        self.model.objects.filter(id = article_id).update(
            delete_flag = False,
        )

        Content.objects.filter(article_id = article_id).update(
            delete_flag = False,
        )

        References.objects.filter(article_id = article_id).update(
            delete_flag = False,
        )

        d = {
            "article_id": article_id,
        }

        messages.success(self.request, "記事の内容が復活しました！！")
        return JsonResponse(d)