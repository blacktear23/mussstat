#!/usr/bin/env python
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from mussstat import load_config
from mussstat.probe import *


def initialize_logging():
    log_file = os.path.dirname(os.path.abspath(__file__)) + "/log/mussstat.log"
    app_logger = logging.getLogger()
    handler = TimedRotatingFileHandler(log_file, "D", 1, 15)
    format = logging.Formatter('[%(asctime)s PID:%(process)d]%(levelname)s:%(message)s')
    handler.setFormatter(format)
    app_logger.addHandler(handler)
    app_logger.setLevel(logging.INFO)


def help():
    print "Usage: drone.py"


def main(args):
    initialize_logging()
    cfg = load_config()
    obj = MussProcessor(cfg)
    obj.run()


if __name__ == "__main__":
    args = sys.argv
    main(args)
