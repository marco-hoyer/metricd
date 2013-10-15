#!/usr/bin/env python

import logging

class CarbonFormatter():

	def __init__(self):
		self.logger = logging.getLogger(__name__)

	def convert_string(self, string):
		return "_".join( string.split() ).lower()

	def format(self,metric_prefix, parsed_data):
		if parsed_data is None:
			return None
		formatted_data = []
		for metric in parsed_data['metrics']:
			self.logger.debug("Writing metric to graphite: " + str(metric))
			typ = parsed_data['hostname']
			typ = typ[3:-2]
			formatted_data.append('%s.%s.%s.%s.%s %s %s\n' % (self.convert_string(typ), self.convert_string(parsed_data['hostname']), self.convert_string(metric_prefix), self.convert_string(parsed_data['servicename']), self.convert_string(metric['name']), metric['value'], parsed_data['timestamp']))
		return formatted_data
