import http.client
import os
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

BASE_URL = os.environ.get("BASE_URL")
DEFAULT_TIMEOUT = 2  # in secs


@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def assert_api_ok(self, path, expected):
        url = f"{BASE_URL}{path}"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), expected, f"Resultado incorrecto en {url}"
        )

    def assert_api_bad_request(self, path):
        url = f"{BASE_URL}{path}"
        with self.assertRaises(HTTPError) as error:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            error.exception.code,
            http.client.BAD_REQUEST,
            f"La API no devolvió 400 en {url}",
        )

    # Raíz
    def test_api_hello(self):
        self.assert_api_ok("/", "Hello from The Calculator!\n")

    # Suma
    def test_api_add(self):
        self.assert_api_ok("/calc/add/2/2", "4")
        self.assert_api_ok("/calc/add/-2/2", "0")
        self.assert_api_ok("/calc/add/1.5/2", "3.5")

    def test_api_add_fails_with_nan_parameter(self):
        self.assert_api_bad_request("/calc/add/a/2")
        self.assert_api_bad_request("/calc/add/2/b")

    # Resta
    def test_api_substract(self):
        self.assert_api_ok("/calc/substract/5/3", "2")
        self.assert_api_ok("/calc/substract/3/5", "-2")

    def test_api_substract_fails_with_nan_parameter(self):
        self.assert_api_bad_request("/calc/substract/a/2")
        self.assert_api_bad_request("/calc/substract/2/b")

    # Multiplicación
    def test_api_multiply(self):
        self.assert_api_ok("/calc/multiply/3/4", "12")
        self.assert_api_ok("/calc/multiply/-2/3", "-6")

    def test_api_multiply_fails_with_nan_parameter(self):
        self.assert_api_bad_request("/calc/multiply/a/2")
        self.assert_api_bad_request("/calc/multiply/2/b")

    # División
    def test_api_divide(self):
        self.assert_api_ok("/calc/divide/6/3", "2.0")
        self.assert_api_ok("/calc/divide/3/2", "1.5")

    def test_api_divide_fails_with_division_by_zero(self):
        self.assert_api_bad_request("/calc/divide/1/0")

    def test_api_divide_fails_with_nan_parameter(self):
        self.assert_api_bad_request("/calc/divide/a/2")
        self.assert_api_bad_request("/calc/divide/2/b")

    # Potenciación
    def test_api_power(self):
        self.assert_api_ok("/calc/power/2/3", "8.0")
        self.assert_api_ok("/calc/power/2/-1", "0.5")

    def test_api_power_fails_with_invalid_operation(self):
        self.assert_api_bad_request("/calc/power/0/-1")
        self.assert_api_bad_request("/calc/power/-8/0.5")

    def test_api_power_fails_with_nan_parameter(self):
        self.assert_api_bad_request("/calc/power/a/2")

    # Raíz cuadrada
    def test_api_sqrt(self):
        self.assert_api_ok("/calc/sqrt/9", "3.0")
        self.assert_api_ok("/calc/sqrt/2.25", "1.5")

    def test_api_sqrt_fails_with_negative_number(self):
        self.assert_api_bad_request("/calc/sqrt/-4")

    def test_api_sqrt_fails_with_nan_parameter(self):
        self.assert_api_bad_request("/calc/sqrt/a")

    # Logaritmo en base 10
    def test_api_log10(self):
        self.assert_api_ok("/calc/log10/100", "2.0")
        self.assert_api_ok("/calc/log10/1", "0.0")

    def test_api_log10_fails_with_zero_or_negative_number(self):
        self.assert_api_bad_request("/calc/log10/0")
        self.assert_api_bad_request("/calc/log10/-10")

    def test_api_log10_fails_with_nan_parameter(self):
        self.assert_api_bad_request("/calc/log10/a")
