import logging
log = logging.getLogger(__name__)


class Car(object):
    def __init__(self, id, model, Manufacture, DriveTrain, ClassCat):
        self.id = id
        self.model = model
        self.year = None
        self.manufacture = Manufacture
        self.driveTrain = DriveTrain
        self.catclass = ClassCat

    def __repr__(self):
        return f"Car(id={self.id}, model={self.model}, manufacture={self.manufacture},driveTrain={self.driveTrain},catclass={self.catclass})"


class CustCarSettings(object):
    # TESTING: Other classes are not going to be embedded. Using more memory with it.
    #          FrontEnd can just query to get further object detail. i.e. query car_id
    def __init__(self, id, car_id, name, cat_id):
        self.id = id
        self.accel = None
        self.brake_balance = None
        self.braking = None
        self.car_id = car_id
        self.cat_id = cat_id
        self.cornering = None
        self.final_gear = None
        self.gear_1 = None
        self.gear_2 = None
        self.gear_3 = None
        self.gear_4 = None
        self.gear_5 = None
        self.gear_6 = None
        self.gear_7 = None
        self.max_power = None
        self.max_speed = None
        self.max_torque = None
        self.name = name
        self.power_ratio = None
        self.stability = None
        self.tire_code = None
        self.top_speed = None
        self.traction_control = None
        self.weight = None
        self.weight_reduction = None

    @property
    def stability(self):
        return self._stability

    @stability.setter
    def stability(self,val):
        self._stability = self.convert_floatORNone('stability',val)

    @property
    def cornering(self):
        return self._cornering

    @cornering.setter
    def cornering(self,val):
        self._cornering = self.convert_floatORNone('cornering',val)

    @property
    def braking(self):
        return self._braking

    @braking.setter
    def braking(self,val):
        self._braking = self.convert_floatORNone('braking',val)

    @property
    def max_speed(self):
        return self._max_speed

    @max_speed.setter
    def max_speed(self,val):
        self._max_speed = self.convert_floatORNone('max_speed',val)

    @property
    def accel(self):
        return self._accel

    @accel.setter
    def accel(self,val):
        log.debug('setting accel')
        self._accel = self.convert_floatORNone('accel',val)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self,val):
        self._id = self.validate_int('id',val)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,val):
        self._name = self.validate_str('name',val)

    @property
    def car_id(self):
        return self._car_id

    @car_id.setter
    def car_id(self,val):
        self._car_id = self.validate_int('car_id',val)

    @property
    def cat_id(self):
        return self._cat_id

    @cat_id.setter
    def cat_id(self,val):
        self._cat_id = self.validate_int('cat_id',val)

    @property
    def max_power(self):
        return self._max_power

    @max_power.setter
    def max_power(self,val):
        self._max_power = self.convert_intOrNone('max_power',val)

    @property
    def max_torque(self):
        return self._max_torque

    @max_torque.setter
    def max_torque(self,val):
        self._max_torque = self.convert_floatORNone('max_torque',val)

    @property
    def power_ratio(self):
        return self._power_ratio

    @power_ratio.setter
    def power_ratio(self,val):
        self._power_ratio = self.convert_intOrNone('power_ratio',val)

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self,val):
        self._weight = self.convert_intOrNone('weight',val)

    @property
    def weight_reduction(self):
        return self._weight_reduction

    @weight_reduction.setter
    def weight_reduction(self,val):
        self._weight_reduction = self.convert_intOrNone('weight_reduction',val)

    @property
    def traction_control(self):
        return self._traction_control

    @traction_control.setter
    def traction_control(self,val):
        self._traction_control = self.convert_intOrNone('traction_control',val)

    @property
    def brake_balance(self):
        return self._brake_balance

    @brake_balance.setter
    def brake_balance(self,val):
        self._brake_balance = self.convert_intOrNone('brake_balance',val)

    @property
    def top_speed(self):
        return self._top_speed

    @top_speed.setter
    def top_speed(self,val):
        self._top_speed = self.convert_intOrNone('top_speed',val)

    @property
    def tire_code(self):
        return self._tire_code

    @tire_code.setter
    def tire_code(self,val):
        self._tire_code = self.validate_strORNone('tire_code',val)

    @property
    def gear_1(self):
        return self._gear_1

    @gear_1.setter
    def gear_1(self,val):
        self._gear_1 = self.validate_strORNone('gear_1',val)

    @property
    def gear_2(self):
        return self._gear_2

    @gear_2.setter
    def gear_2(self,val):
        self._gear_2 = self.validate_strORNone('gear_2',val)

    @property
    def gear_3(self):
        return self._gear_3

    @gear_3.setter
    def gear_3(self,val):
        self._gear_3 = self.validate_strORNone('gear_3',val)

    @property
    def gear_4(self):
        return self._gear_4

    @gear_4.setter
    def gear_4(self,val):
        self._gear_4 = self.validate_strORNone('gear_4',val)

    @property
    def gear_5(self):
        return self._gear_5

    @gear_5.setter
    def gear_5(self,val):
        self._gear_5 = self.validate_strORNone('gear_5',val)

    @property
    def gear_6(self):
        return self._gear_6

    @gear_6.setter
    def gear_6(self,val):
        self._gear_6 = self.validate_strORNone('gear_6',val)

    @property
    def gear_7(self):
        return self._gear_7

    @gear_7.setter
    def gear_7(self,val):
        self._gear_7 = self.validate_strORNone('gear_7',val)

    @property
    def final_gear(self):
        return self._final_gear

    @final_gear.setter
    def final_gear(self,val):
        self._final_gear = self.validate_strORNone('final_gear',val)

    def convert_floatORNone(self,key,val):
        """Convert val to float or None. If not able to ValueError is raised

        Args:
            key (str): This should be the property that is being tested, as this appears
                       in the error message to assist in debugging
            val : The value that is being validated is a float
        """
        log.debug(f"Converting key={key} value={val} to float or None")

        if val is None:
            log.debug(f"None ok. returning None")
            return val

        if type(val) == int:
            log.debug(f"value is an int. Converting to float")
            return float(val)

        if type(val) == float:
            log.debug(f"value is an float. just returning")
            return val

        if val == "":
            log.debug(f"value is an empty string. Converting to None")
            return None

        raise ValueError(f"{key} must be a float")

    def validate_int(self,key,val):
        """Validates that val must be an int. If not ValueError is raised.

        Args:
            key (str): This should be the property that is being tested, as this appears
                       in the error message to assist in debugging
            val : The value that is being validated is an integer
        """
        log.debug(f"validating if key={key} value={val} is an int")
        if type(val) != int:
            errMsg = f"{key} must be an integer"
            log.debug(f"Raising value error: {errMsg}")
            raise ValueError(errMsg)

        # Passed validation
        log.debug(f"validation passed for key={key} value={val} is an int")
        return val

    def convert_intOrNone(self,key,val):
        """Convert val to int or None. If not able to ValueError is raised

        Args:
            key (str): This should be the property that is being tested, as this appears
                       in the error message to assist in debugging
            val : The value that is being converted
        """
        log.debug(f"Converting key={key} value={val} to float or None")
        if val is None:
            log.debug(f"None ok. returning None")
            return val

        if type(val) == int:
            log.debug(f"value is an int. This is ok, returning it.")
            return val

        if val == "":
            log.debug(f"value is an empty string. Converting to None")
            return None

        errMsg = f"{key} must be an integer or None. It is type {type(val)}"
        log.debug(f"Raising value error: {errMsg}")
        raise ValueError(errMsg)


    def validate_str(self,key,val):
        """Validates that val must be a string. If not ValueError is raised.

        Args:
            key (str): This should be the property that is being tested, as this appears
                       in the error message to assist in debugging
            val : The value that is being validated is a string
        """
        log.debug(f"validating if key={key} value={val} is a string")
        if type(val) != str:
            errMsg = f"{key} must be a string"
            log.debug(f"Raising value error: {errMsg}")
            raise ValueError(errMsg)

        if val == "":
            errMsg = f"{key} must be a string"
            log.debug(f"Raising value error: {errMsg}")
            raise ValueError(errMsg)

        # Passed validation
        log.debug(f"validation passed for key={key} value={val} is a string")
        return val

    def validate_strORNone(self,key,val):
        """val must be an string or None to be valid else an error will be raised"""
        log.debug(f"validating if key={key} value={val} is a string")
        if val is None:
            log.debug(f"validation passed for key={key} value={val} is None")
            return val

        if type(val) != str:
            errMsg = f"{key} must be a string or None"
            log.debug(f"Raising value error: {errMsg}")
            raise ValueError(errMsg)

        log.debug(f"validation passed for key={key} value={val} is string")
        return val


class Circuit(object):
    def __init__(self, id, name):
        """
        Circut object. This object is a property of different race tracks.

        id   : type int. Unique for all circuits in db.
        name : type str. name of the circuit, unique in db.
        """
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Circuit(id={self.id}, name={self.name})"


class ClassCat(object):
    def __init__(self, id, name, desc):
        """
        Class/Category object. Classification for cars.

        id   : type int. Unique for all class/cat's in db.
        name : type str. Short name of the class/cat. Unique in db.
        desc : type str. Full text describing the class/cat.
        """
        self.id = id
        self.name = name
        self.desc = desc
        self.sortOrder = None

    def __repr__(self):
        return f"ClassCat(id={self.id}, name={self.name}, desc={self.desc})"


class Country(object):

    def __init__(self, cntryID, cntryName, alpha2, alpha3, region):
        self.id = cntryID
        self.cntryName = cntryName
        self.alpha2 = alpha2
        self.alpha3 = alpha3
        self.region = region

    def __repr__(self):
        return f"Country(id={self.id}, cntryName={self.cntryName}, alpha2={self.alpha2}, alpha3={self.alpha3}, region={self.region})"


class DriveTrain(object):
    def __init__(self, id, code, desc):
        """
        Drive Train object. Primarily used with cars.

        id   : type int. Unique for all drive trains in db.
        code : type str. Unique for all drive trains.
        desc : type str. Free text describing the Drive Train.
        """
        self.id = id
        self.code = code
        self.desc = desc

    def __repr__(self):
        return f"DriveTrain(id={self.id},code={self.code},desc={self.desc})"


class League(object):
    def __init__(self, id, name, sortord):
        """
        League object.

        id     : type int. Unique for all Leagues in db.
        name   : type str. name of the League, unique in db.
        sortord: type int. Order which the object should be sorted.
        """
        self.id = id
        self.name = name
        self.sortord = sortord

    def __repr__(self):
        return f"League(id={self.id}, name={self.name}, sortord={self.sortord})"


class Manufacture(object):
    def __init__(self, id, name, countryObj):
        """
        Manufacture object. Used by car, and many other objects
        id     : type int. Unique for all manufactures in db
        Name   : type str. Unique for all manufactures in db
        countryObj: object created from the Country Class.
        """
        self.id = id
        self.name = name
        self.country = countryObj

    def __repr__(self):
        return f"Manufacture(id={self.id},name={self.name}, countryObj={self.country})"


class Race(object):
    def __init__(self, id, name, trackLayout, raceCollection, raceType, weather):
        """[summary]

        Args:
            id (int): Unique ID of race
            name (str): Name of race
            racetime (HH:MM): Time race is taking place in the day
            limits (str): Limits in the race. (15 laps or 15 minutes)
            trackLaout (object): Track Layout Object
            raceCollection (object): Race Collection Object
            raceType (object): Race Type Object
            weather (object): Weather Object
        """
        self.id = id
        self.name = name
        self.racetime = None
        self.limits = None
        self.trackLayout = trackLayout
        self.raceCollection = raceCollection
        self.raceType = raceType
        self.weather = weather
        self.notes = None

    def __repr__(self):
        return f"Race(id={self.id}, name={self.name},trackLayout={self.trackLayout},raceCollection={self.raceCollection},raceType={self.raceType},weather={self.weather})"


class RaceCollection(object):
    def __init__(self, id, name, desc, leagueObj):
        """
        Race Collection object.
        id     : type int. ID of the race collection
        Name   : type str. Name of the Race collection
        Desc   : Description of the Race Collection
        leagueObj: object created from the League Class.
        """

        self.id = id
        self.name = name
        self.desc = desc
        self.league = leagueObj
        # classcat is the ClassCat object. This is optional
        self.classcat = ClassCat(id=None, name="", desc="")
        self.prize1 = 0
        self.prize2 = 0
        self.prize3 = 0

    def __repr__(self):
        return f"RaceCollection(id={self.id}, name={self.name}, desc={self.desc},leagueObj={self.league})"


class RaceType(object):
    def __init__(self, id, name):
        """Init the Race type object

        Args:
            id (int): Unique ID for the Race Type
            name (string): Name of the Race type
        """
        self.id = id
        self.name = name

    def __repr__(self):
        return f"RaceType(id={self.id}, name={self.name})"


class Track(object):

    def __init__(self, id, name, countryObj):
        """
        Track object. Used by car, and many other objects

        id     : type int. Unique for all manufactures in db
        Name   : type str. Unique for all manufactures in db
        countryObj: object created from the Country Class.
        """
        self.id = id
        self.name = name
        self.country = countryObj

    def __repr__(self):
        return f"Track(id={self.id},name={self.name},countryObj={self.country})"


class TrackLayout(object):
    def __init__(self, id, name, miles, trackObj, circuitObj):
        """
        Track Layout.

        id       : type int. ID of the Track Layout. Unique ID for the track laout
        track_id : ID linking to the Track object
        """
        self.id = id
        self.name = name
        self.track = trackObj
        self.circuit = circuitObj
        self.miles = miles

    def __repr__(self):
        return f"TrackLayout(id={self.id},name={self.name},miles={self.miles}), trackObj={self.track},circuitObj={self.circuit}"


class Weather(object):
    def __init__(self, id, name):
        """Init the Weather object

        Args:
            id (int): Unique ID for the weather
            name (string): Name of the Weather
        """
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Weather(id={self.id}, name={self.name})"
