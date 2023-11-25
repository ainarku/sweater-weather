from unittest.mock import patch
from django.test import RequestFactory, TestCase
from .utils import api_request
from .utils import process_weather_data
from .utils import process_forecast_data
from .utils import kelvin_to_celsius, kelvin_to_fahrenheit
from .utils import extract_request_data


class TestApiRequest(TestCase):
    @patch('requests.get')
    def test_api_request_valid_response(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.text = '{"main": {"temp": 300}, "weather": [{"description": "Clear"}]}'

        result = api_request('London', 'weather', 'C')

        self.assertIsNotNone(result)
        self.assertAlmostEqual(result['temperature'], 26.85, places=2)


class TestProcessWeatherData(TestCase):
    def test_process_weather_data(self):
        sample_data = {
            'name': 'London',
            'main': {'temp': 300, 'feels_like': 298, 'humidity': 70},
            'weather': [{'description': 'Clear'}]
        }

        result = process_weather_data(sample_data, 'C')

        self.assertIsNotNone(result)
        self.assertAlmostEqual(result['temperature'], 26.85, places=2)


class TestProcessForecastData(TestCase):
    def test_process_forecast_data(self):
        sample_data = {
            'list': [
                {
                    'dt': 1637644800,
                    'main': {
                        'temp': 300,
                        'feels_like': 298,
                        'humidity': 70
                    },
                    'weather': [
                        {'description': 'Clear'}
                    ]
                },
            ]
        }

        result = process_forecast_data(sample_data, 'C')

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)


class TestTemperatureConversion(TestCase):
    def test_temperature_conversion(self):
        kelvin_value = 300

        celsius_result = kelvin_to_celsius(kelvin_value)
        fahrenheit_result = kelvin_to_fahrenheit(kelvin_value)

        self.assertAlmostEqual(celsius_result, 26.85, places=2)
        self.assertAlmostEqual(fahrenheit_result, 80.33, places=2)


class TestExtractRequestData(TestCase):
    def test_extract_request_data(self):
        factory = RequestFactory()
        request = factory.post('/some-url/', {'city': 'London', 'temperature_unit': 'C'})

        city, temperature_unit = extract_request_data(request)

        self.assertEqual(city, 'London')
        self.assertEqual(temperature_unit, 'C')
