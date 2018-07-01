import os



def celery_worker():
    os.system('cd call_center/call_center')
    os.system('celery -A call_center worker -l info')

if __name__ == '__main__':
    celery_worker()
