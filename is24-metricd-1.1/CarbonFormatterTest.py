import unittest
from CarbonFormatter import CarbonFormatter

class CarbonFormatterTest(unittest.TestCase):

	def test_formats_carbon_lines(self):
		formatter = CarbonFormatter()
		metric = {'metrics': [{'name': 'rta', 'value': '0.888000'}, {'name': 'pl', 'value': '0'}], 'timestamp': '1364909110', 'hostname': 'tuvdbs50', 'servicename': 'ping'}
		result = formatter.format(metric)
		self.assertEquals(len(result), 2)
		self.assertEquals(result[0], 'dbs.tuvdbs50.ping.rta 0.888000 1364909110\n')
		self.assertEquals(result[1], 'dbs.tuvdbs50.ping.pl 0 1364909110\n')
		
if __name__ == '__main__':
	unittest.main()
