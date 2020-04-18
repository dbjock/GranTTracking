import logging
import sqlite3
from pathlib import Path

# TODO:Delete-Manufacture, Update-Manufacture, Create-Manufacture
# Custom App modules
from GranT import gtclasses
logger = logging.getLogger(__name__)


class GTdb:
    def __init__(self, name=None):
        self.conn = None
        if name:
            logging.debug(f"attempt open db {name}")
            try:
                self.conn = sqlite3.connect(
                    name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
                # self.cursor = self.conn.cursor()
            except sqlite3.Error as errID:
                logger.critical(
                    f"Database connection failure. ", exc_info=True)
                quit()
            c = self.conn.cursor()
            c.execute("PRAGMA database_list;")
            xtmp = c.fetchall()
            logging.debug(f"{xtmp}")
            self.dbfile = xtmp[0][2]

    def exeScriptFile(self, scriptFileName=None):
        """
        Executes a Script file.
        scriptFileName : SQL script file to run
        """
        logging.debug(f"loading script {scriptFileName} to memory")
        scriptFile = open(scriptFileName, 'r')
        script = scriptFile.read()
        scriptFile.close()
        try:
            c = self.conn.cursor()
            c.executescript(script)
        except:
            logger.critical(
                f"Unexpected Error running script {scriptFileName}", exc_info=True)
            quit()

        self.conn.commit()
        logging.debug(f"script commited")

    def getMfg(self, value=None, key='recID'):
        """
        Gets the manufacture record from the database based on the key being used.

        PARMS
        value : Is the value being search for.
        key   : the column name to search on. recID, or mfgName. Default is recID
        Returns : Manufacture object
        """
        logger.info(f"Getting Manufacture key={key} value={value}")
        selectSQL = """SELECT mfg.id as mfgid,
                mfg.name AS Make,
                c.id as cntryID,
                c.name AS Country,
                c.alpha2,
                c.alpha3,
                c.region
                FROM manufacture AS mfg
                LEFT JOIN country AS c ON mfg.country_id = c.ID """

        if key == 'recID':
            if not isinstance(value, int):
                logger.error(f"recID must be an integer value")
                return None

            whereSQL = "WHERE mfgid = ?"
        elif key == 'Make':
            whereSQL = "WHERE Make = ?"
        else:
            logger.error(f'key {key} does not exist')
            return None

        theVars = (value,)
        sql = selectSQL + whereSQL
        # Ready to execute SQL
        try:
            logger.debug(f"sql: {sql}")
            # Enable the .keys() to get column names.
            self.conn.row_factory = sqlite3.Row
            c = self.conn.cursor()
            c.execute(sql, theVars)
            row = c.fetchone()
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            return None

        # Place results into Manufacture class
        xCountry = gtclasses.Country(
            cntryID=row['cntryID'], cntryName=row['Country'],
            alpha2=row['alpha2'], alpha3=row['alpha3'], region=row['region'])

        xMake = gtclasses.Manufacture(
            mfgid=row['mfgid'], mfgName=row['Make'], countryObj=xCountry)

        logger.info(f"Returning Manufacture results")
        return xMake

    def getAllMfg(self, orderBy='id'):
        """Returns manufacture records ordered by choice.

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

    def initDB(self, scriptPath=None):
        """Create tables, views, indexes

        PARM
        scriptPath : path to script files *Required
        """
        logger.debug(f"scriptPath={scriptPath}")
        scripts = ['createTables.sql',
                   'LoadLookUpData.sql',
                   'LoadOtherData.sql']

        gtScripts = Path(scriptPath)

        for sFile in scripts:
            scriptFile = gtScripts / sFile
            logger.info(f"Executing {scriptFile}")
            self.exeScriptFile(scriptFileName=f'{scriptFile}')
