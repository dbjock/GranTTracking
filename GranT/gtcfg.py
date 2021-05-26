import logging
import configparser
import os

logger = logging.getLogger(__name__)


def load_config(cfgFile):
    """
    Load configuraton file and store in sectional dict\n
    cfgFile : Configuration file to open (requried)\n
    """
    config.read(cfgFile)
    dbcfg['dbFile'] = config.get('database', 'dbfile', fallback=None)
    logcfg['logDir'] = config.get('logging', 'logDir', fallback=None)
    logcfg['level'] = config.get('logging', 'level', fallback="INFO")


dbcfg = dict()
logcfg = dict()
config = configparser.ConfigParser()
load_config('./GTTracking.conf')
