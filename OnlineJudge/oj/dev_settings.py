# coding=utf-8
import os

if 'JUDGE_SERVER_TOKEN' not in os.environ:
    os.environ['JUDGE_SERVER_TOKEN'] = (
        'e23db591aae7131eaff626d896a30c440435524acfc837224f5391709a15fa63'
    )

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '127.0.0.1',
        'PORT': 5435,
        'NAME': "onlinejudge",
        'USER': "onlinejudge",
        'PASSWORD': 'onlinejudge'
    }
}

REDIS_CONF = {
    "host": "127.0.0.1",
    "port": "6380"
}

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATA_DIR = f"{BASE_DIR}/data"
