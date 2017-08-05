============
Installation
============

Install via pip::

    $ pip install django-pwned-passwords


Add it to your :code:`INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_pwned_passwords',
        ...
    )


Add django-pwned-passwords's :code:`PWNEDPasswordValidator` to :code:`AUTH_PASSWORD_VALIDATORS`:

.. code-block:: python

    AUTH_PASSWORD_VALIDATORS = [
        ...
        {
            'NAME': 'django_pwned_passwords.password_validation.PWNEDPasswordValidator'
        }
    ]

