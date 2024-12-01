import os, sys, random, string

MOLLIE_API_KEY = 'REDACTED'

DEBUG = 'runserver' in sys.argv
PROJECT_NAME = 'copyshop'
CANONICAL_URL = 'https://www.copyshopdenbosch.nl'
KEYFILE = f'/tmp/{PROJECT_NAME}.secret'
ADMINS = [('JJ Vens', 'jj@rtts.eu')]
DEFAULT_FROM_EMAIL = 'noreply@rtts.eu'
DEFAULT_TO_EMAIL = ['info@copyshopdenbosch.nl']
CONTACT_FORM_EMAIL_ADDRESS = "info@copyshopdenbosch.nl"
CONTACT_FORM_EMAIL_SUBJECT = "Contactformulier Copyshopdenbosch.nl"
ALLOWED_HOSTS = ['*']
ROOT_URLCONF = PROJECT_NAME + '.urls'
WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'
LANGUAGE_CODE = 'nl'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = '/srv/' + PROJECT_NAME + '/static'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/srv/' + PROJECT_NAME + '/media'
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CACHE_MIDDLEWARE_SECONDS = 0

try:
    with open(KEYFILE) as f:
        SECRET_KEY = f.read()
except IOError:
    SECRET_KEY = ''.join(random.choice(string.printable) for x in range(50))
    with open(KEYFILE, 'w') as f:
        f.write(SECRET_KEY)

INSTALLED_APPS = [
    PROJECT_NAME,
    'pricing',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cms',
    'embed_video',
    'easy_thumbnails',
    'django_extensions',
]
if not DEBUG:
    INSTALLED_APPS += ['django.contrib.staticfiles']

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'cms.middleware.SassMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': PROJECT_NAME,
        'NAME': PROJECT_NAME,
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': PROJECT_NAME,
    }
}
