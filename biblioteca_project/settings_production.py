import os
from .settings import *
from decouple import config # ← Usamos decouple en lugar de os.environ

# ==========================================
# CONFIGURACIÓN DE SEGURIDAD PARA PRODUCCIÓN
# ==========================================

# decouple maneja el cast=bool automáticamente
DEBUG = config('DEBUG', default=False, cast=bool)

# Leer el dominio desde el .env
WEB_DOMAIN = config('WEB_DOMAIN', default='dorameriosluis.pythonanywhere.com')

ALLOWED_HOSTS = [
    WEB_DOMAIN,
    'localhost',
    '127.0.0.1',
]

# ==========================================
# BASE DE DATOS (Conectada al .env vía decouple)
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'), 
        'USER': config('DB_USER'), 
        'PASSWORD': config('DB_PASSWORD'), 
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ==========================================
# ARCHIVOS ESTÁTICOS
# ==========================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Middleware para servir archivos estáticos (Whitenoise)
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# ==========================================
# SEGURIDAD HTTPS Y COOKIES
# ==========================================
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# ==========================================
# CORS Y OAUTH
# ==========================================
CORS_ALLOWED_ORIGINS = [
    f'https://{WEB_DOMAIN}',
]

# Variable dinámica para tu oauth_views.py
OAUTH_REDIRECT_URI = f'https://{WEB_DOMAIN}/api/auth/google/callback/'