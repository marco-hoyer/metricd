#!/usr/bin/env python

import re
import logging

class IcingaParser():

	def __init__(self):
		self.non_decimal = re.compile(r'[^\d.]+')
                logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
                self.logger = logging.getLogger('IcingaParser')

	def parse(self,raw_data):
		parsed_data = {}
		fields = raw_data.split('|')
		if len(fields) != 4:
			self.logger.warn('Invalid perfdata format: %s' % raw_data)
			return None
		parsed_data['hostname'] = fields[0]
		parsed_data['servicename'] = fields[1].lower()
		
		metrics_str = fields[2].split()
		metrics = []
		for metric_str in metrics_str:
			(name_with_value, separator, rest) = metric_str.partition(';')
			(name, separator, value_with_unit) = name_with_value.partition('=')
			metric = {}
			metric['name'] = name
			metric['value'] = self.non_decimal.sub('', value_with_unit)
			metrics.append(metric)

		parsed_data['metrics'] = metrics
		parsed_data['timestamp'] = fields[3].rstrip()
		return parsed_data
		
