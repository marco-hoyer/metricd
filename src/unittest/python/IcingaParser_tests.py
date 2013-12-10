import unittest
from metricd.IcingaParser import IcingaParser

class IcingaParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = IcingaParser()
        self.result = self.parser.parse('tuvdbs50|Ping|rta=0.888000ms;3000.000000;5000.000000;0.000000 pl=0%;80;100;0|1364909110')

    def test_parses_hostname(self):
        self.assertEquals(self.result.get('hostname'), 'tuvdbs50')

    def test_parses_servicename(self):
        self.assertEquals(self.result.get('servicename'), 'ping')

    def test_parses_metrics(self):
        metrics = self.result.get('metrics')
        self.assertEquals(len(metrics), 2)
        self.assertEquals(metrics[0].get('name'), 'rta')
        self.assertEquals(metrics[0].get('value'), '0.888000')
        self.assertEquals(metrics[1].get('name'), 'pl')
        self.assertEquals(metrics[1].get('value'), '0')

    def test_parses_timestamp(self):
        self.assertEquals(self.result.get('timestamp'), '1364909110')

    def test_parses_empty_line(self):
        result = self.parser.parse('')
        self.assertTrue(result is None)

if __name__ == '__main__':
    unittest.main()
