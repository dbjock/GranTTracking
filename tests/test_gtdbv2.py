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
from GranT import GTClasses as GT

_gtPath = Path.cwd()
_gtLogs = _gtPath / 'Logs'
_gtScripts = _gtPath / 'Scripts'
_gtData = _gtPath / 'Data'
_logfile = _gtLogs / f"Testing-{datetime.now().strftime('%Y%j%H%M%S')}.log"

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


class TestMfg(unittest.TestCase):

    def test_addMfg(self):
        """Test various adding a manufacture scenerios
        """
        logger.info(
            "==== BEGIN Add Manufacture (Requirements: Name is unique. Required to have a country)")
        countryExist = GT.Country(
            cntryID=235, cntryName='United Kingdom of Great Britain and Northern Ireland', alpha2='GB', alpha3='GBR', region='Europe')
        countryNonExist = GT.Country(
            cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None)
        countryNull = GT.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = 'NEW Manufacture'
        testMfg = GT.Manufacture(
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
        testMfg = GT.Manufacture(
            id=0, name=mfgName, countryObj=countryExist)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Existing (all caps), Country ID: Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = 'HONDA'
        testMfg = GT.Manufacture(
            id=0, name=mfgName, countryObj=countryExist)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = 'NEW manufacture'
        testMfg = GT.Manufacture(
            id=0, name=mfgName, countryObj=countryNonExist)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info("Add Manufacture - Name: Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = 'Honda'
        testMfg = GT.Manufacture(
            id=0, name=mfgName, countryObj=countryNull)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Null/None")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = 'new Manufacture'
        testMfg = GT.Manufacture(
            id=0, name=mfgName, countryObj=countryNull)
        result = dbConn1.addMfg(testMfg)
        self.assertNotEqual(result[0], 0)
        del dbConn1

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Non-Existing")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        mfgName = 'Another new one that should fail'
        testMfg = GT.Manufacture(
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
        countryExist = GT.Country(
            cntryID=235, cntryName='', alpha2='', alpha3='', region='')
        countryNonExist = GT.Country(
            cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None)
        countryNull = GT.Country(
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

    def test_addTrack(self):
        logger.info(
            "==== BEGIN TEST Adding a Track")
        cntryExist = GT.Country(
            cntryID=235, cntryName=None, alpha2=None, alpha3=None, region=None)
        cntryNonExist = GT.Country(
            cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)

        # Existing Track is picked as it has a null and non null layouts
        tExist = GT.Track(7, "Blue Moon Bay Speedway", cntryExist)
        tNonExist = GT.Track(9999, "I dont exist", cntryExist)

        circuitExist = GT.Circuit(id=1, name=None)
        circuitNonExist = GT.Circuit(id=9999, name="I do not exist")

        tlNameExist = "Infield B"
        tlNameNonExist = "Layout name that does not exist"

        logger.info(
            "0 - Circuit ID Existing: No, Miles empty: No, Track Name Existing: No")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        miles = .1
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, tNonExist, circuitNonExist)
        logger.info(f"{xTlayout}")
        result = dbConn1.addTrack(xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")
        del dbConn1

        logger.info(
            "1 - Circuit ID Existing: No, Miles empty: No, Track Name Existing: Yes")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        miles = .1
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, tExist, circuitNonExist)
        logger.info(f"{xTlayout}")
        result = dbConn1.addTrack(xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")
        del dbConn1

        logger.info(
            "2 - Circuit ID Existing: No, Miles empty: Yes, Track Name Existing: No")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        miles = None
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, tNonExist, circuitNonExist)
        logger.info(f"{xTlayout}")
        result = dbConn1.addTrack(xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")
        del dbConn1

        logger.info(
            "3 - Circuit ID Existing: No, Miles empty: Yes, Track Name Existing: Yes")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        miles = None
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, tExist, circuitNonExist)
        logger.info(f"{xTlayout}")
        result = dbConn1.addTrack(xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")
        del dbConn1

        logger.info(
            "4 - Circuit ID Existing: Yes, Miles empty: No, Track Name Existing: No")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        miles = .1
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, tNonExist, circuitExist)
        logger.info(f"{xTlayout}")
        result = dbConn1.addTrack(xTlayout)
        logger.info(f"result = {result}")
        self.assertEqual(result[0], 0, "Records should be saved")
        del dbConn1

        logger.info(
            "5 - Circuit ID Existing: Yes, Miles empty: No, Track Name Existing: Yes")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        miles = .1
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, tExist, circuitExist)
        logger.info(f"{xTlayout}")
        result = dbConn1.addTrack(xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")
        del dbConn1

        logger.info(
            "6 - Circuit ID Existing: Yes, Miles empty: Yes, Track Name Existing: No")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        miles = None
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, tNonExist, circuitExist)
        logger.info(f"{xTlayout}")
        result = dbConn1.addTrack(xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")
        del dbConn1

        logger.info(
            "7 - Circuit ID Existing: Yes, Miles empty: Yes, Track Name Existing: Yes")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        miles = None
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, tExist, circuitExist)
        logger.info(f"{xTlayout}")
        result = dbConn1.addTrack(xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")
        del dbConn1

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
        logger.info("===== BEGIN Update Track")
        countryExist = GT.Country(
            cntryID=235, cntryName='', alpha2='', alpha3='', region='')
        countryNonExist = GT.Country(
            cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None)
        countryNull = GT.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)

        tExistName = "Red Bull Ring"
        tNonExistName = "IM the New Name"
        # trackIdExist must not be trackId of tExistName for valid testing
        trackIdExist = 1
        trackIdNonExist = 99999

        testmsg = '1 - TrackId Exist: No.'
        logger.info(testmsg)
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GT.Track(trackIdNonExist, tNonExistName, countryExist)
        logger.info(testTrack)
        result = dbConn1.updateTrack(testTrack)
        logger.info(f"result={result}")
        self.assertNotEqual(result[0], 0)
        del dbConn1

        testmsg = '2 - Unique Name for existing TrackId: No'
        logger.info(testmsg)
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GT.Track(trackIdExist, tExistName, countryExist)
        logger.info(testTrack)
        result = dbConn1.updateTrack(testTrack)
        logger.info(f"result={result}")
        self.assertNotEqual(result[0], 0)
        del dbConn1

        testmsg = '3 - Country Exist for existing TrackId: No'
        logger.info(testmsg)
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GT.Track(trackIdExist, tNonExistName, countryNonExist)
        logger.info(testTrack)
        result = dbConn1.updateTrack(testTrack)
        logger.info(f"result={result}")
        self.assertNotEqual(result[0], 0)
        del dbConn1

        testmsg = '4 - Existing TrackId with a Unique Name and Existing Country: Yes'
        logger.info(testmsg)
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GT.Track(trackIdExist, tNonExistName, countryExist)
        logger.info(testTrack)
        result = dbConn1.updateTrack(testTrack)
        logger.info(f"result={result}")
        self.assertEqual(result[0], 0)
        del dbConn1

        testmsg = "A - Null CountryId for existing TrackId: Yes"
        logger.info(testmsg)
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        testTrack = GT.Track(trackIdExist, tNonExistName, countryNull)
        logger.info(testTrack)
        result = dbConn1.updateTrack(testTrack)
        logger.info(f"result={result}")
        self.assertEqual(result[0], 0)
        del dbConn1

        logger.info(f"==== END Upate Track test\n")

    def test_trackDelete(self):
        logger.info("===== BEGIN Delete Track")
        # Delete Track - Track Exist: Yes, Track Layouts: Yes
        testmsg = '1 - Delete existing TrackId'
        logger.info(testmsg)
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        trackId = 6  # Track has multiple layouts
        result = dbConn1.deleteTrack(trackId)
        logger.info(f"result={result}")
        self.assertEqual(result[0], 0)

        testmsg = '2 - Delete existing TrackId'
        logger.info(testmsg)
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        trackId = 99999  # Track has multiple layouts
        result = dbConn1.deleteTrack(trackId)
        logger.info(f"result={result}")
        self.assertEqual(result[0], 0)

        logger.info("===== END Delete Track")


class TestTrackLayout(unittest.TestCase):

    def test_getLayout(self):
        logger.info("==== BEGIN Get/Read track Layout")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')

        logger.info("Get Track Layout by Track Layout ID: Exists")
        testVal = 2
        testLayout = dbConn1.getLayout(testVal)
        logger.info(f"testLayout={testLayout}")
        self.assertEqual(testLayout.id, testVal)

        logger.info("Get Track Layout by Track Layout ID: Non Exists")
        testVal = 999
        testLayout = dbConn1.getLayout(testVal)
        logger.info(f"testLayout={testLayout}")
        self.assertEqual(testLayout.id, 0)
        del dbConn1
        logger.info("==== END Get/Read track Layout\n")

    def test_getLayoutList(self):
        logger.info("==== BEGIN get Layout List")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')

        logger.info("Get Layout List by trackId")
        testVal = 2
        layoutList = dbConn1.getLayoutList('trackId', testVal)
        logger.info(f"layoutList={layoutList}")
        self.assertGreaterEqual(len(layoutList), 1)

        logger.info("Get Layout List by layoutId")
        testVal = 1
        layoutList = dbConn1.getLayoutList('layoutId', testVal)
        logger.info(f"layoutList={layoutList}")
        self.assertEqual(len(layoutList), 1)

        logger.info("Get Layout List by circuitId")
        testVal = 2
        layoutList = dbConn1.getLayoutList('circuitId', testVal)
        logger.info(f"layoutList={layoutList}")
        self.assertGreaterEqual(len(layoutList), 1)

        logger.info("Get Layout List by cntryId")
        testVal = 237
        layoutList = dbConn1.getLayoutList('cntryId', testVal)
        logger.info(f"layoutList={layoutList}")
        self.assertGreaterEqual(len(layoutList), 1)
        logger.info("==== END get Layout List")

    def test_trackLayoutAdd(self):
        logger.info("==== BEGIN Add Track Layout")
        xCircuit = GT.Circuit(id=0, name=None)
        xCountry = GT.Country(
            cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)
        xTrack = GT.Track(id=0, name=None, countryObj=xCountry)
        blank_track_layout = GT.TrackLayout(
            id=0, name=None, miles=None, trackObj=xTrack, circuitObj=xCircuit)

        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')

        logger.info(
            "Add Track Layout : Layout name Dupe for same track")
        testLayout = blank_track_layout
        testLayout.name = "Infield B"
        testLayout.miles = 9999
        testLayout.track.id = 7
        testLayout.circuit.id = 3
        result = dbConn1.addLayout(testLayout)
        logger.info(f"result is {result}")
        self.assertNotEqual(result[0], 0)

        logger.info(
            "Add Track Layout : Layout name Dupe 'None' for same track")
        testLayout = blank_track_layout
        testLayout.name = None
        testLayout.miles = 9999
        testLayout.track.id = 7
        testLayout.circuit.id = 3
        result = dbConn1.addLayout(testLayout)
        logger.info(f"result is {result}")
        self.assertNotEqual(result[0], 0)

        logger.info(
            "Add Track Layout : Layout name non existant for same track")
        testLayout = blank_track_layout
        testLayout.name = "I am a new track layout"
        testLayout.miles = 9999
        testLayout.track.id = 7
        testLayout.circuit.id = 3
        result = dbConn1.addLayout(testLayout)
        logger.info(f"result is {result}")
        self.assertEqual(result[0], 0)
        logger.info("==== END Add Track Layout")

    def test_deleteTrackLayout(self):
        logger.info("==== BEGIN Deleting Track Layout")

        logger.info("Delete track layout exists : yes")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        layoutId = 29
        logger.info(f"layoutId={layoutId}")
        result = dbConn1.deleteTrackLayout(layoutId)
        logger.info(f"result={result}")
        errMsg = "delete existing track layout unsuccessful"
        self.assertEqual(result[0], 0, errMsg)

        logger.info("Delete track layout exists : no")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')
        layoutId = 99999
        logger.info(f"layoutId={layoutId}")
        result = dbConn1.deleteTrackLayout(layoutId)
        logger.info(f"result={result}")
        errMsg = "delete non existing track layout unsuccessful"
        self.assertEqual(result[0], 0, errMsg)

        logger.info("==== END Deleting Track Layout")


class TestCircuit(unittest.TestCase):
    def test_getCircuit(self):
        logger.info("==== BEGIN Get Circuit")
        dbConn1 = gtdbV2.GTdb(name=':memory:')
        dbConn1.initDB(scriptPath=f'{_gtScripts}')

        logger.info("Get Circuit by ID - Exist")
        testVal = 1
        logger.info(f"Circuit ID = {testVal}")
        xCircuit = dbConn1.getCircuit(key='id', value=testVal)
        logger.info(f"result is {xCircuit}")
        self.assertNotEqual(xCircuit.id, 0)

        logger.info("Get Circuit by ID - Non Exist")
        testVal = 999
        logger.info(f"Circuit ID = {testVal}")
        xCircuit = dbConn1.getCircuit(key='id', value=testVal)
        logger.info(f"result is {xCircuit}")
        self.assertEqual(xCircuit.id, 0)

        logger.info("Get Circuit by name - Exist")
        testVal = "Dirt / Snow"
        logger.info(f"Circuit name = {testVal}")
        xCircuit = dbConn1.getCircuit(key='name', value=testVal)
        logger.info(f"result is {xCircuit}")
        self.assertNotEqual(xCircuit.id, 0)

        logger.info("Get Circuit by name - Non Exist")
        testVal = "I donot exist"
        logger.info(f"Circuit name = {testVal}")
        xCircuit = dbConn1.getCircuit(key='id', value=testVal)
        logger.info(f"result is {xCircuit}")
        self.assertEqual(xCircuit.id, 0)

        logger.info("==== END Get Circuit")
