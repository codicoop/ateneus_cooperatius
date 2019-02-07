"""
Django settings for coopolis_backoffice project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '../apps')))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(*th*d##@a1!hu4_ziu_hd=a9q=y9(iiz%6-bc=!^x@1f0d5o!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.coopolis.apps.CoopolisConfig',
    'apps.cc_users.apps.UsersConfig',
    'apps.cc_courses.apps.CoursesConfig',
    'django.contrib.admin',
    'constance.backends.database',
    'constance',
    'django_summernote',
    'storages'
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

ROOT_URLCONF = 'coopolis_backoffice.urls'

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

WSGI_APPLICATION = 'coopolis_backoffice.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'coopolis',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword',
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ca'

TIME_ZONE = 'Europe/Andorra'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = 'loginsignup'
LOGIN_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTH_USER_MODEL = 'coopolis.User'
DEV_SETTINGS_MODULE = 'coopolis_backoffice.settings.dev'

# APPS

USERS_APP_TITLE = 'Gestió de persones'
COURSES_APP_TITLE = "les formacions i activitats"

FIXTURES_PATH_TO_COURSE_IMAGES = 'test-images/coopolis-courses'

# Storage Service

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = 'codi.coop.test'
AWS_S3_CUSTOM_DOMAIN = f's3.wasabisys.com/{AWS_STORAGE_BUCKET_NAME}'
AWS_S3_ENDPOINT_URL = 'https://s3.wasabisys.com'
AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'cc_lib.storages.MediaStorage'
EXTERNAL_MEDIA_PATH = 'coopolis/media'
MEDIA_FILE_OVERWRITE = True

# Constance
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'INTRODUCTION_TEXT': ("""
Des de Coòpolis disposem d’una oferta regular de formació en economia social i cooperativisme per a tots els públics, tant per a aquelles persones que tenen ganes d’apropar-se a l’economia social i solidària, com per a aquelles persones o col·lectius que estan pensant en constituir el seu propi projecte econòmic. A més de les activitats a l’espai Coòpolis de Can Batlló, també oferim formacions descentralitzades en altres espais comunitaris i seus de l’economia social i solidària barcelonina.
""", 'Text de presentació')
}
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True

# CC Courses

COURSES_LIST_VIEW_CLASS = 'apps.coopolis.views.CoopolisCoursesListView'
COURSES_CLASS_TO_ENROLL = 'coopolis.User'
COURSES_CLASSES_CAN_ENROLL = ['cc_courses.models.Course']

FIXTURE_FACTORIES = [
    ('coopolis.tests.fixtures.UserFactory', {}),
    ('coopolis.tests.fixtures.ProjectFactory', {}),
    ('cc_courses.tests.fixtures.CourseFactory', {}),
    ('cc_courses.tests.fixtures.EntityFactory', {}),
    ('cc_courses.tests.fixtures.CoursePlaceFactory', {}),
    ('cc_courses.tests.fixtures.ActivityFactory', {
        'number': 500
    }),
]

STATIC_ROOT = 'static'


SIGNUP_FORM = 'coopolis.forms.MySignUpForm'