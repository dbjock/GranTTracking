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
        mfgid     : type int. Unique for all manufactures in db
        mfgName   : type str. Unique for all manufactures in db
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


class League(object):
    def __init__(self, id, name, sortord):
        """
        League object.

        id     : type int. Unique for all circuits in db.
        name   : type str. name of the circuit, unique in db.
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
