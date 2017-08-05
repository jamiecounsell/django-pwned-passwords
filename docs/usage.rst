=====
Usage
=====

To use django-pwned-passwords in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_pwned_passwords.apps.DjangoPwnedPasswordsConfig',
        ...
    )

Add django-pwned-passwords's URL patterns:

.. code-block:: python

    from django_pwned_passwords import urls as django_pwned_passwords_urls


    urlpatterns = [
        ...
        url(r'^', include(django_pwned_passwords_urls)),
        ...
    ]
