import logging
from GranT import DBClass

class Manufacture(object):

    def __init__(self,dbObj):
        self.name = None
        self.id = 0
        self.db = dbObj

    def load(self,id):
        """
        Get manufacture from database
        id : Manufacture ID (int) REQUIRED
        """
        if not isinstance(id, int):
            logging.debug("integer not passed.")
            return False

        if id > 0:
            logging.debug("Loading Manufacture")
            mfgRecord = self.db.get_manufacture(id)

        if len(mfgRecord) > 0:

            self.id = mfgRecord[0]
            self.name = mfgRecord[1]
