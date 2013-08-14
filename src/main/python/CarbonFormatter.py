#!/usr/bin/env python

import logging

class CarbonFormatter():

	def __init__(self):
                logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
                self.logger = logging.getLogger('CarbonFormatter')

        def format(self,parsed_data):
		if parsed_data is None:
			self.logger.warn('Received invalid data')
			return None
                formatted_data = []
                for metric in parsed_data['metrics']:
			typ = parsed_data['hostname']
			typ = typ[3:-2]
                        formatted_data.append('%s.%s.%s.%s %s %s\n' % (typ.lower(), parsed_data['hostname'].lower(), parsed_data['servicename'].lower(), metric['name'].lower(), metric['value'], parsed_data['timestamp']))
                return formatted_data
