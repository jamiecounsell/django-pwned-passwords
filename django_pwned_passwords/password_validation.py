from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext as _

import requests


class PWNEDPasswordValidator(object):
    """
    This password validator returns a ValidationError if the PWNED Passwords API
    detects the password in its data set. Note that the API is heavily rate-limited,
    so there is a timeout (PWNED_VALIDATOR_TIMEOUT).

    If self.fail_safe is True, anything besides an API-identified bad password
    will pass, including a timeout. If self.fail_safe is False, anything
    besides a good password will fail and raise a ValidationError.
    """

    def __init__(self, min_length=8):
        self.min_length = min_length
        self.timeout = getattr(settings, 'PWNED_VALIDATOR_TIMEOUT', 2)
        self.fail_safe = getattr(settings, 'PWNED_VALIDATOR_FAIL_SAFE', True)
        self.url = getattr(settings, 'PWNED_VALIDATOR_URL',
                             'https://haveibeenpwned.com/api/v2/pwnedpassword/{password}')
        self.error_msg = getattr(settings, 'PWNED_VALIDATOR_ERROR',
                             "Your password was detected in a major security breach.")
        self.error_fail_msg = getattr(settings, 'PWNED_VALIDATOR_ERROR_FAIL',
                             "We could not validate the safety of this password. This does not mean the password is invalid. Please try again later.")
        self.help_text = getattr(settings, 'PWNED_VALIDATOR_HELP_TEXT',
                             "Your password must not have been detected in a major security breach.")

    def validate(self, password, user=None):
        if not self.check_valid(password):
            raise ValidationError(self.error_msg)

    def check_valid(self, password):
        """
        Tests that a password is valid using the API. Note: The API returns
        the following status codes:

        200 - Password was found in data set. Bad password!
        404 - Password was not found in data set.

        If self.fail_safe is True, anything besides a bad password will
        return True. If self.fail_safe is False, anything besides a good password
        will return False.

        :param password: The password to test
        :return: True if the password is valid. Else, False.
        """

        VALID = True
        INVALID = False

        try:
            response = requests.get(self.get_url(password), timeout = self.timeout)
        except requests.exceptions.RequestException:
            if not self.fail_safe:
                raise ValidationError(self.error_fail_msg)
            return VALID

        if response.status_code == 200:
            return INVALID
        elif response.status_code == 404:
            return VALID

        if self.fail_safe:
            return VALID
        raise ValidationError(self.error_fail_msg)

    def get_url(self, password):
        return self.url.format(
            password = password
        )

    def get_help_text(self):
        return _(
            self.help_text
        )
