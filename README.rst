=============================
Django PWNED Passwords
=============================

.. image:: https://badge.fury.io/py/django-pwned-passwords.svg
    :target: https://badge.fury.io/py/django-pwned-passwords

.. image:: https://travis-ci.org/jamiecounsell/django-pwned-passwords.svg?branch=master
    :target: https://travis-ci.org/jamiecounsell/django-pwned-passwords

.. image:: https://codecov.io/gh/jamiecounsell/django-pwned-passwords/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jamiecounsell/django-pwned-passwords

django-pwned-passwords is a Django password validator that checks Troy Hunt's PWNED Passwords API to see if a password has been involved in a major security breach before.

Documentation
-------------

The full documentation is at https://django-pwned-passwords.readthedocs.io.

Quickstart
----------

Install django-pwned-passwords::

    pip install django-pwned-passwords

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_pwned_passwords',
        ...
    )

Add django-pwned-passwords's PWNEDPasswordValidator:

.. code-block:: python

    AUTH_PASSWORD_VALIDATORS = [
        ...
        {
            'NAME': 'django_pwned_passwords.password_validation.PWNEDPasswordValidator'
        }
    ]


Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
