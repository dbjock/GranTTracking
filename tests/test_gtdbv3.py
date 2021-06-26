# python -m unittest tests.test_gtdbv3
# If you want to run specific tests:
# python -m unittest tests.test_gtdbv3.Class.method
import unittest
from pathlib import Path
import logging
import os
import sys
from datetime import datetime

# App Testing requirements
from GranT import gtdbV3
from GranT import GTClasses as GT

_gtPath = Path.cwd()
_gtLogs = _gtPath / 'Logs'
_gtScripts = _gtPath / 'Scripts'
_logfile = _gtLogs / f"Testing-{datetime.now().strftime('%Y%j-%H%M%S')}.log"

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

fileHandler = logging.FileHandler(_logfile)
fileHandler.setFormatter(detailFormat)
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

print(f"Logging to {_logfile}")


class TestCountry(unittest.TestCase):
    def test_getCountry(self):
        logger.info("==== BEGIN Get Country")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Get Country : Existing Country by id")
        testVal = 1
        logger.info(f"Country ID = {testVal}")
        xCountry = gtdbV3.getCountry(d1, testVal)
        logger.info(f"result is {xCountry}")
        self.assertEqual(
            xCountry.id, 1, "Failed Get Country : Existing Country by id. should be countryid 1")

        logger.info("Get Country : Non Existing Country by id")
        testVal = 9999
        logger.info(f"Country ID = {testVal}")
        xCountry = gtdbV3.getCountry(d1, testVal)
        logger.info(f"result is {xCountry}")
        self.assertEqual(
            xCountry.id, 0, "Failed Get Country : Non Existing Country by id. should be countryid 0")


class TestCircuit(unittest.TestCase):
    def test_getCircuit(self):
        logger.info("==== BEGIN Get Circuit")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Get Circuit : Existing Circuit by ID")
        testVal = 1
        logger.info(f"Circuit ID = {testVal}")
        xCircuit = gtdbV3.getCircuit(d1, key='id', value=testVal)
        logger.info(f"result is {xCircuit}")
        self.assertEqual(
            xCircuit.id, 1, "Failed Get Circuit : Existing Circuit by ID. should be circuitid 1")

        logger.info("Get Circuit : Non Existing Circuit by ID")
        testVal = 999
        logger.info(f"Circuit ID = {testVal}")
        xCircuit = gtdbV3.getCircuit(d1, key='id', value=testVal)
        logger.info(f"result is {xCircuit}")
        self.assertEqual(
            xCircuit.id, 0, "Failed Get Circuit : Non Existing Circuit by ID. Should be circuitid 0")

        logger.info("Get Circuit by name - Exist")
        testVal = "Dirt / Snow"
        logger.info(f"Circuit name = {testVal}")
        xCircuit = gtdbV3.getCircuit(d1, key='name', value=testVal)
        logger.info(f"result is {xCircuit}")
        self.assertNotEqual(xCircuit.id, 0)

        logger.info("Get Circuit by name - Non Exist")
        testVal = "I donot exist"
        logger.info(f"Circuit name = {testVal}")
        xCircuit = gtdbV3.getCircuit(d1, key='id', value=testVal)
        logger.info(f"result is {xCircuit}")
        self.assertEqual(xCircuit.id, 0)

        logger.info("==== END Get Circuit")
