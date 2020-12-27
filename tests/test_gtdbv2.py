# python -m unittest Tests.test_gtdbv2
# If you want to run specific tests:
# python -m unittest Tests.test_gtdbv2.Class.method
import unittest
from pathlib import Path
import logging
import os
import sys
from datetime import datetime

# App Testing requirements
from GranT import gtdbV2
from GranT import gtclasses as GTClass

# TODO: Add delete Manufacture where mfg relationship may break
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
conHandler.setLevel(logging.CRITICAL)
logger.addHandler(conHandler)

fileHandler = logging.FileHandler(_logfile)
fileHandler.setFormatter(detailFormat)
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

print(f"Logging to {_logfile}.")


class TestMfg(unittest.TestCase):

    def test_addMfg(self):
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
        mfgName = 'NEW Manufacture'
        testMfg = GTClass.Manufacture(
            id=0, name=mfgName, countryObj=countryExist)
        result = dbConn1.addMfg(testMfg)
        logger.info(f"result is {result}")
        self.assertEqual(result[0], 0)
        # Need to confirm it was saved to db
        logger.info("Confirming new record saved")
        testMfg = dbConn1.getMfg(key='Make', value=mfgName)
        self.assertEqual(testMfg.name, mfgName)
        self.assertNotEqual(testMfg.id, 0)
        del dbConn1

        logger.info("Add Manufacture - Name: Existing, Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = 'Honda'
        testMfg = GTClass.Manufacture(
            id=0, name=mfgName, countryObj=countryExist)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Existing (all caps), Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = 'HONDA'
        testMfg = GTClass.Manufacture(
            id=0, name=mfgName, countryObj=countryExist)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = 'NEW manufacture'
        testMfg = GTClass.Manufacture(
            id=0, name=mfgName, countryObj=countryNonExist)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info("Add Manufacture - Name: Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = 'Honda'
        testMfg = GTClass.Manufacture(
            id=0, name=mfgName, countryObj=countryNull)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = 'new Manufacture'
        testMfg = GTClass.Manufacture(
            id=0, name=mfgName, countryObj=countryNull)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = 'Another new one that should fail'
        testMfg = GTClass.Manufacture(
            id=0, name=mfgName, countryObj=countryNonExist)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

    def test_deleteMfg(self):
        logger.info("==== BEGIN Delete Manufacture")

        logger.info("Delete Manufacture = Manufacture ID: Non Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgId = 999999
        result = dbConn1.deleteMfg(mfgId)
        # Sqlite.. the delete works, even if record doesn't exist.
        self.assertEqual(result[0], 0)
        # Confirm record deleted
        logger.info("Confirming record does not exist")
        testMfg = dbConn1.getMfg(value=mfgId)
        self.assertEqual(testMfg.id, 0)
        del dbConn1

        logger.info("Delete Manufacture = Manufacture ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgId = 1
        result = dbConn1.deleteMfg(mfgId)
        self.assertEqual(result[0], 0)
        logger.info("Confirming record does not exist")
        testMfg = dbConn1.getMfg(value=mfgId)
        self.assertEqual(testMfg.id, 0)
        del dbConn1

        logger.info("==== END Delete Manufacture\n")

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

    def test_updateMfg(self):
        logger.info(
            "==== BEGIN UPDATE Manufacture (Assuming Get manufacture works)")
        countryExist = GTClass.Country(
            cntryID=235, cntryName='', alpha2='', alpha3='', region='')
        countryNonExist = GTClass.Country(
            cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None)
        countryNull = GTClass.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)

        logger.info(
            "Update Manufacture: Name: Change, Country ID: No change.")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = "MY new NAME"
        testMfg = dbConn1.getMfg(value=1)
        testMfg.name = mfgName
        result = dbConn1.updateMfg(testMfg)
        self.assertEqual(result[0], 0)
        # Need to confirm it was saved to db
        logger.info("Confirming update saved in db")
        testMfg = dbConn1.getMfg(key='Make', value=mfgName)
        self.assertEqual(testMfg.name, mfgName)
        self.assertNotEqual(testMfg.id, 0)
        del dbConn1

        logger.info(
            "Update Manufacture: Name: No Change, Country ID: Change to null.")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = dbConn1.getMfg(value=4)
        testMfg.country = countryNull
        result = dbConn1.updateMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Update Manufacture: Name: Change, Country ID: No Change, Mfg ID: Non Existing.")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = dbConn1.getMfg(value=14)
        testMfg.id = 99999
        result = dbConn1.updateMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Update Manufacture: Name: Change to Existing, Country ID: No change ")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        xMfg = dbConn1.getMfg(value=3)
        testMfg = dbConn1.getMfg(value=14)
        testMfg.name = xMfg.name
        result = dbConn1.updateMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Update Manufacture: Name: No change, Country ID: Change to Non Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testMfg = dbConn1.getMfg(value=14)
        testMfg.country = countryNonExist
        result = dbConn1.updateMfg(testMfg)
        self.assertNotEqual(result[0], 0)
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
        testVal = 'New Track name'
        testTrack = GTClass.Track(
            id=0, name=testVal, countryObj=countryExist)
        result = dbConn1.addTrack(testTrack)
        logger.info(f"result is {result}")
        self.assertEqual(result[0], 0)
        # Confirm added to db
        logger.info("Confirming new record saved")
        testTrack = dbConn1.getTrack(key='track', value=testVal)
        logger.info(f"testTrack = {testTrack}")
        self.assertEqual(testTrack.name, testVal)
        self.assertNotEqual(testTrack.id, 0)
        del dbConn1

        logger.info("Add Track - Name: Existing, Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='Nurburgring', countryObj=countryExist)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Track - Name: Existing (all caps), Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='NURBURGRING', countryObj=countryExist)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info("Add Track - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='New Track name', countryObj=countryNonExist)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info("Add Track - Name: Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='Nurburgring', countryObj=countryNull)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info("Add Track - Name: Non-Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testVal = 'New Track Name'
        testTrack = GTClass.Track(
            id=0, name=testVal, countryObj=countryNull)
        result = dbConn1.addTrack(testTrack)
        self.assertEqual(result[0], 0)
        # Confirm added to db
        logger.info("Confirming new record saved")
        testTrack = dbConn1.getTrack(key='track', value=testVal)
        logger.info(f"testTrack = {testTrack}")
        self.assertEqual(testTrack.name, testVal)
        self.assertNotEqual(testTrack.id, 0)
        del dbConn1

        logger.info("Add Track - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GTClass.Track(
            id=0, name='New Track Name', countryObj=countryNonExist)
        result = dbConn1.addTrack(testTrack)
        self.assertNotEqual(result[0], 0)

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
        logger.info("===== BEGIN Update Track (Assumption getTrack works)")
        countryExist = GTClass.Country(
            cntryID=235, cntryName='', alpha2='', alpha3='', region='')
        countryNonExist = GTClass.Country(
            cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None)
        countryNull = GTClass.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)

        logger.info("Update Track - Name: Change, Country ID: No change")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        xTrackID = 4
        xTrackNewName = "Track Name change test"
        testTrack = dbConn1.getTrack(value=xTrackID)
        testTrack.name = xTrackNewName
        result = dbConn1.updateTrack(testTrack)
        self.assertEqual(result[0], 0)
        # Confirm of record updated in db
        logger.info("Confirming record updated in db")
        newTrack = dbConn1.getTrack(key='track', value=xTrackNewName)
        logger.info(f"newTrack = {newTrack}")
        self.assertEqual(newTrack.name, xTrackNewName)
        self.assertEqual(newTrack.id, xTrackID)
        del dbConn1

        logger.info(
            "Update Track - Name: Change to Existing, Country ID: No change")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = dbConn1.getTrack(value=4)
        testTrack.name = "Nurburgring"
        result = dbConn1.updateTrack(testTrack)
        self.assertNotEqual(result[0], 0)  # Record should not save
        del dbConn1

        logger.info(
            "Update Track - Name: No change, Country ID: Change to null")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        xTrackID = 4
        testTrack = dbConn1.getTrack(value=xTrackID)
        testTrack.country = countryNull
        result = dbConn1.updateTrack(testTrack)
        self.assertEqual(result[0], 0)
        # Confirm of record updated in db
        logger.info("Confirming record updated in db")
        newTrack = dbConn1.getTrack(value=xTrackID)
        self.assertEqual(newTrack.country.id, None)
        del dbConn1

        logger.info(
            "Update Track - Name: No change, Country ID: Change to Non Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = dbConn1.getTrack(value=4)
        testTrack.country = countryNonExist
        result = dbConn1.updateTrack(testTrack)
        self.assertNotEqual(result[0], 0, "Record should not have been saved")
        del dbConn1

        logger.info(
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
        logger.info("===== BEGIN Delete Track (Assumption getTrack works)")
        countryExist = GTClass.Country(
            cntryID=235, cntryName='United Kingdom of Great Britain and Northern Ireland', alpha2='GB', alpha3='GBR', region='Europe')

        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')

        # Delete Track - Track ID: Existing, Track Layout: No relation
        logger.info(
            "Delete Track - Track ID: Existing, Track Layout: No relation")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        logger.info("Create new track, will have no track layouts")
        xTrackName = 'New Track name to delete'
        testTrack = GTClass.Track(
            id=0, name=xTrackName, countryObj=countryExist)
        result = dbConn1.addTrack(testTrack)
        if result[0] != 0:  # Unsuccessfull test add
            logger.critical(
                "Unable to test track delete as test track was unable to be created.")
            sys.exit(1)
        # Getting new test track ID
        testTrack = dbConn1.getTrack(key='track', value=xTrackName)
        logger.info("Deleting the new track")
        result = dbConn1.deleteTrack(testTrack.id)
        self.assertEqual(result[0], 0)
        logger.info("Confirming record does not exist in db")
        testTrack = dbConn1.getTrack(value=testTrack.id)
        self.assertEqual(testTrack.id, 0)

        # Delete Track - Track ID: Existing, Track Layout: Related
        logger.info(
            "Delete Track - Track ID: Existing, Track Layout: Related")
        # Track id 2, 'Dragon Tail' has several Track Layouts
        xTrackId = 2
        result = dbConn1.deleteTrack(xTrackId)
        logger.debug(f"result={result}")
        self.assertNotEqual(result[0], 0)

        # Delete Track - Track ID: Non Existing
        logger.info("Delete Track - Track ID: Non Existing")
        xTrackId = 999999
        result = dbConn1.deleteTrack(xTrackId)
        # Sqlite.. the delete works, even if record doesn't exist.
        self.assertEqual(result[0], 0)
        logger.info("Confirming record does not exist in db")
        testTrack = dbConn1.getTrack(value=testTrack.id)
        self.assertEqual(testTrack.id, 0)
        logger.info("===== End Delete Track\n")


class TestTrackLayout(unittest.TestCase):

    def test_trackLayoutGet(self):
        logger.info("==== BEGIN Get/Read track Layout")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')

        logger.info("Get Track Layout - Track Layout ID: Exists")
        testVal = 2
        testLayout = dbConn1.getTrackLayout(value=testVal)
        self.assertEqual(testLayout.id, testVal)

        logger.info("Get Track Layout - Track Layout ID: Non Exists")
        testVal = 999
        testLayout = dbConn1.getTrackLayout(value=testVal)
        self.assertEqual(testLayout.id, 0)  # No record found

        del dbConn1
        logger.info("==== END Get/Read track Layout\n")
