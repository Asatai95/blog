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
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from django.db import models
from django.db.models import Q, Count, Max
from .models import (
    User, Article,
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

# from .forms import (

# )

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


class MainView(generic.ListView):
    template_name = "apps/index.html"
    model = Article

    def get(self, request, *args, **kwargs):
        print("test")
        return render(self.request, self.template_name)