#!/usr/bin/env python

import logging
import re


class CarbonFormatter():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.default_hostname_pattern = re.compile(r"[A-Za-z]{6}[0-9]{2}")

    def convert_string(self, string):
        return "_".join(string.split()).lower()


    def get_type_from_hostname(self, hostname):
        if self.default_hostname_pattern.match(hostname):
            return hostname[3:-2]
        else:
            return ""

    def format(self, metric_prefix, parsed_data):
        if parsed_data is None:
            return None
        formatted_data = []
        for metric in parsed_data['metrics']:
            self.logger.debug("Writing metric to graphite: " + str(metric))
            typ = self.get_type_from_hostname(parsed_data['hostname'])
            metric_string = '%s.%s.%s.%s.%s %s %s\n' % (
                self.convert_string(typ), self.convert_string(parsed_data['hostname']), self.convert_string(metric_prefix),
                self.convert_string(parsed_data['servicename']), self.convert_string(metric['name']), metric['value'],
                parsed_data['timestamp'])
            formatted_data.append(metric_string.strip('.'))
        return formatted_data
