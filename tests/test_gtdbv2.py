# python -m unittest Tests.test_gtdbv2
import unittest
from pathlib import Path
import logging
import os

# App Testing requirements
from GranT import gtdbV2
from GranT import gtclasses as GTClass

# logging.basicConfig(level=logging.DEBUG, filename='test.log', filemode='w')

logger = logging.getLogger()
handler = logging.StreamHandler()
conFormat = logging.Formatter(
    ' %(name)-16s %(levelname)-8s %(message)s')
handler.setFormatter(conFormat)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

fileHandler = logging.FileHandler('testing.log')
fileFormat = logging.Formatter(
    '%(asctime)s %(levelname)-8s:%(name)s.%(funcName)s: %(message)s')

fileHandler.setFormatter(fileFormat)
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

logger.setLevel(logging.DEBUG)

print("Logging test test.log. You may see warnings below which are normal")


class TestMfg(unittest.TestCase):
    gtPath = Path.cwd()
    gtData = gtPath / 'Data'
    gtScripts = gtPath / 'Scripts'

    def test_mfgAdd(self):
        logger.info("==== BEGIN Add Manufacure add")
        logger.info("Add Manufacture with non existing name")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testMfg = dbConn1.getMfg(key='mfgId', value=1)
        testMfg.mfgName = "NEW Manufacture"
        result = dbConn1.addMfg(testMfg)
        self.assertEqual(result[0], 0)

        logger.info("Add Manufacture with existing name")
        testMfg = dbConn1.getMfg(key='mfgId', value=1)
        testMfg.mfgName = "Honda"
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)

        logger.info("Add Manufacture with Null/None Country id")
        testMfg = dbConn1.getMfg(key='mfgId', value=1)
        testMfg.mfgName = "Another new one that should fail"
        testMfg.country.id = None
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)

        del dbConn1
        logger.info(f"====END Add Manufacure add\n")

    def test_mfgGet(self):
        logger.info("==== BEGIN Get/read Manufacture")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')

        logger.info("Get Manufacture by mfgid")
        mfgId = 4
        testMfg = dbConn1.getMfg(value=mfgId)
        self.assertEqual(testMfg.id, mfgId)

        logger.info("Get Manufacture by name")
        mfgName = 'honda'
        testMfg = dbConn1.getMfg(key='Make', value=mfgName)
        self.assertEqual(testMfg.mfgName.upper(), mfgName.upper())
        self.assertNotEqual(testMfg.id, 0)

        logger.info("Get non exist Manfuacture by id")
        mfgId = 99999
        testMfg = dbConn1.getMfg(value=mfgId)
        self.assertEqual(testMfg.id, 0)

        logger.info("Get non exist Manfuacture by name")
        mfgName = 'ZZINoExist'
        testMfg = dbConn1.getMfg(key='Make', value=mfgName)
        self.assertEqual(testMfg.id, 0)

        del dbConn1
        logger.info(f"==== END Get/read Manufacture\n")

    def test_mfgDel(self):
        logger.info("==== BEGIN Delete Manufacture")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')

        logging.info("Delete Manufacture that does not exist")
        mfgId = 999999
        result = dbConn1.delMfg(mfgId)
        # Sqlite.. the delete works, even if record doesn't exist.
        self.assertEqual(result[0], 0)

        logging.info("Delete Manufacture that exist")
        mfgId = 1
        result = dbConn1.delMfg(mfgId)
        self.assertEqual(result[0], 0)

        del dbConn1
        logger.info(f"==== END Delete Manufacture\n")

    def test_mfgUpdate(self):
        logger.info("==== BEGIN UPDATE Manufacture")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')

        logging.info("Change/Update Manufacture Name.")
        orgMfg = dbConn1.getMfg(value=1)
        updateMfg = orgMfg
        updateMfg.mfgName = "MY new NAME"
        result = dbConn1.updateMfg(updateMfg)
        self.assertEqual(result[0], 0)

        logging.info("Change Country null on Manufacture.")
        orgMfg = dbConn1.getMfg(value=4)
        updateMfg = orgMfg
        updateMfg.country.id = None
        result = dbConn1.updateMfg(updateMfg)
        self.assertNotEqual(result[0], 0)

        logging.info("Testing change with Mfgid not in database.")
        orgMfg = dbConn1.getMfg(value=14)
        updateMfg = orgMfg
        updateMfg.id = 99999
        result = dbConn1.updateMfg(updateMfg)
        self.assertNotEqual(result[0], 0)

        del dbConn1
        logger.info(f"==== END UPDATE Manufacture\n")
