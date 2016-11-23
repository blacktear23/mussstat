import os
import pickle
import logging


class FileDatabase(object):
    DB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/db"

    def __init__(self, name, default=None):
        self.name = name
        self.filename = "%s/%s.db" % (self.DB_PATH, name)
        self.data = None
        self.load(default)

    def load(self, default=None):
        if not os.path.exists(self.filename):
            self.data = default
            return self.data
        try:
            with open(self.filename, "r") as fp:
                self.data = pickle.load(fp)
                return self.data
        except Exception as e:
            logging.exception(e)
            self.data = default
            return self.data

    def save(self):
        with open(self.filename, "w+") as fp:
            pickle.dump(self.data, fp)
