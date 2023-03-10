"""
Django settings for memeta_core project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# to keep secrets secret
import environ
env = environ.Env()
#reading .env file
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'memeta_app',
    'ckeditor',
    'members',
    'bootstrap4',
    'bootstrap_datepicker_plus',
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

ROOT_URLCONF = 'memeta_core.urls'

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

WSGI_APPLICATION = 'memeta_core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  BASE_DIR / 'db.sqlite3' #env("DATABASE_NAME"),
        #'USER': env(DATABASE_USER),
        #'PASSWORD': env(DATABASE_PASSWORD),
        #'HOST': env(DATABASE_HOST),
        #'PORT': env(DATABASE_PORT),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'de-CH'

TIME_ZONE = 'Europe/Zurich'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'



# ck-editor configs

CKEDITOR_CONFIGS = {
'default': {
    "toolbar_Full": [
        ["Bold","Italic", "Underline", "Strike", "Subscript", "Superscript" ],
        #["SpecialChar"],
        ["TextColor", "BGColor", "FontSize"],
        ["NumberedList", "BulletedList", "Table"],
        ["JustifyLeft", "JustifyCenter", "JustifyRight"],
        ["Link", "Image"],#, "Unlink"],
        #["Undo", "Redo"],
        #["Maximize"]
    ],
    "toolbar": "Full",
    "height": "20rem",
    "width": "auto",
}}

# datepicker confics

BOOTSTRAP_DATEPICKER_PLUS = {
    "options": {
        "locale": 'de_ch',
        "showClose": True,
        "showClear": True,
        #"showTodayButton": True,
        "allowInputToggle": True,
        "focusOnShow": False,
        "useCurrent": True
    },
    "variant_options": {
        "date": {
            "format": "DD.MM.YYYY HH.mm",
        },
    }
}