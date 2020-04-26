import logging
import sqlite3
from pathlib import Path

# TODO:Delete-Manufacture, Update-Manufacture, Create-Manufacture
# Custom App modules
from GranT import gtclasses as gtClass

logger = logging.getLogger(__name__)


class GTdb:
    def __init__(self, name=None):
        self.conn = None
        self._selectTrackLayoutSQL = """SELECT t.id as trackId, t.name AS track, l.id AS layouId, l.name AS layout, l.miles AS Miles, c.id as circuitId, c.name AS Circuit, cntry.ID as cntryId, cntry.name as Country, cntry.alpha2, cntry.alpha3, cntry.region as Region FROM track as t INNER JOIN track_layout as l ON t.id = l.track_id LEFT JOIN country as cntry ON t.country_id = cntry.ID INNER JOIN circuit AS c ON l.circuit_id = c.id"""
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

    def _exeSQL(self, sql, theVals):
        """Submit InsertSql provided. (internal use only)

        ARGS
        sql : The insert Sql to use.
        theVals   : The value parms passed into the sql

        Returns - list (ResultCode, ResultText)
                ResultCode 0 = Success execution
                Resultcode != 0 - See ResultText for details
        """
        logger.debug(f"Sql: {sql}")
        logger.debug(f"Values: {theVals}")
        try:
            c = self.conn.cursor()
            c.execute(sql, theVals)
            self.conn.commit()

        except sqlite3.IntegrityError as e:
            logger.warning(f"sqlite integrity error: {e.args[0]}")
            return [2, f"sqlite integrity error: {e.args[0]}"]
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            quit()

        logger.debug("successful commit of sql")
        return [0, "Commit successful"]

    def _exeScriptFile(self, scriptFileName=None):
        """
        Executes a Script file. (internal use only)
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

    def getMfg(self, key='mfgId', value=None):
        """
        Gets the manufacture record from the database based on the key being used.

        ARGS:
        value : Is the value being search for.
        key   : the column to search on. mfgId, or Make. Default is mfgid
        Returns : ManufactureObject. IF ManufactureObject.mfgid = 0 then nothing found
        """
        logger.debug(f"Getting Manufacture: {key}={value}")
        selectSQL = """SELECT mfg.id as mfgId,
                mfg.name AS Make,
                c.id as cntryId,
                c.name AS Country,
                c.alpha2,
                c.alpha3,
                c.region
                FROM manufacture AS mfg
                LEFT JOIN country AS c ON mfg.country_id = c.ID """

        whereSQL = f" WHERE {key} = ?"

        theVars = (value,)
        sql = selectSQL + whereSQL
        # Ready to execute SQL
        logger.debug(f"{theVars}")
        logger.debug(f"sql: {sql}")
        try:
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
            xCountry = gtClass.Country(
                cntryID=row['cntryId'], cntryName=row['Country'],
                alpha2=row['alpha2'], alpha3=row['alpha3'], region=row['region'])

            xMake = gtClass.Manufacture(
                id=row['mfgid'], name=row['Make'], countryObj=xCountry)

            logger.debug(f"Returning Manufacture results")
        else:
            # Create blank Manufacture object
            logger.debug("manufacture not found.")
            xCountry = gtClass.Country(
                cntryID=0, cntryName='', alpha2='', alpha3='', region='')

            xMake = gtClass.Manufacture(
                id=0, name='', countryObj=xCountry)

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
            self._exeScriptFile(scriptFileName=f'{scriptFile}')

    def mfg_add(self, mfgObj):
        """Adding a manufacture record to database.

        ARGS
        mfgObj : Manufacture class object
        Returns - list (ResultCode, ResultText)
                 ResultCode 0 = Success Add
                 Resultcode <> 0 - See ResultText for details
        Fields which cause common errors.
         - mfgObj.mfgName must be unique in db (case insensitive).
         - mfgObj.country.id must exist in Country table in db.
          mfgObj.id is ignored
        """
        logger.debug(f"add mfg: MfgObj= {mfgObj}")
        sql = "INSERT INTO manufacture (name, country_id) VALUES (:mfgName, :cntryID)"
        theVals = {'mfgName': mfgObj.name, 'cntryID': mfgObj.country.id}
        r = self._exeSQL(sql, theVals)
        if r[0] == 0:
            r[1] = f"Manufacture name: {mfgObj.name} added"
        else:
            logger.debug(f"problem with manufacture add {r}.")

        logger.debug(f"returning {r}")
        return r

    def addTrack(self, trackObj):
        """Adding a Track record to the database

        ARGS
        trackObj : Track class object
        Returns - list (ResultCode, ResultText)
                 ResultCode 0 = Success Add
                 Resultcode <> 0 - See ResultText for details
        """
        logger.debug(f"addTrack: trackObj={trackObj}")
        theVals = {'trackName': trackObj.name, 'cntryID': trackObj.country.id}
        sql = "INSERT INTO track (name, country_id) VALUES (:trackName, :cntryID)"

        return self._exeSQL(sql, theVals)

    def mfg_delete(self, mfgId):
        """Delete manufacture record from database

        ARGS:
        mfgId: UniqueID of Manufacture in DB(Manufacture.id)
        Returns - list(ResultCode, ResultText)
                 ResultCode 0 = it worked
                 Resultcode <> 0 - See ResultText for details
        """
        logger.debug(f"delete manufacture id={mfgId}")
        sql = "DELETE FROM manufacture WHERE id = ?"
        theVals = (mfgId,)
        r = self._exeSQL(sql, theVals)
        if r[0] == 0:
            r[1] = "Manufacture Deleted"
        else:
            logger.debug(f"problem with manufacture delete {r}.")

        logger.debug(f"returning {r}")
        return r

    def getTrackLayout(self, key='layoutId', value=None):
        """
        Gets a single Track Layout record from database based on key and value passed.

        ARGS:
        value : Is the value being search for.
        key   : the column to search on. layoutId, or Layout. Default is layoutId
        Returns : TrackLayout Object. IF TrackLayoutObject.id == 0 then nothing found
        """
        if key == 'layoutId':
            whereSQL = "WHERE l.id = ?"
        elif key == 'Layout':
            whereSQL = "WHERE l.name = ?"

        sql = self._selectTrackLayoutSQL + " " + whereSQL
        theVals = (value,)
        # Execute the SQL
        logger.debug(f"sql: {sql}")
        try:
            # Enable the .keys() to get column names.
            self.conn.row_factory = sqlite3.Row
            c = self.conn.cursor()
            c.execute(sql, theVals)
            row = c.fetchone()
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            return None

        if row:  # Populate trackLayout obj
            logger.debug("track layout found")
            xCircuit = gtClass.Circuit(row['circuitId'], row['Circuit'])
            xCountry = gtClass.Country(
                cntryID=row['cntryId'], cntryName=row['Country'],
                alpha2=row['alpha2'], alpha3=row['alpha3'], region=row['region'])
            xTrack = gtClass.Track(
                row['trackId'], name=row['track'], countryObj=xCountry)
            xTrackLayout = gtClass.TrackLayout(
                row['layouId'], row['layout'], miles=row['Miles'], trackObj=xTrack, circuitObj=xCircuit)

        else:  # Create blank trackLayout obj (no data returned)
            logger.debug("track layout not found")
            xCircuit = gtClass.Circuit(id=0, name=None)
            xCountry = gtClass.Country(
                cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)
            xTrack = gtClass.Track(id=0, name=None, countryObj=xCountry)
            xTrackLayout = gtClass.TrackLayout(
                id=0, name=None, miles=None, trackObj=xTrack, circuitObj=xCircuit)

        return xTrackLayout

    def getTrack(self, key='trackId', value=None):
        """
        Gets a single Track record from database based on key and value passed.

        ARGS:
        value : Is the value being search for.
        key   : the column to search on. trackId, or track. Default is trackId
        Returns : Track Object. IF TrackObject.id == 0 then nothing found.
        """
        if key == 'trackId':
            whereSQL = "WHERE trackId = ?"
        elif key == 'track':
            whereSQL = "WHERE track = ?"

        sql = self._selectTrackLayoutSQL + " " + whereSQL
        theVals = (value,)
        logger.debug(f"sql = {sql}")
        logger.debug(f"theVals = {theVals}")
        try:
            # Enable the .keys() to get column names.
            self.conn.row_factory = sqlite3.Row
            c = self.conn.cursor()
            c.execute(sql, theVals)
            row = c.fetchone()
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            return None
        if row:  # Populate the track object
            logger.debug("track found")
            xCountry = gtClass.Country(
                cntryID=row['cntryId'], cntryName=row['Country'], alpha2=row['alpha2'], alpha3=row['alpha3'], region=row['Region'])
            xTrack = gtClass.Track(
                id=row['trackId'], name=row['track'], countryObj=xCountry)

        else:  # create a blank track object
            logger.debug("no track found")
            xCountry = gtClass.Country(
                cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)
            xTrack = gtClass.Track(id=0, name=None, countryObj=xCountry)

        logger.debug(f'track = {xTrack}')
        return xTrack

    def mfg_update(self, mfgObj):
        """Update a manufacture record in database

        ARGS: mfgObj is the Manufacture class object
        - Record that will be UPDATED is based on mfgObj.id.
        WARNING! - Do not change original mfgObj.id. Unexpected results will occur
        Returns - list(ResultCode, ResultText)
                ResultCode 0 = Success execution
                Resultcode != 0 - See ResultText for details
        """
        logger.debug(f"manufacture record update {mfgObj}")
        # Sanity check - does the mfgRecord exist in db?
        logger.debug("sanity check. confirm mfg Record exists.")
        testMfg = self.getMfg(value=mfgObj.id)
        if testMfg.id == 0:  # Mfg is not in database
            r = [1, f"manufacture id {mfgObj.id} not in database."]
            logger.debug(f"returning {r}")
            return r

        logger.debug("sanity check passed. execute SQL")
        theVals = {'mfgID': mfgObj.id, 'mfgName': mfgObj.name,
                   'cntryID': mfgObj.country.id}
        sql = "UPDATE manufacture SET name = :mfgName, country_id = :cntryID WHERE id = :mfgID"

        r = self._exeSQL(sql, theVals)
        if r[0] == 0:
            r[1] = f"Manufacture id: {mfgObj.id} Updated"
        else:
            logger.debug(f"problem updating manufacture id: {mfgObj.id}")

        logger.debug(f"returning {r}")
        return r

    def updateTrack(self, trackObj):
        """Update a manufacture record in database

        ARGS: mfgObj is the Manufacture class object
        - Record that will be UPDATED is based on mfgObj.id.
        WARNING! - Do not change original TrackObj.id. Unexpected results will occur
        Returns - list(ResultCode, ResultText)
                ResultCode 0 = Success execution
                Resultcode != 0 - See ResultText for details
        """
        logger.debug(f"track record update {trackObj}")
        # Sanity check - does the track record exist in db?
        testMfg = self.getTrack(value=trackObj.id)
        if testMfg.id == 0:  # Mfg is not in database
            return [1, f"track id {trackObj.id} not in database."]

        theVals = {'trackID': trackObj.id, 'trackName': trackObj.name,
                   'cntryID': trackObj.country.id}
        sql = "UPDATE track SET name = :trackName, country_id = :cntryID WHERE id = :trackID"

        return self._exeSQL(sql, theVals)
