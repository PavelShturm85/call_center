import os
import time


def celery_worker():
    os.system('celery -A call_center worker --workdir /crm/call_center/ -l info')

if __name__ == '__main__':
    time.sleep(5)
    celery_worker()
