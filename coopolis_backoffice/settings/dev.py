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
    'constance.backends.database',
    'constance',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'django_summernote',
    'storages',
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
                'constance.context_processors.config',
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
    },
    'old': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'coopolis_old',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
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

USERS_APP_TITLE = 'Usuàries'
COURSES_APP_TITLE = "Formacions"

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
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_SUPERUSER_ONLY = False
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    # Courses
    'CONTENT_COURSES_INTRODUCTION': (
        "Des de Coòpolis disposem d’una oferta regular de formació en economia social i cooperativisme per a tots els "
        "públics, tant per a aquelles persones que tenen ganes d’apropar-se a l’economia social i solidària, com per "
        "a aquelles persones o col·lectius que estan pensant en constituir el seu propi projecte econòmic. A més de "
        "les activitats a l’espai Coòpolis de Can Batlló, també oferim formacions descentralitzades en altres espais "
        "comunitaris i seus de l’economia social i solidària barcelonina.",
        "Formació: text d'introducció a la franja blava"),
    # Project
    'CONTENT_PROJECT_INTRODUCTION': (
        "<p>Des de Coòpolis acompanyem projectes en la seva posada en marxa i constitució com a cooperatives, en aquells "
        "aspectes centrals per a la seva activitat i facilitem eines i recursos per a la seva consolidació i "
        "creixement. També dissenyem itineraris per a la transformació d’associacions i altres formes d’empreses a "
        "cooperatives.</p>",
        "Apartat Projecte: text d'introducció a la franja blava."),
    'CONTENT_PROJECT_TITLE': (
        "Assessorament",
        "Apartat Projecte: text d'encapçalament"),
    'CONTENT_PROJECT_INFO': (
        "<p>Per sol·licitar acompanyament per al teu projecte, accedeix amb el teu compte o crea'n un amb els "
        "formularis que hi ha a continuació.</p>",
        "Aartat Projecte: Text que es mostra a l'apartat si hi accedeix sense haver fet login"),
    'CONTENT_PROJECT_NEW': (
        "<p>Omple el següent formulari per sol·licitar un acompanyament.</p>",
        "Apartat Projecte: Text que es mostra al formulari per sol·licitar un acompanyament"),
    # Home
    'CONTENT_HOME_COURSES_TITLE': (
        "Formació i activitats",
        "Portada, títol del bloc que informa sobre la formació."),
    'CONTENT_HOME_COURSES_TEXT': (
        "Disposem d’una oferta regular de formació en economia solidària i cooperativisme per a tots els públics, tant "
        "per a aquelles persones que tenen ganes d’apropar-se a l’ESS per primera vegada, els col·lectius que estan "
        "engegant un projecte, i cooperatives que volen consolidar la seva activitat incorporant nous coneixements "
        "especialitzats.",
        "Portada, títol del bloc que informa sobre la formació."),
    'CONTENT_HOME_INTRODUCTION': (
        "<p>Benvingudes a la web de gestió d’inscripcions i acompanyaments de Coòpolis!</p>"
        "<p>Podreu realitzar les inscripcions de les formacions, i sol·licitar assessorament per a la creació de "
        "projectes cooperatius.</p>"
        "<p>Si encara no formeu part, registreu-vos!</p>"
        "<p>Si ja en formeu part, entreu al vostre perfil per a poder gestionar inscripcions i projectes.</p>",
        "Portada, text d'introducció a la franja blava."),
    "CONTENT_HOME_PROJECTS_TITLE": (
        "Acompanyament de projectes",
        "Portada: títol del bloc que informa sobre l'acompanyament de projectes."),
    "CONTENT_HOME_PROJECTS_TEXT": (
        "Des de Coòpolis acompanyem projectes en la seva posada en marxa i constitució com a cooperatives, en aquells "
        "aspectes centrals per a la seva activitat i facilitem eines i recursos per a la seva consolidació i "
        "creixement. També dissenyem itineraris per a la transformació d’associacions i altres formes d’empreses a "
        "cooperatives.",
        "Portada: bloc que informa sobre l'acompanyament de projectes."),
    'CONTENT_HOME_TITLE': (
        "Extranet de Coòpolis per gestionar cursos i projectes",
        'Portada: títol.'),
    # E-mails
    'EMAIL_NEW_PROJECT': (
        "Nova sol·licitud d'acompanyament<br />"                          
        "<br />"
        "Nom del projecte: {} <br />"
        "Telèfon de contacte: {} <br />"
        "Correu electrònic de contacte del projecte: {} <br />"
        "Correu electrònic de l'usuari que l'ha creat: {} <br />",
        "Cos del correu que s'envia quan algú sol·licita un acompanyament."),
    'EMAIL_NEW_PROJECT_SUBJECT': (
        "Nova sol·licitud d'acompanyament: {}",
        "Assumpte del correu que s'envia quan algú sol·licita un acompanyament."),
    'EMAIL_ENROLLMENT_CONFIRMATION': (
        "Inscripció a l'activitat: {} <br />"
        "<br />Dades de l'activitat:<br />"
        "Data: {}<br />"
        "Horari: de {} a {}<br />"
        "Lloc: {}<br />"
        "<br />"
        "Les places son limitades. Si finalment no pots assistir-hi, si us plau anul·la la "
        "teva inscripció. Per fer-ho, pots gestionar les teves inscripcions accedint al "
        "back-office de Coòpolis amb el teu correu i contrassenya <a href=\"{}\">aquí</a> "
        "o bé contactar-nos al correu electrònic {}, o trucar-nos al {}.",
        "Cos del correu que s'envia quan algú s'inscriu a una activitat"),
    'EMAIL_ENROLLMENT_CONFIRMATION_SUBJECT': (
        "Confirmació d'inscripció a l'activitat: {}",
        "Assumpte del correu que s'envia quan algú s'inscriu a una activitat"),
    'EMAIL_ENROLLMENT_REMINDER': (
        "",
        "Cos del correu de recordatori que s'envia a tothom que s'ha inscrit"
        "a una activitat mitjançant el botó per enviar el recordatori a tothom."),
    'EMAIL_ENROLLMENT_REMINDER_SUBJECT': (
        "",
        "Assumpte del correu de recordatori que s'envia a tothom que s'ha inscrit"
        "a una activitat mitjançant el botó per enviar el recordatori a tothom."),
    # Configuration
    'EMAIL_FROM': ('Coòpolis, Ateneu Cooperatiu <coopolis@bcn.coop>', 'Remitent dels correus electrònics'),
    'EMAIL_TO_DEBUG': ('p.picornell@gmail.com', 'Correu per fer tests del codi.'),
    'EMAIL_TO': ('coopolis.laie@gmail.com', "Correu on s'envien les notificacions generals (p.ex. nous projectes)"),
    'CONTACT_PHONE_NUMBER': ("93 432 00 63", "Número de telèfon que voleu indicar per si algú té dubtes o gestions."),
    'CONTACT_EMAIL': (
        "coopolis@bcn.coop",
        "Correu electrònic que voleu indicar per si algú té dubtes o gestions."),
}
CONSTANCE_CONFIG_FIELDSETS = {
    'Configuració': ('CONTACT_PHONE_NUMBER', 'CONTACT_EMAIL', 'EMAIL_TO_DEBUG', 'EMAIL_TO', 'EMAIL_FROM'),
    'Correus': ('EMAIL_NEW_PROJECT_SUBJECT', 'EMAIL_NEW_PROJECT', 'EMAIL_ENROLLMENT_CONFIRMATION_SUBJECT',
                'EMAIL_ENROLLMENT_CONFIRMATION', 'EMAIL_ENROLLMENT_REMINDER_SUBJECT', 'EMAIL_ENROLLMENT_REMINDER',),
    "Apartat Portada": ('CONTENT_HOME_COURSES_TITLE', 'CONTENT_HOME_COURSES_TEXT', 'CONTENT_HOME_PROJECTS_TITLE',
                        "CONTENT_HOME_PROJECTS_TEXT", 'CONTENT_HOME_TITLE', 'CONTENT_HOME_INTRODUCTION'),
    'Apartat Projectes': ('CONTENT_PROJECT_INTRODUCTION', 'CONTENT_PROJECT_TITLE', 'CONTENT_PROJECT_INFO',
                          'CONTENT_PROJECT_NEW'),
    "Apartat Formació": ('CONTENT_COURSES_INTRODUCTION',),
}

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

# Static texts
ADMIN_HEADER = 'Back-office de Coòpolis'
ADMIN_SITE_TITLE = ''
ADMIN_INDEX_TITLE = ''

# Grappeli (https://django-grappelli.readthedocs.io/en/latest/customization.html)
GRAPPELLI_ADMIN_TITLE = "Back-office de Coòpolis"
GRAPPELLI_SWITCH_USER = False
GRAPPELLI_INDEX_DASHBOARD = 'coopolis.dashboard.MyDashboard'

