""""""
import os
import logging

# Simple logging configuration, an example output might be:
# 2013-06-03 15:07:55.740 p7470 {start_here.py:31} INFO - This is an example log message
LOG_FILE_NAME = "log.log"
# The date format is ISO 8601, format includes a decimal separator for
# milliseconds (not the default comma) as dateutil.parser cannot read the
# command but it can read the decimal separator (both are allowed in ISO 8601)
fmt = '%(asctime)s.%(msecs)d p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILE_NAME,
                    level=logging.DEBUG,
                    format=fmt, datefmt='%Y-%m-%d %H:%M:%S')
# note that it might be useful to use the ConcurrentLogHandler or
# RotatingLogHandler here (either require some more setup)

# environment variable for configuration
CONFIG_ENV_VAR = "CONFIG"


class ConfDev(object):
    """Configuration for development scenario"""
    name = "dev"

    def __init__(self):
        pass


class ConfDevWindows(object):
    """Example 2nd configuration, a development scenario on Windows"""
    name = "dev_windows"

    def __init__(self):
        pass

configurations = [ConfDev, ConfDevWindows]


def get(configuration=None):
    """Return a configuration based on name or environment variable"""
    if configuration is None:
        configuration = os.getenv(CONFIG_ENV_VAR)

    # look through the available configurations, find the
    # match and instantiate it
    for c in configurations:
        if c.name == configuration:
            conf = c()
            return conf

    assert False, "You must choose a configuration"
