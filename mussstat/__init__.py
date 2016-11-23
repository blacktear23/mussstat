import os
import imp


def load_config():
    ret = {}
    file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/config/config.py"
    module = imp.load_source('config', file_path)
    for attr_name in dir(module):
        if attr_name.startswith("__"):
            continue
        value = getattr(module, attr_name)
        ret[attr_name.lower()] = value
    return ret
