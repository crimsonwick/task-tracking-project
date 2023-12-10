#superuser: ceo, ezpz@123
"""
Django settings for TaskTrackingApp project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4(1_p(5$2zme35arzx%*4_7s703bu+xn*5aa3^ke%t$a@0^x^z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRDPARTY_APPS = (
    'rest_framework',
    'oauth2_provider'
)

PROJECT_APPS = (
    'api',
    'main',
    'api.users',
    'api.task',
)

INSTALLED_APPS = DJANGO_APPS + THIRDPARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'TaskTrackingApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'TaskTrackingApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'TaskTracking',
        'USER': os.getenv('PG_USER', 'postgres'),
        'PASSWORD': os.getenv('PG_PASSWORD', 'password'),
        'HOST': os.getenv('PG_HOST', 'localhost'),
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Temporary allowing CORS.
# CORS_ORIGIN_ALLOW_ALL = True

#required for authentication of user through our authentication backends
AUTH_USER_MODEL = "users.User"


# OAuth Authentication Setup

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
]

OAUTH2_PROVIDER = {
    # For now, saving access token for 9 Hours!
    'ACCESS_TOKEN_EXPIRE_SECONDS': 60 * 60 * 9,
}
HOST_URL = os.getenv(
    'HOST_URL',
    'http://127.0.0.1:8000'
)
AUTHORIZATION_SERVER_URL = f'{HOST_URL}/api/oauth/token/'
REVOKE_TOKEN_URL = os.getenv(
    'REVOKE_TOKEN_URLs',
    f'{HOST_URL}/api/oauth/revoke-token/'
)
OAUTH_CLIENT_ID = os.getenv(
    'OAUTH_CLIENT_ID',
    'g7oWmo7JuYFQKD71jhE5bCsgHFVM6frqV0mn8VgD'
)
OAUTH_CLIENT_SECRET = os.getenv(
    'OAUTH_CLIENT_SECRET',
    'pAje47ISzhW0mazvVpxYfvRBpUy5OIRnIllT2VLLpp6L37rnSJfcxNNS7rWLMx8XgSHHhTmNAG7vebqVaE0PcenadkizAD9kf0DIt08e9vz0tcZv2Sx7tscNYTgPMbvG'
)

SUPER_ADMIN = ["admin@yopmail.com",]
WEB_URL = ""
