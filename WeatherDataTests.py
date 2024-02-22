import unittest
from WeatherData import WeatherData


class TestWeatherData(unittest.TestCase):
    sampleJson = {
        "weather": [{"main": "clear", "description": "death", "icon": "skull"}],
        "dt": 1707253946,
        "main": {"temp": "666", "feels_like": "69", "humidity": "40"},
        "wind": {"speed": "100"},
        "sys": {"sunrise": 1707221372, "sunset": 1707259106},
    }

    def test_parse_weather_data_exists(self):
        returnValue = WeatherData._parse_data(self, TestWeatherData.sampleJson)
        self.assertIsNotNone(returnValue)

    def test_parse_weather_data_description(self):
        returnValue = WeatherData._parse_data(self, TestWeatherData.sampleJson)
        self.assertEqual(returnValue.description, "death")
