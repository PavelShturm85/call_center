import os
import time


def migrate():
    '''
    Делаем миграцию базы данных с созданием суперюзера
    '''
    time.sleep(5)
    os.system('python call_center/manage.py migrate')


def uwsgi():
    time.sleep(5)
    os.system('uwsgi --master --ini /crm/conf/uwsgi/call_center.ini')


if __name__ == '__main__':

    migrate()
    uwsgi()
