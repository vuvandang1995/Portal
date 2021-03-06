"""
Django settings for kvmvdi project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7hv4f0ouw@aj1gtksutos-af)2@i&@b&i1+671l31sdhi(+^00'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
ASGI_APPLICATION = 'kvmvdi.routing.application'


# Application definition

INSTALLED_APPS = [
    'channels',
    'superadmin',
    'client',
    'django_rq',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

AUTH_USER_MODEL = 'superadmin.MyUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kvmvdi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'kvmvdi.wsgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('rd', 6379)],
        },
    },
}

# rq
RQ_QUEUES = {
    'default': {
        'HOST': 'rd',
        'PORT': 6379,
        'DB': 0,
    },
    'with-sentinel': {
       'SENTINELS': [('localhost', 26736), ('localhost', 26737)],
       'MASTER_NAME': 'redismaster',
       'DB': 0,
       'PASSWORD': 'secret',
       'SOCKET_TIMEOUT': None,
    },
    'high': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'), # If you're on Heroku
        'DEFAULT_TIMEOUT': 500,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    }
}


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kvm_vdi',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'db',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ticketmdtpro@gmail.com'
EMAIL_HOST_PASSWORD = 'meditech2018'
EMAIL_PORT = 587


OPS_IP = '10.10.10.99'
# OPS_IP = '192.168.40.146'
OPS_ADMIN = 'admin'
OPS_PASSWORD = 'ITC*123@654'
# OPS_PASSWORD = 'admin'
OPS_PROJECT = 'admin'
OPS_TOKEN_EXPIRED = 1500

ROLE_USER = 'user'
ROLE_ADMIN = 'admin'
# ROLE_USER = '_member_'
# ROLE_ADMIN = 'admin'

# list_net_provider = ['public']
list_net_provider = ['VLAN999', 'VLAN_699']
NET_SELF = ''

DISK_SSD = 'ceph-ssd'
DISK_HDD = 'ceph-hdd'

VNPAY_RETURN_URL = 'http://portal.intercom.vn/payment_return'  # get from config
VNPAY_PAYMENT_URL = 'http://sandbox.vnpayment.vn/paymentv2/vpcpay.html'  # get from config
VNPAY_API_URL = 'http://sandbox.vnpayment.vn/merchant_webapi/merchant.html'
VNPAY_TMN_CODE = 'INTERCOM'  # Website ID in VNPAY System, get from config
VNPAY_HASH_SECRET_KEY = 'REWEKUZMPNPFLYPPEEMYABEEDDYMKXFN'  # Secret key for create checksum,get from config

PRICE_RAM = 50000
PRICE_VCPUS = 60000
PRICE_DISK_HDD = 3000
PRICE_DISK_SSD = 5000
