"""
Django settings for jCode project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-co&qhn&q2*%rg3491&*5#l9ts=fj2$a^mcha)h1_76n8hfg%dc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites', # New
    'sslserver',
    'star_ratings',
    'crispy_forms',
    'social_django',
    'social_core',
    'wkhtmltopdf',
    'app',
    'video',
    # ------------
    # social login
    # ------------
    'allauth', # New
    'allauth.account', # New
    'allauth.socialaccount', # New
    'allauth.socialaccount.providers.google', # New
    'allauth.socialaccount.providers.facebook', # new
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',

]

ROOT_URLCONF = 'jCode.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors1.category_list',
                'app.context_processors1.member_list',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'jCode.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jcode',
        'USER': 'root',
        'PASSWORD': 'APPc0de@2018y',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# localhost
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'Jcode',
#         'USER': 'postgres',
#         'PASSWORD': 'Pentai17',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / '/static'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

VIDEO_SERVER_URL = 'http://206.189.95.6:5000/video?videoname='
# test
# VIDEO_SERVER_URL = 'http://192.168.1.6:5000/video?videoname='

# SOCIAL_AUTH_FACEBOOK_KEY = "226390943256247"
# SOCIAL_AUTH_FACEBOOK_SECRET = "5a14605e50be071ea58f50af47a34f29"

# # SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '581497689095-a8c76nhcj55gu8kiqb7sspb58bfa7iet.apps.googleusercontent.com'
# # SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

# LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = 'home'
# LOGOUT_URL = 'logout'
# LOGOUT_REDIRECT_URL = 'login'

# ACCOUNT_DEFAULT_HTTP_PROTOCOL='http'

# SOCIAL_AUTH_PIPELINE = (
#     'social_core.pipeline.social_auth.social_details',
#     'social_core.pipeline.social_auth.social_uid',
#     'social_core.pipeline.social_auth.social_user',
#     'social_core.pipeline.user.get_username',
#     'social_core.pipeline.social_auth.associate_by_email',
#     'social_core.pipeline.user.create_user',
#     'social_core.pipeline.social_auth.associate_user',
#     'social_core.pipeline.social_auth.load_extra_data',
#     'social_core.pipeline.user.user_details',
# )

# SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [
#     ('name', 'name'),
#     ('email', 'email'),
#     ('picture', 'picture'),
#     ('link', 'profile_url'),
# ]

# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
#     'social_core.backends.facebook.FacebookOAuth2',
#     'app.loginemail.EmailBackend',


# ]

# # Facebook configuration
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
#     'fields': 'id, name, email'
# }

# Google configuration
# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']
# SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
#     'access_type': 'offline'
# }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''


# ------------
# social login
# ------------

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'app.loginemail.EmailBackend',
)

SITE_ID = 3
LOGIN_REDIRECT_URL = '/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        "APP": {
            "client_id": '684625158779-dars436078lb1osj3homo2s7o9km41f3.apps.googleusercontent.com',
            "secret": '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',
        },
    },
    'facebook': {
        'SCOPE': [
            'email',
        ],
        'FIELDS': ['email', 'first_name', 'last_name'],
        'APP': {
            'client_id': '226390943256247',
            'secret': '5a14605e50be071ea58f50af47a34f29',
        },
    }
}

SOCIALACCOUNT_ADAPTER = 'app.views.UserAccountAdapter'
