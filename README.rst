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

**Note: This app currently sends user passwords to a third party. There are obvious security risks associated with this practice.**

Documentation
-------------

The full documentation is at https://django-pwned-passwords.readthedocs.io.

Requirements
------------

* Django [1.8, 1.11]
* Python 2.7, [3.4, 3.6]

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

+------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| Setting                            | Description                                                                                                         | Default                                                                                                                          |
+------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_TIMEOUT`    | The timeout in seconds. The validator will not wait longer than this for a response from the API.                   | :code:`2`                                                                                                                        |
+------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_FAIL_SAFE`  | If the API fails to get a valid response, should we fail safe and allow the password through?                       | :code:`True`                                                                                                                     |
+------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_URL`        | The URL for the API in a string format.                                                                             | :code:`https://haveibeenpwned.com/api/v2/pwnedpassword/{password}`                                                               |
+------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_ERROR`      | The error message for an invalid password.                                                                          | :code:`"Your password was detected in a major security breach."`                                                                 |
+------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_ERROR_FAIL` | The error message when the API fails. Note: this will only display if :code:`PWNED_VALIDATOR_FAIL_SAFE` is `False`. | :code:`"We could not validate the safety of this password. This does not mean the password is invalid. Please try again later."` |
+------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| :code:`PWNED_VALIDATOR_HELP_TEXT`  | The help text for this password validator.                                                                          | :code:`"Your password must not have been detected in a major security breach."`                                                  |
+------------------------------------+---------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+

Rate Limiting
-------------

Requests to the Pwned Passwords API are limited to one per every 1500 milliseconds each from any given IP address
(an address may request both APIs within this period). Any request that exceeds the limit will receive an
HTTP 429 "Too many requests" response. If :code:`PWNED_VALIDATOR_FAIL_SAFE` is `True`, rate limited responses will simply
allow the password through. Otherwise, they will fail and the user will not be able to register until the
API returns a non-429 status code.

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
