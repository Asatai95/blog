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

class Login(LoginView):

    form_class = LoginForm
    template_name = 'register/login.html'

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, {"form": self.form_class})

class Logout(LoginRequiredMixin, LogoutView):

    def get(self, request, *args, **kwargs):
        return redirect("apps:logout")

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
        tmp_tag = []
        if tags.first():
            for x in tags:
                for y in table:
                    if x.id == y.tags:
                        tmp_tag.append(x.name)
            count_tag = Counter(tmp_tag)
            for k, v in count_tag.items():
                count_tag[k] = str(v)
            count_tag = dict(count_tag)
        else:
            count_tag = None

        category_table = CategoryInfo.objects.all()
        tmp_category = []
        if category_table.first():
            for x in category_table:
                for y in table:
                    if x.id == y.category:
                        tmp_category.append(x.name)
            count_category_tag = dict(Counter(tmp_category))
        else:
            count_category_tag = None

        return render(self.request, self.template_name, {"table": table, "date": tmp_date, "tags": tags, "count_tag": count_tag, "category_table": category_table, "count_category_tag": count_category_tag})

class ArticleInfo(generic.DetailView):
    template_name = "apps/info.html"
    model = Article

    def get(self, request, *args, **kwargs):

        pk = self.kwargs.get("pk")
        print("pk")
        print(pk)
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
        tmp_tag = []
        if tags.first():
            for x in tags:
                if x.id == table.tags:
                    tmp_tag.append(x.name)
            count_tag = dict(Counter(tmp_tag))
        else:
            count_tag = None

        category_table = CategoryInfo.objects.all()
        tmp_category = []
        if category_table.first():
            for x in category_table:
                for y in self.model.objects.all():
                    if x.id == y.category:
                        tmp_category.append(x.name)
            count_category_tag = dict(Counter(tmp_category))
        else:
            count_category_tag = None

        return render(request, self.template_name, {"info": table, "date": tmp_date, "content": content, "content_id": content_id, "category_table": category_table,
                                                    "references": references, "tags": tags, "count_tag": count_tag, "count_category_tag": count_category_tag} )

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
        tmp_tag = []
        if tags.first():
            for x in tags:
                for y in self.model.objects.all():
                    if x.id == y.tags:
                        tmp_tag.append(x.name)
            count_tag = dict(Counter(tmp_tag))
        else:
            count_tag = None

        category_table = CategoryInfo.objects.all()
        tmp_category = []
        if category_table.first():
            for x in category_table:
                for y in self.model.objects.all():
                    if x.id == y.category:
                        tmp_category.append(x.name)
            count_category_tag = dict(Counter(tmp_category))
        else:
            count_category_tag = None

        return render(self.request, self.template_name, {"table": table, "date": tmp_date, "tags": tags, "count_tag": count_tag,
                                                         "category_table": category_table, "count_category_tag": count_category_tag})

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
        tmp_tag = []
        if tags.first():
            for x in tags:
                for y in self.model.objects.all():
                    if x.id == y.tags:
                        tmp_tag.append(x.name)
            count_tag = Counter(tmp_tag)
            for k, v in count_tag.items():
                count_tag[k] = str(v)
            count_tag = dict(count_tag)
        else:
            count_tag = None

        category_table = CategoryInfo.objects.all()
        tmp_category = []
        if category_table.first():
            for x in category_table:
                for y in self.model.objects.all():
                    if x.id == y.category:
                        tmp_category.append(x.name)
            count_category_tag = dict(Counter(tmp_category))
        else:
            count_category_tag = None

        return render(self.request, self.template_name, {"table": table, "date": tmp_date, "tags": tags, "count_tag": count_tag, "category_id": id,
                                                         "category_table": category_table, "count_category_tag": count_category_tag})

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
        tmp_tag = []
        if tags.first():
            for x in tags:
                for y in table:
                    if x.id == y.tags:
                        tmp_tag.append(x.name)
            count_tag = dict(Counter(tmp_tag))
        else:
            count_tag = None
        category_table = CategoryInfo.objects.all()
        tmp_category = []
        if category_table.first():
            for x in category_table:
                for y in self.model.objects.all():
                    if x.id == y.category:
                        tmp_category.append(x.name)
            count_category_tag = dict(Counter(tmp_category))
        else:
            count_category_tag = None

        return render(self.request, self.template_name, {"table": table, "date": tmp_date, "tags": tags, "count_tag": count_tag, "all_tags": "all_tags",
                                                         "category_table": category_table, "count_category_tag": count_category_tag})

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
        tmp_tag = []
        if tags.first():
            for x in tags:
                for y in self.model.objects.all():
                    if x.id == y.tags:
                        tmp_tag.append(x.name)
            count_tag = dict(Counter(tmp_tag))
        else:
            count_tag = None

        category_table = CategoryInfo.objects.all()
        tmp_category = []
        if category_table.first():
            for x in category_table:
                for y in self.model.objects.all():
                    if x.id == y.category:
                        tmp_category.append(x.name)
            count_category_tag = dict(Counter(tmp_category))
        else:
            count_category_tag = None

        return render(self.request, self.template_name, {"table": table, "date": tmp_date, "tags": tags, "count_tag": count_tag, "tags_id": id,
                                                         "category_table": category_table, "count_category_tag": count_category_tag})

class ArticleCreate(generic.FormView):
    template_name = "register/insert.html"
    model = Article
    form_class = InputForm

    def get(self, request, *args, **kwargs):

        tags_table = TagsInfo.objects.all()
        category_table = CategoryInfo.objects.all()
        content = Content.objects.all()

        return render(self.request, self.template_name, {"form": self.form_class, "tags": tags_table, "category_table": category_table, "content": content})

    def form_valid(self, form):

        return render(self.request, self.template_name, {"form": form})