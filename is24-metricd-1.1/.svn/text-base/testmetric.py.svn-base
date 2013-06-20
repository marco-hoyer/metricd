import unittest
from metric import Metric

class TestMetric(unittest.TestCase):

	def test_parses_hostname(self):
		metric = Metric()		
		result = metric.parse('tuvdbs50|Ping|rta=0.888000ms;3000.000000;5000.000000;0.000000 pl=0%;80;100;0|1364909110')
		self.assertEquals(result.get('hostname'), 'tuvdbs50')

	def test_parses_servicename(self):
		metric = Metric()
		result = metric.parse('tuvdbs50|Ping|rta=0.888000ms;3000.000000;5000.000000;0.000000 pl=0%;80;100;0|1364909110')
		self.assertEquals(result.get('servicename'), 'ping')

	def test_parses_metrics(self):
		metric = Metric()
		result = metric.parse('tuvdbs50|Ping|rta=0.888000ms;3000.000000;5000.000000;0.000000 pl=0%;80;100;0|1364909110')
		metrics = result.get('metrics')
		self.assertEquals(len(metrics), 2)
		self.assertEquals(metrics[0].get('name'), 'rta')
		self.assertEquals(metrics[0].get('value'), '0.888000')
                self.assertEquals(metrics[1].get('name'), 'pl')
                self.assertEquals(metrics[1].get('value'), '0')

	def test_parses_timestamp(self):
                metric = Metric()
                result = metric.parse('tuvdbs50|Ping|rta=0.888000ms;3000.000000;5000.000000;0.000000 pl=0%;80;100;0|1364909110')
		self.assertEquals(result.get('timestamp'), '1364909110')

	def test_creates_carbon_lines(self):
		metric = Metric()
		result = metric.format(metric.parse('tuvdbs50|Ping|rta=0.888000ms;3000.000000;5000.000000;0.000000 pl=0%;80;100;0|1364909110'))
		self.assertEquals(len(result), 2)
		self.assertEquals(result[0], 'tuvdbs50.ping.rta 0.888000 1364909110\n')
		self.assertEquals(result[1], 'tuvdbs50.ping.pl 0 1364909110\n')
		

if __name__ == '__main__':
	unittest.main()
