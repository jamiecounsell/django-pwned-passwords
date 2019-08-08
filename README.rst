======================
Django PWNED Passwords
======================

.. image:: https://badge.fury.io/py/django-pwned-passwords.svg
    :target: https://badge.fury.io/py/django-pwned-passwords

.. image:: https://travis-ci.org/jamiecounsell/django-pwned-passwords.svg?branch=master
    :target: https://travis-ci.org/jamiecounsell/django-pwned-passwords

.. image:: https://codecov.io/gh/jamiecounsell/django-pwned-passwords/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jamiecounsell/django-pwned-passwords

django-pwned-passwords is a Django password validator that checks Troy Hunt's PWNED Passwords API to see if a password has been involved in a major security breach before.

**Note: This app currently sends a portion of a user's hashed password to a third party. Before using this application, you should understand how that impacts you.**

Documentation
-------------

The full documentation is at https://django-pwned-passwords.readthedocs.io.

Requirements
------------

* Django [1.9, 2.1]
* Python 2.7, [3.5, 3.6, 3.7]

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
