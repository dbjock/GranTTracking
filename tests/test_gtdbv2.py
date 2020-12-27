# python -m unittest Tests.test_gtdbv2
import unittest
from pathlib import Path
import logging
import os
import sys
from datetime import datetime

# App Testing requirements
from GranT import gtdbV2
from GranT import gtclasses as GTClass

_gtPath = Path.cwd()
_gtLogs = _gtPath / 'Logs'
_gtScripts = _gtPath / 'Scripts'
_gtData = _gtPath / 'Data'
_logfile = _gtLogs / f"Testing-{datetime.now().strftime('%Y%j%H%M%S')}.log"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Log formats
# simpleFormat = logging.Formatter(
#     ' %(name)-16s %(levelname)-8s %(message)s')
simpleFormat = logging.Formatter(
    ' %(levelname)-8s:%(name)s.%(funcName)s: %(message)s')
detailFormat = logging.Formatter(
    '%(asctime)s %(levelname)-8s:%(name)s.%(funcName)s: %(message)s')

# Log Handlers
conHandler = logging.StreamHandler()
conHandler.setFormatter(simpleFormat)
conHandler.setLevel(logging.INFO)
logger.addHandler(conHandler)


# fileHandler = logging.FileHandler(
#     _gtLogs / f"Testing-{datetime.now().strftime('%Y%j%H%M%S')}.log")
fileHandler = logging.FileHandler(_logfile)
fileHandler.setFormatter(detailFormat)
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

print(
    f"Logging to {_logfile}. You may see warnings below which are normal")


class TestMfg(unittest.TestCase):

    def test_mfg_add(self):
        """Test various adding a manufacture scenerios
        """
        logger.info(
            "==== BEGIN Add Manufacture (Requirements: Name is unique. Required to have a country)")
        countryExist = GTClass.Country(
            cntryID=235, cntryName='United Kingdom of Great Britain and Northern Ireland', alpha2='GB', alpha3='GBR', region='Europe')
        countryNonExist = GTClass.Country(
            cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None)
        countryNull = GTClass.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = GTClass.Manufacture(
            id=0, name='NEW Manufacture', countryObj=countryExist)
        result = dbConn1.mfg_add(testMfg)
        logger.info(f"result is {result}")
        self.assertEqual(
            result[0], 0, "Result should have been zero 0")
        del dbConn1

        logger.info("Add Manufacture - Name: Existing, Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = GTClass.Manufacture(
            id=0, name='Honda', countryObj=countryExist)
        result = dbConn1.mfg_add(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Existing (all caps), Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = GTClass.Manufacture(
            id=0, name='HONDA', countryObj=countryExist)
        result = dbConn1.mfg_add(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = GTClass.Manufacture(
            id=0, name='NEW manufacture', countryObj=countryNonExist)
        result = dbConn1.mfg_add(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info("Add Manufacture - Name: Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = GTClass.Manufacture(
            id=0, name='Honda', countryObj=countryNull)
        result = dbConn1.mfg_add(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = GTClass.Manufacture(
            id=0, name='new Manufacture', countryObj=countryNull)
        result = dbConn1.mfg_add(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = GTClass.Manufacture(
            id=0, name='Another new one that should fail', countryObj=countryNonExist)
        result = dbConn1.mfg_add(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

    def test_getMfg(self):
        logger.info("==== BEGIN Get/read Manufacture")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')

        logger.info("Get Manufacture by id")
        mfgId = 4
        testMfg = dbConn1.getMfg(value=mfgId)
        self.assertEqual(testMfg.id, mfgId)

        logger.info("Get Manufacture by name")
        mfgName = 'honda'
        testMfg = dbConn1.getMfg(key='Make', value=mfgName)
        self.assertEqual(testMfg.name.upper(), mfgName.upper())
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

    def test_mfg_delete(self):
        logger.info("==== BEGIN Delete Manufacture")

        logging.info("Delete Manufacture = Manufacture ID: Non Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgId = 999999
        result = dbConn1.mfg_delete(mfgId)
        # Sqlite.. the delete works, even if record doesn't exist.
        self.assertEqual(result[0], 0)
        del dbConn1

        logging.info("Delete Manufacture = Manufacture ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgId = 1
        result = dbConn1.mfg_delete(mfgId)
        self.assertEqual(result[0], 0)
        del dbConn1

        logger.info("==== END Delete Manufacture\n")

    def test_mfg_update(self):
        logger.info(
            "==== BEGIN UPDATE Manufacture (Assumpting Get manufacture works)")
        countryExist = GTClass.Country(
            cntryID=235, cntryName='', alpha2='', alpha3='', region='')
        countryNonExist = GTClass.Country(
            cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None)
        countryNull = GTClass.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)

        logging.info(
            "Update Manufacture: Name: Change, Country ID: No change.")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = dbConn1.getMfg(value=1)
        testMfg.name = "MY new NAME"
        result = dbConn1.mfg_update(testMfg)
        self.assertEqual(result[0], 0)
        del dbConn1

        logging.info(
            "Update Manufacture: Name: No Change, Country ID: Change to null.")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = dbConn1.getMfg(value=4)
        testMfg.country = countryNull
        result = dbConn1.mfg_update(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logging.info(
            "Update Manufacture: Name: Change, Country ID: No Change, Mfg ID: Non Existing.")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = dbConn1.getMfg(value=14)
        testMfg.id = 99999
        result = dbConn1.mfg_update(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logging.info(
            "Update Manufacture: Name: Change to Existing, Country ID: No change ")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        xMfg = dbConn1.getMfg(value=3)
        testMfg = dbConn1.getMfg(value=14)
        testMfg.name = xMfg.name
        result = dbConn1.mfg_update(testMfg)
        self.assertNotEqual(result[0], 0)  # Should save
        del dbConn1

        logging.info(
            "Update Manufacture: Name: No change, Country ID: Change to Non Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = dbConn1.getMfg(value=14)
        testMfg.country = countryNonExist
        result = dbConn1.mfg_update(testMfg)
        self.assertNotEqual(result[0], 0)  # Should save
        del dbConn1


class TestTrack(unittest.TestCase):

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
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='New Track name', countryObj=countryExist)
        result = dbConn1.addTrack(testTrack)
        self.assertEqual(result[0], 0)
        del dbConn1

        logger.info("Add Track - Name: Existing, Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='Nurburgring', countryObj=countryExist)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)  # This record show not be saved
        del dbConn1

        logger.info(
            "Add Track - Name: Existing (all caps), Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='NURBURGRING', countryObj=countryExist)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)  # This record show not be saved
        del dbConn1

        logger.info("Add Track - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='New Track name', countryObj=countryNonExist)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)  # This record show not be saved
        del dbConn1

        logger.info("Add Track - Name: Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='Nurburgring', countryObj=countryNull)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)  # This record show not be saved
        del dbConn1

        logger.info("Add Track - Name: Non-Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='New Track Name', countryObj=countryNull)
        result = dbConn1.addTrack(testTrack)
        self.assertEqual(result[0], 0)

        logger.info("Add Track - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='New Track Name', countryObj=countryNonExist)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)  # This record show not be saved

        logger.info("==== END TEST Add Track")

    def test_trackGet(self):
        logger.info("==== BEGIN Get/read Track")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')

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

    def test_trackUpdate(self):
        logging.info("===== BEGIN Update Track (Assumption getTrack works)")
        countryExist = GTClass.Country(
            cntryID=235, cntryName='', alpha2='', alpha3='', region='')
        countryNonExist = GTClass.Country(
            cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None)
        countryNull = GTClass.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)

        logging.info("Update Track - Name: Change, Country ID: No change")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = dbConn1.getTrack(value=4)
        testTrack.name = "Track Name change test"
        result = dbConn1.updateTrack(testTrack)
        self.assertEqual(result[0], 0)
        del dbConn1

        logging.info(
            "Update Track - Name: Change to Existing, Country ID: No change")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = dbConn1.getTrack(value=4)
        testTrack.name = "Nurburgring"
        result = dbConn1.updateTrack(testTrack)
        self.assertNotEqual(result[0], 0)  # Record should not save
        del dbConn1

        logging.info(
            "Update Track - Name: No change, Country ID: Change to null")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = dbConn1.getTrack(value=4)
        testTrack.country = countryNull
        result = dbConn1.updateTrack(testTrack)
        self.assertEqual(result[0], 0)
        del dbConn1

        logging.info(
            "Update Track - Name: No change, Country ID: Change to Non Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = dbConn1.getTrack(value=4)
        testTrack.country = countryNonExist
        result = dbConn1.updateTrack(testTrack)
        self.assertNotEqual(result[0], 0, "Record should not have been saved")
        del dbConn1

        logging.info(
            "Update Track - Name: Change, Country ID: No change, ID: Non Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = dbConn1.getTrack(value=99999)
        testTrack.name = "Track Name change test"
        result = dbConn1.updateTrack(testTrack)
        logger.debug(f"result={result}")
        self.assertNotEqual(result[0], 0, "Record should not have been saved")
        del dbConn1

        logger.info(f"==== END Upate Track test\n")

    def test_trackDelete(self):
        logging.info("===== BEGIN Delete Track (Assumption getTrack works)")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')

        # Delete Track - Track ID: Existing
        # Delete TRack - Track ID: Non Existing

        logging.info("===== End Delete Track\n")


class TestTrackLayout(unittest.TestCase):

    def test_trackLayoutGet(self):
        logger.info("==== BEGIN Get/Read track Layout")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')

        logger.info("Get Track Layout - Track Layout ID: Exists")
        testVal = 2
        testLayout = dbConn1.getTrackLayout(value=testVal)
        self.assertEqual(testLayout.id, testVal)

        logging.info("Get Track Layout - Track Layout ID: Non Exists")
        testVal = 999
        testLayout = dbConn1.getTrackLayout(value=testVal)
        self.assertEqual(testLayout.id, 0)  # No record found

        del dbConn1
        logger.info("==== END Get/Read track Layout\n")
