"""
Django settings for realestate project.
"""

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-local-development-key")

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://buy-sel-frontend.vercel.app",
]


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "https://buy-sel-frontend.vercel.app",
]


INSTALLED_APPS = [
    "cloudinary_storage",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "cloudinary",

    "rest_framework",
    "corsheaders",
    "rest_framework.authtoken",

    "accounts",
    "plans",
    "payments",
    "properties",
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
]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}


ROOT_URLCONF = "realestate.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "realestate.wsgi.application"

AUTH_USER_MODEL = "accounts.CustomUser"


DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "buysel_db",
            "USER": "postgres",
            "PASSWORD": "5866",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"

# CLOUDINARY_STORAGE = {
#     "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
#     "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
#     "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
# }

# STORAGES = {
#     "default": {
#         "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#     },
# }

# STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


# RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
# RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")


# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

WHITENOISE_AUTOREFRESH = True
WHITENOISE_USE_FINDERS = True


RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"