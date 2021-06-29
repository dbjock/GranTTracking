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

    def test_getCircuitList(self):
        logger.info("==== BEGIN Get Circuit List")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        testList = gtdbV3.getCircuitList(d1)
        # Test there are more than 1 row
        logger.info("Checking for at least 1 row returned")
        self.assertGreater(
            len(testList), 1, "Failed Get Circuit List returned zero rows")
        # Test there are only 2 elements per row.
        logger.info("Checking for at least 2 columns")
        testRow = testList[0]
        self.assertGreaterEqual(len(
            testRow), 2, "Failed Get Circuit List did not return minimum number of columns")
        logger.info(f"==== END Get Circuit List\n")


class TestLeagues(unittest.TestCase):
    def test_getLeague(self):
        logger.info("==== BEGIN Get/read League")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Get League by id")
        testVal = 1
        testObj = gtdbV3.getLeague(d1, value=testVal)
        self.assertEqual(testObj.id, testVal, "Failed getting by league id")

        logger.info("Get League by name (case insensitve)")
        testVal = 'amATeur'
        testObj = gtdbV3.getLeague(d1, key='name', value=testVal)
        # If not found zero is returned
        self.assertNotEqual(
            testObj.id, 0, "Failed getting league by existing name")

        logger.info("Get non exist League by id")
        testVal = 99999
        testObj = gtdbV3.getLeague(d1, value=testVal)
        self.assertEqual(
            testObj.id, 0, "Failed getting league by non exist league id")

        logger.info("Get non exist League by name")
        testVal = 'ZZINoExist'
        testObj = gtdbV3.getLeague(d1, key='name', value=testVal)
        self.assertEqual(testObj.id, 0)

        logger.info(f"==== END Get/read League\n")


class TestRaceCollection(unittest.TestCase):

    def test_getRaceCollection(self):
        logger.info("==== BEGIN Get Race Collection")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Getting an existing Race Collection")
        testVal = 1
        r = gtdbV3.getRaceCollection(d1, rcId=testVal)
        self.assertEqual(r.id, 1, "Failed to get existing race collection")

        logger.info("Getting non existing Race Collection")
        testVal = 9999
        r = gtdbV3.getRaceCollection(d1, rcId=testVal)
        self.assertEqual(
            r.id, 0, "Failed getting non existing race collection")

    def test_getRaceCollectionList(self):
        logger.info("=== BEGIN getRaceCollectionList testing")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Getting list for existing League")
        testVal = 2  # leagueId 2 should bring back at least 2 elements
        testList = gtdbV3.getRaceCollectionList(d1, leagueId=testVal)
        logger.info(f"testList = {testList}")
        self.assertEqual(testList[0][0], 12, "Failed. First row incorrect")

        logger.info("Getting list for non existing league")
        testVal = 9999  # leagueId 10 does not exist
        testList = gtdbV3.getRaceCollectionList(d1, leagueId=testVal)
        logger.info(f"testList = {testList}")
        self.assertEqual(len(testList), 0,
                         "Failed. Getting list from non exist League")


class TestTrack(unittest.TestCase):
    def test_addTrack(self):
        logger.info(
            "==== BEGIN TEST Adding a Track")
        d1 = gtdbV3.create_connection(":memory:")

        # Existing Track Layout name
        tlNameExist = "Infield B"
        tlNameNonExist = "Layout name that does not exist"

        logger.info(
            "0 - Circuit ID Existing: No, Miles empty: No, Track Name Existing: No")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        miles = .1
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, GT.Track(9999, "I dont exist", GT.Country(cntryID=235, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(id=9999, name="I do not exist"))
        logger.info(f"{xTlayout}")
        result = gtdbV3.addTrack(d1, xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")

        logger.info(
            "1 - Circuit ID Existing: No, Miles empty: No, Track Name Existing: Yes")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        miles = .1
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, GT.Track(7, "Blue Moon Bay Speedway", GT.Country(cntryID=235, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(id=9999, name="I do not exist"))
        logger.info(f"{xTlayout}")
        result = gtdbV3.addTrack(d1, xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")

        logger.info(
            "2 - Circuit ID Existing: No, Miles empty: Yes, Track Name Existing: No")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        miles = None
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, GT.Track(9999, "I dont exist", GT.Country(cntryID=235, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(id=9999, name="I do not exist"))
        logger.info(f"{xTlayout}")
        result = gtdbV3.addTrack(d1, xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")

        logger.info(
            "3 - Circuit ID Existing: No, Miles empty: Yes, Track Name Existing: Yes")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        miles = None
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, GT.Track(7, "Blue Moon Bay Speedway", GT.Country(cntryID=235, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(id=9999, name="I do not exist"))
        logger.info(f"{xTlayout}")
        result = gtdbV3.addTrack(d1, xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")

        logger.info(
            "4 - Circuit ID Existing: Yes, Miles empty: No, Track Name Existing: No")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        miles = .1
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, GT.Track(9999, "I dont exist", GT.Country(cntryID=235, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(id=1, name=None))
        logger.info(f"{xTlayout}")
        result = gtdbV3.addTrack(d1, xTlayout)
        logger.info(f"result = {result}")
        self.assertEqual(result[0], 0, "Records should be saved")

        logger.info(
            "5 - Circuit ID Existing: Yes, Miles empty: No, Track Name Existing: Yes")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        miles = .1
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, GT.Track(7, "Blue Moon Bay Speedway", GT.Country(cntryID=235, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(id=1, name=None))
        logger.info(f"{xTlayout}")
        result = gtdbV3.addTrack(d1, xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")

        logger.info(
            "6 - Circuit ID Existing: Yes, Miles empty: Yes, Track Name Existing: No")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        miles = None
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, GT.Track(9999, "I dont exist", GT.Country(cntryID=235, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(id=1, name=None))
        logger.info(f"{xTlayout}")
        result = gtdbV3.addTrack(d1, xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")

        logger.info(
            "7 - Circuit ID Existing: Yes, Miles empty: Yes, Track Name Existing: Yes")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        miles = None
        xTlayout = GT.TrackLayout(
            None, tlNameExist, miles, GT.Track(7, "Blue Moon Bay Speedway", GT.Country(cntryID=235, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(id=1, name=None))
        logger.info(f"{xTlayout}")
        result = gtdbV3.addTrack(d1, xTlayout)
        logger.info(f"result = {result}")
        self.assertNotEqual(result[0], 0, "No records should be created")

        logger.info("==== END TEST Add Track")

    def test_deleteTrack(self):
        logger.info("===== BEGIN Delete Track")
        d1 = gtdbV3.create_connection(":memory:")

        # Delete Track - Track Exist: Yes, Track Layouts: Yes
        testmsg = '1 - Delete existing TrackId'
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        trackId = 6  # Track has multiple layouts
        result = gtdbV3.deleteTrack(d1, trackId)
        logger.info(f"result={result}")
        self.assertEqual(result[0], 0)

        testmsg = '2 - Delete existing TrackId'
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        trackId = 99999  # Track has multiple layouts
        result = gtdbV3.deleteTrack(d1, trackId)
        logger.info(f"result={result}")
        self.assertEqual(result[0], 0)

        logger.info("===== END Delete Track")

    def test_getTrack(self):
        logger.info("==== BEGIN Get/read Track")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Get a Track by the track id")
        testVal = 4
        testTrack = gtdbV3.getTrack(d1, value=testVal)
        self.assertEqual(testTrack.id, testVal, 'Failed Getting a Track by id')

        logger.info("Get a Track by name")
        testVal = 'Northern Isle Speedway'
        logger.info(f"Getting track by track name = {testVal}")
        testTrack = gtdbV3.getTrack(d1, key='track', value=testVal)
        self.assertEqual(testTrack.name, testVal,
                         'Failed Getting a Track by name')

        logger.info("Get non exist Track by id")
        testVal = 99999
        testTrack = gtdbV3.getTrack(d1, value=testVal)
        self.assertEqual(
            testTrack.id, 0, "Failed Get non exist Track by id")

        logger.info("Get non exist Track by name")
        testVal = 'NON exist track test'
        testTrack = gtdbV3.getTrack(d1, key='track', value=testVal)
        self.assertEqual(testTrack.id, 0, 'Failed Get non exist Track by name')

        logger.info(f"==== END Get/read Track\n")

    def test_getTrackList(self):
        logger.info("==== BEGIN get Tracks")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Getting a list of tracks")
        testVal = 17  # First element should be trackid 17
        testList = gtdbV3.getTrackList(d1)
        logger.info(f"testList={testList}")
        self.assertEqual(
            testList[0][0], testVal, "Failed. First track or should have track id 17")

        logger.info(f"==== END get Tracks\n")

    def test_updateTrack(self):
        logger.info("===== BEGIN Update Track")
        d1 = gtdbV3.create_connection(":memory:")
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
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testTrack = GT.Track(trackIdNonExist, tNonExistName, GT.Country(
            cntryID=235, cntryName='', alpha2='', alpha3='', region=''))
        logger.info(testTrack)
        result = gtdbV3.updateTrack(d1, testTrack)
        logger.info(f"result={result}")
        self.assertNotEqual(result[0], 0)

        testmsg = '2 - Unique Name for existing TrackId: No'
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testTrack = GT.Track(trackIdExist, tExistName, GT.Country(
            cntryID=235, cntryName='', alpha2='', alpha3='', region=''))
        logger.info(testTrack)
        result = gtdbV3.updateTrack(d1, testTrack)
        logger.info(f"result={result}")
        self.assertNotEqual(result[0], 0)

        testmsg = '3 - Country Exist for existing TrackId: No'
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testTrack = GT.Track(trackIdExist, tNonExistName, countryNonExist)
        logger.info(testTrack)
        result = gtdbV3.updateTrack(d1, testTrack)
        logger.info(f"result={result}")
        self.assertNotEqual(result[0], 0)

        testmsg = '4 - Existing TrackId with a Unique Name and Existing Country: Yes'
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testTrack = GT.Track(trackIdExist, tNonExistName, GT.Country(
            cntryID=235, cntryName='', alpha2='', alpha3='', region=''))
        logger.info(testTrack)
        result = gtdbV3.updateTrack(d1, testTrack)
        logger.info(f"result={result}")
        self.assertEqual(result[0], 0)

        testmsg = "A - Null CountryId for existing TrackId: Yes"
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testTrack = GT.Track(trackIdExist, tNonExistName, countryNull)
        logger.info(testTrack)
        result = gtdbV3.updateTrack(d1, testTrack)
        logger.info(f"result={result}")
        self.assertEqual(result[0], 0)

        logger.info(f"==== END Upate Track test\n")


class TestTrackLayout(unittest.TestCase):

    def test_addTrackLayout(self):
        logger.info("==== BEGIN Add Track Layout")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info(
            "Add Track Layout : Layout name Dupe for same track")
        testLayout = GT.TrackLayout(id=0, name=None, miles=None, trackObj=GT.Track(id=0, name=None, countryObj=GT.Country(
            cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)), circuitObj=GT.Circuit(id=0, name=None))
        testLayout.name = "Infield B"
        testLayout.miles = 9999
        testLayout.track.id = 7
        testLayout.circuit.id = 3
        result = gtdbV3.addLayout(d1, testLayout)
        logger.info(f"result is {result}")
        self.assertNotEqual(result[0], 0)

        logger.info(
            "Add Track Layout : Layout name 'None' for same track")
        testLayout = GT.TrackLayout(id=0, name=None, miles=None, trackObj=GT.Track(id=0, name=None, countryObj=GT.Country(
            cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)), circuitObj=GT.Circuit(id=0, name=None))
        testLayout.name = None
        testLayout.miles = 9999
        testLayout.track.id = 7
        testLayout.circuit.id = 3
        result = gtdbV3.addLayout(d1, testLayout)
        logger.info(f"result is {result}")
        self.assertNotEqual(
            result[0], 0, "Failed Layout name 'None' for same track")

        logger.info(
            "Add Track Layout : Layout name empty string for same track")
        testLayout = GT.TrackLayout(id=0, name=None, miles=None, trackObj=GT.Track(id=0, name=None, countryObj=GT.Country(
            cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)), circuitObj=GT.Circuit(id=0, name=None))
        testLayout.name = ""
        testLayout.miles = 9999
        testLayout.track.id = 7
        testLayout.circuit.id = 3
        result = gtdbV3.addLayout(d1, testLayout)
        logger.info(f"result is {result}")
        self.assertNotEqual(
            result[0], 0, "Add Track Layout : Layout name empty string for same track")

        logger.info(
            "Add Track Layout : Layout name non existant for same track")
        testLayout = GT.TrackLayout(id=0, name=None, miles=None, trackObj=GT.Track(id=0, name=None, countryObj=GT.Country(
            cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)), circuitObj=GT.Circuit(id=0, name=None))
        testLayout.name = "I am a new track layout"
        testLayout.miles = 9999
        testLayout.track.id = 7
        testLayout.circuit.id = 3
        result = gtdbV3.addLayout(d1, testLayout)
        logger.info(f"result is {result}")
        self.assertEqual(
            result[0], 0, "Failed Add Track Layout : Layout name non existant for same track")

        logger.info("==== END Add Track Layout")

    def test_getLayout(self):
        logger.info("==== BEGIN Get/Read track Layout")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Get Track Layout by Track Layout ID: Exists")
        testVal = 2
        testLayout = gtdbV3.getLayout(d1, testVal)
        logger.info(f"testLayout={testLayout}")
        self.assertEqual(testLayout.id, testVal)

        logger.info("Get Track Layout by Track Layout ID: Non Exists")
        testVal = 999
        testLayout = gtdbV3.getLayout(d1, testVal)
        logger.info(f"testLayout={testLayout}")
        self.assertEqual(testLayout.id, 0)

        logger.info("==== END Get/Read track Layout\n")

    def test_getLayoutList(self):
        logger.info("==== BEGIN get Layout List")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Get Track Layout List")
        testVal = 5  # Track ID 5
        layoutList = gtdbV3.getLayoutList(d1, testVal)
        logger.info(f"layoutList={layoutList}")
        self.assertEqual(layoutList[0][0], 18,
                         "Failed getting correct trackLayoutId from list")

        logger.info("==== END get Layout List")

    def test_deleteTrackLayout(self):
        logger.info("==== BEGIN Deleting Track Layout")
        d1 = gtdbV3.create_connection(":memory:")

        logger.info("Delete track layout exists : yes")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        layoutId = 29
        logger.info(f"layoutId={layoutId}")
        result = gtdbV3.deleteTrackLayout(d1, layoutId)
        logger.info(f"result={result}")
        errMsg = "delete existing track layout unsuccessful"
        self.assertEqual(result[0], 0, errMsg)

        logger.info("Delete track layout exists : no")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        layoutId = 99999
        logger.info(f"layoutId={layoutId}")
        result = gtdbV3.deleteTrackLayout(d1, layoutId)
        logger.info(f"result={result}")
        errMsg = "delete non existing track layout unsuccessful"
        self.assertEqual(result[0], 0, errMsg)

        logger.info("==== END Deleting Track Layout")

    def test_updateTrackLayout(self):
        logger.info("===== BEGIN Track Layout Update ")
        d1 = gtdbV3.create_connection(":memory:")
        testmsg = '1 - Circuit ID Exist: No, Miles a number: Yes, Unique name for Track: Yes'
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        xLayout = GT.TrackLayout(33, 'IamUnique', 4, GT.Track(7, "Note Tested", GT.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(1, "Note Tested"))
        xLayout.circuit.id = 0
        logger.info(f'xLayout={xLayout}')
        result = gtdbV3.updateTrackLayout(d1, xLayout)
        logger.info(f"result={result}")
        self.assertNotEqual(result[0], 0)

        testmsg = '2 - Circuit ID Exist: Yes, Miles a number: No (Null), Unique name for Track: Yes'
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        xLayout = GT.TrackLayout(33, 'IamUnique', 4, GT.Track(7, "Note Tested", GT.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(1, "Note Tested"))
        xLayout.miles = None
        logger.info(f'xLayout={xLayout}')
        result = gtdbV3.updateTrackLayout(d1, xLayout)
        logger.info(f"result={result}")
        self.assertNotEqual(result[0], 0)

        testmsg = '2a - Circuit ID Exist: Yes, Miles a number: No (string), Unique name for Track: Yes'
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        xLayout = GT.TrackLayout(33, 'IamUnique', 4, GT.Track(7, "Note Tested", GT.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(1, "Note Tested"))
        xLayout.miles = '1 mile'
        logger.info(f'xLayout={xLayout}')
        result = gtdbV3.updateTrackLayout(d1, xLayout)
        logger.info(f"result={result}")
        self.assertNotEqual(result[0], 0)

        testmsg = '3 - Circuit ID Exist: Yes, Miles a number: Yes, Unique name for Track: No'
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        xLayout = GT.TrackLayout(33, 'IamUnique', 4, GT.Track(7, "Note Tested", GT.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(1, "Note Tested"))
        xLayout.name = 'Infield B II'
        logger.info(f'xLayout={xLayout}')
        result = gtdbV3.updateTrackLayout(d1, xLayout)
        logger.info(f"result={result}")
        self.assertNotEqual(result[0], 0)

        testmsg = '4 - Circuit ID Exist: Yes, Miles a number: Yes, Unique name for Track: Yes'
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        xLayout = GT.TrackLayout(33, 'IamUnique', 4, GT.Track(7, "Note Tested", GT.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(1, "Note Tested"))
        logger.info(f'xLayout={xLayout}')
        result = gtdbV3.updateTrackLayout(d1, xLayout)
        logger.info(f"result={result}")
        self.assertEqual(result[0], 0)

        testmsg = '5 - Testing if duplicate nulls will be caught, so record will not be saved'
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        xLayout = GT.TrackLayout(33, 'IamUnique', 4, GT.Track(7, "Note Tested", GT.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(1, "Note Tested"))
        xLayout.name = None
        logger.info(f'xLayout={xLayout}')
        result = gtdbV3.updateTrackLayout(d1, xLayout)
        logger.info(f"result={result}")
        self.assertNotEqual(result[0], 0)

        testmsg = '6 - Track Id does not exist'
        logger.info(testmsg)
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        xLayout = GT.TrackLayout(33, 'IamUnique', 4, GT.Track(0, "Note Tested", GT.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)), GT.Circuit(1, "Note Tested"))
        logger.info(f'xLayout={xLayout}')
        result = gtdbV3.updateTrackLayout(d1, xLayout)
        logger.info(f"result={result}")
        self.assertNotEqual(result[0], 0)


class TestWeather(unittest.TestCase):
    def test_getWeatherList(self):
        logger.info("==== BEGIN Get Weather List")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Getting a list of all weather types")
        testList = gtdbV3.getWeatherList(d1)
        logger.info(f"testList={testList}")
        self.assertGreater(
            len(testList), 1, "More than one weather should be returned")
        self.assertEqual(
            len(testList[0]), 2, "There should be 2 fields for each weather row")

    def test_getWeather(self):
        logger.info("==== BEGIN Get/read Weather")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Get a weather object by id")
        testVal = 1
        testObj = gtdbV3.getWeather(d1, testVal)
        self.assertEqual(testObj.id, testVal,
                         "Failed getting by Weather object by id")

        logger.info("Get non exist weather by id")
        testVal = 99999
        testObj = gtdbV3.getWeather(d1, testVal)
        self.assertEqual(
            testObj.id, 0, "Failed getting weather by non exist id")

        logger.info("=== END Get/read Weather")
