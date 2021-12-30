import pytz

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users/', blank=True)
    age = models.PositiveSmallIntegerField(default=18, verbose_name='Возраст')

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expired = models.DateTimeField(blank=True, null=True)

    def is_activation_key_expired(self):
        return datetime.now(pytz.timezone(settings.TIME_ZONE)) <= self.activation_key_expired + timedelta(hours=48)


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'N'

    GENDERS = (
        (MALE, 'M'),
        (FEMALE, 'F'),
        (UNKNOWN, 'N'),
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tag_lines = models.CharField(max_length=128, blank=True, null=True, verbose_name='Тэги')
    about_me = models.CharField(max_length=512, blank=True, null=True, verbose_name='Обо мне')
    gender = models.CharField(max_length=1, choices=GENDERS, default=UNKNOWN, verbose_name='Пол')
    github_profile = models.URLField(verbose_name='Github', null=True, blank=True)
