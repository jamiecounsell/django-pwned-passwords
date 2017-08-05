#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-pwned-passwords
---------------------------

Tests for `django-pwned-passwords` password_validation module.
"""

from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from django_pwned_passwords.password_validation import PWNEDPasswordValidator

import requests_mock
import requests


class TestPasswordValidation(TestCase):


    @requests_mock.mock()
    def test_pwned_password_fails(self, m):
        validator = PWNEDPasswordValidator()
        password = "common"

        m.get(validator.url.format(
            password = password
        ), status_code = 200)

        with self.assertRaises(ValidationError):
            validator.validate(password)

    @requests_mock.mock()
    def test_unpwned_password_succeeds(self, m):
        validator = PWNEDPasswordValidator()
        password = "supersecret"

        m.get(validator.url.format(
            password = password
        ), status_code = 404)

        try:
            validator.validate(password)
        except ValidationError:
            self.fail("ValidationError was raised for valid password")

    @requests_mock.mock()
    def test_fail_safe_ignores_rate_limit(self, m):
        validator = PWNEDPasswordValidator()
        password = "supersecret"

        m.get(validator.url.format(
            password = password
        ), status_code = 429)

        try:
            validator.validate(password)
        except ValidationError:
            self.fail("ValidationError was raised for valid password")

    @requests_mock.mock()
    def test_custom_fail_safe_ignores_exceptions(self, m):
        validator = PWNEDPasswordValidator()
        password = "doesntmatter"

        m.get(validator.url.format(
            password = password
        ), exc = requests.exceptions.RequestException)

        try:
            validator.validate(password)
        except ValidationError:
            self.fail("ValidationError was raised for valid password")

    @requests_mock.mock()
    @override_settings(PWNED_VALIDATOR_FAIL_SAFE = False)
    def test_not_fail_safe_fails_on_rate_limit(self, m):
        validator = PWNEDPasswordValidator()
        password = "doesntmatter"

        m.get(validator.url.format(
            password = password
        ), status_code = 429)

        with self.assertRaises(ValidationError):
            validator.validate(password)

    @requests_mock.mock()
    @override_settings(PWNED_VALIDATOR_ERROR = "failure")
    def test_custom_error_message(self, m):
        validator = PWNEDPasswordValidator()
        password = "doesntmatter"

        m.get(validator.url.format(
            password = password
        ), status_code = 200)

        try:
            validator.validate(password)
        except ValidationError as e:
            self.assertEqual(e.message, "failure")
            return
        self.fail("No exception was thrown")

    @requests_mock.mock()
    @override_settings(
        PWNED_VALIDATOR_ERROR_FAIL = "failure",
        PWNED_VALIDATOR_FAIL_SAFE = False)
    def test_custom_fail_message(self, m):
        validator = PWNEDPasswordValidator()
        password = "doesntmatter"

        m.get(validator.url.format(
            password = password
        ), status_code = 500)

        try:
            validator.validate(password)
        except ValidationError as e:
            self.assertEqual(e.message, "failure")
            return
        self.fail("No exception was thrown")

    @requests_mock.mock()
    @override_settings(
        PWNED_VALIDATOR_ERROR_FAIL = "failure",
        PWNED_VALIDATOR_FAIL_SAFE = False)
    def test_custom_fail_message_timeout(self, m):
        validator = PWNEDPasswordValidator()
        password = "doesntmatter"

        m.get(validator.url.format(
            password = password
        ), exc = requests.exceptions.ConnectTimeout)

        try:
            validator.validate(password)
        except ValidationError as e:
            self.assertEqual(e.message, "failure")
            return
        self.fail("No exception was thrown")

    def test_help_text(self):
        validator = PWNEDPasswordValidator()
        self.assertEqual(validator.get_help_text(), validator.help_text)

    @override_settings(PWNED_VALIDATOR_HELP_TEXT="help!")
    def test_custom_help_text(self):
        validator = PWNEDPasswordValidator()
        self.assertEqual(validator.get_help_text(), "help!")
