import sys
import logging
import sqlite3
from pathlib import Path

# TODO: Put logger.warning for add/update/delete. Should just rely on _exeSQL for warning. Not sure what called it.
# TODO: got to work on TrackLayout stuff
# Custom App modules
from GranT import GTClasses as gtClass

logger = logging.getLogger(__name__)


class GTdb:
    def __init__(self, name=None):
        self.conn = None
        logger.debug(f'name is {name}')
        if name:
            logger.debug(f"attempt open db {name}")
            try:
                self.conn = sqlite3.connect(
                    name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            except sqlite3.Error as errID:
                logger.critical(
                    f"Database connection failure. ", exc_info=True)
                sys.exit(1)
            c = self.conn.cursor()
            logger.debug(f"Connected {name}")
            c.execute("PRAGMA database_list;")
            xtmp = c.fetchall()
            logger.debug(f"database_list={xtmp}")
            self.dbfile = xtmp[0][2]

    def _exeSQL(self, sql, theVals):
        """Executes INSERT, DELETE, UPDATE sql. (internal use only)

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
            # Enabling full sql traceback to logger.debug
            self.conn.set_trace_callback(logger.debug)
            c.execute(sql, theVals)
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            logger.warning(f"sqlite integrity error: {e.args[0]}")
            return [2, f"sqlite integrity error: {e.args[0]}"]
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            sys.exit(1)

        logger.debug("successful commit of sql")
        # Disable full sql traceback to logger.debug
        self.conn.set_trace_callback(None)
        return [0, "Commit successful"]

    def _exeScriptFile(self, scriptFileName=None):
        """
        Executes a Script file. (internal use only)
        scriptFileName : SQL script file to run
        """
        logger.debug(f"loading script {scriptFileName} to memory")
        scriptFile = open(scriptFileName, 'r')
        script = scriptFile.read()
        scriptFile.close()
        try:
            c = self.conn.cursor()
            c.executescript(script)
        except:
            logger.critical(
                f"Unexpected Error running script {scriptFileName}", exc_info=True)
            sys.exit(1)

        self.conn.commit()
        logger.debug(f"script commited")

    def _addLayoutRec(self, tLayout):
        """Internal use only. Add layout rec to db with no checks

        Args:
            tLayout (TrackLayout Object)

        Returns:
            list: ResultCode, ResultText
            ResultCode = 0 Successfull
            ResultCode != 0 See ResultText for details
        """
        logger.debug(f"trackobj = {tLayout}")
        theVals = {'layoutName': tLayout.name, 'miles': tLayout.miles,
                   'circuitId': tLayout.circuit.id, 'trackId': tLayout.track.id}
        sql = 'INSERT INTO track_layout (name, miles, track_id, circuit_id) VALUES (:layoutName, :miles, :trackId, :circuitId)'
        return self._exeSQL(sql, theVals)

    def trackLayoutTests(self, trackLayout):
        """Tests to save/update a track layout

        Args:
            trackLayout (TrackLayout object): Track Layout that is being saved

        Returns:
            list: (True/False, msg)
            True = Tests passed
            False = See msg for what did not pass
        """
        logger.debug(f"trackLayout={trackLayout}")
        # Layout name must be unique for the Track
        logger.info(
            f"Checking if layout [{trackLayout.name}] already exists for track (case insensitve)")
        layoutList = self.getLayoutList('trackId', trackLayout.track.id)
        if trackLayout.name:  # layout name exists go uppercase
            xLayoutName = trackLayout.name.upper()
        else:
            xLayoutName = trackLayout.name

        for row in layoutList:
            logger.debug(f"check {row[3]}")
            if row[3]:  # layout name exists go uppercase
                testName = row[3].upper()
            else:
                testName = row[3]
            if testName == xLayoutName:  # layout name exist for track
                msg = f"Layout name [{trackLayout.name}] for Track [{row[1]}] already exists"
                result = (False, msg)
                logger.info(f"returning = {result}")
                return result

        # Miles is not a string. (Null is allowed in this test)
        logger.info(f"Checking miles [{trackLayout.miles}] is not a string")
        if isinstance(trackLayout.miles, str):  # miles is a string
            result = (False, f"Miles must not contain letters")
            logger.info(f"returning = {result}")
            return result
        # Miles is not null. not tested. DB should provide integrity error: NOT NULL constraint failed
        # Circuit ID existance not tested. DB should provide integrity error: FOREIGN KEY constraint failed
        # Track ID existance not tested. DB should provide integrity error: FOREIGN KEY constraint failed
        # All tests passed
        result = (True, "Track Layout Tests Passed")
        logger.info(f"returning = {result}")
        return result

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
            # Enabling full sql traceback to logger.debug
            self.conn.set_trace_callback(logger.debug)
            c = self.conn.cursor()
            c.execute(sql, theVars)
            row = c.fetchone()
            # Disable full sql traceback to logger.debug
            self.conn.set_trace_callback(None)
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            sys.exit(1)

        if row:
            # Place results into Manufacture object
            logger.debug("manufacture found.")
            xCountry = gtClass.Country(
                cntryID=row['cntryId'], cntryName=row['Country'],
                alpha2=row['alpha2'], alpha3=row['alpha3'], region=row['region'])

            xMake = gtClass.Manufacture(
                id=row['mfgid'], name=row['Make'], countryObj=xCountry)
            logger.debug(f"returning manufacture object")
        else:
            # Create blank Manufacture object
            logger.debug("manufacture not found.")
            xCountry = gtClass.Country(
                cntryID=0, cntryName='', alpha2='', alpha3='', region='')

            xMake = gtClass.Manufacture(
                id=0, name='', countryObj=xCountry)
            logger.debug(f"returning blank manufacture object")

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
            # Enabling full sql traceback to logger.debug
            self.conn.set_trace_callback(logger.debug)
            dbCursor.execute(sql)
            result = dbCursor.fetchall()
            logger.info(f"Returning all Manufacture results")
            # Disable full sql traceback to logger.debug
            self.conn.set_trace_callback(None)
            return result
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            sys.exit(1)

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

    def addMfg(self, mfgObj):
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

    def addTrack(self, layout):
        """Adding a Track and a Layout for it

        Args:
            layout : Track layout object

        Returns:
            list: ResultCode, ResultText
            ResultCode = 0 Successfull
            ResultCode != 0 See ResultText for details
        """
        logger.info(f"Adding a new track {layout}")
        xtrack = self.getTrack('track', layout.track.name)
        if xtrack.id != 0:  # track with same name exists - ReturnCode 100
            msg = f"Unable to save. Track name already in db. Track name = {layout.track.name}"
            logger.warning(msg)
            result = (100, msg)
            logger.debug(f"returning: {result}")
            return result
        else:
            logger.info("Confirmed track doesn't exist")

        xcircuit = self.getCircuit('id', layout.circuit.id)
        if xcircuit.id == 0:  # circuit does not exist -ReturnCode 102
            msg = f'Unable to save. Circuit does not exist'
            logger.warning(msg)
            result = (102, msg)
            logger.debug(f"returning: {result}")
            return result
        else:
            logger.info("Confirmed circuit exists")

        if not layout.miles:  # Miles must have a value - ReturnCode 103.
            msg = f"Unable to save. Invalid miles value {layout.miles}"
            logger.warning(msg)
            result = (103, msg)
            logger.debug(f"returning: {result}")
            return result
        else:
            logger.info("Confirmed miles has a value")

        # Tests Passed. Now we add records
        # Add track record
        logger.info("Saving new track record")
        theVals = {'trackName': layout.track.name,
                   'cntryID': layout.track.country.id}
        sql = "INSERT INTO track (name, country_id) VALUES (:trackName, :cntryID)"
        logger.debug(f"sql={sql}")
        logger.debug(f"theVals={theVals}")
        result = self._exeSQL(sql, theVals)
        if result[0] == 2:  # integrity error
            msg = f"error saving track record. error: {result}"
            logger.error(msg)
            result = (104, msg)
            logger.debug(f"returning: {result}")
            return result
        else:
            # Get new track.id from db to update layout object
            logger.debug("Getting new track.id")
            uTrack = self.getTrack("track", layout.track.name)
            logger.info(f"Successfully saved new track record {uTrack}")
            logger.debug(
                "update trackLayout object with new track.id {uTrack.id}")
            layout.track.id = uTrack.id

        # Add track layout record
        logger.info("Saving track_layout record")
        result = self._addLayoutRec(layout)
        if result[0] == 2:  # integrity error
            msg = f"error saving track_layout record. error: {result}"
            logger.error(msg)
            result = (105, msg)
            logger.debug(f"returning: {result}")
            return result
        else:
            logger.info("Successfully saved new track_layout record")

        logger.debug(f"returning: {result}")
        return result

    def addLayout(self, trackLayout):
        """Adds a Track Layout record

        Args:
            trackLayout : TrackLayout Object

        Returns:
            list: ResultCode, ResultText
                ResultCode 0 = Success
                ResultCode != 0 = see ResultText for details
        """
        logger.debug(f"addTrackLayout: trackLayout={trackLayout}")
        logger.info(
            f"Adding track layout {trackLayout.name} for track {trackLayout.track.name}.")
        tResult = self.trackLayoutTests(trackLayout)
        if tResult[0]:  # Tests passed
            result = self._addLayoutRec(trackLayout)
        else:
            logger.warning(tResult[1])
            result = (1, tResult[1])

        logger.debug(f"returning: {result}")
        return result

    def deleteMfg(self, mfgId):
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

    def deleteTrack(self, trackId):
        """Delete track and all related track layouts from db

        Args:
            trackId (int): UniqueID of the track in the db

        Returns:
            list: ResultCode, ResultText
                ResultCode 0 : successfull
                Resultcode != 0 : See ResultText for details
        """
        logger.info(
            f"Delete track trackId={trackId} and related track layouts.")
        result = (1, "method is not ready yet")
        # 1-Get and delete track_layout records for track id
        #   Get list of track_layouts for trackid
        logger.info(f"Getting track layouts for trackid {trackId}")
        trackLayouts = self.getLayoutList(key='trackId', value=trackId)
        logger.info(f"track layouts to delete: {len(trackLayouts)}")
        logger.info(f"trackLayouts = {trackLayouts}")
        #   Delete each track layout
        for tLayout in trackLayouts:
            layoutId = tLayout[2]
            logger.debug(f"Deleting trackLayoutID {layoutId}: {tLayout}")
            result = self.deleteTrackLayout(layoutId)
            if result[0] != 0:  # error with delete. Stop deleting
                logger.warning(
                    f"problem deleting track layout id={layoutId}. See {result}.")
                return result

        # 2-If that was successfull then delete track
        sql = "DELETE FROM track WHERE id = ?"
        theVals = (trackId,)
        logger.debug(f"sql={sql}")
        logger.debug(f"theVals={theVals}")
        result = self._exeSQL(sql, theVals)
        if result[0] == 0:
            result[1] = f"track id={trackId} deleted"
        else:
            logger.warning(
                f"problem deleting track id={trackId}. See {result}.")

        return result

    def deleteTrackLayout(self, layoutId):
        """Delete track layout from db

        Args:
            layoutId (int): UniqueID of the track layout in the db

        Returns:
            list: ResultCode, ResultText
                ResultCode 0 : successfull
                Resultcode != 0 : See ResultText for details
        """
        logger.info(f"Delete track layout id={layoutId}.")
        result = (1, "method is not ready yet")
        sql = "DELETE FROM track_layout WHERE id = ?"
        theVals = (layoutId,)
        logger.debug(f"sql={sql}")
        logger.debug(f"theVals={theVals}")
        result = self._exeSQL(sql, theVals)
        if result[0] == 0:
            result[1] = f"track layout id={layoutId} deleted"
        else:
            logger.warning(
                f"problem deleting track layout id={layoutId}. See {result}.")

        logger.info(f"returning {result}")
        return result

    def getCircuit(self, key, value):
        """Get circuit record from db

        Args:
            key (str): key to search for value.
                'id' or 'name'
            value : Value to search for in key

        Returns:
            CircuitObject
        """
        logger.info(f"Getting a circuit key={key}, value={value}")
        selectSQL = "SELECT c.id as circuitId, c.name AS Circuit FROM circuit AS c"

        if key == 'id':
            whereSQL = "WHERE c.id = ?"
        elif key == 'name':
            whereSQL = "WHERE c.name = ?"
        else:  # no key passed
            logger.critical("Invalid or missing key value passed.")
            sys.exit(1)

        sql = f"{selectSQL} {whereSQL}"
        theVals = (value,)
        logger.debug(f"sql = {sql}")
        logger.debug(f"theVals = {theVals}")
        try:
            self.conn.row_factory = sqlite3.Row  # .keys() enabled for column names
            # enable full sql trackback to logger.debug
            self.conn.set_trace_callback(logger.debug)
            c = self.conn.cursor()
            c.execute(sql, theVals)
            row = c.fetchone()
            # Disable full sql traceback
            self.conn.set_trace_callback(None)
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            sys.exit(1)

        if row:  # populate ciruit object
            logger.info(f"Circuit found")
            xCircuit = gtClass.Circuit(row['circuitId'], row['Circuit'])
        else:  # create blank ciruit object
            logger.info(f"Circuit not found")
            xCircuit = gtClass.Circuit(id=0, name=None)

        logger.debug(f"returning: {xCircuit}")
        return xCircuit

    def getLayout(self, layoutId):
        """Gets a single Track Layout record from database.

        Args:
            layoutId (int): Track layoutID number to get from database.
        Returns:
            TrackLayout Object: IF TrackLayoutObject.id == 0 then nothing found
        """
        logger.info(f"Getting track layout id {layoutId}")
        sql = """SELECT t.id as trackId, t.name AS track, l.id AS layoutId, l.name AS layout, l.miles AS Miles, c.id as circuitId, c.name AS Circuit, cntry.ID as cntryId, cntry.name as Country, cntry.alpha2, cntry.alpha3, cntry.region as Region FROM track as t INNER JOIN track_layout as l ON t.id = l.track_id LEFT JOIN country as cntry ON t.country_id = cntry.ID INNER JOIN circuit AS c ON l.circuit_id = c.id WHERE l.id = ?"""
        theVals = (layoutId,)
        # Execute the SQL
        logger.debug(f"sql: {sql}")
        try:
            # Enable the .keys() to get column names.
            self.conn.row_factory = sqlite3.Row
            # Enabling full sql traceback to logger.debug
            self.conn.set_trace_callback(logger.debug)
            c = self.conn.cursor()
            c.execute(sql, theVals)
            row = c.fetchone()
            # Disable full sql traceback to logger.debug
            self.conn.set_trace_callback(None)
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            sys.exit(1)

        if row:  # Populate trackLayout obj
            logger.info(f"Found track layout id {layoutId}")
            xCircuit = gtClass.Circuit(row['circuitId'], row['Circuit'])
            logger.debug(f"xCircuit={xCircuit}")
            xCountry = gtClass.Country(
                cntryID=row['cntryId'], cntryName=row['Country'],
                alpha2=row['alpha2'], alpha3=row['alpha3'], region=row['region'])
            logger.debug(f"xCountry={xCountry}")
            xTrack = gtClass.Track(
                row['trackId'], name=row['track'], countryObj=xCountry)
            logger.debug(f"xTrack={xTrack}")
            xTrackLayout = gtClass.TrackLayout(
                row['layoutId'], row['layout'], miles=row['Miles'], trackObj=xTrack, circuitObj=xCircuit)

        else:  # Create blank trackLayout obj (no data returned)
            logger.info(f"Unable to find track layout id {layoutId}")
            logger.debug(f"creating empty tracklayout object")
            xCircuit = gtClass.Circuit(id=0, name=None)
            xCountry = gtClass.Country(
                cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)
            xTrack = gtClass.Track(id=0, name=None, countryObj=xCountry)
            xTrackLayout = gtClass.TrackLayout(
                id=0, name=None, miles=None, trackObj=xTrack, circuitObj=xCircuit)

        logger.debug(f"returning object xTrackLayout={xTrackLayout} ")
        return xTrackLayout

    def getLayoutList(self, key, value):
        """Get a list track layouts by key/column

        Args:
            key (str): The key/column to search for value. Defaults to 'trackId'.
            value: Value to search for in key/column.

        Returns:
            list: (trackId,track,layoutId,layout,Miles,circuitId,
                   Circuit,cntryId,Country,alpha2,alpha3,Region)
        """
        logger.info(f"Getting track layout list: key={key}, value={value}")
        selectSQL = """SELECT t.id as trackId, t.name AS track, l.id AS layoutId, l.name AS layout, l.miles AS Miles, c.id as circuitId, c.name AS Circuit, cntry.ID as cntryId, cntry.name as Country, cntry.alpha2, cntry.alpha3, cntry.region as Region FROM track as t INNER JOIN track_layout as l ON t.id = l.track_id LEFT JOIN country as cntry ON t.country_id = cntry.ID INNER JOIN circuit AS c ON l.circuit_id = c.id"""
        orderBySQL = "ORDER BY t.name, l.name"
        if key == 'trackId':
            whereSQL = "WHERE trackId = ?"
        elif key == 'layoutId':
            whereSQL = "WHERE layoutId = ?"
        elif key == 'circuitId':
            whereSQL = "WHERE circuitId = ?"
        elif key == 'cntryId':
            whereSQL = "WHERE cntryId = ?"

        dbCursor = self.conn.cursor()
        # Enabling full sql traceback to logger.debug
        self.conn.set_trace_callback(logger.debug)
        if key == None:
            sql = f"{selectSQL} {orderBySQL}"
            logger.debug(f"NO KEY PROVIDED")
            logger.debug(f"sql = {sql}")
            try:
                dbCursor.execute(sql)
            except:
                logger.critical(
                    f'Unexpected error executing sql: {sql}', exc_info=True)
                sys.exit(1)
        else:
            logger.debug(f"KEY PROVIDED")
            sql = f"{selectSQL} {whereSQL} {orderBySQL}"
            theVals = (value,)
            logger.debug(f"sql = {sql}")
            logger.debug(f"theVals = {theVals}")
            try:
                dbCursor.execute(sql, theVals)
            except:
                logger.critical(
                    f'Unexpected error executing sql: {sql}', exc_info=True)
                sys.exit(1)

        result = dbCursor.fetchall()
        # Disable full sql traceback to logger.debug
        self.conn.set_trace_callback(None)
        return result

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

        sqlSelect = """SELECT t.id as trackId, t.name AS track, cntry.ID as cntryId, cntry.name as Country, cntry.alpha2, cntry.alpha3, cntry.region as Region FROM track as t LEFT JOIN country as cntry ON t.country_id = cntry.ID"""
        sql = sqlSelect + " " + whereSQL
        theVals = (value,)
        logger.debug(f"sql = {sql}")
        logger.debug(f"theVals = {theVals}")
        try:
            # Enable the .keys() to get column names.
            self.conn.row_factory = sqlite3.Row
            # Enabling full sql traceback to logger.debug
            self.conn.set_trace_callback(logger.debug)
            c = self.conn.cursor()
            c.execute(sql, theVals)
            row = c.fetchone()
            # Disable full sql traceback to logger.debug
            self.conn.set_trace_callback(None)
        except:
            logger.critical(
                f'Unexpected error executing sql: {sql}', exc_info=True)
            sys.exit(1)
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

    def updateMfg(self, mfgObj):
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
        """[summary]

        Args:
            trackObj ([type]): [description]

        Returns:
            list: ResultCode, ResultText
                ResultCode 0 = Success
                ResultCode != 0 = see ResultText for details
        """
        logger.debug(f"track record update {trackObj}")
        # Sanity check - See if tracking id exists
        testObj = self.getTrack(value=trackObj.id)
        if testObj.id == 0:  # Not found in db
            return [1, f"track id {trackObj.id} not in database."]

        theVals = {'trackID': trackObj.id, 'trackName': trackObj.name,
                   'cntryID': trackObj.country.id}
        sql = "UPDATE track SET name = :trackName, country_id = :cntryID WHERE id = :trackID"

        return self._exeSQL(sql, theVals)

    def updateTrackLayout(self, uLayout):
        """Update the track layout record in database

        Args:
            uLayout (TrackLayout Object) : Updated TrackLayout Object

        Returns:
            list: ResultCode, ResultText
                ResultCode 0 = Success
                ResultCode != 0 = see ResultText for details
        """
        logger.info(f"Updating Track Layout {uLayout}")

        tResult = self.trackLayoutTests(uLayout)
        if tResult[0]:  # Tests passed
            logger.info("Updating track layout id: {uLayout.id}")
            sql = "UPDATE track_layout SET name = :layoutName, miles = :miles, track_id = :trackId, circuit_id = :circuitId"
            theVals = {'layoutName': uLayout.name, 'miles': uLayout.miles,
                       'circuitId': uLayout.circuit.id, 'trackId': uLayout.track.id}
            logger.debug("sql={sql}")
            logger.debug("theVals = {theVals}")
            result = self._exeSQL(sql, theVals)
        else:
            logger.warning(tResult[1])
            result = (1, tResult[1])

        logger.debug(f"returning: {result}")
        return result

    def _logtest(self):
        """Test logging by sending text to all levels
        """
        logger.info("Log Test - info level")
        logger.warning("Log Test - info warning")
        logger.error("Log Test - info error")
        logger.critical("Log Test - info critical")
        logger.debug("Log Test - info debug")
