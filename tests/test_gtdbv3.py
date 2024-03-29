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
_gtLogs = Path("z:/logs")
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


class TestCar(unittest.TestCase):
    def test_addCar(self):
        logger.info("==== BEGIN get car tests")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        # init car table createUserTables.sql
        gtdbV3._exeScriptFile(d1, scriptFileName=_gtScripts /
                              'createUserTables.sql')
        # Load test car data
        gtdbV3._exeScriptFile(d1, scriptFileName=_gtPath /
                              'tests' / 'test_carData.sql')
        # Default country
        xcountry = GT.Country(235, cntryName='NA',
                              alpha2='NA', alpha3='NA', region='NA')

        ## Now the testing ##
        logger.info("Testing Add Car : Manufacture id does not exist")
        xdriveTrain = GT.DriveTrain(id=1, code='NA', desc='NA')
        xclassCat = GT.ClassCat(id=1, name='NA', desc='NA')
        # Alter xmfg so id does not exist
        xmfg = GT.Manufacture(id=9999, name='NA', countryObj=xcountry)
        xObj = GT.Car(id=0, model='Test model name 9999', Manufacture=xmfg,
                      DriveTrain=xdriveTrain, ClassCat=xclassCat)
        logger.info(f"Saving car {xObj}")
        result = gtdbV3.addCar(d1, xObj)
        logger.info(f"result: {result}")
        self.assertNotEqual(
            result[0], 0, "Failed: Add Car : Manufacture id does not exist. Car should not have been saved")

        logger.info("Testing Add Car : Manufacture id=0")
        xdriveTrain = GT.DriveTrain(id=1, code='NA', desc='NA')
        xclassCat = GT.ClassCat(id=1, name='NA', desc='NA')
        # Alter xmfg so id is 0
        xmfg = GT.Manufacture(id=0, name='NA', countryObj=xcountry)
        xObj = GT.Car(id=0, model='Test model name 9999', Manufacture=xmfg,
                      DriveTrain=xdriveTrain, ClassCat=xclassCat)
        logger.info(f"Saving car {xObj}")
        result = gtdbV3.addCar(d1, xObj)
        logger.info(f"result: {result}")
        self.assertNotEqual(
            result[0], 0, "Failed: Add Car : Manufacture id=0. Car should not have been saved")

        logger.info("Testing Add Car : DriveTrain id does not exist")
        # Alter drivetrain.id so number does not exist
        xdriveTrain = GT.DriveTrain(id=9999, code='NA', desc='NA')
        xclassCat = GT.ClassCat(id=1, name='NA', desc='NA')
        xmfg = GT.Manufacture(id=1, name='NA', countryObj=xcountry)
        xObj = GT.Car(id=0, model='Test model name 9999', Manufacture=xmfg,
                      DriveTrain=xdriveTrain, ClassCat=xclassCat)
        logger.info(f"Saving car {xObj}")
        result = gtdbV3.addCar(d1, xObj)
        logger.info(f"result: {result}")
        self.assertNotEqual(
            result[0], 0, "Failed: Add Car : DriveTrain id does not exist. Car should not have been saved")

        logger.info("Testing Add Car : DriveTrain id = 0")
        # Alter drivetrain.id so its zero
        xdriveTrain = GT.DriveTrain(id=0, code='NA', desc='NA')
        xclassCat = GT.ClassCat(id=1, name='NA', desc='NA')
        xmfg = GT.Manufacture(id=1, name='NA', countryObj=xcountry)
        xObj = GT.Car(id=0, model='Test model name 9999', Manufacture=xmfg,
                      DriveTrain=xdriveTrain, ClassCat=xclassCat)
        logger.info(f"Saving car {xObj}")
        result = gtdbV3.addCar(d1, xObj)
        logger.info(f"result: {result}")
        self.assertNotEqual(
            result[0], 0, "Failed: Add Car : DriveTrain id = 0. Car should not have been saved")

        logger.info("Testing Add Car : cat Class id does not exist")
        xdriveTrain = GT.DriveTrain(id=1, code='NA', desc='NA')
        # Alter classcat.id so number does not exist
        xclassCat = GT.ClassCat(id=9999, name='NA', desc='NA')
        xmfg = GT.Manufacture(id=1, name='NA', countryObj=xcountry)
        xObj = GT.Car(id=0, model='Test model name 9999', Manufacture=xmfg,
                      DriveTrain=xdriveTrain, ClassCat=xclassCat)
        logger.info(f"Saving car {xObj}")
        result = gtdbV3.addCar(d1, xObj)
        logger.info(f"result: {result}")
        self.assertNotEqual(
            result[0], 0, "Failed: Add Car : cat Class id does not exist. Car should not have been saved")

        logger.info("Testing Add Car : cat Class id is 0")
        xdriveTrain = GT.DriveTrain(id=1, code='NA', desc='NA')
        # Alter classcat.id so number does not exist
        xclassCat = GT.ClassCat(id=9999, name='NA', desc='NA')
        xmfg = GT.Manufacture(id=1, name='NA', countryObj=xcountry)
        xObj = GT.Car(id=0, model='Test model name 9999', Manufacture=xmfg,
                      DriveTrain=xdriveTrain, ClassCat=xclassCat)
        logger.info(f"Saving car {xObj}")
        result = gtdbV3.addCar(d1, xObj)
        logger.info(f"result: {result}")
        self.assertNotEqual(
            result[0], 0, "Failed: Add Car : cat Class id is 0. Car should not have been saved")

        logger.info("Testing Add Car : Model Name is None")
        xdriveTrain = GT.DriveTrain(id=1, code='NA', desc='NA')
        xclassCat = GT.ClassCat(id=1, name='NA', desc='NA')
        xmfg = GT.Manufacture(id=1, name='NA', countryObj=xcountry)
        xObj = GT.Car(id=0, model=None, Manufacture=xmfg,
                      DriveTrain=xdriveTrain, ClassCat=xclassCat)
        logger.info(f"Saving car {xObj}")
        result = gtdbV3.addCar(d1, xObj)
        logger.info(f"result: {result}")
        self.assertNotEqual(
            result[0], 0, "Failed: Add Car : Model Name is None. Car should not have been saved")

        logger.info("Testing Add Car : Model Name is ''")
        xdriveTrain = GT.DriveTrain(id=1, code='NA', desc='NA')
        xclassCat = GT.ClassCat(id=1, name='NA', desc='NA')
        xmfg = GT.Manufacture(id=1, name='NA', countryObj=xcountry)
        xObj = GT.Car(id=0, model='', Manufacture=xmfg,
                      DriveTrain=xdriveTrain, ClassCat=xclassCat)
        logger.info(f"Saving car {xObj}")
        result = gtdbV3.addCar(d1, xObj)
        logger.info(f"result: {result}")
        self.assertNotEqual(
            result[0], 0, "Failed: Add Car : Model Name is ''. Car should not have been saved")

        logger.info("Testing Add Car : Model Name not unique")
        xdriveTrain = GT.DriveTrain(id=1, code='NA', desc='NA')
        xclassCat = GT.ClassCat(id=1, name='NA', desc='NA')
        # test_carData.sql data has model='Test Car B' and mfg_id=10.
        #    using that existing info for testing
        xmfg = GT.Manufacture(id=10, name='NA', countryObj=xcountry)
        xObj = GT.Car(id=0, model='Test Car B', Manufacture=xmfg,
                      DriveTrain=xdriveTrain, ClassCat=xclassCat)
        logger.info(f"Saving car {xObj}")
        result = gtdbV3.addCar(d1, xObj)
        self.assertNotEqual(
            result[0], 0, "Failed: Add Car : Model Name not unique. Record should not have been saved")

        logger.info("Testing Add Car : Year is text")
        xdriveTrain = GT.DriveTrain(id=1, code='NA', desc='NA')
        xclassCat = GT.ClassCat(id=1, name='NA', desc='NA')
        xmfg = GT.Manufacture(id=10, name='NA', countryObj=xcountry)
        xObj = GT.Car(id=0, model='Test model name 9999', Manufacture=xmfg,
                      DriveTrain=xdriveTrain, ClassCat=xclassCat)
        xObj.year = "ABC"
        logger.info(f"Saving car {xObj}")
        result = gtdbV3.addCar(d1, xObj)
        self.assertNotEqual(
            result[0], 0, "Failed: Add Car : Testing Add Car : Year is text. Record should not have been saved")

        logger.info("Testing Add Car : Valid Car")
        xdriveTrain = GT.DriveTrain(id=1, code='NA', desc='NA')
        xclassCat = GT.ClassCat(id=1, name='NA', desc='NA')
        xmfg = GT.Manufacture(id=10, name='NA', countryObj=xcountry)
        xObj = GT.Car(id=0, model='Test model name 9999', Manufacture=xmfg,
                      DriveTrain=xdriveTrain, ClassCat=xclassCat)
        xObj.year = 123
        logger.info(f"Saving car {xObj}")
        result = gtdbV3.addCar(d1, xObj)
        self.assertEqual(
            result[0], 0, "Failed: Add Car : Valid Car. Record should have been saved")

        logger.info("==== END BEGIN add car tests===")


class TestCar_Get(unittest.TestCase):
    def setUp(self):
        self.testDb = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(self.testDb, scriptPath=f'{_gtScripts}')
        # init car table createUserTables.sql
        gtdbV3._exeScriptFile(self.testDb, scriptFileName=_gtScripts /
                              'createUserTables.sql')
        # Load test car data
        gtdbV3._exeScriptFile(self.testDb, scriptFileName=_gtPath /
                              'tests' / 'test_carData.sql')

    def tearDown(self):
        self.testDb.close()

    def test_getCar(self):
        logger.info("==== BEGIN testing getCar method")
        logger.info("Get existing car by id")
        testVal = 1
        logger.info(f"Getting carId = {testVal}")
        xObj = gtdbV3.getCar(self.testDb, id=testVal)
        logger.info(f"Returned: {xObj}")
        self.assertEqual(
            xObj.id, 1, "Failed Get existing car by id. Expecting car Id=1")

        logger.info("Get NON existing car by id")
        testVal = 999
        logger.info(f"Getting carId = {testVal}")
        xObj = gtdbV3.getCar(self.testDb, id=testVal)
        logger.info(f"Returned: {xObj}")
        self.assertEqual(
            xObj.id, 0, "Failed Get NON existing car by id. Expecting car id = 0")

        logger.info("==== END testing getCar method")

    def test_getCarList(self):
        logger.info("==== BEGIN testing getCarList method")
        logger.info("Get car list by name")
        result = gtdbV3.getCarList(self.testDb, mfgID=3, sortBy="name")
        self.assertGreaterEqual(
            len(result), 1, "Failed Get car list by name. Should have at minimum 1 row")

        logger.info("Get car list by year")
        result = gtdbV3.getCarList(self.testDb, mfgID=3, sortBy="year")
        self.assertGreaterEqual(
            len(result), 1, "Failed Get car list by year. Should have at minimum 1 row")

        logger.info("Get car list by ClassCat")
        result = gtdbV3.getCarList(self.testDb, mfgID=3, sortBy="ClassCat")
        self.assertGreaterEqual(
            len(result), 1, "Failed Get car list by ClassCat. Should have at minimum 1 row")

        logger.info("Get car list by drivetrain")
        result = gtdbV3.getCarList(self.testDb, mfgID=3, sortBy="drivetrain")
        self.assertGreaterEqual(
            len(result), 1, "Failed Get car list by drivetrain. Should have at minimum 1 row")

        logger.info("Get car list by something")
        result = gtdbV3.getCarList(self.testDb, mfgID=3, sortBy="something")
        self.assertGreaterEqual(
            len(result), 1, "Failed Get car list by something. Should have at minimum 1 row")


class TestCarCat(unittest.TestCase):
    def test_getCarCats(self):
        logger.info("==== BEGIN Get Car category tests")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Getting a list of car category/classes")
        testVal = 1  # First row, first element should be this
        testList = gtdbV3.getCarCatList(d1)
        logger.info(f"testList = {testList}")
        self.assertEqual(testList[0][0], testVal,
                         "Failed getting car category and classes")

        logger.info("Getting first Car Category")
        testVal = 1
        test = gtdbV3.getCarCat(d1, testVal)
        logger.info(f"Car Category = {test}")
        self.assertEqual(test.id, testVal, "Failed to get CarCat id 1")

        logger.info("Testing for not found Car Category ")
        testVal = 99999
        test = gtdbV3.getCarCat(d1, testVal)
        logger.info(f"Car Category = {test}")
        self.assertEqual(test.id, 0, "Failed not found CarCat id")

        logger.info("==== END Get Car category tests")


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


class TestCarSetting(unittest.TestCase):
    def test_addCarSetting(self):
        logger.info("===== BEGIN testing add Car setting")
        d1 = gtdbV3.create_connection(":memory:")
        # d1 = gtdbV3.create_connection(_gtPath / 'Data' / 'testdb.db')
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        # init user tables
        gtdbV3._exeScriptFile(d1, scriptFileName=_gtScripts /
                              'createUserTables.sql')
        # Load car test data
        gtdbV3._exeScriptFile(d1, scriptFileName=_gtPath /
                              'tests' / 'test_carData.sql')

        logger.info("TEST Add CarSetting: Duplicate name for same Car ID")
        testVal = 'IB3F0SK1'
        xObj = GT.CustCarSettings(id=0,car_id=1,name=testVal,cat_id=1)
        logger.info(f"xObj={xObj.__dict__}")
        result = gtdbV3.addCarSetting(d1, xObj)
        logger.info(f"Valiation result={result}")
        self.assertEqual(
            result[0], 1, "Failed: Add CarSetting: Duplicate name for Car ID. Record should not have been saved")

        logger.info(
            "TEST Add CarSetting: Duplicate name for Car ID testing trim")
        testVal = 'IB3F0SK1    '
        xObj = GT.CustCarSettings(id=0,car_id=1,name=testVal,cat_id=1)
        result = gtdbV3.addCarSetting(d1, xObj)
        logger.info(f"result={result}")
        self.assertEqual(
            result[0], 1, "Failed: Add CarSetting: Duplicate name for Car ID testing trim. Record should not have been saved")

        logger.info("TEST Add CarSetting: car_id does not exist")
        xObj = GT.CustCarSettings(id=0,car_id=99999,name='I should not save',cat_id=1)
        result = gtdbV3.addCarSetting(d1, xObj)
        logger.info(f"result={result}")
        self.assertEqual(
            result[0], 1, "Failed: Add CarSetting: car_id does not exist. Record should not have been saved")

        logger.info("TEST Add CarSetting: cat_id does not exist")
        xObj = GT.CustCarSettings(id=0,car_id=1,name='I should not save',cat_id=999)
        result = gtdbV3.addCarSetting(d1, xObj)
        logger.info(f"result={result}")
        self.assertEqual(
            result[0], 1, "Failed: Add CarSetting: cat_id does not exist. Record should not have been saved")

        logger.info("TEST Add CarSetting: tire_code does not exist")
        xObj = GT.CustCarSettings(id=0,car_id=1,name='I should not save',cat_id=1)
        xObj.tire_code="ZZZZZZ"
        result = gtdbV3.addCarSetting(d1, xObj)
        logger.info(f"result={result}")
        self.assertEqual(
            result[0], 1, "Failed: Add CarSetting: tire_code does not exist. Record should not have been saved")

        logger.info("TEST Add CarSetting: Minimum required to create a record")
        xObj = GT.CustCarSettings(id=0,car_id=2,name='Here are just the mandatory values',cat_id=1)
        result = gtdbV3.addCarSetting(d1, xObj)
        logger.info(f"result={result}")
        self.assertEqual(
            result[0], 0, "Failed: Add CarSetting: Minimum required to create a record. Record should have been saved")

        logger.info("TEST Add CarSetting: All Properties have values - Valid record")
        xObj = GT.CustCarSettings(id=0,car_id=1,name='I should be able to be saved',cat_id=1)
        xObj.accel = 9.23
        xObj.brake_balance=-2
        xObj.braking = 4.0
        xObj.cornering = 2.10
        xObj.final_gear="8.888"
        xObj.gear_1="1.000/1"
        xObj.gear_2="2.001/2"
        xObj.gear_3="3.020/3"
        xObj.gear_4="4.300/4"
        xObj.gear_5="5.304/5"
        xObj.gear_6="6.060/6"
        xObj.gear_7="7.070/7"
        xObj.max_power=100
        xObj.max_speed = 123.45
        xObj.max_torque=876.5
        xObj.power_ratio=90
        xObj.stability = 123.45
        xObj.tire_code="RH"
        xObj.top_speed=1000
        xObj.traction_control=-1
        xObj.weight=12345
        xObj.weight_reduction=80
        result = gtdbV3.addCarSetting(d1, xObj)
        logger.info(f"result={result}")
        self.assertEqual(
            result[0], 0, "Failed: Add CarSetting: All Properties have values - Valid record. Record should have been saved")

    def test_delCarSetting(self):
        logger.info("===== BEGIN testing delete Car settings")
        d1 = gtdbV3.create_connection(":memory:")
        # d1 = gtdbV3.create_connection(_gtPath / 'Data' / 'testdb.db')
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        # init user tables
        gtdbV3._exeScriptFile(d1, scriptFileName=_gtScripts /
                              'createUserTables.sql')
        # Load car test data
        gtdbV3._exeScriptFile(d1, scriptFileName=_gtPath /
                              'tests' / 'test_carData.sql')

        logger.info("TEST deleting non existing CarSetting")
        result = gtdbV3.deleteCarSetting(d1,id=99999)
        logger.info(f"Returned result = {result}")
        self.assertNotEqual(result[0],0, "Failed: Delete non existing CarSetting: Should not get a success result code")

        logger.info("TEST deleting existing CarSetting")
        result = gtdbV3.deleteCarSetting(d1,id=1)
        logger.info(f"Returned result = {result}")
        self.assertEqual(result[0],0, "Failed: Delete existing CarSetting: Expecting a success result")

    def test_getCarSetting(self):
        logger.info("===== BEGIN testing get Car setting")
        d1 = gtdbV3.create_connection(":memory:")
        # d1 = gtdbV3.create_connection(_gtPath / 'Data' / 'testdb.db')
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        # init user tables
        gtdbV3._exeScriptFile(d1, scriptFileName=_gtScripts /
                              'createUserTables.sql')
        # Load car test data
        gtdbV3._exeScriptFile(d1, scriptFileName=_gtPath /
                              'tests' / 'test_carData.sql')

        logger.info("TEST Get non existing CarSetting")
        testVal = 999999
        xObj = gtdbV3.getCarSetting(d1,id=testVal)
        logger.info(f"CustCarSetting Object={xObj.__dict__}")
        self.assertEqual(xObj.id,0, "Failed Get non existing CarSetting.")

        logger.info("TEST Get existing CarSetting")
        testVal = 1
        xObj = gtdbV3.getCarSetting(d1,id=testVal)
        logger.info(f"CustCarSetting Object={xObj.__dict__}")
        self.assertEqual(xObj.id,1, "Failed Get existing CarSetting.")

    def test_updateCarSetting(self):
        logger.info("===== BEGIN testing update Car setting. Assumption getCarSetting works")
        d1 = gtdbV3.create_connection(":memory:")
        # d1 = gtdbV3.create_connection(_gtPath / 'Data' / 'testdb.db')
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        # init user tables
        gtdbV3._exeScriptFile(d1, scriptFileName=_gtScripts /
                              'createUserTables.sql')
        # Load car test data
        gtdbV3._exeScriptFile(d1, scriptFileName=_gtPath /
                              'tests' / 'test_carData.sql')

        logger.info("Update CarSetting: Duplicate name for same Car ID ")
        logger.info("Getting dummy data")
        dummyData = gtdbV3.getCarSetting(d1,id=1)
        logger.info("Getting car setting id 5 to change")
        xObj = gtdbV3.getCarSetting(d1,id=5)
        logger.info(f"Before memory Change = {xObj.__dict__}")
        xObj.car_id = dummyData.car_id
        xObj.name = dummyData.name
        logger.info(f"After memory Change = {xObj.__dict__}")
        logger.info(f"Attempt update")
        retVal = gtdbV3.updateCarSetting(d1,xObj)
        logger.info(f"return value = {retVal}")
        self.assertNotEqual(retVal[0],0,"Failed: Update CarSetting. CarSetting name is same for carID therefore should not be saved")

        logger.info("Update CarSetting: car_id does not exist")
        logger.info("Getting dummy data")
        dummyData = gtdbV3.getCarSetting(d1,id=1)
        logger.info("Getting car setting id 5 to change")
        xObj = gtdbV3.getCarSetting(d1,id=5)
        logger.info(f"Before memory Change = {xObj.__dict__}")
        xObj.car_id = 9999999
        xObj.name = "This car setting should not be saved"
        logger.info(f"After memory Change = {xObj.__dict__}")
        logger.info(f"Attempt update")
        retVal = gtdbV3.updateCarSetting(d1,xObj)
        logger.info(f"return value = {retVal}")
        self.assertNotEqual(retVal[0],0, "Failed: Update CarSetting: car_id does not exist. Record should not have been saved")

        logger.info("Update CarSetting: cat_id does not exist")
        logger.info("Getting dummy data")
        dummyData = gtdbV3.getCarSetting(d1,id=1)
        logger.info("Getting car setting id 5 to change")
        xObj = gtdbV3.getCarSetting(d1,id=5)
        logger.info(f"Before memory Change = {xObj.__dict__}")
        xObj.cat_id = 99999
        logger.info(f"After memory Change = {xObj.__dict__}")
        logger.info(f"Attempt update")
        retVal = gtdbV3.updateCarSetting(d1,xObj)
        logger.info(f"return value = {retVal}")
        self.assertNotEqual(retVal[0],0, "Failed: Update CarSetting: cat_id does not exist. Record should not have been saved")

        logger.info("Update CarSetting: tire_code does not exist")
        logger.info("Getting dummy data")
        dummyData = gtdbV3.getCarSetting(d1,id=1)
        logger.info("Getting car setting id 5 to change")
        xObj = gtdbV3.getCarSetting(d1,id=5)
        logger.info(f"Before memory Change = {xObj.__dict__}")
        xObj.tire_code = "AZZ"
        logger.info(f"After memory Change = {xObj.__dict__}")
        logger.info(f"Attempt update")
        retVal = gtdbV3.updateCarSetting(d1,xObj)
        logger.info(f"return value = {retVal}")
        self.assertNotEqual(retVal[0],0, "Failed: Update CarSetting: tire_code does not exist")

        logger.info("Update CarSetting: Valid change - Name change")
        logger.info("Getting dummy data")
        dummyData = gtdbV3.getCarSetting(d1,id=1)
        logger.info("Getting car setting id 5 to change")
        xObj = gtdbV3.getCarSetting(d1,id=5)
        logger.info(f"Before memory Change = {xObj.__dict__}")
        xName = "My Name is being changed"
        xObj.name = xName
        logger.info(f"After memory Change = {xObj.__dict__}")
        logger.info(f"Attempt update")
        retVal = gtdbV3.updateCarSetting(d1,xObj)
        logger.info(f"return value = {retVal}")
        self.assertEqual(retVal[0],0, "Failed: Update CarSetting: Name changed update failed")
        logger.info("Confirm commited to db")
        tempObj = gtdbV3.getCarSetting(d1,id=5)
        logger.info(f"From db = {xObj.__dict__}")
        self.assertEqual(tempObj.name,xName, "Failed: Update CarSetting: get from db different")

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


class TestDriveTrain(unittest.TestCase):
    def test_getDriveTrain(self):
        logger.info("==== BEGIN Get Drivetrain")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Get existing Drivetrain by id")
        testVal = 1
        xObj = gtdbV3.getDriveTrain(d1, id=testVal)
        logger.info(f"Returned: {xObj}")
        self.assertEqual(
            xObj.id, 1, "Failed Get existing Drivetrain by id. Expecting id=1")

        logger.info("Get non existing Drivetrain by id")
        testVal = 999
        xObj = gtdbV3.getDriveTrain(d1, id=testVal)
        logger.info(f"Returned: {xObj}")
        self.assertEqual(
            xObj.id, 0, "Failed Get non existing Drivetrain by id. Expecting id=0")


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

    def test_getLeagueList(self):
        logger.info("==== BEGIN Get League List")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testList = gtdbV3.getLeagueList(d1)
        # Test for more than 1 row
        logger.info("Checking to be sure more than one row is returned")
        self.assertGreater(
            len(testList), 1, "Failed Get League List. returned zero rows")


class TestMfg(unittest.TestCase):

    def test_addMfg(self):
        """Test various adding a manufacture scenerios
        """
        logger.info(
            "==== BEGIN Add Manufacture (Requirements: Name is unique. Required to have a country)")
        d1 = gtdbV3.create_connection(":memory:")

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Existing")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        mfgName = 'NEW Manufacture'
        testMfg = GT.Manufacture(
            id=0, name=mfgName, countryObj=GT.Country(cntryID=235, cntryName='United Kingdom of Great Britain and Northern Ireland', alpha2='GB', alpha3='GBR', region='Europe'))
        result = gtdbV3.addMfg(d1, testMfg)
        logger.info(f"result is {result}")
        self.assertEqual(
            result[0], 0, "Failed: Add Manufacture - Name: Non-Existing, Country ID: Existing. Record should have been saved")

        logger.info("Add Manufacture - Name: Existing, Country ID: Existing")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        mfgName = 'Honda'
        testMfg = GT.Manufacture(
            id=0, name=mfgName, countryObj=GT.Country(cntryID=235, cntryName='United Kingdom of Great Britain and Northern Ireland', alpha2='GB', alpha3='GBR', region='Europe'))
        result = gtdbV3.addMfg(d1, testMfg)
        self.assertNotEqual(
            result[0], 0, "Failed: Add Manufacture - Name: Existing, Country ID: Existing - Record should not have been saved")

        logger.info(
            "Add Manufacture - Name: Existing (all caps), Country ID: Existing")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        mfgName = 'HONDA'
        testMfg = GT.Manufacture(
            id=0, name=mfgName, countryObj=GT.Country(cntryID=235, cntryName='United Kingdom of Great Britain and Northern Ireland', alpha2='GB', alpha3='GBR', region='Europe'))
        result = gtdbV3.addMfg(d1, testMfg)
        self.assertNotEqual(
            result[0], 0, "Failed: Add Manufacture - Name: Existing (all caps), Country ID: Existing - Record should not have been saved")

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Non-Existing")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        mfgName = 'NEW manufacture'
        testMfg = GT.Manufacture(
            id=0, name=mfgName, countryObj=GT.Country(cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None))
        result = gtdbV3.addMfg(d1, testMfg)
        self.assertNotEqual(
            result[0], 0, "Failed: Add Manufacture - Name: Non-Existing, Country ID: Non-Existing. Record should not have been saved")

        logger.info("Add Manufacture - Name: Existing, Country ID: Null/None")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        mfgName = 'Honda'
        testMfg = GT.Manufacture(
            id=0, name=mfgName, countryObj=GT.Country(cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None))
        result = gtdbV3.addMfg(d1, testMfg)
        self.assertNotEqual(
            result[0], 0, "Failed: Add Manufacture - Name: Existing, Country ID: Null/None. Record should not have been saved")

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Null/None")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        mfgName = 'new Manufacture'
        testMfg = GT.Manufacture(
            id=0, name=mfgName, countryObj=GT.Country(cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None))
        result = gtdbV3.addMfg(d1, testMfg)
        self.assertNotEqual(
            result[0], 0, "Failed: Add Manufacture - Name: Non-Existing, Country ID: Null/None. Record should not have been saved")

        logger.info(
            "Add Manufacture - Name: Non-Existing, Country ID: Non-Existing")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        mfgName = 'Another new one that should fail'
        testMfg = GT.Manufacture(
            id=0, name=mfgName, countryObj=GT.Country(cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None))
        result = gtdbV3.addMfg(d1, testMfg)
        self.assertNotEqual(
            result[0], 0, "Failed: Add Manufacture - Name: Non-Existing, Country ID: Non-Existing. Record should not have been saved")

    def test_deleteMfg(self):
        logger.info("==== BEGIN Delete Manufacture")
        d1 = gtdbV3.create_connection(":memory:")

        logger.info("Delete Manufacture = Manufacture ID: Non Existing")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        mfgId = 999999
        result = gtdbV3.deleteMfg(d1, mfgId)
        # Sqlite.. the delete works, even if record doesn't exist.
        self.assertEqual(result[0], 0)

        logger.info("Delete Manufacture = Manufacture ID: Existing")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        mfgId = 1
        result = gtdbV3.deleteMfg(d1, mfgId)
        self.assertEqual(
            result[0], 0, "Failed: Delete Manufacture = Manufacture ID: Existing")

        logger.info("==== END Delete Manufacture\n")

    def test_getMfg(self):
        logger.info("==== BEGIN Get/read Manufacture")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        logger.info("Get Manufacture by id")
        mfgId = 4
        testMfg = gtdbV3.getMfg(d1, value=mfgId)
        self.assertEqual(testMfg.id, mfgId)

        logger.info("Get Manufacture by all name (case insensitve")
        mfgName = 'honda'
        testMfg = gtdbV3.getMfg(d1, key='Make', value=mfgName)
        self.assertNotEqual(testMfg.id, 0)

        logger.info("Get non exist Manfuacture by id")
        mfgId = 99999
        testMfg = gtdbV3.getMfg(d1, value=mfgId)
        self.assertEqual(testMfg.id, 0)

        logger.info("Get non exist Manfuacture by name")
        mfgName = 'ZZINoExist'
        testMfg = gtdbV3.getMfg(d1, key='Make', value=mfgName)
        self.assertEqual(testMfg.id, 0)

        logger.info(f"==== END Get/read Manufacture\n")

    def test_updateMfg(self):
        logger.info(
            "==== BEGIN UPDATE Manufacture (Assuming Get manufacture works)")
        d1 = gtdbV3.create_connection(":memory:")

        logger.info(
            "Update Manufacture: Name: Change, Country ID: No change.")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        mfgName = "MY new NAME"
        testMfg = gtdbV3.getMfg(d1, value=1)
        testMfg.name = mfgName
        result = gtdbV3.updateMfg(d1, testMfg)
        self.assertEqual(result[0], 0)
        # Need to confirm it was saved to db
        logger.info("Confirming update saved in db")
        testMfg = gtdbV3.getMfg(d1, key='Make', value=mfgName)
        self.assertEqual(testMfg.name, mfgName)
        self.assertNotEqual(testMfg.id, 0)

        logger.info(
            "Update Manufacture: Name: No Change, Country ID: Change to null.")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testMfg = gtdbV3.getMfg(d1, value=4)
        testMfg.country = GT.Country(
            cntryID=None, cntryName=None, alpha2=None, alpha3=None, region=None)
        result = gtdbV3.updateMfg(d1, testMfg)
        self.assertNotEqual(result[0], 0)

        logger.info(
            "Update Manufacture: Name: Change, Country ID: No Change, Mfg ID: Non Existing.")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testMfg = gtdbV3.getMfg(d1, value=14)
        testMfg.id = 99999
        result = gtdbV3.updateMfg(d1, testMfg)
        self.assertNotEqual(result[0], 0)

        logger.info(
            "Update Manufacture: Name: Change to Existing, Country ID: No change ")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        xMfg = gtdbV3.getMfg(d1, value=3)
        testMfg = gtdbV3.getMfg(d1, value=14)
        testMfg.name = xMfg.name
        result = gtdbV3.updateMfg(d1, testMfg)
        self.assertNotEqual(result[0], 0)

        logger.info(
            "Update Manufacture: Name: No change, Country ID: Change to Non Existing")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testMfg = gtdbV3.getMfg(d1, value=14)
        testMfg.country = GT.Country(
            cntryID=999, cntryName=None, alpha2=None, alpha3=None, region=None)
        result = gtdbV3.updateMfg(d1, testMfg)
        self.assertNotEqual(result[0], 0)

    def test_getMfgList(self):
        logger.info("==== BEGIN get mfg List")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Testing more than 5 rows are return")
        testList = gtdbV3.getMfgList(d1)
        logger.info(f"layoutList={testList}")
        self.assertGreaterEqual(len(testList), 5,
                                "Failed: Manufacture list should be 5 or greater rows")


class TestRaceCollection(unittest.TestCase):

    def test_addRaceCollection(self):
        logger.info("=== BEGIN Add RaceCollection testing")
        d1 = gtdbV3.create_connection(":memory:")
        existingLeague = GT.League(id=1, name='NA', sortord=0)

        # Add with existing name for league
        # Note- League 1 should have race collection = "Clubman Cup"
        logger.info(
            "Add Race Collection : name existing for League")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testCollection = GT.RaceCollection(
            id=0, name="Clubman Cup", desc="", leagueObj=existingLeague)
        logging.info(f"Saving collection={testCollection}")
        result = gtdbV3.addRaceCollection(d1, testCollection)
        logger.info(f"result is {result}")
        self.assertNotEqual(
            result[0], 0, "Failed. Add Race Collection : name existing for League")

        # Add Collection name is null
        logger.info(
            "Add Race Collection : name=None, League=existing")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testCollection = GT.RaceCollection(
            id=0, name=None, desc="", leagueObj=existingLeague)
        logging.info(f"Saving collection={testCollection}")
        result = gtdbV3.addRaceCollection(d1, testCollection)
        logger.info(f"result is {result}")
        self.assertNotEqual(
            result[0], 0, "Failed. Add Race Collection : name=None, League=existing")

        # Add collection with name=""
        logger.info(
            "Add Race Collection : name='', League=existing")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testCollection = GT.RaceCollection(
            id=0, name="", desc="", leagueObj=existingLeague)
        logging.info(f"Saving collection={testCollection}")
        result = gtdbV3.addRaceCollection(d1, testCollection)
        logger.info(f"result is {result}")
        self.assertNotEqual(
            result[0], 0, "Failed. Add Race Collection : name='', League=existing")

        # Add with existing collection ID
        #    -Not tested as the collection id provided in the collection object
        #     is ignored/not used. The SQL to add/insert the collection object
        #     does not provide the id and sqlite will auto increment

        # Add with with non existing league id >0
        logger.info(
            "Add Race Collection : Non existing League using 9999")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        xLeague = GT.League(id=99999, name='NA', sortord=0)
        testCollection = GT.RaceCollection(
            id=0, name="I am brand new", desc="", leagueObj=xLeague)
        logging.info(f"Saving collection={testCollection}")
        result = gtdbV3.addRaceCollection(d1, testCollection)
        logger.info(f"result is {result}")
        self.assertNotEqual(
            result[0], 0, "Failed. Add Race Collection : Non existing League using 9999")

        # Add with with league id 0
        logger.info(
            "Add Race Collection : League ID 0")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        xLeague = GT.League(id=0, name='NA', sortord=0)
        testCollection = GT.RaceCollection(
            id=0, name="I am brand new", desc="", leagueObj=xLeague)
        logging.info(f"Saving collection={testCollection}")
        result = gtdbV3.addRaceCollection(d1, testCollection)
        logger.info(f"result is {result}")
        self.assertNotEqual(
            result[0], 0, "Failed. Add Race Collection : League ID 0")

        # Add race collection where ClassCat id has no match
        logger.info("Add Race Collection: Class Cateogry does not exist")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        goodCollection = GT.RaceCollection(
            id=0, name="I am brand new", desc="", leagueObj=existingLeague)
        goodCollection.classcat.id = 99999
        logging.info(f"Saving collection={goodCollection}")
        result = gtdbV3.addRaceCollection(d1, goodCollection)
        logger.info(f"result is {result}")
        self.assertNotEqual(
            result[0], 0, "Failed: Add Race Collection: Class Cateogry does not exist")

        # Add race collection that should work
        logger.info(
            "Add Race Collection : non existant name, existing League")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        goodCollection = GT.RaceCollection(
            id=0, name="I am brand new", desc="", leagueObj=existingLeague)
        logging.info(f"Saving collection={goodCollection}")
        result = gtdbV3.addRaceCollection(d1, goodCollection)
        logger.info(f"result is {result}")
        self.assertEqual(
            result[0], 0, "Failed: Add Race Collection : non existant name, existing League")

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


class TestRace(unittest.TestCase):

    def test_addRace(self):
        logger.info("==== BEGIN Add Race")
        d1 = gtdbV3.create_connection(":memory:")
        country = GT.Country(cntryID=1, cntryName="Testing",
                             alpha2=None, alpha3=None, region=None)
        circuit = GT.Circuit(id=1, name="Testing")
        weather = GT.Weather(id=1, name="Testing")
        league = GT.League(id=1, name="Testing", sortord=1)
        raceType = GT.RaceType(id=1, name="Test")
        track = GT.Track(id=1, name="Testing", countryObj=country)
        raceCollection = GT.RaceCollection(
            id=1, name="Testing", desc=None, leagueObj=league)
        tLayout = GT.TrackLayout(
            id=1, name="TestTrace", miles=1, trackObj=track, circuitObj=circuit)

        logger.info("Add Race : Race name must be unique for Race Collection")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        # Have to successfully save a test Race for this dupe testing
        setupRace = GT.Race(id=900,
                            name="Testing Race",
                            trackLayout=tLayout,
                            raceCollection=raceCollection,
                            raceType=raceType,
                            weather=weather)
        xRace = GT.Race(id=999,
                        name="Testing Race",
                        trackLayout=tLayout,
                        raceCollection=raceCollection,
                        raceType=raceType,
                        weather=weather)
        logger.info(f"Setup existing race setupRace={setupRace}")
        result = gtdbV3.addRace(d1, setupRace)
        logger.info(f"result={result}")
        if result[0] != 0:
            logger.info(
                f"Can not test for unique race name. Unable to save a unique test race")
            self.assertEqual(
                result[0], 0, "Unable to test Add Race : Race name must be unique for Race Collection, because test case could not be setup")
        else:
            logger.info(f"Saving race with dupe name xRace={xRace}")
            result = gtdbV3.addRace(d1, xRace)
            logger.info(f"result={result}")
            self.assertNotEqual(
                result[0], 0, "Failed Add Race : Race name must be unique for Race Collection")

        # Test Add Race with None/null race name
        logger.info("Add Race : Race name None/Null")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        xRace = GT.Race(id=999,
                        name=None,
                        trackLayout=tLayout,
                        raceCollection=raceCollection,
                        raceType=raceType,
                        weather=weather)
        logger.info(f"xRace={xRace}")
        result = gtdbV3.addRace(d1, xRace)
        logger.info(f"result={result}")
        self.assertNotEqual(
            result[0], 0, f"Failed Add Race : Race name None/Null test")

        logger.info("Add Race : Race name blank")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        xRace = GT.Race(id=999,
                        name="",
                        trackLayout=tLayout,
                        raceCollection=raceCollection,
                        raceType=raceType,
                        weather=weather)
        logger.info(f"xRace={xRace}")
        result = gtdbV3.addRace(d1, xRace)
        logger.info(f"result={result}")
        self.assertNotEqual(
            result[0], 0, f"Failed Add Race : Race name blank test")

        logger.info("Add Race : weather.id=0")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        badweather = GT.Weather(id=0, name="Testing")
        xRace = GT.Race(id=999,
                        name="Test Race",
                        trackLayout=tLayout,
                        raceCollection=raceCollection,
                        raceType=raceType,
                        weather=badweather)
        logger.info(f"xRace={xRace}")
        result = gtdbV3.addRace(d1, xRace)
        logger.info(f"result={result}")
        self.assertNotEqual(
            result[0], 0, "Failed Add Race with weather.id = 0")

        # Test Add Race with non exisitng weather.id (Not Allowed)
        logger.info("Add Race : non existing weather.id")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        badweather = GT.Weather(id=999, name="Testing")
        xRace = GT.Race(id=999,
                        name="Test Race",
                        trackLayout=tLayout,
                        raceCollection=raceCollection,
                        raceType=raceType,
                        weather=badweather)
        logger.info(f"xRace={xRace}")
        result = gtdbV3.addRace(d1, xRace)
        logger.info(f"result={result}")
        self.assertNotEqual(
            result[0], 0, "Failed Add Race with non existing weather.id.")

        logger.info("Add Race : non trackLayout.id=0")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        badtLayout = GT.TrackLayout(
            id=0, name="TestTrace", miles=1, trackObj=track, circuitObj=circuit)
        xRace = GT.Race(id=999,
                        name="Test Race",
                        trackLayout=badtLayout,
                        raceCollection=raceCollection,
                        raceType=raceType,
                        weather=weather)
        logger.info(f"xRace={xRace}")
        result = gtdbV3.addRace(d1, xRace)
        logger.info(f"result={result}")
        self.assertNotEqual(
            result[0], 0, "Failed Add Race : non trackLayout.id=0")

        logger.info("Add Race : non existing trackLayout.id")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        badtLayout = GT.TrackLayout(
            id=9999, name="TestTrace", miles=1, trackObj=track, circuitObj=circuit)
        xRace = GT.Race(id=999,
                        name="Test Race",
                        trackLayout=badtLayout,
                        raceCollection=raceCollection,
                        raceType=raceType,
                        weather=weather)
        logger.info(f"xRace={xRace}")
        result = gtdbV3.addRace(d1, xRace)
        logger.info(f"result={result}")
        self.assertNotEqual(
            result[0], 0, "Failed Add Race : non existing trackLayout.id")

        logger.info("Add Race : raceType.id=0")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        badraceType = GT.RaceType(id=0, name="Test")
        xRace = GT.Race(id=999,
                        name="Test Race",
                        trackLayout=tLayout,
                        raceCollection=raceCollection,
                        raceType=badraceType,
                        weather=weather)
        logger.info(f"xRace={xRace}")
        result = gtdbV3.addRace(d1, xRace)
        logger.info(f"result={result}")
        self.assertNotEqual(
            result[0], 0, "Failed Add Race : raceType.id=0")

        logger.info("Add Race : raceType.id=999")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        badraceType = GT.RaceType(id=999, name="Test")
        xRace = GT.Race(id=999,
                        name="Test Race",
                        trackLayout=tLayout,
                        raceCollection=raceCollection,
                        raceType=badraceType,
                        weather=weather)
        logger.info(f"xRace={xRace}")
        result = gtdbV3.addRace(d1, xRace)
        logger.info(f"result={result}")
        self.assertNotEqual(
            result[0], 0, "Failed Add Race : raceType.id=999")

        logger.info("Add Race : race_collection.id=0")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        badraceCollection = GT.RaceCollection(
            id=0, name="Testing", desc=None, leagueObj=league)
        xRace = GT.Race(id=999,
                        name="Test Race",
                        trackLayout=tLayout,
                        raceCollection=badraceCollection,
                        raceType=raceType,
                        weather=weather)
        logger.info(f"xRace={xRace}")
        result = gtdbV3.addRace(d1, xRace)
        logger.info(f"result={result}")
        self.assertNotEqual(
            result[0], 0, "Failed Add Race : race_collection.id=0")

        # Test Add Race with non existing race_collection.id (Not Allowed)
        logger.info("Add Race : race_collection.id=999")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        badraceCollection = GT.RaceCollection(
            id=999, name="Testing", desc=None, leagueObj=league)
        xRace = GT.Race(id=999,
                        name="Test Race",
                        trackLayout=tLayout,
                        raceCollection=badraceCollection,
                        raceType=raceType,
                        weather=weather)
        logger.info(f"xRace={xRace}")
        result = gtdbV3.addRace(d1, xRace)
        logger.info(f"result={result}")
        self.assertNotEqual(
            result[0], 0, "Failed Add Race : race_collection.id=999")

    def test_getRace(self):
        logger.info("==== BEGIN Get Race")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Get Race : Existing Race by ID")
        testVal = 1
        logger.info(f"Race ID = {testVal}")
        xObj = gtdbV3.getRace(d1, testVal)
        logger.info(f"Result = {xObj}")
        self.assertEqual(
            xObj.id, testVal, f"Failed Get Race : Existing Race by ID. Should be {testVal}")

        logger.info("Get Race : Non Existing Race by ID")
        testVal = 999999
        logger.info(f"Race ID = {testVal}")
        xObj = gtdbV3.getRace(d1, testVal)
        logger.info(f"Result = {xObj}")
        self.assertEqual(
            xObj.id, 0, f"Failed Get Race : Non Existing Race by ID.")

        logger.info("==== END Get Race")


class TestRacetype(unittest.TestCase):
    def test_getRaceType(self):
        logger.info("==== BEGIN Get/read Race Type")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')

        logger.info("Getting a list of race types")
        testList = gtdbV3.getRaceTypeList(d1)
        logger.info(f"testList={testList}")
        self.assertGreater(
            len(testList), 1, "FAILED: Getting race type list. More than one race type should be returned")
        self.assertGreater(
            len(testList[0]), 1, "FAILED: Getting race type list. There should be at least 2 fields for each row")

        logger.info("Getting a race type")
        testRt = gtdbV3.getRaceType(d1, id=1)
        logger.info(f"testRt={testRt}")
        self.assertEqual(
            testRt.id, 1, "Failed: Getting a race type. Race type id = 1")

        logger.info("=== END Get/read Race Type")


class TestTireList(unittest.TestCase):
    def test_getTireList(self):
        logger.info("==== BEGIN TEST Tire List")
        d1 = gtdbV3.create_connection(":memory:")
        gtdbV3.initDB(d1, scriptPath=f'{_gtScripts}')
        testList = gtdbV3.getTireList(d1)
        logger.info(f"testList={testList}")
        self.assertGreaterEqual(
            len(testList), 1, "Failed - Tire List should have at least 1 record")


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
