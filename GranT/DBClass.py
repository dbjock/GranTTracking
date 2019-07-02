import logging
import sqlite3

class GtDB(object):

    def __init__(self,dbFileName):
        self.conn = sqlite3.connect(dbFileName)
        self.c = self.conn.cursor()
        logging.debug(f"Connecting to {dbFileName}")

    def get_manufacture(self,recid: int):
        """
        Get mfg record(s)
        recid : 0 = all records >0 that specific recid
        Returns : [(recid, mfgName)]
        """
        logging.debug(f"Getting the Mfg data with {recid}")
        if not isinstance(recid, int): #recid is not an int
            logging.error('recid was not int type.')
            return False

        if recid > 0:
            sql = "SELECT id, title FROM manufactures WHERE id = ?"
            logging.debug(f'Getting specific recid: {recid} SQL: {sql}')
            self.c.execute(sql, (recid,))
            result = self.c.fetchone()
            logging.debug(f"Returning {result}")
            return result
        else: # Get all the records
            sql = "SELECT id, title FROM manufactures"
            logging.debug(f'none. Getting all manufactures. SQL: {sql}')
            self.c.execute(sql)
            return self.c.fetchall()