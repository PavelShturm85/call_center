import os
import time

def migrate():
    '''
    Делаем миграцию базы данных с созданием суперюзера
    '''
    time.sleep(5)
    os.system('python call_center/manage.py migrate')


def run_server(ip='0.0.0.0', port='8101'):
    '''
    Запускаем сервер с нужным ip и портом
    runserver(ip='0.0.0.0', port='8101')
    '''
    os.system('python call_center/manage.py runserver ' +
              ip + ':' + port)


if __name__ == '__main__':
    
    migrate()
    run_server()
