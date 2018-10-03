import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'call_center.settings')
django.setup()
from django.conf import settings
from crm.models import Call, Client
from django.utils import timezone
import asyncio
import pytz
import requests
from datetime import datetime, timedelta
from panoramisk import Manager


manager = Manager(loop=asyncio.get_event_loop(),
                  host=settings.IP,
                  username=settings.ASTER_USER,
                  secret=settings.ASTER_PASS)


def groups_phone_numbers():
    url = settings.GROUP_PHONE_NUMBER_URL
    phones_json = requests.get(url, verify=False).json()
    return phones_json[settings.NAME_GROUP_PHONE_NUMBER].split('-')


numbers = groups_phone_numbers()


@manager.register_event('Hangup')
@manager.register_event('Newexten')
@manager.register_event('BridgeEnter')
def callback(manager, message):
    phone_number = get_phone_number(message.channel)

    unique_id_call = Call.objects.filter(
        unique_id=message.linkedid).exists()

    if 'BridgeEnter' in message.event \
            and phone_number in numbers \
            and ("macro-dialout-trunk" == message.context or "macro-dial" == message.context):

        phone_number = message.connectedlinenum
        if len(phone_number) == 11 and (phone_number.startswith('7') or phone_number.startswith('8')):
            client_phone = '+7{}'.format(phone_number[1:])
        elif len(phone_number) == 10 and (phone_number.startswith('9') or phone_number.startswith('8')):
            client_phone = '+7{}'.format(phone_number)
        else:
            client_phone = phone_number

        client, _ = Client.objects.get_or_create(
            phone_number=client_phone)
        Call.objects.create(
            client=client,
            unique_id=message.linkedid,
            dst_phone_number=phone_number,
            date_call=get_date_time(message.linkedid),
        )

    elif 'Hangup' in message.event \
            and phone_number in numbers \
            and unique_id_call \
            and 'Up' in message.channelstatedesc:

        params = {'macro-dial-one': 18,
                  'from-internal': 4,
                  'macro-dial': 43,
                  'indigo': 38,
                  }
        for key in params:
            if key in message.context:
                seconds = params[key]
            else:
                seconds = 0

        utc_timezone = pytz.timezone('UTC')
        _call_duration = timezone.now() - utc_timezone.localize(
            datetime.utcfromtimestamp(float(message.linkedid))) - timedelta(seconds=seconds)

        Call.objects.filter(unique_id__exact=message.linkedid).update(
            call_duration=_call_duration,
            is_end=True,
            is_get_history=True,
        )

    elif 'Newexten' in message.event \
            and 'AGI' in message.application \
            and 'macro-hangupcall' in message.context \
            and unique_id_call \
            and get_file_name(message.appdata).endswith('.wav'):

        file_name = get_file_name(message.appdata)
        call = Call.objects.filter(unique_id__exact=message.linkedid)
        filename_list = file_name.split('-')

        if filename_list[0] == 'out':
            disposition = 'OUTGOING'
        elif filename_list[0] == 'internal':
            call.update(
                dst_phone_number=filename_list[1],
            )
            disposition = 'ANSWERED'
        else:
            disposition = 'ANSWERED'

        call.update(
            file_name=file_name,
            disposition=disposition,
        )


def get_file_name(appdata):
    return appdata.split('/')[-1]


def get_date_time(timestamp):
    utc_timezone = pytz.timezone('UTC')
    utc_datatime = utc_timezone.localize(
        datetime.utcfromtimestamp(float(timestamp)))
    timezone = pytz.timezone(settings.TIME_ZONE)
    return timezone.normalize(utc_datatime.astimezone(timezone))


def get_phone_number(channel):
    return channel.split('/')[1].split('-')[0]


def main():
    manager.connect()
    try:
        manager.loop.run_forever()
    except KeyboardInterrupt:
        manager.loop.close()


if __name__ == '__main__':
    main()
