import unittest
from metricd.CarbonFormatter import CarbonFormatter


class CarbonFormatterTest(unittest.TestCase):

    def test_clean_string(self):
        formatter = CarbonFormatter()
        self.assertEquals("ping", formatter.clean_string("ping"))
        self.assertEquals("system_ping", formatter.clean_string("system ping"))
        self.assertEquals("iso_3_6_1_4_1_3375_2_1_14_1_1_0", formatter.clean_string("iso.3.6.1.4.1.3375.2.1.14.1.1.0"))
        self.assertEquals("system", formatter.clean_string("System"))
        self.assertEquals("pl", formatter.clean_string("PL"))
        self.assertEquals("", formatter.clean_string(""))
        self.assertEquals("a_b_c", formatter.clean_string(" a b c "))
        self.assertEquals("", formatter.clean_string(" "))

    def test_get_type_from_hostname(self):
        formatter = CarbonFormatter()
        self.assertEqual("ica", formatter.get_type_from_hostname("devica99"))
        self.assertEqual('be-swt', formatter.get_type_from_hostname("ask-be-swt01"))
        self.assertEqual('uplink', formatter.get_type_from_hostname("be-uplink-datacenter"))
        self.assertEqual('fe-vtm', formatter.get_type_from_hostname("ask-fe-vtm12"))

    def test_get_short_hostname(self):
        formatter = CarbonFormatter()
        self.assertEqual('ask-fe-vtm12', formatter._get_short_hostname("ask-fe-vtm12.fe.dev.lan"))
        self.assertEqual('devica99', formatter._get_short_hostname("devica99.local"))
        self.assertEqual('devica99', formatter._get_short_hostname("devica99"))
        self.assertEqual('', formatter._get_short_hostname(""))

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

    def test_metric_with_negative_value(self):
        formatter = CarbonFormatter()
        metric = {'metrics': [{'name': 'offset', 'value': '-0.888000'}],
                  'timestamp': '1364909110',
                  'hostname': 'my-super-host',
                  'servicename': 'ntp_time'}
        result = formatter.format('icinga', metric)
        self.assertEquals(len(result), 1)
        self.assertEquals('super.my-super-host.icinga.ntp_time.offset -0.888000 1364909110\n', result[0])

    def test_metric_with_network_device_hostname(self):
        formatter = CarbonFormatter()
        metric = {'metrics': [{'name': 'offset', 'value': '-0.888000'}],
                  'timestamp': '1364909110',
                  'hostname': 'ask-fe-vtm12.fe.dev.lan',
                  'servicename': 'ntp_time'}
        result = formatter.format('icinga', metric)
        self.assertEquals(len(result), 1)
        self.assertEquals('fe-vtm.ask-fe-vtm12.icinga.ntp_time.offset -0.888000 1364909110\n', result[0])

if __name__ == '__main__':
    unittest.main()
