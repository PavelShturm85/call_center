import os
import time


def celery_beat():
    os.system('celery -A call_center beat --workdir /crm/call_center/ -l info')

if __name__ == '__main__':
    time.sleep(5)
    celery_beat()
