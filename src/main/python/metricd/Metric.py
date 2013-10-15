#!/usr/bin/env python

import ConfigParser
import argparse
import socket
import time
import re
import logging
import sys

from CarbonFormatter import CarbonFormatter
from IcingaParser import IcingaParser

class Metric:

	def __init__(self):
		self.non_decimal = re.compile(r'[^\d.]+')
		self.sock = socket.socket()
		self.carbonFormatter = CarbonFormatter()
		self.icingaParser = IcingaParser()
		self.reconnect_counter = 0

	def init_logger(self):
		logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S',level=logging.DEBUG)
		self.logger = logging.getLogger(__name__)

	def set_log_level(self, debug):
		if debug:
			level=logging.DEBUG
		else:
			level=logging.INFO
		logging.getLogger().setLevel(level)

	def parse_arguments(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('config', help="Config file for basic daemon configuration", type=str, default = "../../../../res/metricd.conf.sample")
		parser.add_argument('--debug', help="Activate debug output", action="store_true", default = True)
		self.args = parser.parse_args()

	def parse_config(self, config_file):
		try:
			with open(config_file):
				self.config = ConfigParser.RawConfigParser()
				self.config.read(config_file)
		except IOError as e:
			self.logger.error("Error opening config file: " + e.strerror)
			sys.exit(2)
		except Exception as e:
			self.logger.error("Error parsing config file: " + e.strerror)
			sys.exit(2)
			
	def get_config(self, head, key):
		try:
			return self.config.get(head,key)
		except:
			self.logger.error("Error reading config option for " + head + "." + key)
			sys.exit(2)

	def connection_init(self):
		try:
			host = self.get_config('graphite','carbon_server')
			port = int( self.get_config('graphite','carbon_port') )
			self.logger.info('Connecting to graphite host %s:%s',host, port)
			self.sock.connect( (host, port) )
			self.reconnect_counter = 0
			self.logger.info('Connected to graphite host %s:%s',host, port)

		except socket.gaierror as e:
			self.logger.error("Unable to connect to graphite (GAI Error): " + str(e))
			self.connection_reconnect()
		except socket.error as e:
			self.logger.error("Socket Error connecting to graphite: " + str(e))
			self.connection_reconnect()
		except Exception as e:
			self.logger.error("Unexpected error: " + str(e))
			self.connection_reconnect()

	def connection_reconnect(self):
		reconnect_count = int(self.get_config("graphite", "reconnect_count"))
		reconnect_interval = int(self.get_config("graphite", "reconnect_interval"))
		
		self.reconnect_counter = self.reconnect_counter + 1
		self.sock = socket.socket()
		self.logger.debug("Sleeping for " + str(reconnect_interval) + " sec until reconnect")
		time.sleep(reconnect_interval)
		
		if self.reconnect_counter < reconnect_count:
			self.logger.info("Reconnecting to graphite host")
			self.connection_init()
		else:
			self.logger.info("Exit after to many connection retries")
			sys.exit(1)

	def connection_close(self):
		self.logger.info('Closing connection to graphite host')
		self.sock.close()	

	def perfdata_read(self):
		self.connection_init()
		timestamp = int(time.time())
		self.logger.debug("Sending metrics with timestamp: " + str(timestamp))
		with open(self.get_config('icinga','perfdata_pipe'), 'r') as f:
			while True:
				try:
					line = f.readline()
					if line:
						self.logger.debug('In: ' + line.rstrip())
						formatted = self.carbonFormatter.format(self.get_config('graphite','metric_prefix'), self.icingaParser.parse(line))
						if formatted:
							for l in formatted:
								self.logger.debug('Out: ' + l.rstrip())
								self.sock.sendall(l)
				except socket.error as e:
					self.logger.error("Lost connection to graphite: " + str(e))
					self.connection_reconnect()
				except Exception as e:
					self.logger.error("Unexpected error: " + str(e))	
					self.connection_reconnect()

if __name__ == '__main__':
	metric = Metric()
	metric.init_logger()
	metric.parse_arguments()
	metric.parse_config(metric.args.config)
	metric.set_log_level(metric.args.debug)
	metric.perfdata_read()
	metric.connection_close()
	
