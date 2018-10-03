DEBUG = False

IP = "192.168.34.203"
ASTER_USER = 'powcrmami'
ASTER_PASS = 'zimoisnegidet32'

ALLOWED_HOSTS = ['192.168.34.201', 'crm.med-zakaz.reg30.ru', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crm_medzakaz',
        'USER': 'crm_user',
        'PASSWORD': 'Qw12345%',
        'HOST': '192.168.34.201',
        'PORT': '5432',
    }
}

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
NAME_GROUP_PHONE_NUMBER = 'QUEUE'
DIR_ANSWERING_MACHINE_FILES = "0080/INBOX/"
