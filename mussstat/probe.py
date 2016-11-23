import json
import logging
from datetime import datetime
from mussstat.base import *
from mussstat.safesend import *
import requests


class BaseProcessor(object):
    def __init__(self, conf):
        self.conf = conf
        self.date = datetime.now()
        self.sender = SafeSender(conf)

    def get_collector(self):
        raise Exception("Not Implements")

    def run(self):
        logging.info("Collector %s Collecting Samples" % (self.__class__.__name__))
        collector = self.get_collector()
        data = collector.collect_host_samples(self.date)
        self.sender.send_data(data)


class MussProcessor(BaseProcessor):
    def get_collector(self):
        return MussSampleCollector(self.conf)


class MussSampleCollector(BaseSampleCollector):
    samples = {
        'bandwidth': 'collect_bandwidth',
        'connection': 'collect_connection',
    }

    def __init__(self, config):
        self.config = config
        self.bw_cache = FileDatabase("muss-bw-cache", {})
        self.connection_cache = FileDatabase("muss-conn-cache", {})
        self.collected_data = self.request_muss_server()

    def request_muss_server(self):
        try:
            msg = requests.get(self.config['muss_server_url']).text
            return json.loads(msg)
        except Exception as e:
            logging.exception(e)
            return {}

    def after_collect(self):
        self.bw_cache.save()
        self.connection_cache.save()

    def list_instances(self):
        return self.collected_data.keys()

    def collect_bandwidth(self, instance):
        data = self.collected_data[instance]
        flow_out_key = "%s-out" % instance
        flow_in_key = "%s-in" % instance
        flow_out = self.calculate_with_cache(self.bw_cache, flow_out_key, data['BytesOut'], data['BytesIn'])
        flow_in = self.calculate_with_cache(self.bw_cache, flow_in_key, data['BytesIn'], data['BytesIn'])
        return {'inbound': flow_in, 'outbound': flow_out}

    def collect_connection(self, instance):
        data = self.collected_data[instance]
        conn = self.calculate_with_cache(self.connection_cache, str(instance), data['Connections'], data['Connections'])
        return {"value": (int(conn) / self.DURATION)}
