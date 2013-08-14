#!/usr/bin/env python

import os
import ConfigParser
import argparse
import socket
import time
import thread
import re
import logging

import CarbonFormatter
import IcingaParser

class Metric:

	def __init__(self):
		self.non_decimal = re.compile(r'[^\d.]+')
		self.sock = socket.socket()
		self.carbonFormatter = CarbonFormatter.CarbonFormatter()
		self.icingaParser = IcingaParser.IcingaParser()

	def init_logger(self):
		logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
                self.logger = logging.getLogger('Metric')
		self.logger.info('logger initialization completed')

	def parse_arguments(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('config_file')
		self.args = parser.parse_args()

	def parse_config(self, config_file):
		self.config = ConfigParser.RawConfigParser()
		if config_file:
			# use config file parameter (for unit testing)
			self.config.read(config_file)
		else:
			# use config file argument (for normal runtime usage)
			self.config.read(self.args.config_file)

	def connection_init(self):
		try:
			self.logger.info('Connecting to graphite host %s:%s',self.config.get('graphite','carbon_server'),self.config.get('graphite','carbon_port'))
			self.sock.connect((self.config.get('graphite','carbon_server'), self.config.getint('graphite','carbon_port')))
		except socket.gaierror as e:
			self.logger.error("Unable to connect to graphite: %s" % e.strerror)
		except:
			self.logger.error("Unexpected error: %s" % sys.exc_info()[0])

	def connection_close(self):
		self.logger.info('Closing connection to graphite host')
		self.sock.close()

	def perfdata_read(self):
		timestamp = int(time.time())
		with open(self.config.get('icinga','perfdata_pipe'), 'r') as f:
			while True:
				try:
					line = f.readline()
					if line:
						self.logger.debug('in: %s' % line)
						formatted = self.carbonFormatter.format(self.config.get('graphite','metric_prefix'), self.icingaParser.parse(line))
						if formatted:
							for l in formatted:
								self.logger.debug('out: %s' % l)
								self.sock.sendall(l)
				except socket.error as e:
					self.logger.error("Lost connection to graphite: %s" % e.strerror)
					self.connection_init()
				except:
					self.logger.error("Unexpected error: %s" % sys.exc_info()[0])
		
if __name__ == '__main__':
	metric = Metric()
	metric.parse_arguments()
	metric.init_logger()
	metric.parse_config(None)
	metric.connection_init()
	metric.perfdata_read()
	metric.connection_close()
