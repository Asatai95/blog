from django.contrib import auth
from django.conf import settings
from django.db import models, transaction
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, Group, User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import validate_email, EmailValidator, FileExtensionValidator, MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.db.models.manager import EmptyManager
# from django.shortcuts import redirect

import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.models import CloudinaryField

import os
import re
from datetime import datetime

# ユーザー管理
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

# session管理
from django.core.management.base import BaseCommand


class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not email:
            raise ValueError('The given email must be set')

        username_validator = ASCIIUsernameValidator()
        username = self.model.normalize_username(username, required=False, validators=[username_validator])
        email = self.normalize_email(email, required=True)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル(業者用テーブル)"""

    id = models.AutoField(primary_key=True)
    username = models.CharField(_('username'), max_length=150, unique=False)
    password = models.CharField(u"パスワード", max_length=150)
    email = models.EmailField(u'メールアドレス', unique=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    updated_at = models.DateTimeField(_('date joined'), auto_now = True)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'mysite_user'

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Article(models.Model):

    id = models.AutoField(primary_key=True)
    article = models.IntegerField(_('user id'), blank=True , null=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('created at'), auto_now=True)

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('article')
        db_table = 'article'
