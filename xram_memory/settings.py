"""
Django settings for xram_memory project.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os

from configurations import Configuration, values


class Common(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = values.ListValue([])

    # Application definition
    INSTALLED_APPS = [
        'xram_memory.apps.DefaultAdminConfig',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'whitenoise.runserver_nostatic',
        'django.contrib.staticfiles',

        'django_extensions',
        'xram_memory.users',
        'xram_memory.taxonomy',
        'xram_memory.logger',

        'xram_memory.artifact',

        'django_rq',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django_currentuser.middleware.ThreadLocalUserMiddleware',
    ]

    ROOT_URLCONF = 'xram_memory.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'xram_memory', 'templates')],
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

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "xram_memory", "static"),
    ]

    WSGI_APPLICATION = 'xram_memory.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/2.1/ref/settings/#databases
    DATABASES = values.DatabaseURLValue(
        'sqlite:///{}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
    )

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
    LANGUAGE_CODE = 'pt-br'

    TIME_ZONE = 'America/Sao_Paulo'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.1/howto/static-files/
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    AUTH_USER_MODEL = 'users.User'

    RQ_QUEUES = {
        'default': {
            'HOST': 'localhost',
            'PORT': 6379,
            'DB': 0,
            'DEFAULT_TIMEOUT': 360,
            'ASYNC': False
        },
    }
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
    PDF_ARTIFACT_DIR = 'artifacts/documents/pdf_files/'
    IMAGE_ARTIFACT_DIR = 'artifacts/documents/image_files/'
    VALID_FILE_UPLOAD_MIME_TYPES = (
        'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'application/pdf',)


class Development(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True

    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '192.168.99.100']

    INTERNAL_IPS = [
        '127.0.0.1'
    ]

    MIDDLEWARE = Common.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ]

    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'debug_toolbar',
    ]

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        },
    }


class Staging(Common):
    """
    The in-staging settings.
    """
    # Security
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_HSTS_SECONDS = values.IntegerValue(3600)
    SECURE_REDIRECT_EXEMPT = values.ListValue([])
    SECURE_SSL_HOST = values.Value(None)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    SECURE_PROXY_SSL_HEADER = values.TupleValue(
        ('HTTP_X_FORWARDED_PROTO', 'https')
    )

    ALLOWED_HOSTS = ['xram-memory.felipelube.com']
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


class Production(Staging):
    """
    The in-production settings.
    """
    pass
