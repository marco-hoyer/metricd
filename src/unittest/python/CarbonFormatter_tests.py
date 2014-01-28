import unittest
from metricd.CarbonFormatter import CarbonFormatter


class CarbonFormatterTest(unittest.TestCase):

    def test_convert_string(self):
        formatter = CarbonFormatter()
        self.assertEquals(formatter.convert_string("ping"), "ping")
        self.assertEquals(formatter.convert_string("system ping"), "system_ping")
        self.assertEquals(formatter.convert_string("System"), "system")
        self.assertEquals(formatter.convert_string("PL"), "pl")
        self.assertEquals(formatter.convert_string(""), "")
        self.assertEquals(formatter.convert_string(" a b c "), "a_b_c")
        self.assertEquals(formatter.convert_string(" "), "")

    def test_get_type_from_hostname(self):
        formatter = CarbonFormatter()
        self.assertEqual(formatter.get_type_from_hostname("tuvdbs50"),"dbs")
        self.assertEqual(formatter.get_type_from_hostname("my-super-uplink"),'')

    def test_format_carbon_lines(self):
        formatter = CarbonFormatter()
        metric = {'metrics': [{'name': 'rta', 'value': '0.888000'},
                              {'name': 'pl', 'value': '0'}],
                  'timestamp': '1364909110',
                  'hostname': 'tuvdbs50',
                  'servicename': 'ping'}
        result = formatter.format('icinga', metric)
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0],
                'dbs.tuvdbs50.icinga.ping.rta 0.888000 1364909110\n')
        self.assertEquals(result[1],
                'dbs.tuvdbs50.icinga.ping.pl 0 1364909110\n')

    def test_format_metrics_with_spaces_to_carbon_lines(self):
        formatter = CarbonFormatter()
        metric = {'metrics': [{'name': 'rta', 'value': '0.888000'},
                              {'name': 'metric with spaces', 'value': '0'}],
                  'timestamp': '1364909110',
                  'hostname': 'tuvdbs50',
                  'servicename': 'system ping'}
        result = formatter.format('icinga', metric)
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0],
                'dbs.tuvdbs50.icinga.system_ping.rta 0.888000 1364909110\n')
        self.assertEquals(result[1],
                'dbs.tuvdbs50.icinga.system_ping.metric_with_spaces 0 1364909110\n')

    def test_format_metrics_with_special_hostname(self):
        formatter = CarbonFormatter()
        metric = {'metrics': [{'name': 'rta', 'value': '0.888000'},
                              {'name': 'metric with spaces', 'value': '0'}],
                  'timestamp': '1364909110',
                  'hostname': 'my-super-uplink',
                  'servicename': 'system ping'}
        result = formatter.format('icinga', metric)
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0],
                'my-super-uplink.icinga.system_ping.rta 0.888000 1364909110\n')
        self.assertEquals(result[1],
                'my-super-uplink.icinga.system_ping.metric_with_spaces 0 1364909110\n')

if __name__ == '__main__':
    unittest.main()
