import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DJANGO_DEBUG = os.getenv("DJANGO_DEBUG")
if DJANGO_DEBUG == "False" or False:
    DEBUG = False

ALLOWED_HOSTS = ["*", "http://129.148.59.220",]
CSRF_TRUSTED_ORIGINS = [
    "http://129.148.59.220",
    "https://129.148.59.220",
    "http://estampaverso.shop", 
    "https://estampaverso.shop"
]
CORS_ORIGIN_ALLOW_ALL = True



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'fontawesomefree',
    'csp',
]

# Content Security Policy no settings.py

CSP_DEFAULT_SRC = (
    "'self'", 
    "'unsafe-inline'", 
    "'unsafe-eval'",  # Necessário para permitir certas funcionalidades JavaScript
)

CSP_STYLE_SRC = (
    "'self'", 
    "'unsafe-inline'", 
    "https://fonts.googleapis.com",  # Google Fonts
)

CSP_FONT_SRC = (
    "'self'", 
    "https://fonts.gstatic.com",  # Fontes do Google
)

CSP_SCRIPT_SRC = (
    "'self'", 
    "'unsafe-inline'", 
    "'unsafe-eval'",  
    "https://pagead2.googlesyndication.com",  
    "https://www.googletagmanager.com",  
    "https://www.google-analytics.com",  
    "https://cdn.jsdelivr.net",  
    "https://www.gstatic.com",  
    "https://securepubads.g.doubleclick.net",  
    "https://www.google.com",  
    "https://ep2.adtrafficquality.google",  # Adicionando para permitir o script de anúncios
    "https://ep2.adtrafficquality.google/sodar/sodar2.js",  # Adicionando o script específico
)

CSP_FRAME_SRC = (
    "'self'", 
    "https://googleads.g.doubleclick.net",  # Google Ads
    "https://ep2.adtrafficquality.google",  # Google Ads
    "https://www.google.com",  # Google
    "https://td.doubleclick.net",  # DoubleClick
    "https://securepubads.g.doubleclick.net",  # Adicional para o Google Ads
    "https://www.gstatic.com",  # Scripts relacionados ao Google Ads
)

CSP_FRAME_ANCESTORS = (
    "'self'",  # Permitir embutir apenas em seu próprio domínio
    "https://www.google.com",  # Permitir embutir em iframes do Google
    "https://googleads.g.doubleclick.net",  # Permitir iframes do Google Ads
    "https://securepubads.g.doubleclick.net",  # Adicional para anúncios do Google
)

CSP_CONNECT_SRC = (
    "'self'", 
    "https://ep1.adtrafficquality.google",  
    "https://csi.gstatic.com",  
    "https://www.google-analytics.com",  
    "https://analytics.google.com",  
    "https://stats.g.doubleclick.net",  
    "https://pagead2.googlesyndication.com",  
    "https://googleads.g.doubleclick.net",  
    "https://www.googletagmanager.com",  
    "https://www.gstatic.com",  
    "https://www.google.com.br/ads/ga-audiences",  
    "https://ep2.adtrafficquality.google",  # Adicionando domínio para conexões de anúncios
)

CSP_IMG_SRC = (
    "'self'", 
    "data:",  # Permitir imagens em base64
    "https://ep1.adtrafficquality.google",  # Google Ads
    "https://pagead2.googlesyndication.com",  # Google Ads
    "https://www.google.com.br",  # Google Imagens
    "https://www.google.com",  # Google Imagens
    "https://www.googletagmanager.com",  # Imagens do Google Tag Manager
    "https://securepubads.g.doubleclick.net",  # Google Ads
    "https://www.gstatic.com",  # Outros recursos de imagem do Google
)



AUTH_USER_MODEL = 'blog.UserRegistration'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blog.middleware.VerificarURLMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'fatosedados.urls'

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

WSGI_APPLICATION = 'fatosedados.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "db.sqlite3",
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': os.getenv("DB_ENGINE"),
#         'NAME': os.getenv("DB_NAME"),
#         'USER': os.getenv("DB_USER"),
#         'PASSWORD': os.getenv("DB_PASSWORD"),
#         'HOST': os.getenv("DB_HOST"),
#         'PORT': os.getenv("DB_PORT"),
#         'OPTIONS': {
#             'ssl': {'ca': 'us-east-2-bundle.pem'}
#         }
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# STATIC_URL = 'static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
