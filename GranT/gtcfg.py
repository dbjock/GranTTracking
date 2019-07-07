import logging
import configparser
import os

def load_config(cfgFile):
    """
    Load configuraton file and store in sectional dict\n
    cfgFile : Configuration file to open (requried)\n
    """
    config.read(cfgFile)
    dbcfg['dbFile'] = config.get('database','dbfile',fallback=None)

logger = logging.getLogger(__name__)
dbcfg = dict()
config = configparser.ConfigParser()
load_config('./GTTracking.conf')
