# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import sys
import requests
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
# при запуске на сервере - изменить путь 'settings.PATH_TO_PROJECT' до проекта
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
sys.path.append(settings.PATH_TO_PROJECT)
import django
django.setup()
from crm.models import Call, Client, User
from celery import task
from django.utils import timezone


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


@task()
def get_activ_call():
    url = settings.ACTIV_CALL_URL
    repositories = requests.get(url, verify=False).json()

    if repositories:
        for key in repositories:
            active_call = repositories[key]
            try:
                in_option_call = convert_unique_id(active_call['level 14'])
                in_dst_phone = active_call['Caller ID']
                in_src_phone = active_call['Connected Line ID']

                if in_dst_phone in groups_phone_numbers() \
                        and in_option_call \
                        and not Call.objects.filter(unique_id=in_option_call).exists():

                    save_active_call(
                        in_src_phone, in_option_call, in_dst_phone)

            except(KeyError):
                pass

            try:
                out_src_phone = convert_out_src_phone(
                    active_call['SIPURI=sip'])
                out_option_call = convert_unique_id(active_call['level 16'])
                out_dst_phone = convert_out_dst_phone(active_call["level 13"])

                if out_src_phone in groups_phone_numbers() \
                        and not Call.objects.filter(unique_id=out_option_call).exists():

                    save_active_call(
                        out_dst_phone, out_option_call, out_src_phone)

            except(KeyError):
                pass


@task()
def get_call_history():
    url = settings.CALL_HISTORY_URL
    repositories = requests.get(url, verify=False).json()

    if repositories:
        repositories.pop("total")
        for key in repositories:
            call_history = repositories[key]
            try:
                _date_call = call_history["calldate"]
                _call_duration = call_history["billsec"]
                _disposition = call_history["disposition"]
                _file_name = call_history["recordingfile"]
                _unique_id = call_history["uniqueid"]
                unique_id_call = Call.objects.filter(
                    unique_id=_unique_id).exists()
                is_get_history = Call.objects.filter(
                    unique_id=_unique_id).filter(is_get_history=True).exists()

                if unique_id_call and not is_get_history:
                    outgoing_call = "from-internal"
                    no_answer = "NO ANSWER"

                    if outgoing_call in call_history["dcontexts"] \
                            and no_answer in _disposition:
                        current_disposition = "OUT NO ANSWER"

                    elif outgoing_call in call_history["dcontexts"]:
                        current_disposition = "OUTGOING"

                    else:
                        current_disposition = _disposition

                    Call.objects.filter(unique_id__exact=_unique_id).update(
                        date_call=_date_call,
                        call_duration=_call_duration,
                        file_name=_file_name,
                        is_end=True,
                        is_get_history=True,
                        disposition=current_disposition
                    )

            except(KeyError):
                pass


def save_active_call(src_phone, option_call, dst_phone):
    client, _ = Client.objects.get_or_create(
        phone_number=src_phone)
    Call.objects.create(
        client=client,
        unique_id=option_call,
        dst_phone_number=dst_phone,
    )


@task
def del_group_phone_number():
    time = timezone.now() - timezone.timedelta(minutes=2)
    user = User.objects.filter(last_login__lte=time)
    user.update(phone_number_local="")

    
def convert_out_src_phone(out_src_phone):
    return out_src_phone.split('@')[0]


def convert_out_dst_phone(out_dst_phone):
    return out_dst_phone.split('=')[1]


def convert_unique_id(source):
    if not source or not "recordingfile" in source:
        return None
    else:
        return os.path.splitext(source.split('-')[-1])[0]


def groups_phone_numbers():
    url = settings.GROUP_PHONE_NUMBER_URL
    phones_json = requests.get(url, verify=False).json()
    return phones_json[settings.NAME_GROUP_PHONE_NUMBER].split('-')


if __name__ == '__main__':
    get_activ_call()
    get_call_history()
