import hashlib

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


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
        self.timeout = getattr(settings, "PWNED_VALIDATOR_TIMEOUT", 2)
        self.fail_safe = getattr(settings, "PWNED_VALIDATOR_FAIL_SAFE", True)
        self.min_breaches = getattr(settings, "PWNED_VALIDATOR_MINIMUM_BREACHES", 1)
        self.url = getattr(
            settings,
            "PWNED_VALIDATOR_URL",
            "https://api.pwnedpasswords.com/range/{short_hash}",
        )
        self.error_msg = getattr(
            settings,
            "PWNED_VALIDATOR_ERROR",
            "Your password was determined to have been involved in a major security breach.",  # noqa: E501
        )
        self.error_fail_msg = getattr(
            settings,
            "PWNED_VALIDATOR_ERROR_FAIL",
            "We could not validate the safety of this password. "
            "This does not mean the password is invalid. Please try again later.",
        )
        self.help_text = getattr(
            settings,
            "PWNED_VALIDATOR_HELP_TEXT",
            "Your password must not have been detected in a major security breach.",
        )

    def validate(self, password, user=None):
        if not self.check_valid(password):
            raise ValidationError(self.error_msg)

    def check_valid(self, password):
        """
        Tests that a password is valid using the API. Uses k-anonymity model in v2 API.

        If self.fail_safe is True, anything besides a bad password will
        return True. If self.fail_safe is False, anything besides a good password
        will return False.

        :param password: The password to test
        :return: True if the password is valid. Else, False.
        """

        VALID = True
        INVALID = False

        try:
            p_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
            response = requests.get(self.get_url(p_hash[0:5]), timeout=self.timeout)

            if self.get_breach_count(p_hash, response.text) >= self.min_breaches:
                return INVALID
            elif self.fail_safe:
                return VALID
            elif response.status_code in [400, 429, 500]:
                raise ValidationError(self.error_fail_msg)
            elif response.status_code in [200]:
                return VALID
        except (requests.exceptions.RequestException, IndexError, ValueError):
            if not self.fail_safe:
                raise ValidationError(self.error_fail_msg)
            return VALID

        if self.fail_safe:
            return VALID
        raise ValidationError(self.error_fail_msg)

    def get_url(self, short_hash):
        return self.url.format(short_hash=short_hash)

    def get_help_text(self):
        return _(self.help_text)

    @staticmethod
    def get_breach_count(p_hash, response_text):
        for line in response_text.splitlines():
            hash, count = line.split(":")
            if p_hash[5:] == hash:
                return int(count)
        return 0
