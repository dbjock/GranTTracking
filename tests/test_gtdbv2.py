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
        logger.info(
            "==== BEGIN Add Manufacture (Must have unique name, and a country)")
        countryExist = GTClass.Country(
            cntryID=235, cntryName='United Kingdom of Great Britain and Northern Ireland', alpha2='GB', alpha3='GBR', region='Europe')
        countryNonExist = GTClass.Country(
            cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None)
        countryNull = GTClass.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testMfg = GTClass.Manufacture(
            mfgid=0, mfgName='NEW Manufacture', countryObj=countryExist)
        result = dbConn1.addMfg(testMfg)
        self.assertEqual(result[0], 0)
        del dbConn1

        logger.info("Add Manufacture - Name: Existing, Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testMfg = GTClass.Manufacture(
            mfgid=0, mfgName='Honda', countryObj=countryExist)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Existing (all caps), Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testMfg = GTClass.Manufacture(
            mfgid=0, mfgName='HONDA', countryObj=countryExist)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testMfg = GTClass.Manufacture(
            mfgid=0, mfgName='NEW manufacture', countryObj=countryNonExist)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info("Add Manufacture - Name: Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testMfg = GTClass.Manufacture(
            mfgid=0, mfgName='Honda', countryObj=countryNull)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testMfg = GTClass.Manufacture(
            mfgid=0, mfgName='new Manufacture', countryObj=countryNull)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testMfg = GTClass.Manufacture(
            mfgid=0, mfgName='Another new one that should fail', countryObj=countryNonExist)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(f"====END Manufacture\n")

    def test_mfgGet(self):
        logger.info("==== BEGIN Get/read Manufacture")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')

        logger.info("Get Manufacture by id")
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


class TestTrack(unittest.TestCase):
    gtPath = Path.cwd()
    gtData = gtPath / 'Data'
    gtScripts = gtPath / 'Scripts'

    def test_trackAdd(self):
        logger.info(
            "==== BEGIN TEST Add Track (Must have unique name, country not required)")
        countryExist = GTClass.Country(
            cntryID=235, cntryName='United Kingdom of Great Britain and Northern Ireland', alpha2='GB', alpha3='GBR', region='Europe')
        countryNonExist = GTClass.Country(
            cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None)
        countryNull = GTClass.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)

        logger.info("Add Track - Name: Non-Existing, Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='New Track name', countryObj=countryExist)
        result = dbConn1.addTrack(testTrack)
        self.assertEqual(result[0], 0)
        del dbConn1

        logger.info("Add Track - Name: Existing, Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='Nurburgring', countryObj=countryExist)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)  # This record show not be saved
        del dbConn1

        logger.info(
            "Add Track - Name: Existing (all caps), Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='NURBURGRING', countryObj=countryExist)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)  # This record show not be saved
        del dbConn1

        logger.info("Add Track - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='New Track name', countryObj=countryNonExist)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)  # This record show not be saved
        del dbConn1

        logger.info("Add Track - Name: Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='Nurburgring', countryObj=countryNull)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)  # This record show not be saved
        del dbConn1

        logger.info("Add Track - Name: Non-Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='New Track Name', countryObj=countryNull)
        result = dbConn1.addTrack(testTrack)
        self.assertEqual(result[0], 0)

        logger.info("Add Track - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='New Track Name', countryObj=countryNonExist)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)  # This record show not be saved

        logger.info("==== END TEST Add Track")

    def test_trackGet(self):
        logger.info("==== BEGIN Get/read Track")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{self.gtScripts}')

        logger.info("Get a Track by the track id")
        testVal = 4
        testTrack = dbConn1.getTrack(value=testVal)
        self.assertEqual(testTrack.id, testVal)

        logger.info("Get a Track by name")
        testVal = 'Northern Isle Speedway'
        logger.info(f"Getting track by track name = {testVal}")
        testTrack = dbConn1.getTrack(key='track', value=testVal)
        self.assertEqual(testTrack.name, testVal)

        logger.info("Get non exist Track by id")
        testVal = 99999
        testTrack = dbConn1.getTrack(value=testVal)
        self.assertEqual(testTrack.id, 0)

        logger.info("Get non exist Track by name")
        testVal = 'NON exist track test'
        testTrack = dbConn1.getTrack(key='track', value=testVal)
        self.assertEqual(testTrack.id, 0)

        del dbConn1
        logger.info(f"==== END Get/read Track\n")
