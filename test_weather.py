import unittest
from unittest.mock import patch
import argparse  # Standard library import should be placed before local imports
import sys

from weather import get_city_state, get_temperature, display_zipcode, main

class TestWeather(unittest.TestCase):

    @patch('weather.requests.get')
    def test_get_city_state_valid_zipcode(self, mock_get):
        mock_response = {
            "places": [
                {
                    "place name": "Test City",
                    "state abbreviation": "TC",
                    "latitude": "12.34",
                    "longitude": "56.78"
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        city, state, latitude, longitude = get_city_state("12345")
        self.assertEqual(city, "Test City")
        self.assertEqual(state, "TC")
        self.assertEqual(latitude, "12.34")
        self.assertEqual(longitude, "56.78")

    @patch('weather.requests.get')
    def test_get_city_state_invalid_zipcode(self, mock_get):
        mock_get.return_value.status_code = 404

        city, state, latitude, longitude = get_city_state("00000")
        self.assertIsNone(city)
        self.assertIsNone(state)
        self.assertIsNone(latitude)
        self.assertIsNone(longitude)

    @patch('weather.requests.get')
    def test_get_temperature_valid_coordinates(self, mock_get):
        mock_response = {
            "main": {
                "temp": 75.0
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        temperature = get_temperature("12.34", "56.78", "fake_api_key")
        self.assertEqual(temperature, 75.0)

    @patch('weather.requests.get')
    def test_get_temperature_invalid_coordinates(self, mock_get):
        mock_get.return_value.status_code = 404

        temperature = get_temperature("00.00", "00.00", "fake_api_key")
        self.assertIsNone(temperature)

    @patch('weather.get_city_state')
    @patch('weather.get_temperature')
    def test_display_zipcode_valid(self, mock_get_temperature, mock_get_city_state):
        mock_get_city_state.return_value = ("Test City", "TC", "12.34", "56.78")
        mock_get_temperature.return_value = 75.0

        with patch('builtins.print') as mocked_print:
            display_zipcode("12345", "fake_api_key")
            mocked_print.assert_called_with("The zipcode 12345 corresponds to Test City, TC. The current temperature is 75.0°F.")

    @patch('weather.get_city_state')
    @patch('weather.get_temperature')
    def test_display_zipcode_invalid_temperature(self, mock_get_temperature, mock_get_city_state):
        mock_get_city_state.return_value = ("Test City", "TC", "12.34", "56.78")
        mock_get_temperature.return_value = None

        with patch('builtins.print') as mocked_print:
            display_zipcode("12345", "fake_api_key")
            mocked_print.assert_called_with("Could not retrieve temperature for the zipcode: 12345")

    @patch('weather.get_city_state')
    def test_display_zipcode_invalid_zipcode(self, mock_get_city_state):
        mock_get_city_state.return_value = (None, None, None, None)

        with patch('builtins.print') as mocked_print:
            display_zipcode("00000", "fake_api_key")
            mocked_print.assert_called_with("Could not find city and state for the zipcode: 00000")

    @patch('weather.os.getenv')
    @patch('weather.display_zipcode')
    def test_main_missing_api_key(self, mock_display_zipcode, mock_getenv):
        mock_getenv.return_value = None

        with patch('builtins.print') as mocked_print:
            with patch.object(sys, 'argv', ['weather.py', '--zipcode', '12345']):
                main()
                mocked_print.assert_called_with("Error: OPENWEATHERMAP_API_KEY environment variable not set.")
                mock_display_zipcode.assert_not_called()

    @patch('weather.os.getenv')
    @patch('weather.display_zipcode')
    @patch('weather.argparse.ArgumentParser.parse_args')
    def test_main_valid_api_key(self, mock_parse_args, mock_display_zipcode, mock_getenv):
        mock_getenv.return_value = "fake_api_key"
        mock_parse_args.return_value = argparse.Namespace(zipcode="12345")

        with patch.object(sys, 'argv', ['weather.py', '--zipcode', '12345']):
            main()
            mock_display_zipcode.assert_called_with("12345", "fake_api_key")

if __name__ == '__main__':
    unittest.main()