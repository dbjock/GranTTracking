import logging
logger = logging.getLogger(__name__)


class Country(object):

    def __init__(self, cntryID, cntryName, alpha2, alpha3, region):
        self.id = cntryID
        self.cntryName = cntryName
        self.alpha2 = alpha2
        self.alpha3 = alpha3
        self.region = region

    def __repr__(self):
        return f"country(id={self.id}, cntryName='{self.cntryName}', alpha2='{self.alpha2}', alpha3='{self.alpha3}', region='{self.region}')"


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
        return f"Manufacture(id={self.id},name='{self.name}', {self.country})"


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
        return f"DriveTrain(id={self.id},code='{self.code}',desc='{self.desc}')"


class ClassCat(object):
    def __init__(self, id, name, desc):
        """
        Class/Category object. Used in cars, and optional for races to.

        id   : type int. Unique for all class/cat's in db.
        name : type str. Short name of the class/cat. Unique in db.
        desc : type str. Full text describing the class/cat.
        """
        self.id = id
        self.name = name
        self.desc = desc

    def __repr__(self):
        return f"ClassCat(id={self.id}, name='{self.name}', desc='{self.desc}')"


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
        return f"circuit(id={self.id}, name='{self.name}')"


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

    def __repr__(self):
        return f"RaceCollection(id={self.id}, name='{self.name}', desc='{self.desc}',league={self.league}"


class Race(object):
    def __init__(self, id, name,  racetime, limits, tlObj, rcObj, rcTypeObj, weatherObj):
        """[summary]

        Args:
            id ([type]): Unique ID of race
            name ([type]): Name of race
            racetime ([type]): Time race is taking place in the day
            limits ([type]): Limits in the race. (15 laps or 15 minutes)
            tlObj ([type]): Track Layout Object
            rcObj ([type]): Race Collection Object
            rTypeObj ([type]): Race Type Object
            weatherObj ([type]): Weather Object
        """
        self.id = 0
        self.name = name
        self.racetime = racetime
        self.limits = limits
        self.tlObj = tlObj
        self.rcObj = rcObj
        self.rcTypeObj = rcTypeObj
        self.weatherObj = weatherObj

    def __repr__(self):
        return f"Race(id={self.id}, name='{self.name}',racetime={self.racetime}, limits={self.limits}, {self.tlObj}, {self.rcObj}, {self.rTypeObj}, {self.weatherObj}"


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
        return f"Racetype(id={self.id}, name={self.name})"


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
        return f"League(id={self.id}, name='{self.name}', sortord={self.sortord})"


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
        return f"track(id={self.id},name='{self.name}', {self.country})"


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
        return f"tracklayout(id={self.id},name='{self.name}',miles={self.miles}), {self.track}, {self.circuit}"
