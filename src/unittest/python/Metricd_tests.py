import unittest
from metricd.Metricd import Metricd

class MetricdTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.metricd = Metricd()
        self.metricd.init_logger()

    def test_get_config(self):
        with self.assertRaises(SystemExit):
            self.metricd.get_config("Test","Test")

if __name__ == '__main__':
    unittest.main()
