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
        return f"ClassCat(id={self.id}, name='{self.name}', desc='{self.desc}', sortOrder='{self.sortOrder}')"


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
        # classcat is the ClassCat object
        self.classcat = ClassCat(id=None, name="", desc="")
        self.prize1 = 0
        self.prize2 = 0
        self.prize3 = 0

    def __repr__(self):
        return f"RaceCollection(id={self.id}, name='{self.name}', desc='{self.desc}',league={self.league}, classcat={self.classcat}, prize1={self.prize1},prize2={self.prize2}, prize3={self.prize3})"


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
        return f"Race(id={self.id}, name='{self.name}',racetime={self.racetime}, limits={self.limits}, notes={self.notes},{self.trackLayout},{self.raceCollection},{self.raceType},{self.weather})"


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
        return f"raceType(id={self.id}, name={self.name})"


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
        return f"weather(id={self.id}, name={self.name})"


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
        return f"trackLayout(id={self.id},name='{self.name}',miles={self.miles}), {self.track}, {self.circuit}"
