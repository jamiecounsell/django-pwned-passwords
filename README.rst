======================
Django PWNED Passwords
======================

.. image:: https://img.shields.io/pypi/v/django-pwned-passwords-ng.svg
    :target: https://pypi.org/project/django-pwned-passwords-ng/

.. image:: https://github.com/slinkymanbyday/django-pwned-passwords/actions/workflows/test.yml/badge.svg
    :target: https://github.com/slinkymanbyday/django-pwned-passwords/actions/workflows/test.yml

``django-pwned-passwords-ng`` is a maintained fork of `django-pwned-passwords <https://github.com/jamiecounsell/django-pwned-passwords>`_.
It is a drop-in replacement: the Python package, app name and validator path are unchanged.

django-pwned-passwords is a Django password validator that checks Troy Hunt's PWNED Passwords API to see if a password has been involved in a major security breach before.

**Note: This app currently sends a portion of a user's hashed password to a third party. Before using this application, you should understand how that impacts you.**

Documentation
-------------

The full documentation is in the `docs <https://github.com/slinkymanbyday/django-pwned-passwords/tree/master/docs>`_ directory.

Requirements
------------

* Django 5.2, 6.0, 6.1
* Python 3.11, 3.12, 3.13, 3.14, 3.15

Quickstart
----------

Install django-pwned-passwords-ng::

    pip install django-pwned-passwords-ng

.. note::

    ``django-pwned-passwords-ng`` installs the same ``django_pwned_passwords``
    Python package as the original ``django-pwned-passwords``. Uninstall the
    original before installing this one, as having both installed will conflict::

        pip uninstall django-pwned-passwords

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

This password validator returns a ValidationError if the PWNED Passwords API
detects the password in its data set. Note that the API is heavily rate-limited,
so there is a timeout (:code:`PWNED_VALIDATOR_TIMEOUT`).

If :code:`PWNED_VALIDATOR_FAIL_SAFE` is True, anything besides an API-identified bad password
will pass, including a timeout. If :code:`PWNED_VALIDATOR_FAIL_SAFE` is False, anything
besides a good password will fail and raise a ValidationError.


Settings
--------

+-------------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| Setting                                   | Description                                                                                                         | Default                                                                                                                          |
+-------------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_TIMEOUT`           | The timeout in seconds. The validator will not wait longer than this for a response from the API.                   | :code:`2`                                                                                                                        |
+-------------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_FAIL_SAFE`         | If the API fails to get a valid response, should we fail safe and allow the password through?                       | :code:`True`                                                                                                                     |
+-------------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_URL`               | The URL for the API in a string format.                                                                             | :code:`https://haveibeenpwned.com/api/v2/pwnedpassword/{short_hash}`                                                             |
+-------------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_ERROR`             | The error message for an invalid password.                                                                          | :code:`"Your password was determined to have been involved in a major security breach."`                                         |
+-------------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_ERROR_FAIL`        | The error message when the API fails. Note: this will only display if :code:`PWNED_VALIDATOR_FAIL_SAFE` is `False`. | :code:`"We could not validate the safety of this password. This does not mean the password is invalid. Please try again later."` |
+-------------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_HELP_TEXT`         | The help text for this password validator.                                                                          | :code:`"Your password must not have been detected in a major security breach."`                                                  |
+-------------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_MINIMUM_BREACHES`  | The minimum number of breaches needed to raise an error                                                             | :code:`1`                                                                                                                        |
+-------------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+


Rate Limiting
-------------

Historically, requests to the API were rate limited. However, with the new k-anonymity model-based API, there are no such rate limits.

Running Tests
-------------

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
