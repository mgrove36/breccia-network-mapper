"""
Django settings for breccia_mapper project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/

Before production deployment, see
https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/


Many configuration settings are input from `settings.ini`.
The most likely required settings are: SECRET_KEY, DEBUG, ALLOWED_HOSTS, DATABASE_URL, PROJECT_*_NAME, EMAIL_*

- SECRET_KEY (REQUIRED)
  Used to generate CSRF tokens - must never be made public

- DEBUG
  default: False
  Should the server run in debug mode?  Provides information to users which is unsafe in production

- ALLOWED_HOSTS
  default: * if DEBUG else localhost
  Accepted values for server header in request - protects against CSRF and CSS attacks

- DATABASE_URL
  default: sqlite://db.sqlite3
  URL to database - uses format described at https://github.com/jacobian/dj-database-url

- DBBACKUP_STORAGE_LOCATION
  default: .dbbackup
  Directory where database backups should be stored

- LANGUAGE_CODE
  default: en-gb
  Default language - used for translation - has not been enabled

- TIME_ZONE
  default: UTC
  Default timezone

- LOG_LEVEL
  default: INFO
  Level of messages written to log file

- LOG_FILENAME
  default: debug.log
  Path to logfile

- LOG_DAYS
  default: 14
  Number of days of logs to keep - logfile is rotated out at the end of each day

- EMAIL_HOST
  default: None
  Hostname of SMTP server

- DEFAULT_FROM_EMAIL
  default: None
  Email address from which messages are sent

- EMAIL_FILE_PATH (debug only)
  default: mail.log
  Directory where emails will be stored if not using an SMTP server

- EMAIL_HOST_USER
  default: None
  Username to authenticate with SMTP server

- EMAIL_HOST_PASSWORD
  default: None
  Password to authenticate with SMTP server

- EMAIL_PORT
  default: 25
  Port to access on SMTP server

- EMAIL_USE_TLS
  default: True if EMAIL_PORT == 587 else False
  Use TLS to communicate with SMTP server?  Usually on port 587

- EMAIL_USE_SSL
  default: True if EMAIL_PORT == 465 else False
  Use SSL to communicate with SMTP server?  Usually on port 465

- GOOGLE_MAPS_API_KEY
  default: None
  Google Maps API key to display maps of people's locations
"""

import logging
import logging.config
import pathlib

from django.urls import reverse_lazy

from decouple import config, Csv
import dj_database_url

# Settings exported to templates
# https://github.com/jakubroztocil/django-settings-export

SETTINGS_EXPORT = [
    'DEBUG',
    'GOOGLE_MAPS_API_KEY',
]


# Build paths inside the project like this: BASE_DIR.joinpath(...)
BASE_DIR = pathlib.Path(__file__).parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='*' if DEBUG else '127.0.0.1,localhost,localhost.localdomain',
    cast=Csv())

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'bootstrap4',
    'constance',
    'constance.backends.database',
    'dbbackup',
    'django_countries',
    'django_select2',
    'rest_framework',
    'post_office',
    'bootstrap_datepicker_plus',
    'hijack',
]

FIRST_PARTY_APPS = [
    'people',
    'activities',
    'export',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + FIRST_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hijack.middleware.HijackUserMiddleware',
]

ROOT_URLCONF = 'breccia_mapper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('breccia_mapper', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django_settings_export.settings_export',
                'constance.context_processors.config',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'breccia_mapper.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default':
    config('DATABASE_URL',
           default='sqlite:///' + str(BASE_DIR.joinpath('db.sqlite3')),
           cast=dj_database_url.parse)
}

# Django DBBackup
# https://django-dbbackup.readthedocs.io/en/stable/index.html

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'location':
    config('DBBACKUP_STORAGE_LOCATION',
           default=BASE_DIR.joinpath('.dbbackup')),
}

# Django REST Framework
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom user model
# https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

AUTH_USER_MODEL = 'people.User'

# Login flow

LOGIN_URL = reverse_lazy('login')

LOGIN_REDIRECT_URL = reverse_lazy('people:person.profile')

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-gb')

TIME_ZONE = config('TIME_ZONE', default='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR.joinpath('static')

STATICFILES_DIRS = [BASE_DIR.joinpath('breccia_mapper', 'static')]

# Media uploads
MEDIA_ROOT = BASE_DIR.joinpath('breccia_mapper', 'static', 'media')
MEDIA_URL = "/static/media/"

# Logging - NB the logger name is empty to capture all output

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': config('LOG_LEVEL', default='INFO'),
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': config('LOG_FILENAME', default='debug.log'),
            'when': 'midnight',
            'backupCount': config('LOG_DAYS', default=14, cast=int),
            'formatter': 'timestamped',
        },
        'console': {
            'level': config('LOG_LEVEL', default='INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'timestamped',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': config('LOG_LEVEL', default='INFO'),
            'propagate': True,
        },
    },
    'formatters': {
        'timestamped': {
            'format': '[{asctime} {levelname} {module} {funcName}] {message}',
            'style': '{',
        }
    }
}

# Initialise logger now so we can use it in this file

LOGGING_CONFIG = None
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# Admin panel variables

CONSTANCE_ADDITIONAL_FIELDS = {
    'image_field': ['django.forms.ImageField', {}]
}

CONSTANCE_CONFIG = {
    'NOTICE_TEXT': (
        '',
        'Text to be displayed in a notice banner at the top of every page.'),
    'NOTICE_CLASS': (
        'alert-warning',
        'CSS class to use for background of notice banner.'),
    'CONSENT_TEXT': (
        'This is template consent text and should have been replaced. Please contact an admin.',
        'Text to be displayed to ask for consent for data collection.'),
    'PERSON_LIST_HELP': (
        '',
        'Help text to display at the top of the people list.'),
    'ORGANISATION_LIST_HELP': (
        '',
        'Help text to display at the top of the organisaton list.'),
    'RELATIONSHIP_FORM_HELP': (
        '',
        'Help text to display at the top of relationship forms.'),
    'DEPLOYMENT_URL': (
      'http://localhost',
      'URL at which this mapper tool is accessible'),
    'PARENT_PROJECT_NAME': (
      '',
      'Parent project name'),
    'PROJECT_LONG_NAME': (
      'Project Long Name',
      'Project long name'),
    'PROJECT_SHORT_NAME': (
      'Short Name',
      'Project short name'),
    'PROJECT_LEAD': (
      'John Doe',
      'Project lead'),
    'PROJECT_TAGLINE': (
      'Here is your project\'s tagline.',
      'Project tagline'),
    'HOMEPAGE_HEADER_IMAGE': (
      '800x500.png',
      'Homepage header image',
      'image_field'),
    'HOMEPAGE_CARD_1_TITLE': (
      'Step 1',
      'Homepage card #1 title'),
    'HOMEPAGE_CARD_1_DESCRIPTION': (
      'Tell us about your position within the project',
      'Homepage card #1 description'),
    'HOMEPAGE_CARD_1_ICON': (
      'building-user',
      'Homepage card #1 icon'),
    'HOMEPAGE_CARD_2_TITLE': (
      'Step 2',
      'Homepage card #2 title'),
    'HOMEPAGE_CARD_2_DESCRIPTION': (
      'Describe your relationships with other stakeholders',
      'Homepage card #2 description'),
    'HOMEPAGE_CARD_2_ICON': (
      'handshake-simple',
      'Homepage card #2 icon'),
    'HOMEPAGE_CARD_3_TITLE': (
      'Step 3',
      'Homepage card #3 title'),
    'HOMEPAGE_CARD_3_DESCRIPTION': (
      'Use the network view to build new relationships',
      'Homepage card #3 description'),
    'HOMEPAGE_CARD_3_ICON': (
      'diagram-project',
      'Homepage card #3 icon'),
    'HOMEPAGE_ABOUT_TITLE': (
      'About Us',
      'Homepage about section title'),
    'HOMEPAGE_ABOUT_CONTENT': (
      """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. In massa tempor nec feugiat nisl. Eget dolor morbi non arcu risus quis varius quam quisque. Nisl pretium fusce id velit ut tortor pretium viverra suspendisse. Vitae auctor eu augue ut lectus arcu. Tellus molestie nunc non blandit massa enim nec. At consectetur lorem donec massa sapien. Placerat orci nulla pellentesque dignissim enim sit. Sit amet mauris commodo quis imperdiet. Tellus at urna condimentum mattis pellentesque.<br/>In vitae turpis massa sed. Fermentum posuere urna nec tincidunt praesent semper feugiat nibh sed. Ut consequat semper viverra nam libero justo laoreet. Velit ut tortor pretium viverra suspendisse potenti nullam ac tortor. Nunc id cursus metus aliquam eleifend mi in nulla posuere. Aliquam eleifend mi in nulla posuere sollicitudin aliquam. Est ante in nibh mauris cursus mattis molestie a iaculis. Nunc id cursus metus aliquam. Auctor urna nunc id cursus metus aliquam. Porttitor lacus luctus accumsan tortor posuere ac ut consequat semper. Volutpat consequat mauris nunc congue nisi. Leo vel fringilla est ullamcorper eget. Vitae purus faucibus ornare suspendisse sed nisi lacus sed. Massa id neque aliquam vestibulum morbi blandit. Iaculis nunc sed augue lacus viverra vitae congue. Sodales neque sodales ut etiam.""",
      'Homepage about section content'),
    'HOMEPAGE_ABOUT_IMAGE': (
      '400x400.png',
      'Homepage about section image',
      'image_field'),
}  # yapf: disable

CONSTANCE_CONFIG_FIELDSETS = {
    'Project options': (
        'PARENT_PROJECT_NAME',
        'PROJECT_LONG_NAME',
        'PROJECT_SHORT_NAME',
        'PROJECT_LEAD',
        'PROJECT_TAGLINE',
    ),
    'Homepage configuration': (
        'HOMEPAGE_HEADER_IMAGE',
        'HOMEPAGE_CARD_1_TITLE',
        'HOMEPAGE_CARD_1_DESCRIPTION',
        'HOMEPAGE_CARD_1_ICON',
        'HOMEPAGE_CARD_2_TITLE',
        'HOMEPAGE_CARD_2_DESCRIPTION',
        'HOMEPAGE_CARD_2_ICON',
        'HOMEPAGE_CARD_3_TITLE',
        'HOMEPAGE_CARD_3_DESCRIPTION',
        'HOMEPAGE_CARD_3_ICON',
        'HOMEPAGE_ABOUT_TITLE',
        'HOMEPAGE_ABOUT_CONTENT',
        'HOMEPAGE_ABOUT_IMAGE',
    ),
    'Notice banner': (
        'NOTICE_TEXT',
        'NOTICE_CLASS',
    ),
    'Data Collection': (
        'CONSENT_TEXT',
    ),
    'Help text': (
        'PERSON_LIST_HELP',
        'ORGANISATION_LIST_HELP',
        'RELATIONSHIP_FORM_HELP',
    ),
    'Deployment': (
        'DEPLOYMENT_URL',
    ),
}  # yapf: disable

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

# Django Hijack settings
# See https://django-hijack.readthedocs.io/en/stable/

HIJACK_USE_BOOTSTRAP = True

# Bootstrap settings
# See https://django-bootstrap4.readthedocs.io/en/latest/settings.html

BOOTSTRAP4 = {
    'include_jquery': 'full',
}

# Email backend settings
# See https://docs.djangoproject.com/en/3.0/topics/email

EMAIL_HOST = config('EMAIL_HOST', default=None)
DEFAULT_FROM_EMAIL = config(
    'DEFAULT_FROM_EMAIL',
    default=f'{CONSTANCE_CONFIG["PROJECT_SHORT_NAME"][0]}@localhost.localdomain')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

if EMAIL_HOST is None:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = config('EMAIL_FILE_PATH',
                             default=str(BASE_DIR.joinpath('mail.log')))

else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=None)
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=None)

    EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS',
                           default=(EMAIL_PORT == 587),
                           cast=bool)
    EMAIL_USE_SSL = config('EMAIL_USE_SSL',
                           default=(EMAIL_PORT == 465),
                           cast=bool)

# Bootstrap Datepicker Plus Settings
BOOTSTRAP_DATEPICKER_PLUS = {
    "variant_options": {
        "date": {
            "format": "%Y-%m-%d",
        },
    }
}

# Database default automatic primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Upstream API keys

GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default=None)

# Import customisation app settings if present

try:
    from custom.settings import (
        CUSTOMISATION_NAME,
        TEMPLATE_NAME_INDEX,
        TEMPLATE_WELCOME_EMAIL_NAME,
        CONSTANCE_CONFIG as constance_config_custom,
        CONSTANCE_CONFIG_FIELDSETS as constance_config_fieldsets_custom
    )  # yapf: disable

    CONSTANCE_CONFIG.update(constance_config_custom)
    CONSTANCE_CONFIG_FIELDSETS.update(constance_config_fieldsets_custom)

    INSTALLED_APPS.append('custom')
    logger.info("Loaded customisation app: %s", CUSTOMISATION_NAME)

except ImportError as exc:
    logger.info("No customisation app loaded: %s", exc)

    # Set default values if no customisations loaded
    CUSTOMISATION_NAME = None
    TEMPLATE_NAME_INDEX = 'index.html'
    TEMPLATE_WELCOME_EMAIL_NAME = 'welcome-email'
