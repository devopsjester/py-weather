import unittest
import unittest.mock as mock
from unittest.mock import patch, Mock

from weather import get_city_state

class TestGetCityState(unittest.TestCase):

    @patch("weather.requests.get")
    def test_get_city_state_success(self, mock_get):
        mock_response = Mock()
        expected_data = {
            "places": [
                {
                    "place name": "Test City",
                    "state abbreviation": "TS",
                    "latitude": "12.34",
                    "longitude": "56.78",
                }
            ]
        }
        mock_response.status_code = 200
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        city, state, latitude, longitude = get_city_state("12345")
        self.assertEqual(city, "Test City")
        self.assertEqual(state, "TS")
        self.assertEqual(latitude, "12.34")
        self.assertEqual(longitude, "56.78")

    @patch("weather.requests.get")
    def test_get_city_state_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        city, state, latitude, longitude = get_city_state("12345")
        self.assertIsNone(city)
        self.assertIsNone(state)
        self.assertIsNone(latitude)
        self.assertIsNone(longitude)

    @patch("weather.requests.get")
    def test_get_city_state_invalid_json(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        city, state, latitude, longitude = get_city_state("12345")
        self.assertIsNone(city)
        self.assertIsNone(state)
        self.assertIsNone(latitude)
        self.assertIsNone(longitude)

    @patch("weather.requests.get")
    def test_get_city_state_missing_fields(self, mock_get):
        mock_response = Mock()
        expected_data = {
            "places": [
                {
                    "place name": "Test City",
                    # Missing state abbreviation, latitude, and longitude
                    "state abbreviation": "",
                }
            ]
        }
        mock_response.status_code = 200
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        city, state, latitude, longitude = get_city_state("12345")
        self.assertEqual(city, "Test City")
        self.assertIsNone(state)
        self.assertIsNone(latitude)
        self.assertIsNone(longitude)

    @patch("weather.requests.get")
    def test_get_city_state_key_error(self, mock_get):
        mock_response = Mock()
        expected_data = {
            # Missing 'places' key
        }
        mock_response.status_code = 200
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        city, state, latitude, longitude = get_city_state("12345")
        self.assertIsNone(city)
        self.assertIsNone(state)
        self.assertIsNone(latitude)
        self.assertIsNone(longitude)
