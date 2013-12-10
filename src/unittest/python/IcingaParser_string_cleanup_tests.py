import unittest
from metricd.IcingaParser import IcingaParser

class IcingaParserStringCleanupTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.parser = IcingaParser()

    def test_string_with_dots(self):
        self.assertEquals(self.parser.cleanString(".tuvdbs.50.rz.is"), 'tuvdbs50rzis')

    def test_string_with_special_characters(self):
        self.assertEquals(self.parser.cleanString("active_service_checks"), 'active_service_checks')

if __name__ == '__main__':
    unittest.main()
