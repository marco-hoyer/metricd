#!/usr/bin/env python

import re
import logging
import string

class IcingaParser():

	def __init__(self):
		self.non_decimal = re.compile(r'[^\d.]+')
		self.logger = logging.getLogger(__name__)
		
	def cleanString(self, raw_string):
		# this list equals string.punctuation but doesn't include underscores f.e. cause they are allowed
		exclude = set("!\"#$%&'()*+,./:;<=>?@[\]^`{|}~")
		clean_string = ''.join(character for character in raw_string if character not in exclude)
		return clean_string.lower()

	def parse(self,raw_data):
		parsed_data = {}
		fields = raw_data.split('|')
		if len(fields) != 4:
			self.logger.warn('Invalid perfdata format: ' + raw_data.rstrip())
			return None
		parsed_data['hostname'] = self.cleanString(fields[0])
		parsed_data['servicename'] = self.cleanString(fields[1])
		
		metrics_str = fields[2].split()
		metrics = []
		for metric_str in metrics_str:
			(name_with_value, separator, rest) = metric_str.partition(';')
			(name, separator, value_with_unit) = name_with_value.partition('=')
			metric = {}
			metric['name'] = self.cleanString(name)
			metric['value'] = self.non_decimal.sub('', value_with_unit)
			# check if both, name and value, contain anything
			if not len(metric['name']) == 0 and not len(metric['value']) == 0:
				metrics.append(metric)
			else:
				self.logger.warn("Parsed invalid metric for: " + parsed_data['hostname'] + "." + parsed_data['servicename'] + "." + metric['name'] + " (value was: " + metric['value'] + " )")

		parsed_data['metrics'] = metrics
		parsed_data['timestamp'] = fields[3].rstrip()
		self.logger.debug("Parsed Icinga perfdata: " + str(parsed_data))
		return parsed_data
		
