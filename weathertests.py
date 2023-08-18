import unittest
from weather-app import get_city_state, get_temperature, get_weather

class TestWeatherApp(unittest.TestCase):
    def test_get_city_state(self):
        city, state = get_city_state("90210")
        self.assertEqual(city, "Beverly Hills")
        self.assertEqual(state, "California")

    def test_get_temperature(self):
        temperature = get_temperature("Beverly Hills", "California")
        self.assertGreater(temperature, 0)
        self.assertLess(temperature, 200)

    def test_get_weather(self):
        weather = get_weather("Beverly Hills", "California")
        self.assertIn(weather, ["clear sky", "few clouds", "scattered clouds", "broken clouds", "overcast clouds", "light rain", "moderate rain", "heavy intensity rain", "very heavy rain", "extreme rain", "freezing rain", "light intensity shower rain", "shower rain", "heavy intensity shower rain", "ragged shower rain"])

if __name__ == "__main__":
    unittest.main()