"""
Django settings for xram_memory project.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os

from configurations import Configuration, values
from xram_memory.lunr_index.util import LunrBackendValue


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
        "xram_memory.apps.DefaultAdminConfig",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "whitenoise.runserver_nostatic",
        "django.contrib.staticfiles",
        "django_extensions",
        "xram_memory.users",
        "xram_memory.taxonomy",
        "xram_memory.logger",
        "xram_memory.quill_widget",
        "xram_memory.artifact",
        "xram_memory.page",
        "easy_thumbnails",
        "xram_memory.apps.FilerConfig",
        "mptt",
        "rest_framework",
        "rest_framework.authtoken",
        "corsheaders",
        "tags_input",
        "xram_memory.albums",
    ]

    MIDDLEWARE = [
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django_currentuser.middleware.ThreadLocalUserMiddleware",
    ]

    ROOT_URLCONF = "xram_memory.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(BASE_DIR, "xram_memory", "templates")],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "xram_memory", "static"),
    ]

    WSGI_APPLICATION = "xram_memory.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/2.1/ref/settings/#databases
    DATABASES = values.DatabaseURLValue(
        "sqlite:///{}".format(os.path.join(BASE_DIR, "db.sqlite3"))
    )

    # Password validation
    # https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/2.1/topics/i18n/
    LANGUAGE_CODE = "pt-br"

    TIME_ZONE = "America/Sao_Paulo"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.1/howto/static-files/
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_STORAGE = (
        "xram_memory.utils.PatchedCompressedManifestStaticFilesStorage"
    )

    AUTH_USER_MODEL = "users.User"

    RQ_QUEUES = {
        "default": {
            "HOST": "localhost",
            "PORT": 6379,
            "DB": 0,
            "DEFAULT_TIMEOUT": 360,
            "ASYNC": False,
        },
    }
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = "/media/"
    VALID_FILE_UPLOAD_MIME_TYPES = (
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
        "application/pdf",
        "application/zip",
    )
    VALID_FILE_UPLOAD_IMAGES_MIME_TYPES = (
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
    )

    THUMBNAIL_SOURCE_GENERATORS = (
        "easy_thumbnails.source_generators.pil_image",
        "xram_memory.lib.file_previews.pdf_preview",
        "xram_memory.lib.file_previews.icon_preview",
    )

    THUMBNAIL_ALIASES = {
        "": {
            "document_preview": {
                "size": (850, 850),
                "autocrop": False,
                "crop": "scale",
                "upscale": False,
            },
            "document_thumbnail": {
                "size": (0, 250),
                "autocrop": False,
                "crop": "scale",
                "upscale": False,
            },
            "news_page": {
                "size": (0, 350),
                "autocrop": True,
                "crop": "smart",
                "upscale": False,
            },
            "thumbnail": {
                "size": (250, 250),
                "background": "#f3f1f1",
                "autocrop": True,
                "crop": "smart",
            },
            "image_capture": {"size": (670, 204), "autocrop": True, "crop": "scale"},
            # TODO: desabilitar?
            "1280": {"size": (1280, 1280), "crop": "scale"},
            "640": {"size": (640, 360), "crop": "scale"},
            "360": {"size": (360, 360), "crop": "scale"},
            "favicon": {
                "size": (18, 18),
                "autocrop": True,
                "scale_and_crop": "smart",
                "upscale": False,
            },
        }
    }

    STATICFILES_FINDERS = [
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        "npm.finders.NpmFinder",
    ]
    NPM_ROOT_PATH = BASE_DIR
    NPM_FILE_PATTERNS = {
        "file-icon-vectors": [os.path.join("dist", "icons", "vivid", "*")],
        "stopwords-iso": ["stopwords-iso.json"],
        "material-design-icons": [
            os.path.join("navigation", "svg", "production", "ic_fullscreen*"),
            os.path.join("action", "svg", "production", "ic_info_24px*"),
            os.path.join("image", "svg", "production", "ic_picture_as_pdf_24px*"),
            os.path.join("image", "svg", "production", "ic_filter_24px*"),
        ],
        "quill": [os.path.join("dist", "*")],
        "screenfull": [os.path.join("dist", "*")],
    }

    REST_FRAMEWORK = {
        "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
        "DEFAULT_THROTTLE_CLASSES": ("rest_framework.throttling.AnonRateThrottle",),
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.TokenAuthentication",
        ],
        "DEFAULT_THROTTLE_RATES": {
            "anon": "60/minute",
        },
    }

    FILER_FILE_MODELS = ["artifact.Document"]

    TAGS_INPUT_MAPPINGS = {
        "taxonomy.Keyword": {
            "field": "name",
            "create_missing": True,
        },
        "taxonomy.Subject": {
            "field": "name",
            "create_missing": True,
        },
    }
    FILE_UPLOAD_MAX_MEMORY_SIZE = 10621440
    CELERY_BROKER_URL = values.Value("")
    CELERY_CELERYD_MAX_TASKS_PER_CHILD = 10

    FOLDER_CAPTURES = {"name": "Capturas automáticas", "id": 1}

    FOLDER_PHOTO_ALBUMS = {"name": "Álbuns de fotos", "id": 2}

    FOLDER_PDF_CAPTURES = {"name": "Capturas de notícias em PDF", "id": 3}

    FOLDER_IMAGE_CAPTURES = {"name": "Imagens de notícias", "id": 4}

    DEFAULT_FOLDERS = (
        FOLDER_CAPTURES,
        FOLDER_PHOTO_ALBUMS,
        FOLDER_PDF_CAPTURES,
        FOLDER_IMAGE_CAPTURES,
    )

    HASHID_FIELD_SALT = values.Value("4OkZKanuMWUU4EO92FcDmwXkn6PbksGAIClUcG4S")
    HASHID_FIELD_LOOKUP_EXCEPTION = False
    HASHID_FIELD_ALLOW_INT_LOOKUP = False
    # Sal usado para gerar um nome de arquivo nas funções de captura em News
    FILE_HASHING_SALT = values.Value("hs204ViIUpIu45CTTUl3KsoQJgVtnmrHpXvRl8u5")

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": values.Value(
                "127.0.0.1:11211", True, environ_name="MEMCACHED_URL"
            ),
        }
    }


class IndexingWithElasticSearch(Common):
    # Application definition
    INSTALLED_APPS = Common.INSTALLED_APPS + [
        "django_elasticsearch_dsl",
        "xram_memory.search_indexes",
    ]

    ELASTICSEARCH_INDEX_NAMES = {
        "xram_memory.search_indexes.documents.news": "artifact_news",
        "xram_memory.search_indexes.documents.document": "artifact_document",
    }

    ELASTICSEARCH_DSL = {
        "default": {
            "hosts": values.Value(
                "localhost:9200",
                True,
                environ_name="ELASTICSEARCH_HOST",
                environ_prefix="DJANGO",
            ),
            "http_auth": values.TupleValue(
                environ_name="ELASTICSEARCH_CREDENTIALS", environ_prefix="DJANGO"
            ),
            "timeout": 30,
        },
    }

    ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = (
        "xram_memory.search_indexes.signals.FixtureAwareSignalProcessor"
    )


class IndexingWithLunrSearch(Common):
    # Application definition
    INSTALLED_APPS = Common.INSTALLED_APPS + [
        "xram_memory.lunr_index",
    ]

    # Intervalo mínimo entre a criação de arquivos de índice do Lunr
    LUNR_INDEX_REBUILD_INTERVAL = values.IntegerValue(10 * 60)  # 10 minutos
    # Tempo máximo que a operação deve levar, após o qual falhará
    LUNR_INDEX_REBUILD_TIMEOUT = values.IntegerValue(5 * 60)  # 5 minutos
    # Se devemos salvar o documento no indice - somente suportado pelo Elastic Lunr
    LUNR_INDEX_SAVE_DOCUMENT = values.BooleanValue(True)
    # Quais campos dos modelos indexar para busca
    LUNR_INDEX_SEARCH_FIELDS = values.ListValue(["title", "teaser"])
    # Caminho do arquivo do índice relativo a MEDIA_ROOT
    LUNR_INDEX_FILE_PATH = values.Value(
        os.path.join(Common.MEDIA_ROOT, "lunr_index/index.json")
    )
    # Tipo de reconstrução: 'local' (usa lunr.py para gerar localmente) ou 'remote' envia requisição http com dados
    # a serem indexados para o servidor definido em REMOTE_HOST

    # FIXME: exigência condicional de variável não funciona, porque o valor não pode ser lido instantaneamente aqui;
    # alternativa: usar uma connection string: file:///path/to/the/file para processamento local ou
    # http://secret@host:port para processamento remoto, eliminando as variáveis LUNR_INDEX_BACKEND,
    # LUNR_INDEX_FILE_PATH, LUNR_INDEX_REMOTE_HOST e LUNR_INDEX_REMOTE_SECRET
    LUNR_INDEX_BACKEND = LunrBackendValue(environ_required=True)
    # Host para onde as instâncias dos modelos a serem indexados devem ser enviados
    LUNR_INDEX_REMOTE_HOST = values.Value(
        environ_required=LUNR_INDEX_BACKEND == LunrBackendValue.BACKEND_REMOTE
    )
    # Segredo usado para autenticação http Bearer Token no servidor REMOTE_HOST
    LUNR_INDEX_REMOTE_SECRET = values.Value(
        environ_required=LUNR_INDEX_BACKEND == LunrBackendValue.BACKEND_REMOTE
    )


class IndexingWithAllApps(IndexingWithElasticSearch, IndexingWithLunrSearch, Common):
    # Application definition
    INSTALLED_APPS = Common.INSTALLED_APPS + [
        "django_elasticsearch_dsl",
        "xram_memory.search_indexes",
        "xram_memory.lunr_index",
    ]


class Development(IndexingWithAllApps):
    """
    The in-development settings and the default configuration.
    """

    DEBUG = True

    ALLOWED_HOSTS = values.ListValue(
        [
            "localhost",
            "127.0.0.1",
            "[::1]",
            "192.168.99.100",
            "xram-memory.local",
            "xram-memory.localhost",
        ]
    )

    INTERNAL_IPS = ["127.0.0.1"]

    MIDDLEWARE = Common.MIDDLEWARE + ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    INSTALLED_APPS = IndexingWithAllApps.INSTALLED_APPS + [
        "debug_toolbar",
        "cache_fallback",
    ]

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "ERROR",
            },
            "django": {
                "handlers": ["console"],
                "level": "INFO",
            },
        },
    }
    CELERY_BROKER_URL = values.Value("redis://127.0.0.1:6379/0")

    CORS_ORIGIN_ALLOW_ALL = True


class DevelopmentWithDocker(Development):
    # Habilite o debug toolbar no ambiente docker
    # https://gist.github.com/douglasmiranda/9de51aaba14543851ca3
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": "xram_memory.utils.show_toolbar",
    }


class Staging(IndexingWithLunrSearch):
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
    SECURE_PROXY_SSL_HEADER = values.TupleValue(("HTTP_X_FORWARDED_PROTO", "https"))

    ALLOWED_HOSTS = values.ListValue(
        default=["xram-memory.felipelube.com", "xram-memory.localhost"]
    )
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "ERROR",
            },
        },
    }

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": values.Value(
                "127.0.0.1:11211", True, environ_name="MEMCACHED_URL"
            ),
        }
    }


class Production(Staging):
    """
    The in-production settings.
    """
