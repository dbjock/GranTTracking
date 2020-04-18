import logging
logger = logging.getLogger(__name__)


class Country(object):

    def __init__(self, cntryID, cntryName, alpha2, alpha3, region):
        self.cntryID = cntryID
        self.cntryName = cntryName
        self.alpha2 = alpha2
        self.alpha3 = alpha3
        self.region = region

    def __repr__(self):
        return f"Country(cntryID={self.cntryID}, cntryName='{self.cntryName}', alpha2='{self.alpha2}', alpha3='{self.alpha3}', region='{self.region}')"


class Manufacture(object):

    def __init__(self, mfgid, mfgName, countryObj):
        """
        mfgid     : type int
        mfgName   : type string
        countryObj: object created from the Country Class.
        """
        self.mfgid = mfgid
        self.mfgName = mfgName
        self.cntry = countryObj

    def __repr__(self):
        return f"Manufacture(mfgid={self.mfgid},mfgName='{self.mfgName}', countryObj={self.cntry})"

    def WIPload(self, dbConn, id):
        """
        Load manufacture from database in MfgObject.

        PARMS
        dbConn : db Connection object
        id : Manufacture ID (int)\n
        """
        logger.info("Load manufacture data from DB")
        if not isinstance(id, int):
            logger.critical("id must be an integer.")
            raise ValueError("id must be an integer.")

        if id == 0:
            logger.critical("id must be >0.")
            raise ValueError("id must be >0.")

        # mfgRecord = gtdb.getMfg(dbConn, id, key='recID')
        mfgRecord = dbConn.getMfg(value=id, key='recID')
        logger.debug(f"{mfgRecord}")
        self.id = mfgRecord[0]
        self.name = mfgRecord[1]

    def WIP_add(self, dbConn):
        """
        Add Manufacture obj to database.\n
        dbConn : db Connection object\n
        Return: None. *self.id will have recID if successful. False if failed
        """
        logger.info("Adding manufacture data to DB")
        self.id = gtdb.add_Mfg(dbConn, self.name)

    def WIP_update(self, dbConn):
        """
        Update Manufacture obj to database.\n
        dbConn : db Connection object\n
        Return: True if successfull
        """
        logger.info(f"Updating record {self.id} MfgName change to {self.name}")
        gtdb.update_Mfg(dbConn, self.id, self.name)


class WIP_DriveTrain(object):
    def __init__(self):
        self.id = 0
        self.code = ""
        self.desc = ""

    def load(self, dbConn, id):
        """
        Load DriveTrain from database into DriveTrainObject.\n
        dbConn : db Connection object
        id : DriveTrain ID (int)\n
        """
        if not isinstance(id, int):
            logger.debug("id must be an integer")
            raise ValueError("id must be an integer.")

        if id == 0:
            logger.critical("id must be >0.")
            raise ValueError("id must be >0.")

        logger.debug("Loading DriveTrain")
        theRecord = gtdb.getDriveTrain(dbConn, id, key='recID')
        logger.debug(f"{theRecord}")
        self.id = theRecord[0]
        self.code = theRecord[1]
        self.desc = theRecord[2]
