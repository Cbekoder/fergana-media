from .base import *  # noqa

###################################################################
# General
###################################################################

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "ATOMIC_REQUESTS": False,
    }
}

###################################################################
# Django security
###################################################################

# https://docs.djangoproject.com/en/5.1/ref/settings/#use-x-forwarded-host
# https://docs.djangoproject.com/en/5.1/ref/settings/#secure-proxy-ssl-header
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-cookie-secure
# https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-trusted-origins
CSRF_COOKIE_SECURE = True  # if True, CSRF Cookie will work only on HTTPS
CSRF_TRUSTED_ORIGINS = [
    "https://api.ferganamedia.uz",
]

###################################################################
# CORS
###################################################################

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]
