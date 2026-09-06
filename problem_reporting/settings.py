
import os
import dj_database_url

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security 
# SECRET_KEY = 'django-insecure-g-d^jt%j9zmdmx6x8+rauc@un_fu6$sr%^5ab8ky^(i*&*=a*1'
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-g-d^jt%j9zmdmx6x8+rauc@un_fu6$sr%^5ab8ky^(i*&*=a*1')
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('1','true','yes')

# Allow Render's external URL
ALLOWED_HOSTS = ['localhost','127.0.0.1']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
if os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS += [h.strip() for h in os.environ['ALLOWED_HOSTS'].split(',') if h.strip()]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'management_utils',
]

# Add WhiteNoise to Middleware (place right under SecurityMiddleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- Add this here   
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

     # 'django.middleware.security.SecurityMiddleware',
   
]


ROOT_URLCONF = 'problem_reporting.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'management_utils.context_processors.ieprts_access',
            ],
        },
    },
]


# Database Configuration (fallback to SQLite locally, PostgreSQL on Render)
# DATABASES = {
#     'default': dj_database_url.config(
#         default='sqlite:///db.sqlite3',
#         conn_max_age=600
#     )
# }

# DATABASES = {

DATABASES = {
    
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# override the SQLite configuration if a DATABASE_URL environment variable exists
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.parse(
        os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
    
    # Add this line to enforce SSL connection required by Render PostgreSQL
    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}

# # override the SQLite configuration if a DATABASE_URL environment variable exists
# if os.environ.get('DATABASE_URL'):
#     DATABASES['default'] = dj_database_url.parse(
#         os.environ.get('DATABASE_URL'),
#         conn_max_age=600
#     )

# }



# WSGI_APPLICATION = 'problem_reporting.wsgi.application'



# Static Files Configuration
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL','noreply@uniben-ieprts.local')


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = 'login'


CSRF_TRUSTED_ORIGINS = [x.strip() for x in os.environ.get('CSRF_TRUSTED_ORIGINS','').split(',') if x.strip()]
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO','https')
