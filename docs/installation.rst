============
Installation
============

Install via pip::

    $ pip install django-pwned-passwords-ng

.. note::

    ``django-pwned-passwords-ng`` installs the same ``django_pwned_passwords``
    Python package as the original ``django-pwned-passwords``. Uninstall the
    original before installing this one, as having both installed will conflict::

        pip uninstall django-pwned-passwords


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

