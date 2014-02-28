#!/usr/bin/env python

import logging
import re


class CarbonFormatter():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.default_hostname_pattern = re.compile(r"[A-Za-z]{6}[0-9]{2}")
        self.network_device_pattern = re.compile(r"[A-Za-z]{3}-[A-Za-z]{2}-[A-Za-z]{3}[0-9]{2}")
        self.generic_device_pattern = re.compile(r"[A-Za-z0-9]*-[A-Za-z0-9]*-[A-Za-z0-9]*")

    def clean_string(self, string):
        string = "_".join(string.split('.')).lower()
        string = "_".join(string.split()).lower()
        return string


    def get_type_from_hostname(self, hostname):
        if self.default_hostname_pattern.match(hostname):
            return hostname[3:-2]
        elif self.network_device_pattern.match(hostname):
            return hostname[4:6] + '.' + hostname[-5:-2]
        elif self.generic_device_pattern.match(hostname):
            return hostname.split('-')[1]
        else:
            return ''

    def format(self, metric_prefix, parsed_data):
        if parsed_data is None:
            return None
        formatted_data = []
        for metric in parsed_data['metrics']:
            self.logger.debug("Writing metric to graphite: " + str(metric))

            metric_string = '%s.%s.%s.%s.%s %s %s\n' % (
                self.clean_string(self.get_type_from_hostname(parsed_data['hostname'])),
                self.clean_string(parsed_data['hostname']),
                self.clean_string(metric_prefix),
                self.clean_string(parsed_data['servicename']),
                self.clean_string(metric['name']),
                metric['value'],
                parsed_data['timestamp'])
            formatted_data.append(metric_string.strip('.'))
        return formatted_data
