# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import sys
import requests
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
sys.path.append(settings.BASE_DIR)
import django
django.setup()
from crm.models import Call, Client, User
from celery import task
from django.utils import timezone


# Получение звонков ушедших на автоответчик.
class SaveAnsweringMachineCalls():

    def __init__(self, path_to_file):
        self.__path_to_file = path_to_file
        self.__name_file = os.path.basename(self.__path_to_file)
        self.__src_number, self.dst_number, \
            self.__duration, self.__msg_id = self.__get_call

    @property
    def __get_call(self):
        config = configparser.ConfigParser()
        config.read(self.__path_to_file)
        src_number = config.get('message', "callerid")
        dst_number = config.get('message', "origmailbox")
        duration = config.get('message', "duration")
        msg_id = config.get('message', "msg_id")
        return src_number, dst_number, duration, msg_id

    @property
    def __make_waw_file(self):

        return self.__name_file.split('.')[0] + '.wav'

    @property
    def __make_source_number(self):

        return self.__src_number.split('"')[1]

    def save_call(self):

        client, _ = Client.objects.get_or_create(
            phone_number=self.__make_source_number)
        Call.objects.create(
            dst_phone_number=self.dst_number,
            client=client,
            date_call=timezone.now(),
            call_duration=self.__duration,
            file_name=self.__make_waw_file,
            unique_id=self.__msg_id,
            disposition='NO ANSWER',
            is_end=True,
            is_get_history=True,
        )


@task
def del_group_phone_number():
    time = timezone.now() - timezone.timedelta(minutes=2)
    user = User.objects.filter(last_login__lte=time)
    user.update(phone_number_local="")


def groups_phone_numbers():
    url = settings.GROUP_PHONE_NUMBER_URL
    phones_json = requests.get(url, verify=False).json()
    return phones_json[settings.NAME_GROUP_PHONE_NUMBER].split('-')


if __name__ == '__main__':
    pass
