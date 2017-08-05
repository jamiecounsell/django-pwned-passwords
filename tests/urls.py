# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from django_pwned_passwords.urls import urlpatterns as django_pwned_passwords_urls

urlpatterns = [
    url(r'^', include(django_pwned_passwords_urls, namespace='django_pwned_passwords')),
]
