import socket
from mussstat.database import *


def get_host_name():
    return socket.gethostname()


class BaseSampleCollector(object):
    DATE_FORMAT = "%Y-%m-%d %H:%M"
    DURATION = 300
    samples = {}

    def list_instances(self):
        raise Exception("Not Implements")

    def after_collect(self):
        pass

    def collect_host_samples(self, date):
        data = []
        hostname = get_host_name()
        date_str = date.strftime(self.DATE_FORMAT)
        for instance in self.list_instances():
            data.append(self.collect_instance_samples(hostname, instance, date_str))
        self.after_collect()
        return data

    def collect_instance_samples(self, hostname, instance, date_str):
        ret = {
            'instance': instance,
            'host': hostname,
            'date': date_str,
        }
        for name, func_name in self.samples.items():
            func = getattr(self, func_name)
            samples = func(instance)
            if samples is None:
                continue
            ret[name] = samples
        return ret

    def calculate_with_cache(self, cache, key, data, default=0):
        if key in cache.data:
            last = cache.data[key]
            cache.data[key] = data
            if data >= last:
                return data - last
            else:
                return default
        else:
            cache.data[key] = data
            return 0
