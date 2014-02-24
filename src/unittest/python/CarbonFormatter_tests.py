import unittest
from metricd.CarbonFormatter import CarbonFormatter


class CarbonFormatterTest(unittest.TestCase):

    def test_convert_string(self):
        formatter = CarbonFormatter()
        self.assertEquals(formatter.clean_string("ping"), "ping")
        self.assertEquals(formatter.clean_string("system ping"), "system_ping")
        self.assertEquals(formatter.clean_string("System"), "system")
        self.assertEquals(formatter.clean_string("PL"), "pl")
        self.assertEquals(formatter.clean_string(""), "")
        self.assertEquals(formatter.clean_string(" a b c "), "a_b_c")
        self.assertEquals(formatter.clean_string(" "), "")

    def test_get_type_from_hostname(self):
        formatter = CarbonFormatter()
        self.assertEqual(formatter.get_type_from_hostname("devica99"),"ica")
        self.assertEqual(formatter.get_type_from_hostname("ask-be-swt01"),'be.swt')
        self.assertEqual(formatter.get_type_from_hostname("be-uplink-datacenter"),'uplink')

    def test_format_carbon_lines(self):
        formatter = CarbonFormatter()
        metric = {'metrics': [{'name': 'rta', 'value': '0.888000'},
                              {'name': 'pl', 'value': '0'}],
                  'timestamp': '1364909110',
                  'hostname': 'devica99',
                  'servicename': 'ping'}
        result = formatter.format('icinga', metric)
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0],
                'ica.devica99.icinga.ping.rta 0.888000 1364909110\n')
        self.assertEquals(result[1],
                'ica.devica99.icinga.ping.pl 0 1364909110\n')

    def test_format_metrics_with_spaces_to_carbon_lines(self):
        formatter = CarbonFormatter()
        metric = {'metrics': [{'name': 'rta', 'value': '0.888000'},
                              {'name': 'metric with spaces', 'value': '0'}],
                  'timestamp': '1364909110',
                  'hostname': 'devica99',
                  'servicename': 'system ping'}
        result = formatter.format('icinga', metric)
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0],
                'ica.devica99.icinga.system_ping.rta 0.888000 1364909110\n')
        self.assertEquals(result[1],
                'ica.devica99.icinga.system_ping.metric_with_spaces 0 1364909110\n')

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
                'super.my-super-uplink.icinga.system_ping.rta 0.888000 1364909110\n')
        self.assertEquals(result[1],
                'super.my-super-uplink.icinga.system_ping.metric_with_spaces 0 1364909110\n')

if __name__ == '__main__':
    unittest.main()
