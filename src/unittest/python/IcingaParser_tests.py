import unittest
from metricd.IcingaParser import IcingaParser

class IcingaParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = IcingaParser()

    def test_parse(self):
        result = self.parser.parse('tuvdbs50|Ping|rta=0.888000ms;3000.000000;5000.000000;0.000000 pl=0%;80;100;0|1364909110')
        self.assertEquals(result.get('hostname'), 'tuvdbs50')
        self.assertEquals(result.get('servicename'), 'Ping')
        metrics = result.get('metrics')
        self.assertEquals(len(metrics), 2)
        self.assertEquals('rta', metrics[0].get('name'))
        self.assertEquals('0.888000', metrics[0].get('value'))
        self.assertEquals('pl', metrics[1].get('name'))
        self.assertEquals('0', metrics[1].get('value'))
        self.assertEquals(result.get('timestamp'), '1364909110')

    def test_parse_empty_line(self):
        result = self.parser.parse('')
        self.assertTrue(result is None)

    def test_parse_ipmi_check_perfdata(self):
        result = self.parser.parse('tuvesx29|IPMI Hardware Status|01-Inlet Ambient=16.00 02-CPU 1=40.00 03-CPU 2=40.00 04-DIMMs 1=30.00 05-DIMMs 2=33.00 06-HDD Max=35.00 07-Memory 1 1-6=29.00 08-Memory 2 1-6=35.00 09-IOH=54.00 10-Mezz Zone=38.00 11-CNA Zone=32.00 12-Chassis Exit=30.00 13-Chassis Exit=19.00|1393251634')
        self.assertEquals('tuvesx29', result.get('hostname'))
        self.assertEquals('IPMI Hardware Status', result.get('servicename'))
        metrics = result.get('metrics')

        self.assertEquals(len(metrics), 13)
        self.assertEquals('01-Inlet Ambient', metrics[0].get('name'))
        self.assertEquals('16.00', metrics[0].get('value'))
        self.assertEquals('02-CPU 1', metrics[1].get('name'))
        self.assertEquals('40.00', metrics[1].get('value'))

    def test_parse_perfdata_string(self):
        perfdata_string='a=0%;;;; a b=10.1%;10;20;30; metric=0,1'
        self.assertEqual([('a', '0'), (' a b', '10.1'), (' metric', '0,1')], self.parser._parse_perfdata_string(perfdata_string))

    def test_parse_perfdata_with_negative_values(self):
        perfdata_string='offset=-0.002528s;0.500000;0.800000;'
        self.assertEqual([('offset', '-0.002528')], self.parser._parse_perfdata_string(perfdata_string))

    def test_parse_perfdata_string_with_separators_without_values(self):
        perfdata_string='time=0.004983s;;10.000000;0.000000 size=206B;;;0'
        self.assertEqual([('time', '0.004983'), (' size', '206')], self.parser._parse_perfdata_string(perfdata_string))

    def test_parse_perfdata_string_with_special_characters_in_key(self):
        perfdata_string='my super_test-metric=0,1'
        self.assertEqual([('my super_test-metric', '0,1')], self.parser._parse_perfdata_string(perfdata_string))

    def test_parse_perfdata_string_with_number_in_key(self):
        perfdata_string='numacthstchecks5m=643'
        self.assertEqual([('numacthstchecks5m', '643')], self.parser._parse_perfdata_string(perfdata_string))

    def test_parse_perfdata_string_without_last_value(self):
        perfdata_string='offset=-0.004035s;0.500000;0.800000;'
        self.assertEqual([('offset', '-0.004035')], self.parser._parse_perfdata_string(perfdata_string))

    def test_parse_perfdata_string_with_snmp_oid(self):
        perfdata_string='iso.3.6.1.4.1.3375.2.1.14.1.1.0=2'
        self.assertEqual([('iso.3.6.1.4.1.3375.2.1.14.1.1.0', '2')], self.parser._parse_perfdata_string(perfdata_string))

    def test_parse_perfdata_string_with_invalid_string(self):
        perfdata_string='a=a'
        self.assertEqual([], self.parser._parse_perfdata_string(perfdata_string))

    def test_parse_perfdata_string_with_empty_string(self):
        perfdata_string='a=0%;;;; ab'
        self.assertEqual([('a', '0')], self.parser._parse_perfdata_string(perfdata_string))

    def test_parse_perfdata_string_with_invalid_substring(self):
        perfdata_string=''
        self.assertEqual([], self.parser._parse_perfdata_string(perfdata_string))

    def test_clean_string__with_dots(self):
        self.assertEquals('tuvdbs50rzis', self.parser._strip_invalid_characters(".tuvdbs.50.rz.is"))

    def test_metric_string_is_valid(self):
        metric_string = "hoaweb01|Application Status|response_time=0.001|1393251634"
        #metric_string = "a|b|c|1"
        self.assertTrue(self.parser._icinga_output_string_is_valid(metric_string))

    def test_metric_string_is_invalid(self):
        metric_string = "hoaweb01|Application Status|response_time=0.001"
        #metric_string = "a|b|c|1"
        self.assertFalse(self.parser._icinga_output_string_is_valid(metric_string))

    def test_clean_string_with_special_characters(self):
        self.assertEquals('active_service_checks', self.parser._strip_invalid_characters("active_service_checks"))

    def test_validate_metrics_count(self):
        raw_data = "a=1"
        metrics = ['']
        self.assertTrue(self.parser._validate_metrics_count(raw_data, metrics))

    def test_validate_metrics_count_without_metrics(self):
        raw_data = ""
        metrics = []
        self.assertTrue(self.parser._validate_metrics_count(raw_data, metrics))

    def test_validate_metrics_count_with_multiple_metrics(self):
        raw_data = "a=0 c=1 e=2"
        metrics = ['','','']
        self.assertTrue(self.parser._validate_metrics_count(raw_data, metrics))

    def test_validate_metrics_count_with_mismatch(self):
        raw_data = "a=0 c=1 e=2"
        metrics = ['','']
        self.assertFalse(self.parser._validate_metrics_count(raw_data, metrics))

if __name__ == '__main__':
    unittest.main()
