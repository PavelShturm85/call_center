"""
Django settings for call_center project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from celery.schedules import crontab
# import crm

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c=(m^i#+y4!ph%ugvqkq#acr+ml90cram(852)1tl$jc-_%t#h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# new user class
AUTH_USER_MODEL = 'users.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'crm.apps.CrmConfig',
    'django_filters',
    'bootstrap3',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'call_center.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./call_center/templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'call_center.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
} """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crm_medzakaz',
        'USER' : 'crm_user',
        'PASSWORD' : 'Qw12345%',
        'HOST' : '127.0.0.1',
        'PORT' : '5432',
    }
}
# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Saratov'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/choice_phone/'

# Celery application definition
CELERY_IMPORTS = (
    'call_center.tasks',
)
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = False
CELERY_BEAT_SCHEDULE = {
    'task-get_activ_call': {
        'task': 'call_center.tasks.get_activ_call',
        'schedule': 1.0,
        # 'args': (*args)
    },
    'task-get_call_history': {
        'task': 'call_center.tasks.get_call_history',
        'schedule': 2.0,
        # 'args': (*args)
    },
    'task-del_group_phone_number': {
        'task': 'call_center.tasks.del_group_phone_number',
        'schedule': 60.0,
        # 'args': (*args)
    },
}

# EMAIL
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "med.zakaz.crm@gmail.com"
EMAIL_HOST_PASSWORD = "Qw12345%"
EMAIL_USE_TLS = True

# session
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 40000
# SESSION_SAVE_EVERY_REQUEST = True


# paths to tasks.py and watcher.py
PATH_TO_ANSWERING_MACHINE = os.path.join(STATIC_URL, "files/0080/INBOX/")
PATH_TO_CALLS = os.path.join(STATIC_URL, "files/monitor/")
MAIL_PATH_TO_ANSWERING_MACHINE = os.path.join(BASE_DIR, "crm/static/files/0080/INBOX/")
MAIL_PATH_TO_CALLS = os.path.join(BASE_DIR, "crm/static/files/monitor/")
PATH_TO_PROJECT = BASE_DIR
ACTIV_CALL_URL = 'https://192.168.34.203/c2c/conversations.php?act=get'
CALL_HISTORY_URL = 'https://192.168.34.203/c2c/cdr.php?limit=0,200'
GROUP_PHONE_NUMBER_URL = 'https://192.168.34.203/c2c/get_group_members.php'
NAME_GROUP_PHONE_NUMBER = 'QUEUE'

# version
VERSION = "© 2017, 2018 - МедЗаказ - CRM - Версия: 2018.6"
