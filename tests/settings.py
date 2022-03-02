# -*- coding: utf-8
import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_pwned_passwords",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django_pwned_passwords.password_validation.PWNEDPasswordValidator'
    }
]

SITE_ID = 1

if django.VERSION >= (1, 11):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()
