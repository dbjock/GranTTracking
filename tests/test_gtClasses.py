# python -m unittest tests.test_gtClasses
# If you want to run specific tests:
# python -m unittest tests.test_gtClasses.Class.method
import unittest
from pathlib import Path
import logging
import os
import sys
from datetime import datetime

# App Testing requirements
from GranT import GTClasses as GT

_gtPath = Path.cwd()
# _gtLogs = _gtPath / 'Logs'
_gtLogs = Path("z:/logs")
_logfile = _gtLogs / f"Testing-Classes-{datetime.now().strftime('%Y%j-%H%M%S')}.log"

log = logging.getLogger()
log.setLevel(logging.DEBUG)
simpleFormat = logging.Formatter(
    ' %(levelname)-8s:%(name)s.%(funcName)s: %(message)s')
detailFormat = logging.Formatter(
    '%(asctime)s %(levelname)-8s:%(name)s.%(funcName)s: %(message)s')

# Log Handlers
conHandler = logging.StreamHandler()
conHandler.setFormatter(simpleFormat)
conHandler.setLevel(logging.CRITICAL)
log.addHandler(conHandler)

fileHandler = logging.FileHandler(_logfile)
fileHandler.setFormatter(detailFormat)
fileHandler.setLevel(logging.INFO)
log.addHandler(fileHandler)

print(f"Logging to {_logfile}")

class TestCustomCarSettings(unittest.TestCase):
    def test_brake_balance(self):
        log.info("==== BEGIN Testing - customCarSettings brake_balance")

        log.info("Test setting brake_balance to 0")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change brake_balance to 0')
        xObj.brake_balance = 0
        self.assertEqual(xObj.brake_balance,0,"Failed: setting brake_balance to 0 : Valid brake_balance value. object should have been created")

        log.info("Test setting brake_balance to -4")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change brake_balance to -4')
        xObj.brake_balance = -4
        self.assertEqual(xObj.brake_balance,-4,"Failed: setting brake_balance to -4 : Valid brake_balance value. object should have been created")

        log.info("Test setting brake_balance to a string")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change brake_balance to a string')
        with self.assertRaises(ValueError):
            xObj.brake_balance = "I am a string"

        log.info("Test setting brake_balance to an empty string")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change brake_balance to an empty string')
        self.assertEqual(xObj.brake_balance,None,"Failed: setting brake_balance to empty string : Valid brake_balance value. object should have been created and this is None")

        log.info("Test setting brake_balance to None")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change brake_balance to None')
        xObj.brake_balance = None
        self.assertEqual(xObj.brake_balance,None,"Failed: setting brake_balance to None : Valid brake_balance value. object should have been created")

    def test_cat_id(self):
        log.info("==== BEGIN Testing - customCarSettings cat_id")

        log.info('Creating with a cat_id as None')
        with self.assertRaises(ValueError):
            xObj = GT.CustCarSettings(id=9,car_id=9,name="I am a name", cat_id=None)

        log.info('Creating with cat_id as blank string')
        with self.assertRaises(ValueError):
            xObj = GT.CustCarSettings(id=9,car_id=9,name="I am a name", cat_id="")

        log.info('Creating with cat_id as a string')
        with self.assertRaises(ValueError):
            xObj = GT.CustCarSettings(id=9,car_id=9,name="I am a name", cat_id="I am a string")

        log.info('Creating with cat_id = 0')
        xObj = GT.CustCarSettings(id=9,car_id=9,name="I am a name", cat_id=0)
        self.assertEqual(xObj.cat_id,0,"Failed: customCarSetting.cat_id = 0 : Valid id. Object should have been created")

        log.info('Creating with cat_id = 999')
        # 999 is picked because its an int, and not zero
        xObj = GT.CustCarSettings(id=9,car_id=9,name="I am a name", cat_id=999)
        self.assertEqual(xObj.cat_id,999,"Failed: customCarSetting.cat_id = 999 : Valid id. Object should have been created")

        ######################################
        # Testing changing cat_id
        ######################################
        log.info('Change cat_id to None')
        # 999 is picked because its an int, and not zero
        log.debug('creating a good object')
        xObj = GT.CustCarSettings(id=9,car_id=9,name="I am a name", cat_id=999)
        log.info('Attempting to change cat_id to None')
        with self.assertRaises(ValueError):
            xObj.cat_id = None

        log.info('Change cat_id to blank string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=9,car_id=9,name="I am a name", cat_id=999)
        log.info('Attemtping to change id to blank string')
        with self.assertRaises(ValueError):
            xObj.cat_id = ""

        log.info('Change cat_id to string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=9,car_id=9,name="I am a name", cat_id=999)
        log.info('Attemtping to change cat_id to string')
        with self.assertRaises(ValueError):
            xObj.cat_id = "I am a string"

        log.info('Change cat_id to 0')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=9,car_id=9,name="I am a name", cat_id=999)
        log.info('Attemtping to change cat_id to 0')
        xObj.cat_id = 0
        self.assertEqual(xObj.cat_id,0,"Failed: change cat_id to 0 : Valid id. Object should have been changed")

        log.info('Change cat_id to 900')
        # 900 is picked for no specific reason
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=9,car_id=9,name="I am a name", cat_id=999)
        log.info('Attemtping to change id to 900')
        xObj.cat_id = 900
        self.assertEqual(xObj.cat_id,900,"Failed: change id to 900 : Valid id. Object should have been changed")

    def test_dict(self):
        xObj = GT.CustCarSettings(id=9,car_id=10,name="I am a name", cat_id=11)
        xStr=f"CustCarSettings.__dict__ = {xObj.__dict__}"
        log.info(xStr)
        print(xStr)

    def test_id(self):
        log.info("===== BEGIN Testing - customCarSettings id")

        log.info('Creating with id as None')
        with self.assertRaises(ValueError):
            xObj = GT.CustCarSettings(id=None,car_id=0,name="I am a name", cat_id=1)

        log.info('Creating with id as blank string')
        with self.assertRaises(ValueError):
            xObj = GT.CustCarSettings(id="",car_id=0,name="I am a name", cat_id=1)

        log.info('Creating with id as string')
        with self.assertRaises(ValueError):
            xObj = GT.CustCarSettings(id="I am a string",car_id=0,name="I am a name", cat_id=1)

        log.info('Creating with id = 0')
        xObj = GT.CustCarSettings(id=0,car_id=0,name="I am a name", cat_id=1)
        self.assertEqual(xObj.id,0,"Failed: customCarSetting.id = 0 : Valid id. Object should have been created")

        log.info('Creating with id = 999999')
        # 99999 is picked because its an int, and not zero
        xObj = GT.CustCarSettings(id=99999,car_id=0,name="I am a name", cat_id=1)
        self.assertEqual(xObj.id,99999,"Failed: customCarSetting.id = 1 : Valid id. Object should have been created")

        #################################
        # Test changing the id
        #################################
        log.info('Change id to None')
        # 99999 is picked because its an int, and not zero
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=99999,car_id=0,name="I am a name", cat_id=1)
        log.info('Attempting to change id to None')
        with self.assertRaises(ValueError):
            xObj.id = None

        log.info('Change id to blank string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=99999,car_id=0,name="I am a name", cat_id=1)
        log.info('Attemtping to change id to blank string')
        with self.assertRaises(ValueError):
            xObj.id = ""

        log.info('Change id to string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=99999,car_id=0,name="I am a name", cat_id=1)
        log.info('Attemtping to change id to string')
        with self.assertRaises(ValueError):
            xObj.id = "I am a string"

        log.info('Change id to 0')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=99999,car_id=0,name="I am a name", cat_id=1)
        log.info('Attemtping to change id to 0')
        xObj.id = 0
        self.assertEqual(xObj.id,0,"Failed: change id to 0 : Valid id. Object should have been changed")

        log.info('Change id to 900')
        # 900 is picked for no specific reason
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=99999,car_id=0,name="I am a name", cat_id=1)
        log.info('Attemtping to change id to 900')
        xObj.id = 900
        self.assertEqual(xObj.id,900,"Failed: change id to 900 : Valid id. Object should have been changed")

    def test_name(self):
        log.info("==== BEGIN Testing - customCarSettings name")

        log.info('Creating with name as None')
        with self.assertRaises(ValueError):
            xObj = GT.CustCarSettings(id=999,car_id=0,name=None, cat_id=1)

        log.info('Creating with name as blank string')
        with self.assertRaises(ValueError):
            xObj = GT.CustCarSettings(id=999,car_id=0,name="", cat_id=1)

        log.info('Creating with name as = 0')
        with self.assertRaises(ValueError):
            xObj = GT.CustCarSettings(id=999,car_id=0,name=0, cat_id=1)

        log.info('Creating with name as a string')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        self.assertEqual(xObj.name,"I am a string","Failed: customCarSetting.name = str : Valid name object should have been created")

        #################################
        # Test changing the name
        #################################
        log.info('Change name to None')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change name to None')
        with self.assertRaises(ValueError):
            xObj.name = None

        log.info('Change name to blank string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change name to blank string')
        with self.assertRaises(ValueError):
            xObj.name = ""

        log.info('Change name to 1 (an int)')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change name to 1 (an int)')
        with self.assertRaises(ValueError):
            xObj.name = 1

        log.info('Change name to 1 (an int)')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change name to another string')
        xObj.name="I am a different string"
        self.assertEqual(xObj.name,"I am a different string","Failed: changing customCarSetting.name = str : Valid name object should have been created")

    def test_car_id(self):
        log.info("===== BEGIN Testing - customCarSettings car_id")

        log.info('Creating with car_id as None')
        with self.assertRaises(ValueError):
            xObj = GT.CustCarSettings(id=0,car_id=None,name="I am a name", cat_id=1)

        log.info('Creating with car_id as blank string')
        with self.assertRaises(ValueError):
            xObj = GT.CustCarSettings(id=0,car_id="",name="I am a name", cat_id=1)

        log.info('Creating with car_id as string')
        with self.assertRaises(ValueError):
            xObj = GT.CustCarSettings(id=0,car_id="I am a string",name="I am a name", cat_id=1)

        log.info('Creating with car_id = 0')
        xObj = GT.CustCarSettings(id=0,car_id=0,name="I am a name", cat_id=1)
        self.assertEqual(xObj.car_id,0,"Failed: customCarSetting.car_id = 0 : Valid id. Object should have been created")

        log.info('Creating with car_id = 999999')
        # 999999 is picked because its an int and not zero
        xObj = GT.CustCarSettings(id=0,car_id=999999,name="I am a name", cat_id=1)
        self.assertEqual(xObj.car_id,999999,"Failed: customCarSetting.car_id = 999999 : Valid id. Object should have been created")

        log.info('Changing car_id to None')
        xObj = GT.CustCarSettings(id=0,car_id=0,name="I am a name", cat_id=1)
        with self.assertRaises(ValueError):
            xObj.car_id=None

        log.info('Changing car_id to blank string')
        xObj = GT.CustCarSettings(id=0,car_id=0,name="I am a name", cat_id=1)
        with self.assertRaises(ValueError):
            xObj.car_id=""

        log.info('Changing car_id to string')
        xObj = GT.CustCarSettings(id=0,car_id=0,name="I am a name", cat_id=1)
        with self.assertRaises(ValueError):
            xObj.car_id="I am a string"

        log.info('Changing car_id to 999')
        # 999 is picked because its an int and not zero
        xObj = GT.CustCarSettings(id=0,car_id=0,name="I am a name", cat_id=1)
        xObj.car_id=999
        self.assertEqual(xObj.car_id,999,"Failed: Changing customCarSetting.car_id = 999 : Valid id. Object should have been changed")

        log.info('Changing car_id to 0')
        # 999 is picked because its an int and not zero
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a name", cat_id=1)
        xObj.car_id=0
        self.assertEqual(xObj.car_id,0,"Failed: Changing customCarSetting.car_id = 0 : Valid id. Object should have been changed")

    def test_max_power(self):
        log.info("==== BEGIN Testing - customCarSettings max_power")

        log.info("Test setting max_power to 0")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change max_power to 0')
        xObj.max_power = 0
        self.assertEqual(xObj.max_power,0,"Failed: setting max_power to 0 : Valid max_power value. object should have been created")

        log.info("Test setting max_power to -4")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change max_power to -4')
        xObj.max_power = -4
        self.assertEqual(xObj.max_power,-4,"Failed: setting max_power to -4 : Valid max_power value. object should have been created")

        log.info("Test setting max_power to a string")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change max_power to a string')
        with self.assertRaises(ValueError):
            xObj.max_power = "I am a string"

        log.info("Test setting max_power to an empty string")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change max_power to an empty string')
        self.assertEqual(xObj.max_power,None,"Failed: setting max_power to an empty string : Valid max_power value. object should have been created")

        log.info("Test setting max_power to None")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change max_power to None')
        xObj.max_power = None
        self.assertEqual(xObj.max_power,None,"Failed: setting max_power to None : Valid max_power value. object should have been created")

    def test_max_torque(self):
        log.info("==== BEGIN Testing - customCarSettings max_torque")

        log.info("Test setting max_torque to 1")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set max_torque to 1')
        xObj.max_torque = 1
        self.assertEqual(xObj.max_torque,1,"Failed: setting max_torque to 1 : Valid max_torque value.")
        self.assertEqual(type(xObj.max_torque),float,"Failed: setting max_torque to 1 : max_torque should be float.")

        log.info("Test setting max_torque to None")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set max_torque to None')
        xObj.max_torque = None
        self.assertEqual(xObj.max_torque,None,"Failed: setting max_torque to None : Valid max_torque value.")

        log.info("Test setting max_torque to an empty string")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change max_torque to an empty string')
        xObj.max_torque = ""
        self.assertEqual(xObj.max_torque,None,"Failed: setting max_torque to an empty string : Valid max_torque value.")

        log.info("Test setting max_torque to -1")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set max_torque to -1')
        xObj.max_torque = -1
        self.assertEqual(xObj.max_torque,-1,"Failed: setting max_torque to -1 : Valid max_torque value.")
        self.assertEqual(type(xObj.max_torque),float,"Failed: setting max_torque to -1 : Valid max_torque value. max_torque should be float.")

        log.info("Test setting max_torque to 123.40")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set max_torque to 123.40')
        xObj.max_torque = 123.40
        self.assertEqual(xObj.max_torque,123.40,"Failed: setting max_torque to 123.40 : Valid max_torque value.")
        self.assertEqual(type(xObj.max_torque),float,"Failed: setting max_torque to 123.40 : Valid max_torque value. max_torque should be float.")

    def test_power_ratio(self):
        log.info("==== BEGIN Testing - customCarSettings power_ratio")

        log.info("Test setting power_ratio to 0")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change power_ratio to 0')
        xObj.power_ratio = 0
        self.assertEqual(xObj.power_ratio,0,"Failed: setting power_ratio to 0 : Valid power_ratio value. object should have been created")

        log.info("Test setting power_ratio to -4")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change power_ratio to -4')
        xObj.power_ratio = -4
        self.assertEqual(xObj.power_ratio,-4,"Failed: setting power_ratio to -4 : Valid power_ratio value. object should have been created")

        log.info("Test setting power_ratio to a string")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change power_ratio to a string')
        with self.assertRaises(ValueError):
            xObj.power_ratio = "I am a string"

        log.info("Test setting power_ratio to an empty string")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change power_ratio to an empty string')
        self.assertEqual(xObj.power_ratio,None,"Failed: setting power_ratio to an empty string : Valid power_ratio value. object should have been created")

        log.info("Test setting power_ratio to None")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change power_ratio to None')
        xObj.power_ratio = None
        self.assertEqual(xObj.power_ratio,None,"Failed: setting power_ratio to None : Valid power_ratio value. object should have been created")

    def test_traction_control(self):
            log.info("==== BEGIN Testing - customCarSettings traction_control")

            log.info("Test setting traction_control to 0")
            log.debug('creating good object')
            xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
            log.info('Attempting to change traction_control to 0')
            xObj.traction_control = 0
            self.assertEqual(xObj.traction_control,0,"Failed: setting traction_control to 0 : Valid traction_control value. object should have been created")

            log.info("Test setting traction_control to -4")
            log.debug('creating good object')
            xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
            log.info('Attempting to change traction_control to -4')
            xObj.traction_control = -4
            self.assertEqual(xObj.traction_control,-4,"Failed: setting traction_control to -4 : Valid traction_control value. object should have been created")

            log.info("Test setting traction_control to a string")
            log.debug('creating good object')
            xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
            log.info('Attempting to change traction_control to a string')
            with self.assertRaises(ValueError):
                xObj.traction_control = "I am a string"

            log.info("Test setting traction_control to an empty string")
            log.debug('creating good object')
            xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
            log.info('Attempting to change traction_control to an empty string')
            self.assertEqual(xObj.traction_control,None,"Failed: setting traction_control to an empty string : Valid traction_control value. object should have been created")


            log.info("Test setting traction_control to None")
            log.debug('creating good object')
            xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
            log.info('Attempting to change traction_control to None')
            xObj.traction_control = None
            self.assertEqual(xObj.traction_control,None,"Failed: setting traction_control to None : Valid traction_control value. object should have been created")

    def test_top_speed(self):
        log.info("==== BEGIN Testing - customCarSettings top_speed")

        log.info("Test setting top_speed to 0")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change top_speed to 0')
        xObj.top_speed = 0
        self.assertEqual(xObj.top_speed,0,"Failed: setting top_speed to 0 : Valid top_speed value. object should have been created")

        log.info("Test setting top_speed to -4")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change top_speed to -4')
        xObj.top_speed = -4
        self.assertEqual(xObj.top_speed,-4,"Failed: setting top_speed to -4 : Valid top_speed value. object should have been created")

        log.info("Test setting top_speed to a string")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change top_speed to a string')
        with self.assertRaises(ValueError):
            xObj.top_speed = "I am a string"

        log.info("Test setting top_speed to an empty string")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change top_speed to an empty string')
        self.assertEqual(xObj.top_speed,None,"Failed: setting top_speed to an empty string : Valid top_speed value. object should have been created")

        log.info("Test setting top_speed to None")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change top_speed to None')
        xObj.top_speed = None
        self.assertEqual(xObj.top_speed,None,"Failed: setting top_speed to None : Valid top_speed value. object should have been created")

    def test_tire_code(self):
        log.info("==== BEGIN Testing - customCarSettings tire_code")

        log.info('Test setting tire_code to None')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change tire_code to None')
        xObj.tire_code = None
        self.assertEqual(xObj.tire_code,None,"Failed: setting tire_code to None : Valid tire_code value. Object should have been created")

        log.info('Test setting tire_code to blank string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change tire_code to blank string')
        xObj.tire_code = ""
        self.assertEqual(xObj.tire_code,"","Failed: setting tire_code to None : Valid tire_code value. Object should have been created")

        log.info('Test setting tire_code to 1 (an int)')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change tire_code to 1 (an int)')
        with self.assertRaises(ValueError):
            xObj.tire_code = 1

    def test_gear_1(self):
        log.info("==== BEGIN Testing - customCarSettings gear_1")

        log.info('Test setting gear_1 to None')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_1 to None')
        xObj.gear_1 = None
        self.assertEqual(xObj.gear_1,None,"Failed: setting gear_1 to None : Valid gear_1 value. Object should have been created")

        log.info('Test setting gear_1 to blank string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_1 to blank string')
        xObj.gear_1 = ""
        self.assertEqual(xObj.gear_1,"","Failed: setting gear_1 to None : Valid gear_1 value. Object should have been created")

        log.info('Test setting gear_1 to 1 (an int)')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_1 to 1 (an int)')
        with self.assertRaises(ValueError):
            xObj.gear_1 = 1

    def test_gear_2(self):
        log.info("==== BEGIN Testing - customCarSettings gear_2")

        log.info('Test setting gear_2 to None')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_2 to None')
        xObj.gear_2 = None
        self.assertEqual(xObj.gear_2,None,"Failed: setting gear_2 to None : Valid gear_2 value. Object should have been created")

        log.info('Test setting gear_2 to blank string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_2 to blank string')
        xObj.gear_2 = ""
        self.assertEqual(xObj.gear_2,"","Failed: setting gear_2 to None : Valid gear_2 value. Object should have been created")

        log.info('Test setting gear_2 to 1 (an int)')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_2 to 1 (an int)')
        with self.assertRaises(ValueError):
            xObj.gear_2 = 1

    def test_gear_3(self):
        log.info("==== BEGIN Testing - customCarSettings gear_3")

        log.info('Test setting gear_3 to None')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_3 to None')
        xObj.gear_3 = None
        self.assertEqual(xObj.gear_3,None,"Failed: setting gear_3 to None : Valid gear_3 value. Object should have been created")

        log.info('Test setting gear_3 to blank string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_3 to blank string')
        xObj.gear_3 = ""
        self.assertEqual(xObj.gear_3,"","Failed: setting gear_3 to None : Valid gear_3 value. Object should have been created")

        log.info('Test setting gear_3 to 1 (an int)')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_3 to 1 (an int)')
        with self.assertRaises(ValueError):
            xObj.gear_3 = 1

    def test_gear_4(self):
        log.info("==== BEGIN Testing - customCarSettings gear_4")

        log.info('Test setting gear_4 to None')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_4 to None')
        xObj.gear_4 = None
        self.assertEqual(xObj.gear_4,None,"Failed: setting gear_4 to None : Valid gear_4 value. Object should have been created")

        log.info('Test setting gear_4 to blank string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_4 to blank string')
        xObj.gear_4 = ""
        self.assertEqual(xObj.gear_4,"","Failed: setting gear_4 to None : Valid gear_4 value. Object should have been created")

        log.info('Test setting gear_4 to 1 (an int)')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_4 to 1 (an int)')
        with self.assertRaises(ValueError):
            xObj.gear_4 = 1

    def test_gear_5(self):
        log.info("==== BEGIN Testing - customCarSettings gear_5")

        log.info('Test setting gear_5 to None')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_5 to None')
        xObj.gear_5 = None
        self.assertEqual(xObj.gear_5,None,"Failed: setting gear_5 to None : Valid gear_5 value. Object should have been created")

        log.info('Test setting gear_5 to blank string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_5 to blank string')
        xObj.gear_5 = ""
        self.assertEqual(xObj.gear_5,"","Failed: setting gear_5 to None : Valid gear_5 value. Object should have been created")

        log.info('Test setting gear_5 to 1 (an int)')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_5 to 1 (an int)')
        with self.assertRaises(ValueError):
            xObj.gear_5 = 1

    def test_gear_6(self):
        log.info("==== BEGIN Testing - customCarSettings gear_6")

        log.info('Test setting gear_6 to None')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_6 to None')
        xObj.gear_6 = None
        self.assertEqual(xObj.gear_6,None,"Failed: setting gear_6 to None : Valid gear_6 value. Object should have been created")

        log.info('Test setting gear_6 to blank string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_6 to blank string')
        xObj.gear_6 = ""
        self.assertEqual(xObj.gear_6,"","Failed: setting gear_6 to None : Valid gear_6 value. Object should have been created")

        log.info('Test setting gear_6 to 1 (an int)')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_6 to 1 (an int)')
        with self.assertRaises(ValueError):
            xObj.gear_6 = 1

    def test_gear_7(self):
        log.info("==== BEGIN Testing - customCarSettings gear_7")

        log.info('Test setting gear_7 to None')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_7 to None')
        xObj.gear_7 = None
        self.assertEqual(xObj.gear_7,None,"Failed: setting gear_7 to None : Valid gear_7 value. Object should have been created")

        log.info('Test setting gear_7 to blank string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_7 to blank string')
        xObj.gear_7 = ""
        self.assertEqual(xObj.gear_7,"","Failed: setting gear_7 to None : Valid gear_7 value. Object should have been created")

        log.info('Test setting gear_7 to 1 (an int)')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change gear_7 to 1 (an int)')
        with self.assertRaises(ValueError):
            xObj.gear_7 = 1

    def test_final_gear(self):
        log.info("==== BEGIN Testing - customCarSettings final_gear")

        log.info('Test setting final_gear to None')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change final_gear to None')
        xObj.final_gear = None
        self.assertEqual(xObj.final_gear,None,"Failed: setting final_gear to None : Valid final_gear value. Object should have been created")

        log.info('Test setting final_gear to blank string')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change final_gear to blank string')
        xObj.final_gear = ""
        self.assertEqual(xObj.final_gear,"","Failed: setting final_gear to None : Valid final_gear value. Object should have been created")

        log.info('Test setting final_gear to 1 (an int)')
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change final_gear to 1 (an int)')
        with self.assertRaises(ValueError):
            xObj.final_gear = 1

    def test_weight(self):
        log.info("==== BEGIN Testing - customCarSettings weight")

        log.info("Test setting weight to 0")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change weight to 0')
        xObj.weight = 0
        self.assertEqual(xObj.weight,0,"Failed: setting weight to 0 : Valid weight value. object should have been created")

        log.info("Test setting weight to -4")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change weight to -4')
        xObj.weight = -4
        self.assertEqual(xObj.weight,-4,"Failed: setting weight to -4 : Valid weight value. object should have been created")

        log.info("Test setting weight to a string")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change weight to a string')
        with self.assertRaises(ValueError):
            xObj.weight = "I am a string"

        log.info("Test setting weight to an empty string")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change weight to an empty string')
        self.assertEqual(xObj.weight,None,"Failed: setting weight to an empty string : Valid weight value. object should have been created")

        log.info("Test setting weight to None")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change weight to None')
        xObj.weight = None
        self.assertEqual(xObj.weight,None,"Failed: setting weight to None : Valid weight value. object should have been created")

    def test_weight_reduction(self):
        log.info("==== BEGIN Testing - customCarSettings weight_reduction")

        log.info("Test setting weight_reduction to 0")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change weight_reduction to 0')
        xObj.weight_reduction = 0
        self.assertEqual(xObj.weight_reduction,0,"Failed: setting weight_reduction to 0 : Valid weight_reduction value. object should have been created")

        log.info("Test setting weight_reduction to -4")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change weight_reduction to -4')
        xObj.weight_reduction = -4
        self.assertEqual(xObj.weight_reduction,-4,"Failed: setting weight_reduction to -4 : Valid weight_reduction value. object should have been created")

        log.info("Test setting weight_reduction to a string")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change weight_reduction to a string')
        with self.assertRaises(ValueError):
            xObj.weight_reduction = "I am a string"

        log.info("Test setting weight_reduction to an empty string")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change weight_reduction to an empty string')
        self.assertEqual(xObj.weight_reduction,None,"Failed: setting weight_reduction to an empty string : Valid weight_reduction value. object should have been created")

        log.info("Test setting weight_reduction to None")
        log.debug('creating good object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change weight_reduction to None')
        xObj.weight_reduction = None
        self.assertEqual(xObj.weight_reduction,None,"Failed: setting weight_reduction to None : Valid weight_reduction value. object should have been created")

    def test_stability(self):
        log.info("==== BEGIN Testing - customCarSettings stability")

        log.info("Test setting stability to 1")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set stability to 1')
        xObj.stability = 1
        self.assertEqual(xObj.stability,1,"Failed: setting stability to 1 : Valid stability value.")
        self.assertEqual(type(xObj.stability),float,"Failed: setting stability to 1 : stability should be float.")

        log.info("Test setting stability to None")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set stability to None')
        xObj.stability = None
        self.assertEqual(xObj.stability,None,"Failed: setting stability to None : Valid stability value.")

        log.info("Test setting stability to an empty string")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change stability to an empty string')
        xObj.stability = ""
        self.assertEqual(xObj.stability,None,"Failed: setting stability to an empty string : Valid stability value.")

        log.info("Test setting stability to -1")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set stability to -1')
        xObj.stability = -1
        self.assertEqual(xObj.stability,-1,"Failed: setting stability to -1 : Valid stability value.")
        self.assertEqual(type(xObj.stability),float,"Failed: setting stability to -1 : Valid stability value. stability should be float.")

        log.info("Test setting stability to 123.40")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set stability to 123.40')
        xObj.stability = 123.40
        self.assertEqual(xObj.stability,123.40,"Failed: setting stability to 123.40 : Valid stability value.")
        self.assertEqual(type(xObj.stability),float,"Failed: setting stability to 123.40 : Valid stability value. stability should be float.")

    def test_cornering(self):
        log.info("==== BEGIN Testing - customCarSettings cornering")

        log.info("Test setting cornering to 1")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set cornering to 1')
        xObj.cornering = 1
        self.assertEqual(xObj.cornering,1,"Failed: setting cornering to 1 : Valid cornering value.")
        self.assertEqual(type(xObj.cornering),float,"Failed: setting cornering to 1 : cornering should be float.")

        log.info("Test setting cornering to None")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set cornering to None')
        xObj.cornering = None
        self.assertEqual(xObj.cornering,None,"Failed: setting cornering to None : Valid cornering value.")

        log.info("Test setting cornering to an empty string")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change cornering to an empty string')
        xObj.cornering = ""
        self.assertEqual(xObj.cornering,None,"Failed: setting cornering to None : Valid cornering value.")

        log.info("Test setting cornering to -1")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set cornering to -1')
        xObj.cornering = -1
        self.assertEqual(xObj.cornering,-1,"Failed: setting cornering to -1 : Valid cornering value.")
        self.assertEqual(type(xObj.cornering),float,"Failed: setting cornering to -1 : Valid cornering value. cornering should be float.")

        log.info("Test setting cornering to 123.40")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set cornering to 123.40')
        xObj.cornering = 123.40
        self.assertEqual(xObj.cornering,123.40,"Failed: setting cornering to 123.40 : Valid cornering value.")
        self.assertEqual(type(xObj.cornering),float,"Failed: setting cornering to 123.40 : Valid cornering value. cornering should be float.")

    def test_braking(self):
        log.info("==== BEGIN Testing - customCarSettings braking")

        log.info("Test setting braking to 1")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set braking to 1')
        xObj.braking = 1
        self.assertEqual(xObj.braking,1,"Failed: setting braking to 1 : Valid braking value.")
        self.assertEqual(type(xObj.braking),float,"Failed: setting braking to 1 : braking should be float.")

        log.info("Test setting braking to None")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set braking to None')
        xObj.braking = None
        self.assertEqual(xObj.braking,None,"Failed: setting braking to None : Valid braking value.")

        log.info("Test setting braking to an empty string")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change braking to an empty string')
        xObj.braking = ""
        self.assertEqual(xObj.braking,None,"Failed: setting braking to an empty string : Valid braking value.")

        log.info("Test setting braking to -1")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set braking to -1')
        xObj.braking = -1
        self.assertEqual(xObj.braking,-1,"Failed: setting braking to -1 : Valid braking value.")
        self.assertEqual(type(xObj.braking),float,"Failed: setting braking to -1 : Valid braking value. braking should be float.")

        log.info("Test setting braking to 123.40")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set braking to 123.40')
        xObj.braking = 123.40
        self.assertEqual(xObj.braking,123.40,"Failed: setting braking to 123.40 : Valid braking value.")
        self.assertEqual(type(xObj.braking),float,"Failed: setting braking to 123.40 : Valid braking value. braking should be float.")


    def test_max_speed(self):
        log.info("==== BEGIN Testing - customCarSettings max_speed")

        log.info("Test setting max_speed to 1")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set max_speed to 1')
        xObj.max_speed = 1
        self.assertEqual(xObj.max_speed,1,"Failed: setting max_speed to 1 : Valid max_speed value.")
        self.assertEqual(type(xObj.max_speed),float,"Failed: setting max_speed to 1 : max_speed should be float.")

        log.info("Test setting max_speed to None")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set max_speed to None')
        xObj.max_speed = None
        self.assertEqual(xObj.max_speed,None,"Failed: setting max_speed to None : Valid max_speed value.")

        log.info("Test setting max_speed to an empty string")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change max_speed to an empty string')
        xObj.max_speed = ""
        self.assertEqual(xObj.max_speed,None,"Failed: setting max_speed to an empty string : Valid max_speed value.")


        log.info("Test setting max_speed to -1")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set max_speed to -1')
        xObj.max_speed = -1
        self.assertEqual(xObj.max_speed,-1,"Failed: setting max_speed to -1 : Valid max_speed value.")
        self.assertEqual(type(xObj.max_speed),float,"Failed: setting max_speed to -1 : Valid max_speed value. max_speed should be float.")

        log.info("Test setting max_speed to 123.40")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set max_speed to 123.40')
        xObj.max_speed = 123.40
        self.assertEqual(xObj.max_speed,123.40,"Failed: setting max_speed to 123.40 : Valid max_speed value.")
        self.assertEqual(type(xObj.max_speed),float,"Failed: setting max_speed to 123.40 : Valid max_speed value. max_speed should be float.")

    def test_accel(self):
        log.info("==== BEGIN Testing - customCarSettings accel")

        log.info("Test setting accel to 1")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set accel to 1')
        xObj.accel = 1
        self.assertEqual(xObj.accel,1,"Failed: setting accel to 1 : Valid accel value.")
        self.assertEqual(type(xObj.accel),float,"Failed: setting accel to 1 : Accel should be float.")

        log.info("Test setting accel to None")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set accel to None')
        xObj.accel = None
        self.assertEqual(xObj.accel,None,"Failed: setting accel to None : Valid accel value.")

        log.info("Test setting accel to an empty string")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to change accel to an empty string')
        xObj.accel = ""
        self.assertEqual(xObj.accel,None,"Failed: setting accel to an empty string : Valid accel value.")

        log.info("Test setting accel to -1")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set accel to -1')
        xObj.accel = -1
        self.assertEqual(xObj.accel,-1,"Failed: setting accel to -1 : Valid accel value.")
        self.assertEqual(type(xObj.accel),float,"Failed: setting accel to -1 : Valid accel value. Accel should be float.")

        log.info("Test setting accel to 123.40")
        log.debug('Create good car setting object')
        xObj = GT.CustCarSettings(id=999,car_id=0,name="I am a string", cat_id=1)
        log.info('Attempting to set accel to 123.40')
        xObj.accel = 123.40
        self.assertEqual(xObj.accel,123.40,"Failed: setting accel to 123.40 : Valid accel value.")
        self.assertEqual(type(xObj.accel),float,"Failed: setting accel to 123.40 : Valid accel value. Accel should be float.")

# End here