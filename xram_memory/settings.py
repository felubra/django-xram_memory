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
        'django_elasticsearch_dsl',

        'django_extensions',
        'xram_memory.users',
        'xram_memory.taxonomy',
        'xram_memory.logger',
        'xram_memory.search_indexes',

        'xram_memory.quill_widget',
        'xram_memory.artifact',
        'xram_memory.page',
        'easy_thumbnails',
        'xram_memory.apps.FilerConfig',
        'mptt',
        'rest_framework',
        'corsheaders',
        'tags_input',
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
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
    STATICFILES_STORAGE = 'xram_memory.utils.PatchedCompressedManifestStaticFilesStorage'

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
        'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'application/pdf', 'application/zip')
    VALID_FILE_UPLOAD_IMAGES_MIME_TYPES = (
        'image/jpeg', 'image/png', 'image/gif', 'image/webp',)

    THUMBNAIL_SOURCE_GENERATORS = (
        'easy_thumbnails.source_generators.pil_image',
        'xram_memory.lib.file_previews.pdf_preview',
        'xram_memory.lib.file_previews.icon_preview',
    )

    THUMBNAIL_ALIASES = {
        '': {
            'document_thumbnail': {
                'size': (250, 250),
                'autocrop': True,
                'crop': 'scale',
                'upscale': False,
            },
            'thumbnail': {
                'size': (250, 250),
                'background': '#f3f1f1',
                'autocrop': True,
                'crop': 'smart',
            },
            'image_capture': {
                'size': (670, 204),
                'autocrop': True,
                'crop': 'scale'
            },
            '1280': {
                'size': (1280, 1280),
                'crop': 'scale'
            },
            '640': {
                'size': (640, 360),
                'crop': 'scale'
            },
            '360': {
                'size': (360, 360),
                'crop': 'scale'
            }
        }
    }

    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'npm.finders.NpmFinder',
    ]
    NPM_ROOT_PATH = BASE_DIR
    NPM_FILE_PATTERNS = {
        'file-icon-vectors': ['dist/icons/vivid/*'],
        'stopwords-iso': ['stopwords-iso.json'],
        'material-design-icons': [
            'navigation/svg/production/ic_fullscreen*',
            'action/svg/production/ic_info_24px*',
            'image/svg/production/ic_picture_as_pdf_24px*',
            'image/svg/production/ic_filter_24px*',
        ],
        'quill': ['dist/*'],
        'screenfull': ['dist/*'],
    }
    ELASTICSEARCH_INDEX_NAMES = {
        'xram_memory.search_indexes.documents.news': 'artifact_news',
        'xram_memory.search_indexes.documents.document': 'artifact_document',
    }
    ELASTICSEARCH_DSL = {
        'default': {
            'hosts': values.Value('localhost:9200', True, environ_name="ELASTICSEARCH_HOST", environ_prefix="DJANGO"),
            'http_auth': values.TupleValue(environ_name="ELASTICSEARCH_CREDENTIALS", environ_prefix="DJANGO"),
            'timeout': 30,
        },
    }

    REST_FRAMEWORK = {
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework.parsers.JSONParser',
        ),
        'DEFAULT_THROTTLE_CLASSES': (
            'rest_framework.throttling.AnonRateThrottle',
        ),
        'DEFAULT_THROTTLE_RATES': {
            'anon': '60/minute',
        }
    }

    FILER_FILE_MODELS = ['artifact.Document']

    TAGS_INPUT_MAPPINGS = {
        'taxonomy.Keyword': {
            'field': 'name',
            'create_missing': True,
        },
        'taxonomy.Subject': {
            'field': 'name',
            'create_missing': True,
        },
    }
    FILE_UPLOAD_MAX_MEMORY_SIZE = 10621440
    CELERY_BROKER_URL = values.Value('')

    FOLDER_CAPTURES = {
        'name': 'Capturas automáticas',
        'lft': 1,
        'rght': 2,
        'tree_id': 1,
        'level': 0,
        'id': 1
    }

    FOLDER_PHOTO_ALBUMS = {
        'name': 'Álbuns de fotos',
        'lft': 1,
        'rght': 2,
        'tree_id': 2,
        'level': 0,
    }

    FOLDER_PDF_CAPTURES = {
        'name': 'Capturas de notícias em PDF',
        'lft': 1,
        'rght': 2,
        'tree_id': 1,
        'level': 1,
        'parent_id': 1
    }

    FOLDER_IMAGE_CAPTURES = {
        'name': 'Imagens de notícias',
        'lft': 1,
        'rght': 2,
        'tree_id': 1,
        'level': 1,
        'parent_id': 1
    }

    DEFAULT_FOLDERS = (
        FOLDER_CAPTURES,
        FOLDER_PHOTO_ALBUMS,
        FOLDER_PDF_CAPTURES,
        FOLDER_IMAGE_CAPTURES,
    )

    HASHID_FIELD_SALT = values.Value(
        '4OkZKanuMWUU4EO92FcDmwXkn6PbksGAIClUcG4S')
    HASHID_FIELD_LOOKUP_EXCEPTION = False
    HASHID_FIELD_ALLOW_INT_LOOKUP = False


class Development(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True

    ALLOWED_HOSTS = values.ListValue(
        ['localhost', '127.0.0.1', '[::1]', '192.168.99.100', 'xram-memory.local'])

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
                'level': 'ERROR',
            },
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        },
    }
    CELERY_BROKER_URL = values.Value('redis://127.0.0.1:6379/0')

    CORS_ORIGIN_ALLOW_ALL = True


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
                'level': 'ERROR',
            },
        },
    }


class Production(Staging):
    """
    The in-production settings.
    """
