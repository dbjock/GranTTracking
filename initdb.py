# PURPOSE: Create Data/test.db from scripts
from pathlib import Path
import logging
import os
import sys
from datetime import datetime

# App specific required
from GranT import gtdbV2 as gtdb
from GranT import gtcfg

gtPath = Path.cwd()
gtScripts = gtPath / 'Scripts'

gtLogs = Path(gtcfg.logcfg['logDir'])
logfile = gtLogs / \
    f"test-initdb-{datetime.now().strftime('%Y-%j-%H%M%S')}.log"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
simpleFormat = logging.Formatter(
    ' %(levelname)-8s:%(name)s.%(funcName)s: %(message)s')
detailFormat = logging.Formatter(
    '%(asctime)s %(levelname)-8s:%(name)s.%(funcName)s: %(message)s')

# Log Handlers
conHandler = logging.StreamHandler()
conHandler.setFormatter(simpleFormat)
conHandler.setLevel(logging.CRITICAL)
logger.addHandler(conHandler)

fileHandler = logging.FileHandler(logfile)
fileHandler.setFormatter(detailFormat)
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)
# ----------------------------
dbFile = Path(gtcfg.dbcfg['dbFile'])
print(f"Logging to {logfile}")
print(f"This will drop and create tables in {dbFile}")
msg = f"Database init (Drop, create, populate database) {dbFile}"
print(msg)
logger.info(msg)
dbConn1 = gtdb.GTdb(name=dbFile)
dbConn1.initDB(scriptPath=f'{gtScripts}')
msg = f"Work completed on {dbFile}"
print(msg)
logger.info(msg)
