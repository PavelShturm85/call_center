import uuid
import re
import os
from django.db import models
from users.models import User
from django.utils import timezone
# Create your models here.


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(
        max_length=12, verbose_name='Номер телефона с которого звонили')
    surname = models.CharField(max_length=30, verbose_name='Фамилия клиента')
    name = models.CharField(max_length=30, verbose_name='Имя клиента')
    patronymic = models.CharField(
        max_length=30, verbose_name='Отчество клиента')
    coment = models.TextField(verbose_name='Комментарий', blank=True)

    @property
    def fio(self):
        return '{} {} {}'.format(self.surname, self.name, self.patronymic)

    def __str__(self):
        return '{} {} {} {}'.format(self.phone_number, self.surname, self.name, self.patronymic)


class Call(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_call = models.DateTimeField(
        verbose_name='Время звонка', blank=True, null=True)
    call_duration = models.CharField(
        max_length=20, verbose_name='Длительность звонка', blank=True, null=True)
    file_name = models.CharField(
        max_length=100, verbose_name='Файл с записью', blank=True, null=True)
    DISPOSITION_CHOICES = (
        ('ANSWERED', 'Отвечен'),
        ('NO ANSWER', 'Без ответа'),
        ('OUTGOING', 'Исходящий'),
        ('OUT NO ANSWER', 'Исх. без ответа')
    )
    disposition = models.CharField(
        max_length=15, choices=DISPOSITION_CHOICES, verbose_name='Статус звонка', blank=True, null=True)
    type_task = models.CharField(
        max_length=50, verbose_name='Тип проблемы', blank=True, null=True)
    description_task = models.TextField(
        verbose_name='Описание прорблемы', blank=True, null=True)
    dst_phone_number = models.CharField(
        max_length=12, verbose_name='Номер телефона куда звонили')
    unique_id = models.CharField(
        max_length=50, verbose_name='Идентификатор активного звонка и истории')
    # булевые статусы
    task_completed_identifier = models.BooleanField(
        default=False, verbose_name='Идентификатор завершенной задачи')
    status_task = models.BooleanField(
        default=False, verbose_name='Статус проблемы обработана/необработана')
    is_end = models.BooleanField(
        default=False, verbose_name='Завершен ли разговор')
    is_get_history = models.BooleanField(
        default=False, verbose_name='Получена ли история звонка')
    # внешние ключи
    executor_task = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="executor_task", blank=True, null=True)
    login_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="login_name", blank=True, null=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def client_phone(self):
        return self.client.phone_number

    @property
    def client_surname(self):
        return self.client.surname

    @property
    def path_to_file(self):
        path = re.split('[- .]', self.file_name)
        if len(path) > 2:
            date = path[3]
            return os.path.join(date[:4], date[4:6], date[6:])

    @property
    def path_to_file_with_name(self):
        return os.path.join(self.path_to_file, self.file_name)

    def __str__(self):
        return '{} {}'.format(self.date_call, self.client)


class LogCall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    log_time = models.DateTimeField(
        verbose_name='Время звонка', blank=True, null=True)
    call = models.ForeignKey(
        Call, on_delete=models.CASCADE, blank=True, null=True)
    old_executor_task = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="old_executor_task", blank=True, null=True)
    old_type_task = models.CharField(
        max_length=50, verbose_name='Тип проблемы до изменения', blank=True, null=True)
    old_description_task = models.TextField(
        verbose_name='Описание прорблемы до изменения', blank=True, null=True)
    user_changed_record = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_changed_record", blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.log_time, self.call.id)
