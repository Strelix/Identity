import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "secret_key")

AUTH_USER_MODEL = "identity.user"

DEBUG = True if os.environ.get("DEBUG") in ["True", "true", "TRUE", True] else False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_api_key',
    'identity'
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

ROOT_URLCONF = 'identity.settings.urls'

WSGI_APPLICATION = 'identity.settings.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DB_TYPE = os.environ.get("DATABASE_TYPE", "").lower()

print(DB_TYPE)

DATABASES = {
    "default": {
        "ENGINE": (
            "django.db.backends.postgresql_psycopg2" if DB_TYPE == "mysql" else "django.db.backends.postgresql"),
        "NAME": os.environ.get("DATABASE_NAME") or "identity",
        "USER": os.environ.get("DATABASE_USER") or "root",
        "PASSWORD": os.environ.get("DATABASE_PASS") or "",
        "HOST": os.environ.get("DATABASE_HOST") or "localhost",
        "PORT": os.environ.get("DATABASE_PORT") or (3306 if DB_TYPE == "mysql" else 5432),
        "OPTIONS": (
            {
                "sql_mode": "traditional",
            }
            if DB_TYPE == "mysql"
            else {}
        ),
    } if DB_TYPE != "sqlite" else {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get("sqlite_path", BASE_DIR / 'db.sqlite3')
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        # "rest_framework.permissions.IsAuthenticated",
        # "rest_framework_api_key.permissions.HasAPIKey",
        "identity.settings.permissions.HasAPIKey"
    ],
    "DEFAULT_RENDERER_CLASSES": (["rest_framework.renderers.JSONRenderer"]),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "DEFAULT_INFO": "backend.core.api.public.swagger_ui.INFO", # todo change
    "SECURITY_DEFINITIONS": {"Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}},
}

# add a check for https://
URL_LIST: list[str] = [url for url in os.environ.get("URL", "").split(",")]
URL_LIST_HTTPS: list[str] = [URL if URL.startswith("https://") else f"https://{URL}" for URL in URL_LIST]

ALLOWED_HOSTS: list[str] = [url for url in ([os.environ.get("URL", "")] + URL_LIST) if url not in [" ", "", None]]