import logging
import sqlite3

# Version 2 - This module will have everything to CRUD the database.
logger = logging.getLogger(__name__)
# TODO: Need initdb method for creating db.


class GTdb:
    def __init__(self, name=None):
        self.conn = None
        self.cursor = None

        if name:
            self.open(name)

    def open(self, name):
        logging.debug(f"open db {name}")
        try:
            self.conn = sqlite3.connect(
                name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as errID:
            logger.critical(f"Database connection failure. ", exc_info=True)
            quit()

        # Ability to get column names (.keys())
        self.conn.row_factory = sqlite3.Row

        # Turning on foreign_key enforcement
        self.cursor.execute("PRAGMA foreign_keys = ON")

    def exeScriptFile(self, scriptFileName=None):
        """
        Executes a Script file.
        scriptFileName : SQL script file to run
        """
        logging.debug(f"loading script {scriptFileName} to memory")
        scriptFile = open(scriptFileName, 'r')
        script = scriptFile.read()
        scriptFile.close()
        logging.debug(f"execute script")
        c = self.cursor
        try:
            c.executescript(script)
        except:
            logger.critical(
                f"Unexpected Error running script {scriptFileName}", exc_info=True)
            quit()

        self.conn.commit()
        logging.debug(f"changes commit")

    def getMfg(self, value=None, key='recID'):
        """
        Gets the manufacture record from the database based on the key being used.

        PARMS
        value : Is the value being search for.
        key   : the column name to search on. recID, or mfgName. Default is recID
        Returns : list object
        """
        logger.info(f"Getting Manufacture key={key} value={value}")
        selectSQL = "SELECT id, Make, alpha2, Country, region FROM v_manufactures "
        if key == 'recID':
            if not isinstance(value, int):
                logger.error(f"recID must be an integer value")
                return None

            whereSQL = "WHERE id = ?"
            theVars = (value,)
            sql = selectSQL + whereSQL
            logger.debug(f'Getting specific recID: {value} SQL: {sql}')
        elif key == 'Make':
            whereSQL = "WHERE Make = ?"
            theVars = (value,)
            sql = selectSQL + whereSQL
            logger.debug(f'Getting specific recID: {value} SQL: {sql}')
        else:
            logger.error(f'key {key} does not exist')
            return None

        # Ready to execute SQL
        try:
            logger.debug(f"sql: {sql}")
            dbCursor = self.cursor
            dbCursor.execute(sql, theVars)
            result = dbCursor.fetchone()
            logger.debug(f"results: {result}")
            logger.info(f"Returning Manufacture results")
            return result
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            return None

    def getAllMfg(self, orderBy='id'):
        """Returns manufacture records

        PARMS
        orderBy : Column to order by
        """
        logger.info(f"Getting all manufactures, orderd by {orderBy}")
        selectSQL = "SELECT id, Make, alpha2, Country, region FROM v_manufactures "
        sql = selectSQL + f"ORDER BY {orderBy}"

        # Ready to execute SQL
        try:
            logger.debug(f"sql: {sql}")
            dbCursor = self.cursor
            dbCursor.execute(sql)
            result = dbCursor.fetchall()
            logger.info(f"Returning all Manufacture results")
            return result
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            return None
