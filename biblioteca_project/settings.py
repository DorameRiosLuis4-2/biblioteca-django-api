"""
Django settings for biblioteca_project project.
"""

from pathlib import Path
from decouple import config
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================
# SEGURIDAD (Desde .env)
# ==============================
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['DorameRiosLuis', 'localhost', '127.0.0.1']


# ==============================
# APLICACIONES (INSTALLED_APPS)
# ==============================
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Requerido por allauth
    
    # Herramientas de desarrollo
    'django_extensions',

    # Librerías de terceros (API y Auth)
    'rest_framework',
    'corsheaders',
    'django_filters',
    'oauth2_provider',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    # Tu aplicación local
    'libros',
    'channels',
    'graphene_django',
]

# GraphQL Settings
GRAPHENE = {
    'SCHEMA': 'libros.schema.schema',
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
    ],
}

# ==============================
# MIDDLEWARE
# ==============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Debe ir arriba de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'libros.middleware.SecurityMiddleware',
    'libros.middleware.RateLimitMiddleware',
]

ROOT_URLCONF = 'biblioteca_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'biblioteca_project.wsgi.application'

# ASGI Application
ASGI_APPLICATION = 'biblioteca_project.asgi.application'

# Channel Layers - Opción 1: Con Redis (RECOMENDADO para producción)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# ==============================
# BASE DE DATOS (MySQL desde .env)
# ==============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'), 
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8',
            'init_command': "SET default_storage_engine=INNODB, sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# ==============================
# AUTENTICACIÓN Y VALIDACIÓN
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configuración de Site ID (requerido por allauth)
SITE_ID = 1


# ==============================
# IDIOMA Y ZONA HORARIA
# ==============================
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Hermosillo'
USE_I18N = True
USE_TZ = True


# ==============================
# ARCHIVOS ESTÁTICOS
# ==============================
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================
# CONFIGURACIÓN DE CORS
# ==============================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://tudominio.com",
    "https://www.tudominio.com",
]
CORS_ALLOW_CREDENTIALS = True

# Headers permitidos
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ==============================
# DJANGO REST FRAMEWORK
# ==============================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    'DEFAULT_THROTTLE_CLASSES': [
        'libros.throttles.BurstRateThrottle',
        'libros.throttles.SustainedRateThrottle',
    ],

    'DEFAULT_THROTTLE_RATES': {
        'burst': '60/min',        # 60 por minuto
        'sustained': '1000/day',  # 1000 por día
        'anon_burst': '20/min',   # Anónimos: 20 por minuto
        'premium': '10000/day',   # Premium: 10000 por día
    }
}


# ==============================
# SIMPLE JWT CONFIG
# ==============================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# ==============================
# DJANGO ALLAUTH (Google OAuth)
# ==============================
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    }
}


# ==============================
# OAUTH2 PROVIDER (Toolkit)
# ==============================
# ==============================
# OAUTH2 PROVIDER (Toolkit)
# ==============================
OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope - Permite leer datos',
        'write': 'Write scope - Permite escribir datos',
        'groups': 'Access to groups - Acceso a grupos de usuario'
    },
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,  # 1 hora
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400,  # 1 día
    'AUTHORIZATION_CODE_EXPIRE_SECONDS': 600,  # 10 minutos
    'ROTATE_REFRESH_TOKEN': True,
    # Estas líneas aseguran que use los modelos por defecto
    'ACCESS_TOKEN_MODEL': 'oauth2_provider.AccessToken',
    'REFRESH_TOKEN_MODEL': 'oauth2_provider.RefreshToken',
}

# Solo para PRODUCCIÓN (no desarrollo)
if not DEBUG:
    # Forzar HTTPS
    SECURE_SSL_REDIRECT = True
    
    # Cookies seguras
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Headers de seguridad
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Proxy SSL headers
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Orígenes confiables para CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://tudominio.com",
    "https://www.tudominio.com",
]

# Cookie CSRF segura en producción
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = 'Strict'