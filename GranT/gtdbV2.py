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

    def getMfg(self, value=None, key='mfgId'):
        """
        Gets the manufacture record from the database based on the key being used.

        ARGS:
        value : Is the value being search for.
        key   : the column to search on. mfgId, or mfgName. Default is mfgid
        Returns : ManufactureObject. IF ManufactureObject.mfgid = 0 then nothing found
        """
        logger.debug(f"Getting Manufacture: {key}={value}")
        selectSQL = """SELECT mfg.id as mfgId,
                mfg.name AS Make,
                c.id as cntryID,
                c.name AS Country,
                c.alpha2,
                c.alpha3,
                c.region
                FROM manufacture AS mfg
                LEFT JOIN country AS c ON mfg.country_id = c.ID """

        if key == 'mfgId':
            if not isinstance(value, int):
                logger.error(f"mfgId must be an integer value")
                return None

            whereSQL = "WHERE mfgId = ?"
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

        if row:
            # Place results into Manufacture object
            logger.debug("manufacture found.")
            xCountry = gtclasses.Country(
                cntryID=row['cntryID'], cntryName=row['Country'],
                alpha2=row['alpha2'], alpha3=row['alpha3'], region=row['region'])

            xMake = gtclasses.Manufacture(
                mfgid=row['mfgid'], mfgName=row['Make'], countryObj=xCountry)

            logger.debug(f"Returning Manufacture results")
        else:
            # Create blank Manufacture object
            logger.debug("manufacture not found.")
            xCountry = gtclasses.Country(
                cntryID=0, cntryName='', alpha2='', alpha3='', region='')

            xMake = gtclasses.Manufacture(
                mfgid=0, mfgName='', countryObj=xCountry)

        return xMake

    def getAllMfg(self, orderBy='id'):
        """Returns manufacture records ordered by choice.

        PARMS
        orderBy : Column to order by
        returns a list
        """
        logger.info(f"Getting all manufactures, orderd by {orderBy}")
        selectSQL = """SELECT mfg.id as id,
                    mfg.name AS Make,
                    c.alpha2,
                    c.name AS Country,
                    c.region
                FROM manufacture AS mfg
                LEFT JOIN country AS c ON mfg.country_id = c.ID """

        sql = selectSQL + f"ORDER BY {orderBy}"

        # Ready to execute SQL
        logger.debug(f"sql: {sql}")
        try:
            dbCursor = self.conn.cursor()
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
            logger.debug(f"Executing {scriptFile}")
            self.exeScriptFile(scriptFileName=f'{scriptFile}')

    def addMfg(self, mfgObj):
        """Adding a manufuture record to database.

        ARGS
        mfgObj : Manufacture class object
        Returns - list (ResultCode, ResultText)
                 ResultCode 0 = it worked
                 Resultcode <> 0 - See ResultText for details
        Fields which cause common errors.
         - mfgObj.mfgName must be unique in db (case insensitive).
         - mfgObj.country.id must exist in Country table in db.
        """
        logger.debug(f"addMfg: MfgObj= {mfgObj}")
        sql = "INSERT INTO manufacture (name, country_id) VALUES (:mfgName, :cntryID)"
        theVals = {'mfgName': mfgObj.mfgName, 'cntryID': mfgObj.country.id}

        logger.debug(f"Sql: {sql}")
        try:
            c = self.conn.cursor()
            c.execute(sql, theVals)
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            logger.error(f"sqlite integrity error: {e.args[0]}")
            return [2, f"sqlite integrity error: {e.args[0]}"]
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            return [3, "Critical error see logs"]

        logger.debug("Manufacture Saved")
        return [0, "Manufacture Saved"]

    def delMfg(self, mfgId):
        """Delete manufacutre record from database

        ARGS:
        mfgId : UniqueID of Manufacture in DB (Manufacture.id)
        Returns - list (ResultCode, ResultText)
                 ResultCode 0 = it worked
                 Resultcode <> 0 - See ResultText for details
        """
        logger.debug(f"delete manufacture id={mfgId}")
        sql = "DELETE FROM manufacture WHERE id = ?"
        theVals = (mfgId,)
        logger.debug(f"sql: {sql}")
        try:
            c = self.conn.cursor()
            c.execute(sql, theVals)
            self.conn.commit()
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            return [3, "Critical error see logs"]

        logger.debug("manufacture deleted")
        return [0, "Manufacture Deleted"]

    def getAllTracksBy(self, orderBy='Track'):
        selectSQL = """SELECT t.id as id,
                t.name as track,
                c.alpha2,
                c.name AS Country,
                c.region
                FROM track as t
                INNER JOIN
                country as c ON t.country_id = c.id """

        sql = selectSQL + f"ORDER BY {orderBy}"
        # Execute the SQL
        logger.debug(f"sql: {sql}")
        try:
            dbCursor = self.conn.cursor()
            dbCursor.execute(sql)
            result = dbCursor.fetchall()
            logger.info(f"Returning All Track info")
            return result
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            return None
