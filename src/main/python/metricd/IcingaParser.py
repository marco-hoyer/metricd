#!/usr/bin/env python

import re
import logging
import string


class IcingaParser():
    def __init__(self):
        self.non_decimal = re.compile(r'[^\d.]+')
        self.logger = logging.getLogger(__name__)

        # filter for <something>|<something>|<something>|<some number>
        self.perfdata_pattern = re.compile(r'([a-zA-Z0-9]+=[0-9]+[;]*)+')

    def _strip_invalid_characters(self, raw_string):
        # this list equals string.punctuation but doesn't include underscores f.e. cause they are allowed
        exclude_list = set("!\"#$%&'()*+,./:;<=>?@[\]^`{|}~")
        clean_string = ''.join(character for character in raw_string if character not in exclude_list)
        return clean_string

    def _metric_string_is_valid(self, metric_string):
        if metric_string.count('|') == 3:
            return True
        else:
            return False

    def _perfdata_string_is_valid(self, perfdata_string):
        #perfdata_string = re.escape(perfdata_string)
        #print perfdata_string
        return self.perfdata_pattern.match(perfdata_string)

    def parse(self, raw_data):
        parsed_data = {}
        if not self._metric_string_is_valid(raw_data):
            self.logger.warn('Invalid perfdata format: ' + raw_data.rstrip())
            return None

        fields = raw_data.split('|')
        parsed_data['hostname'] = self._strip_invalid_characters(fields[0])
        parsed_data['servicename'] = self._strip_invalid_characters(fields[1])

        metrics_str = fields[2].split()
        metrics = []
        for metric_str in metrics_str:
            (name_with_value, separator, rest) = metric_str.partition(';')
            (name, separator, value_with_unit) = name_with_value.partition('=')
            metric = {}
            metric['name'] = self._strip_invalid_characters(name)
            metric['value'] = self.non_decimal.sub('', value_with_unit)
            # check if both, name and value, contain anything
            if not len(metric['name']) == 0 and not len(metric['value']) == 0:
                metrics.append(metric)
            else:
                self.logger.warn(
                    "Parsed invalid metric for: " + parsed_data['hostname'] + "." + parsed_data['servicename'] + "." +
                    metric['name'] + " (value was: " + metric['value'] + " )")

        parsed_data['metrics'] = metrics
        parsed_data['timestamp'] = fields[3].rstrip()
        self.logger.debug("Parsed Icinga perfdata: " + str(parsed_data))
        return parsed_data
