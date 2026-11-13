#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-pwned-passwords
---------------------------

Tests for `django-pwned-passwords` password_validation module.
"""

import hashlib

import requests
import requests_mock
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from django_pwned_passwords.password_validation import PWNEDPasswordValidator


class TestPasswordValidation(TestCase):
    def get_hash(self, password):
        return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    @requests_mock.mock()
    def test_pwned_password_fails(self, m):
        validator = PWNEDPasswordValidator()
        password = "common"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(
            validator.url.format(short_hash=short_hash),
            status_code=200,
            text=p_hash[5:] + ":1",
        )

        with self.assertRaises(ValidationError):
            validator.validate(password)

    @override_settings(PWNED_VALIDATOR_MINIMUM_BREACHES=2)
    @requests_mock.mock()
    def test_above_limit_password_fails(self, m):
        validator = PWNEDPasswordValidator()
        password = "common"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(
            validator.url.format(short_hash=short_hash),
            status_code=200,
            text=p_hash[5:] + ":3",
        )

        with self.assertRaises(ValidationError):
            validator.validate(password)

    @override_settings(PWNED_VALIDATOR_MINIMUM_BREACHES=10)
    @requests_mock.mock()
    def test_below_limit_password_passes(self, m):
        validator = PWNEDPasswordValidator()
        password = "common"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(
            validator.url.format(short_hash=short_hash),
            status_code=200,
            text=p_hash[5:] + ":9",
        )

        try:
            validator.validate(password)
        except ValidationError:
            self.fail("ValidationError was raised for valid password")

    @requests_mock.mock()
    def test_zero_results_succeeds(self, m):
        validator = PWNEDPasswordValidator()
        password = "supersecret"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(validator.url.format(short_hash=short_hash), status_code=404)

        try:
            validator.validate(password)
        except ValidationError:
            self.fail("ValidationError was raised for valid password")

    @requests_mock.mock()
    def test_unpwned_password_succeeds(self, m):
        validator = PWNEDPasswordValidator()
        password = "supersecret"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(
            validator.url.format(short_hash=short_hash),
            status_code=200,
            text="07A60BA364011AACB2F0470CC983FCA6AF5:1",
        )

        try:
            validator.validate(password)
        except ValidationError:
            self.fail("ValidationError was raised for valid password")

    @requests_mock.mock()
    def test_fail_safe_ignores_rate_limit(self, m):
        validator = PWNEDPasswordValidator()
        password = "supersecret"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(validator.url.format(short_hash=short_hash), status_code=429)

        try:
            validator.validate(password)
        except ValidationError:
            self.fail("ValidationError was raised for valid password")

    @requests_mock.mock()
    def test_custom_fail_safe_ignores_exceptions(self, m):
        validator = PWNEDPasswordValidator()
        password = "doesn'tmatter"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(
            validator.url.format(short_hash=short_hash),
            exc=requests.exceptions.RequestException,
        )

        try:
            validator.validate(password)
        except ValidationError:
            self.fail("ValidationError was raised for valid password")

    @requests_mock.mock()
    @override_settings(PWNED_VALIDATOR_FAIL_SAFE=False)
    def test_not_fail_safe_fails_on_rate_limit(self, m):
        validator = PWNEDPasswordValidator()
        password = "doesn'tmatter"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(validator.url.format(short_hash=short_hash), status_code=429)

        with self.assertRaises(ValidationError):
            validator.validate(password)

    @requests_mock.mock()
    @override_settings(PWNED_VALIDATOR_FAIL_SAFE=False)
    def test_not_fail_safe_pwned_password_fails(self, m):
        validator = PWNEDPasswordValidator()
        password = "common"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(
            validator.url.format(short_hash=short_hash),
            status_code=200,
            text=p_hash[5:] + ":1",
        )

        with self.assertRaises(ValidationError):
            validator.validate(password)

    @requests_mock.mock()
    @override_settings(PWNED_VALIDATOR_FAIL_SAFE=False)
    def test_not_fail_safe_zero_results_fails(self, m):
        validator = PWNEDPasswordValidator()
        password = "supersecret"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(validator.url.format(short_hash=short_hash), status_code=404)

        with self.assertRaises(ValidationError):
            validator.validate(password)

    @requests_mock.mock()
    @override_settings(PWNED_VALIDATOR_FAIL_SAFE=False)
    def test_not_fail_safe_redirect_fails(self, m):
        validator = PWNEDPasswordValidator()
        password = "supersecret"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(validator.url.format(short_hash=short_hash), status_code=301)

        with self.assertRaises(ValidationError):
            validator.validate(password)

    @requests_mock.mock()
    @override_settings(PWNED_VALIDATOR_FAIL_SAFE=False)
    def test_not_fail_safe_unpwned_password_succeeds(self, m):
        validator = PWNEDPasswordValidator()
        password = "supersecret"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(
            validator.url.format(short_hash=short_hash),
            status_code=200,
            text=self.get_hash("notsecret")[5:] + ":1",
        )

        try:
            validator.validate(password)
        except ValidationError:
            self.fail("ValidationError was raised for valid password")

    @requests_mock.mock()
    @override_settings(PWNED_VALIDATOR_ERROR="failure")
    def test_custom_error_message(self, m):
        validator = PWNEDPasswordValidator()
        password = "doesn'tmatter"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(
            validator.url.format(short_hash=short_hash),
            status_code=200,
            text=p_hash[5:] + ":1",
        )

        try:
            validator.validate(password)
        except ValidationError as e:
            self.assertEqual(e.message, "failure")
            return
        except Exception as e:
            print(e)
        self.fail("No exception was thrown")

    @requests_mock.mock()
    @override_settings(
        PWNED_VALIDATOR_ERROR_FAIL="failure", PWNED_VALIDATOR_FAIL_SAFE=False
    )
    def test_custom_fail_message(self, m):
        validator = PWNEDPasswordValidator()
        password = "doesn'tmatter"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(validator.url.format(short_hash=short_hash), status_code=500)

        try:
            validator.validate(password)
        except ValidationError as e:
            self.assertEqual(e.message, "failure")
            return
        self.fail("No exception was thrown")

    @requests_mock.mock()
    @override_settings(
        PWNED_VALIDATOR_ERROR_FAIL="failure", PWNED_VALIDATOR_FAIL_SAFE=False
    )
    def test_custom_fail_message_timeout(self, m):
        validator = PWNEDPasswordValidator()
        password = "doesn'tmatter"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(
            validator.url.format(short_hash=short_hash),
            exc=requests.exceptions.ConnectTimeout,
        )

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

    @requests_mock.mock()
    @override_settings(PWNED_VALIDATOR_FAIL_SAFE=False)
    def test_pwned_password_bad_response(self, m):
        validator = PWNEDPasswordValidator()
        password = "common"
        p_hash = self.get_hash(password)
        short_hash = p_hash.upper()[:5]

        m.get(
            validator.url.format(short_hash=short_hash),
            status_code=200,
            text="random test with no colons",
        )

        with self.assertRaises(ValidationError):
            validator.validate(password)
