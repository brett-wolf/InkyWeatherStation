import unittest
from ConfigHandler import ConfigHandler

class TestConfigHandler(unittest.TestCase):
    
    def setUp(self):
        self.config = ConfigHandler()

    def test_config_exists(self):
        self.assertIsNotNone(self.config)

    def test_config_latitude(self):        
        self.assertEqual(self.config.latitude, "37.55589989488259")
    
    def test_config_longitude(self):
        self.assertEqual(self.config.longitude, "-77.4800165092538")

    def test_config_weatherurl(self):
        self.assertIsNotNone(self.config.weather_url)

if __name__ == '__main__':
    unittest.main()