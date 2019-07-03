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

    def write_manufacture(self,recid, title):
        """
        Writes/Creates a manufacture record.
        All PARMS requried.
        recid : 0 = Attempt to Create Record
                !0 Record will update/create as needed
        title : title/name of the manufacture (Must not be None,null,blank)
        Returns True if successful, False if error
        """
        logging.debug(f"PARMS: recid: {recid}, title: {title}")
        if not isinstance(recid, int):
            logging.error(f"recid is not an integer. No Add/Update")
            return False

        # Can't allow blank data in (Note.. db doesn't consider this null)
        if title is None or title == '':
            logging.error(f"title must contain a value. No Add/Update")
            return False

        #Setting up SQL for Create or Update
        if recid == 0: #Add record. If title uniquie, will add with unique recid
            logging.debug(f"Creating record for title: {title}")
            theRecord = (title,)
            sql = "INSERT INTO manufactures (title) Values (?)"
        else: #Add/replace record with provided data based on recID
            logging.debug(f"Create/Update record")
            theRecord = (recid, title)
            sql = "INSERT OR REPLACE INTO manufactures (id, title) Values (?, ?)"

        # Execute SQL
        logging.debug(f"Sql: {sql}")
        with self.conn:
            try:
                self.c.execute(sql, theRecord)
            except sqlite3.IntegrityError as e:
                logging.warning(f"theRecord: {theRecord} sqlite integrity error: {e.args[0]}")
                return False
            except:
                logging.error('Something went wrong', exc_info = True)
                return False

        logging.info(f"theRecord: {theRecord} : committed")
        return True