#!/usr/bin/env python

import re
import logging


class IcingaParser():
    def __init__(self):
        self.non_decimal = re.compile(r'[^\d.]+')
        self.logger = logging.getLogger(__name__)
        self.perfdata_pattern = re.compile(r'([a-zA-Z0-9\s\-\_]+)=(([0-9]+)([\.|,]{,1})([0-9]*))([a-zA-Z]*|%)(([;](([0-9]+)([\.|,]{,1})([0-9]*))){,4})')

    def _strip_invalid_characters(self, raw_string):
        # this list equals string.punctuation but doesn't include underscores f.e. cause they are allowed
        exclude_list = set("!\"#$%&'()*+,./:;<=>?@[\]^`{|}~")
        clean_string = ''.join(character for character in raw_string if character not in exclude_list)
        return clean_string.strip()

    def _icinga_output_string_is_valid(self, metric_string):
        if metric_string.count('|') == 3:
            return True
        else:
            return False

    def _metric_is_valid(self, metric):
        if not len(metric['name']) == 0 and not len(metric['value']) == 0:
            return True
        else:
            return False

    def _parse_perfdata_string(self, perfdata_string):
        parsed_perfdata = re.findall(self.perfdata_pattern, perfdata_string)

        perfdata_list = []
        for item in parsed_perfdata:
            perfdata_list.append((item[0], item[1]))
        return perfdata_list

    def parse(self, raw_data):

        parsed_data = {}
        if not self._icinga_output_string_is_valid(raw_data):
            self.logger.warn('Invalid perfdata format: ' + raw_data.rstrip())
            return None

        raw_data_fields = raw_data.split('|')
        parsed_data['hostname'] = self._strip_invalid_characters(raw_data_fields[0])
        parsed_data['servicename'] = self._strip_invalid_characters(raw_data_fields[1])

        # separate perfdata output from raw_data and parse metrics from it
        perfdata_string = raw_data_fields[2]
        parsed_metrics = self._parse_perfdata_string(perfdata_string)

        metrics = []
        for parsed_metric in parsed_metrics:
            metric = {}
            metric['name'] = self._strip_invalid_characters(parsed_metric[0])
            metric['value'] = self.non_decimal.sub('', parsed_metric[1])
            if self._metric_is_valid(metric):
                metrics.append(metric)
            else:
                self.logger.warn(
                    "Parsed invalid metric for: " + parsed_data['hostname'] + "." + parsed_data['servicename'] + "." +
                    metric['name'] + " (value was: " + metric['value'] + " )")

        parsed_data['metrics'] = metrics
        parsed_data['timestamp'] = raw_data_fields[3].rstrip()
        self.logger.debug("Parsed Icinga perfdata: " + str(parsed_data))
        return parsed_data
