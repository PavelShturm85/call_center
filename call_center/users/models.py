import uuid
import requests
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):

    DIRECTOR = 'DIR'
    OPERATOR = 'OPR'
    DEFAULT = ''
    POSITION_CHOICES = (
        (DEFAULT, ''),
        (DIRECTOR, 'Директор'),
        (OPERATOR, 'Оператор'),
    )
    position = models.CharField(max_length=3,
                                choices=POSITION_CHOICES,
                                default=DEFAULT,
                                verbose_name='Должность', blank=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    send_email = models.BooleanField(
        default=False, verbose_name='Уведомлять по почте')
    phone_number = models.CharField(
        max_length=11, verbose_name='Личный номер', blank=True)
    phone_number_local = models.CharField(
        max_length=4, verbose_name='Внутренний номер', blank=True, null=True)
