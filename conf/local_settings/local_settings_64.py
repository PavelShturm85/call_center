DEBUG = False

IP = "192.168.4.203"

ALLOWED_HOSTS = ['192.168.4.206', 'crm.med-zakaz.reg64.ru', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crm_medzakaz',
        'USER': 'crm_user',
        'PASSWORD': 'Qw12345%',
        'HOST': 'db',
        'PORT': '5432',
    }
}

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
