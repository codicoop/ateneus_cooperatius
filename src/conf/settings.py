import environ
import os

from django.core.management.utils import get_random_secret_key

env = environ.Env()

DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Instance's absolute URL (given we're not using Sites framework)
ABSOLUTE_URL = env.str('ABSOLUTE_URL', default="")

# Necessari per tal que al recuperar password faci servir el mateix host que
# la URL que s'està visitant. Si això fos False, caldria activar el Sites
# Framework i configurar el nom del host.
USE_X_FORWARDED_HOST = True

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env.str('SECRET_KEY', default=get_random_secret_key())

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DB_NAME', default="postgres"),
        'USER': env.str('DB_USER', default="postgres"),
        'PASSWORD': env.str('DB_PASSWORD', default=""),
        'HOST': env.str('DB_HOST', default=""),
        'PORT': env.int('DB_PORT', default=5432),
    },
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Wasabi cloud storage configuration
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID', default="")
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY', default="")
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME', default="")
AWS_S3_ENDPOINT_URL = env.str('AWS_S3_ENDPOINT_URL', default="")
AWS_DEFAULT_ACL = env.str('AWS_DEFAULT_ACL', default="")
AWS_PUBLIC_MEDIA_LOCATION = env.str('AWS_PUBLIC_MEDIA_LOCATION', default="")
AWS_S3_BASE_DOMAIN = env.str('AWS_S3_BASE_DOMAIN', default='')
AWS_S3_CUSTOM_DOMAIN = f"{AWS_S3_BASE_DOMAIN}/{AWS_STORAGE_BUCKET_NAME}"
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
EXTERNAL_STATIC = AWS_S3_ENDPOINT_URL+"/"+AWS_STORAGE_BUCKET_NAME+"/local"
# In templates use {% external_static "/logo.png" %}
AWS_PRIVATE_MEDIA_LOCATION = env.str('AWS_PRIVATE_MEDIA_LOCATION', default="")
MEDIA_FILE_OVERWRITE = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# TODO: delete this commented code if it proves to be deprecatred.
# sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '../apps')))

# Local strings
ADMIN_HEADER = env.str("ADMIN_HEADER", "")
GRAPPELLI_ADMIN_TITLE = env.str("GRAPPELLI_ADMIN_TITLE", "")
CIRCLE_NAMES = [
    env.str("CIRCLE_NAME_ATENEU", ""),
    env.str("CIRCLE_NAME_1", ""),
    env.str("CIRCLE_NAME_2", ""),
    env.str("CIRCLE_NAME_3", ""),
    env.str("CIRCLE_NAME_4", ""),
    env.str("CIRCLE_NAME_5", ""),
]

# Application definition
INSTALLED_APPS = [
    "django_extensions",
    "maintenance_mode",
    "django.contrib.postgres",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "post_office",
    "apps.dataexports",
    "apps.cc_users",
    "apps.cc_courses",
    "apps.facilities_reservations",
    "apps.coopolis",
    "apps.celery",
    "grappelli.dashboard",
    "grappelli",
    "tagulous",
    "logentry_admin",
    "constance.backends.database",
    "constance",
    "django_object_actions",
    "django.contrib.admin",
    "django_summernote",
    "storages",
    "easy_thumbnails",
    "apps.modelclone",
    "apps.coopolis.templatetags.my_tag_library",
    "django.contrib.humanize",
    "localflavor",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]

ROOT_URLCONF = 'conf.urls'

# https://docs.djangoproject.com/en/4.2/ref/settings/#templates
develop_loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]
production_loaders = [
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates",
        ],
        "OPTIONS": {
            "context_processors": [
                'constance.context_processors.config',
                "maintenance_mode.context_processors.maintenance_mode",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'apps.coopolis.context_processors.global_context',
                'apps.coopolis.context_processors.projects_menu_context',
            ],
            "loaders": develop_loaders if DEBUG else production_loaders,
        },
    },
]


# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'constance.context_processors.config',
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#                 'apps.coopolis.context_processors.global_context',
#             ],
#         },
#     },
# ]

WSGI_APPLICATION = 'conf.wsgi.application'


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

# For Tagulous
SERIALIZATION_MODULES = {
    'xml':    'tagulous.serializers.xml_serializer',
    'json':   'tagulous.serializers.json',
    'python': 'tagulous.serializers.python',
    'yaml':   'tagulous.serializers.pyyaml',
}

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "assets"),
# ]

STORAGES = {
    "default": {
        "BACKEND": "apps.coopolis.storage_backends.PublicMediaStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

LOGIN_URL = 'loginsignup'
LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'coopolis.User'
DEV_SETTINGS_MODULE = 'conf.settings'

# APPS

USERS_APP_TITLE = 'Usuàries'
COURSES_APP_TITLE = "Accions"

FIXTURES_PATH_TO_COURSE_IMAGES = 'test-images/coopolis-courses'

# Constance
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_SUPERUSER_ONLY = False
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    # Configurable modules or features
    'ENABLE_STAGE_SUBTYPES': (
        False, "Mostrar el camp \"Subtipus\" a les justificacions "
               "d'acompanyament.", bool),
    # Sign up
    'CONTENT_SIGNUP_LEGAL1': (
        "La participació en les activitats de Coòpolis, Ateneu Cooperatiu de "
        "Barcelona, està subjecta a un seguit de condicions que entre altres "
        "aspectes recullen el tractament que es farà de les vostres dades "
        "segons la nova Llei del RGPT i el permís per utilitzar la vostra "
        "imatge per a arxiu i difusió de l'activitat, i mai amb cap ús "
        "comercial.",
        'Casella per acceptar #1.'),
    'CONTENT_SIGNUP_LEGAL2': (
        "Sóc coneixedor/a del caràcter de subvenció pública amb la qual es "
        "finança l’actuació en la qual vull participar, mitjançant el "
        "cofinançament del Ministeri d’Ocupació i Seguretat Social, i "
        "l’Ajuntament de Barcelona.",
        'Casella per acceptar #2.'),
    # Configuration
    'EMAIL_FROM_ENROLLMENTS': (
        'formacio@bcn.coop',
        "És el remitent del correu que rep la gent a l'inscriure's a una "
        "sessió. Quan s'envia un recordatori a tothom inscrit a una sessió, "
        "s'envia a aquest compte i posa en còpia oculta els correus de la "
        "gent."),
    'EMAIL_FROM_PROJECTS': (
        'suport@bcn.coop',
        "Quan algú sol·licita un acompanyament es genera un correu per "
        "notificar-ho a l'equip, que s'envia a aquest compte. Aquest camp, a "
        "diferència dels altres, permet indicar diversos comptes, separant-los"
        " per comes."),
    'EMAIL_TO_DEBUG': (
        'p.picornell@gmail.com', 'Correu per fer tests del codi.'),
    'PROJECT_NAME': ("Ateneu", "Nom curt de l'ateneu."),
    'PROJECT_FULL_NAME': (
        "Ateneu cooperatiu",
        "Nom llarg, p.ex.: 'Coòpolis. Ateneu cooperatiu de Barcelona'. També "
        "hi podeu posar el mateix que al nom curt, si voleu."),
    'PROJECT_CONTACT_URL': (
        "https://bcn.coop/contacte/",
        "Enllaç a la pàgina de contacte de l'ateneu, apareix a peu de "
        "pàgina."),
    'PROJECT_LEGAL_URL': (
        "https://bcn.coop/avis-legal-i-proteccio-de-dades/",
        "Enllaç a la pàgina de les condicions legals de l'ateneu. Apareix a: "
        "missatge d'acceptar cookies, peu de pàgina, i al text d'acceptació "
        "de condicions legals del formulari d'alta."),
    'PROJECT_WEBSITE_URL': (
        "https://bcn.coop",
        "Enllaç a la pàgina principal de l'ateneu. Apareix al menú "
        "principal."),
    'CONTACT_PHONE_NUMBER': (
        "93 432 00 63",
        "Apareix al correu que s'envia a la gent que s'inscriu a activitats, "
        "perquè sàpiguen on contactar si tenen dubtes. De la mateixa manera "
        "apareix al correu que s'envia quan envieu un recordatori a tota la "
        "gent inscrita a una sessió."),
    'PROJECT_FACEBOOK_URL': (
        "",
        "Si s'indica la URL del perfil de Facebook, apareixerà a la plantilla "
        "dels correus electrònics."),
    'PROJECT_TWITTER_URL': (
        "",
        "Si s'indica la URL del perfil de Twitter, apareixerà a la plantilla "
        "dels correus electrònics."),
    'PROJECT_INSTAGRAM_URL': (
        "",
        "Si s'indica la URL del perfil d'Instagram, apareixerà a la plantilla "
        "dels correus electrònics."),
    'CONTACT_EMAIL': (
        "coopolis@bcn.coop",
        "Apareix al correu que s'envia a la persona que s'ha inscrit a una "
        "sessió (i al de recordatori que s'enviamassivament des de l'admin) "
        "per indicar que si tenen dubtes, escriguin a aquest correu."),
    'ATTENDEE_LIST_FOOTER_IMG': (
        "https://s3.eu-central-1.wasabisys.com/ateneus-coopolis/local"
        "/peu_signatures_pdf.png",
        "URL de l'imatge pel peu de pàgina del llistat d'assistència."),
}
CONSTANCE_CONFIG_FIELDSETS = {
    'Configuració': (
        'PROJECT_NAME', 'PROJECT_FULL_NAME',
        'ENABLE_STAGE_SUBTYPES',
        'PROJECT_WEBSITE_URL', 'PROJECT_LEGAL_URL', 'PROJECT_CONTACT_URL',
        'CONTACT_PHONE_NUMBER', 'CONTACT_EMAIL', 'EMAIL_TO_DEBUG',
        'EMAIL_FROM_ENROLLMENTS', 'EMAIL_FROM_PROJECTS',
        'PROJECT_FACEBOOK_URL', 'PROJECT_TWITTER_URL', 'PROJECT_INSTAGRAM_URL'
    ),
    "Formulari d'alta": ('CONTENT_SIGNUP_LEGAL1', 'CONTENT_SIGNUP_LEGAL2',),
    "Llistat d'assistència": ('ATTENDEE_LIST_FOOTER_IMG',),
}

# CC Courses

COURSES_CLASS_TO_ENROLL = 'coopolis.User'
COURSES_CLASSES_CAN_ENROLL = ['apps.cc_courses.models.Course']

FIXTURE_FACTORIES = [
    ('apps.coopolis.tests.fixtures.UserFactory', {}),
    ('apps.coopolis.tests.fixtures.ProjectFactory', {}),
    ('apps.cc_courses.tests.fixtures.CourseFactory', {}),
    ('apps.cc_courses.tests.fixtures.EntityFactory', {}),
    ('apps.cc_courses.tests.fixtures.CoursePlaceFactory', {}),
    ('apps.cc_courses.tests.fixtures.ActivityFactory', {
        'number': 500
    }),
]

SIGNUP_FORM = 'apps.coopolis.forms.MySignUpForm'

# Static texts and option fields
ADMIN_SITE_TITLE = ''
ADMIN_INDEX_TITLE = ''
AXIS_OPTIONS = (
    ('A', 'Eix A'),
    ('B', 'Eix B'),
    ('C', "Eix C"),
    ('D', 'Eix D'),
    ('E', 'Eix E'),
    ('F', 'Eix F'),
)
SUBAXIS_OPTIONS = {
    'A': {
        ('A1', "A.1 Reunions de la taula territorial"),
        ('A2', "A.2 Diagnosi entitats socials del territori"),
        ('A3', "A.3 Elaboració catàleg bones pràctiques"),
        ('A4', "A.4 Jornades per presentar experiències de bones pràctiques o "
               "jornades sectorials i/o d'interès per al territori"),
        ('A5', "A.5 Assistència a fires, actes per visibilitzar el programa"),
        ('A6', "A.6 Publicitat en mitjans de comunicació.  Web del programa"),
        ('A7', "A.7 Altres")
    },
    'B': {
        ('B1', "B.1 Accions de suport a la inserció laboral i a la creació de "
               "cooperatives i societats laborals (concursos de projectes "
               "cooperatius o altres accions)"),
        ('B2', "B.2 Tallers sensibilització o dinamització"),
        ('B3', "B.3 Acompanyament a empreses i entitats"),
        ('B4', "B.4 Altres"),
    },
    'C': {
        ('C1', "C.1 Tallers de dinamització adreçats al teixit associatiu i a "
               "empreses"),
        ('C2', "C.2 Tallers de dinamització adreçats a professionals que "
               "s'agrupen per prestar serveis de manera conjunta"),
        ('C3', "C.3 Acompanyament a mida per a la creació o transformació"),
        ('C4', "C.4 Altres"),
    },
    'D': {
        ('D1', "D.1 Accions de difusió"),
        ('D2', "D.2 Activitats de sensibilització o dinamització."),
        ('D3', "D.3 Acompanyament individualitzat"),
        ('D4', "D.4 Altres"),
    },
    'E': {
        ('E1', "E.1 Tallers a joves"),
        ('E2', "E.2 Atenció individual professorat"),
        ('E3', "E.3 Complementàries (recursos, eines, productes, publicacions "
               "sectorials pròpies )"),
        ('E4', "E.4 Altres"),
    },
    'F': {
        ('F1', "F.1 Pla d'actuació"),
        ('F2', "F.2 Tallers de creació de cooperatives o societats laborals, "
               "o transformació d'associacions, altres entitats"),
        ('F3', "F.3 Altres"),
    }
}
DISTRICTS = (
    ('CV', 'Ciutat Vella'),
    ('EX', 'Eixample'),
    ('HG', 'Horta-Guinardó'),
    ('LC', 'Les Corts'),
    ('NB', 'Nou Barris'),
    ('SA', 'Sant Andreu'),
    ('SM', 'Sant Martí'),
    ('ST', 'Sants-Montjuïc'),
    ('SS', 'Sarrià-Sant Gervasi'),
    ('GR', 'Gràcia')
)
PROJECT_STATUS = (
    ('PENDENT', "Pendent d’enviar proposta de trobada"),
    ('ENVIAT', "Enviat email amb proposta de data per trobar-nos"),
    ('CONCERTADA', "Data de trobada concertada"),
    ('ACOLLIT', "Acollida realitzada"),
    ('EN_CURS', "Acompanyament en curs"),
    ('PAUSA', "Acompanyament en pausa"),
    ('CANCEL', "Acompanyament cancel·lat")
)
CALENDAR_COLOR_FOR_ACTIVITIES_OUTSIDE = '#808080'

# Grappeli
# (https://django-grappelli.readthedocs.io/en/latest/customization.html)
GRAPPELLI_SWITCH_USER = False
GRAPPELLI_INDEX_DASHBOARD = 'apps.coopolis.dashboard.MyDashboard'

# Celery
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default=None)
CELERY_TIMEZONE = TIME_ZONE
DAILY_TASKS_EXECUTION_TIME = env.int("DAILY_TASKS_EXECUTION_TIME", default=5)
REMIND_SESSION_ORGANIZER_DAYS_BEFORE = env.int(
    "REMIND_SESSION_ORGANIZER_DAYS_BEFORE",
    default=3,
)

# Maintenance mode
MAINTENANCE_MODE = env.bool("MAINTENANCE_MODE", default=False)

LOGGLY_TOKEN = env.str("LOGGLY_TOKEN", default="")
LOGGLY_TAG = env.str("LOGGLY_TAG", default="ateneu-sense-tag")

if LOGGLY_TOKEN:
    if DEBUG:
        LOGGLY_TAG = f"develop,{LOGGLY_TAG}"
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
            },
            "simple": {
                "format": "%(levelname)s %(message)s"
            },
            "json": {
                "format": '{ "loggerName":"%(name)s", "asciTime":"%(asctime)s", "fileName":"%(filename)s", "logRecordCreationTime":"%(created)f", "functionName":"%(funcName)s", "levelNo":"%(levelno)s", "lineNo":"%(lineno)d", "time":"%(msecs)d", "levelName":"%(levelname)s", "message":"%(message)s"}',
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "verbose",
            },
            "loggly": {
                "class": "loggly.handlers.HTTPSHandler",
                "level": "INFO",
                "formatter": "json",
                "url": f"https://logs-01.loggly.com/inputs/{LOGGLY_TOKEN}/tag/{LOGGLY_TAG}",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console", ],
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            },
            "": {
                "handlers": ["console", "loggly"],
                "level": "INFO",
            },
        },
    }

################################################################################
#                                  Email                                       #
################################################################################

# Post Office
# https://github.com/ui/django-post_office#settings
POST_OFFICE = {
    "BACKENDS": {
        "default": env(
            "POST_OFFICE_DEFAULT_BACKEND",
            default="django.core.mail.backends.console.EmailBackend",
        ),
    },
    "DEFAULT_PRIORITY": env("POST_OFFICE_DEFAULT_PRIORITY", default="now"),
    "MESSAGE_ID_ENABLED": True,
    "MESSAGE_ID_FQDN": env("POST_OFFICE_MESSAGE_ID_FQDN", default="example.com"),
    "CELERY_ENABLED": env("POST_OFFICE_CELERY_ENABLED", bool, default=False),
    "OVERRIDE_RECIPIENTS": env.list("POST_OFFICE_OVERRIDE_RECIPIENTS", default=None)
}

# https://docs.djangoproject.com/en/4.2/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=None)

# Sendgrid
# https://github.com/sklarsa/django-sendgrid-v5#other-settings
SENDGRID_API_KEY = env("SENDGRID_API_KEY", default="")
SENDGRID_SANDBOX_MODE_IN_DEBUG = env(
    "SENDGRID_SANDBOX_MODE_IN_DEBUG", bool, default=False
)
SENDGRID_ECHO_TO_STDOUT = env(
    "SENDGRID_ECHO_TO_STDOUT", bool, default=False
)

# SMTP
# These are set to false as default given that Sendgrid's Web API is the default
# https://docs.djangoproject.com/en/4.2/ref/settings/#email
EMAIL_HOST = env.str("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default="")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
