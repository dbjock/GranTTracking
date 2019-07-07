import logging
from GranT import gtdb
logger = logging.getLogger(__name__)
class Manufacture(object):

    def __init__(self):
        self.id = 0
        self.name = None

    def load(self,dbConn,id):
        """
        Load manufacture from database in MfgObject.\n
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

        mfgRecord = gtdb.getMfg(dbConn,id,key='recID')
        logger.debug(f"{mfgRecord}")
        self.id = mfgRecord[0]
        self.name = mfgRecord[1]

    def add(self,dbConn):
        """
        Add Manufacture obj to database.\n
        dbConn : db Connection object\n
        Return: None. *self.id will have recID if successful. False if failed
        """
        logger.info("Adding manufacture data to DB")
        self.id = gtdb.add_Mfg(dbConn,self.name)

    def update(self,dbConn):
        """
        Update Manufacture obj to database.\n
        dbConn : db Connection object\n
        Return: True if successfull
        """
        logger.info(f"Updating record {self.id} MfgName change to {self.name}")
        gtdb.update_Mfg(dbConn,self.id,self.name)

class DriveTrain(object):
    def __init__(self):
        self.id = 0
        self.code = ""
        self.desc = ""

    def load(self,dbConn,id):
        """
        Load DriveTrain from database into DriveTrainObject.\n
        dbConn : db Connection object
        id : DriveTrain ID (int)\n
        """
        if not isinstance(id,int):
            logger.debug("id must be an integer")
            raise ValueError("id must be an integer.")

        if id == 0:
            logger.critical("id must be >0.")
            raise ValueError("id must be >0.")

        logger.debug("Loading DriveTrain")
        theRecord = gtdb.getDriveTrain(dbConn,id,key='recID')
        logger.debug(f"{theRecord}")
        self.id = theRecord[0]
        self.code = theRecord[1]
        self.desc = theRecord[2]
