import os


def migrate():
    '''
    Делаем миграцию базы данных с созданием суперюзера
    '''
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
