from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext as _

import hashlib
import requests


class PWNEDPasswordValidator(object):
    def __init__(self, min_length=8):
        self.min_length = min_length
        self.url = getattr(settings, 'PWNED_VALIDATOR_URL',
                             'https://haveibeenpwned.com/api/v2/pwnedpassword/{password}')
        self.error_msg = getattr(settings, 'PWNED_VALIDATOR_ERROR',
                             "Your password was detected in a major security breach.")
        self.help_text = getattr(settings, 'PWNED_VALIDATOR_ERROR',
                             "Your password must not have been detected in a major security breach.")

    def validate(self, password, user=None):
        if self.lookup(password):
            raise ValidationError(self.error_msg)

    def lookup(self, password):
        response = requests.get(self.get_url(password))
        return response.status_code == 200

    def get_url(self, password):
        return self.url.format(
            password = password
        )

    def get_hash(self, password):
        return hashlib.sha1(password).hexdigest()

    def get_help_text(self):
        return _(
            self.help_text
        )
