from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-73^w0oydk6(59liwfssx9w16zh#@+dz_r9ac=@(h=+dcrrwu4-'
DEBUG = True
domen = 'najmiddin.pythonanywhere.com'
ALLOWED_HOSTS = ['http://'+domen+'/', domen, 'https://'+domen+'/']
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'api_app',
    'rest_framework',
    'django_cleanup.apps.CleanupConfig',
    'modeltranslation',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bot_project.urls'

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
WSGI_APPLICATION = 'bot_project.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
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

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LANGUAGES = (
    ("uz", 'Uzbek'),
    ("ru", 'Russian'),
)
MODELTRANSLATION_TRANSLATION_FILES = (
    'api_app.translation',
)
MODELTRANSLATION_DEBUG = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MODELTRANSLATION_LANGUAGES = ("uz", "ru",)

LOCALE_PATHS = (
    [BASE_DIR, 'locale/']
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
JAZZMIN_SETTINGS = {
    "site_brand": "Bot Admin",
    "welcome_sign": "Sotuv Adminiga xush kelibsiz!",
}
