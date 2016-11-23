import json
import httplib
import logging
from mussstat.database import *


class SafeSender(object):
    DB_NAME = 'safe_sender'
    TIMEOUT = 300
    protocol = 'http'

    def __init__(self, conf):
        self.host = conf['host']
        self.port = conf['port']
        self.path = conf['path']
        self.protocol = conf.get('protocol', 'http')
        self.db = FileDatabase(self.DB_NAME, [])

    def prepare_send_data(self, data):
        self.db.data.append(data)

    def after_send(self):
        self.db.save()

    def send_data(self, data):
        logging.info("Sending Data")
        self.prepare_send_data(data)
        if self.do_http_request(self.db.data):
            logging.info("Send Success")
            self.db.data = []
        else:
            logging.info("Send Fail")
        self.after_send()

    def do_http_request(self, data):
        try:
            if self.protocol == "https":
                conn = httplib.HTTPSConnection(self.host, self.port, timeout=self.TIMEOUT)
            else:
                conn = httplib.HTTPConnection(self.host, self.port, timeout=self.TIMEOUT)

            headers = {
                "Content-type": "text/json",
            }
            conn.request('POST', self.path, json.dumps(data), headers)
            resp = conn.getresponse()
            if resp.status == 200:
                return True
            else:
                logging.error("HTTP Status: %s\n%s" % (resp.status, resp.read()))
        except Exception as e:
            logging.exception(e)
        return False
