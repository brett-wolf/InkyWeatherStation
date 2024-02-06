import unittest
from ConfigHandler import ConfigHandler

class TestConfigHandler(unittest.TestCase):
    
    def test_init(self):
        config = ConfigHandler()

        self.assertIsNotNone(config)
        self.assertEqual(config.latitude, "37.55589989488259")
        self.assertEqual(config.longitude, "-77.4800165092538")

if __name__ == '__main__':
    unittest.main()