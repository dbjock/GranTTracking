import sys
import logging
import sqlite3
from pathlib import Path

# Custom App modules
from GranT import GTClasses as gtClass

logger = logging.getLogger(__name__)


def create_connection(dbLoc=":memory:"):
    """Create a connection to a sqlite3 db.
    Note: This will NOT init db with the schema.

    Args:
        dbLoc ([str]): dbFile to connect to
        Default value is ":memory:"

    Returns:
        sqlite3.connect [object]: Connection to database
    """
    logger.debug(f"dbLoc = {dbLoc}")
    if dbLoc:
        logger.info(f"Connecting to {dbLoc}")
        try:
            conn = sqlite3.connect(
                dbLoc, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        except Exception as err:
            logger.critical(f"Unable to connect to {dbLoc}")
            logger.critical(f"Error:  {err}", exc_info=True)
            sys.exit(1)

        logger.info(f"Successful connection to {dbLoc}")
        logger.debug(f"sqlite3 version {sqlite3.version}")
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = on;")
        cur.execute("PRAGMA database_list;")
        xtmp = cur.fetchall()
        logger.debug(f"database_list={xtmp}")
        return conn
    else:  # Critical exit
        logger.critical('dbLoc must contain a value')
        sys.exit(1)
    sys.exit(1)


def _addLayoutRec(dbConn, tLayout):
    """Internal use only. Add layout rec to db with no checks

    Args:
        dbConn (sqlite3.connect): Database connection
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
    return _exeDML(dbConn, sql, theVals)


def _exeDML(dbConn, sql, theVals):
    """Executes DML commands, INSERT, DELETE, UPDATE sql.

    Args:
        dbConn (sqlite3.connect): Database connection
        sql (string): Sql to execute
        theVals : Values to be sanitized
    Returns:
        list (ResultCode, ResultText)
        ResultCode == 0 Success. ResultText will have cursor.lastrowid
        ResultCode != 0 - See ResultText for details
    """
    logger.debug(f"Passed sql={sql}")
    logger.debug(f"Passed Vals={theVals}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        rowID = cur.lastrowid
        logger.debug(f"RowID = {rowID}")
        dbConn.commit()
    except sqlite3.IntegrityError as e:
        logger.warning(f"sqlite integrity error: {e.args[0]}")
        # Disable full sql traceback to logger.debug
        dbConn.set_trace_callback(None)
        return [2, f"sqlite integrity error: {e.args[0]}"]
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
        logger.debug("successful commit of sql")
        # Disable full sql traceback to logger.debug
        dbConn.set_trace_callback(None)
        return [0, f"Commit successful rowID={rowID}"]

    logger.debug("successful commit of sql")
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)
    return [0, f"Commit successful rowID={rowID}"]


def _exeScriptFile(dbConn, scriptFileName=None):
    """ INTERNAL USE Only. executes a Script file.

    Args:
        dbConn (sqlite3.connect): Database connection
        scriptFileName : SQL script file to run. Defaults to None.
    """
    logger.debug(f"loading script {scriptFileName} to memory")
    scriptFile = open(scriptFileName, 'r')
    script = scriptFile.read()
    scriptFile.close()
    try:
        cur = dbConn.cursor()
        cur.executescript(script)
    except:
        logger.critical(
            f"Unexpected Error running script {scriptFileName}", exc_info=True)
        sys.exit(1)

    dbConn.commit()
    logger.debug(f"script commited")


def addTrack(dbConn, layout):
    """Adding a Track and a Layout for it

    Args:
        dbConn (sqlite3.connect): Database connection
        layout : Track layout object

    Returns:
            list: ResultCode, ResultText
            ResultCode = 0 Successfull
            ResultCode != 0 See ResultText for details
    """
    logger.info(f"Adding a new track {layout}")
    xtrack = getTrack(dbConn, key='track', value=layout.track.name)
    if xtrack.id != 0:  # track with same name exists - ReturnCode 100
        msg = f"Unable to save. Track name already in db. Track name = {layout.track.name}"
        logger.warning(msg)
        result = (100, msg)
        logger.debug(f"returning: {result}")
        return result
    else:
        logger.info("Confirmed track doesn't exist")

    xcircuit = getCircuit(dbConn, key='id', value=layout.circuit.id)
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
    result = _exeDML(dbConn, sql, theVals)
    if result[0] == 2:  # integrity error
        msg = f"error saving track record. error: {result}"
        logger.error(msg)
        result = (104, msg)
        logger.debug(f"returning: {result}")
        return result
    else:
        # Get new track.id from db to update layout object
        logger.debug("Getting new track.id")
        uTrack = getTrack(dbConn, key="track", value=layout.track.name)
        logger.info(f"Successfully saved new track record {uTrack}")
        logger.debug(
            "update trackLayout object with new track.id {uTrack.id}")
        layout.track.id = uTrack.id

    # Add track layout record
    logger.info("Saving track_layout record")
    result = _addLayoutRec(dbConn, layout)
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


def addLayout(dbConn, trackLayout):
    """Adds a Track Layout record

    Args:
        dbConn (sqlite3.connect): Database connection
        trackLayout : TrackLayout Object

    Returns:
        list: ResultCode, ResultText
              ResultCode 0 = Success
              ResultCode != 0 = see ResultText for details
    """
    logger.debug(f"addTrackLayout: trackLayout={trackLayout}")
    logger.info(
        f"Adding track layout {trackLayout.name} for track {trackLayout.track.name}.")
    tResult = validateTrackLayout(dbConn, trackLayout)
    if tResult[0]:  # Tests passed
        result = _addLayoutRec(dbConn, trackLayout)
    else:
        logger.warning(tResult[1])
        result = (1, tResult[1])

    logger.debug(f"returning: {result}")
    return result


def addMfg(dbConn, mfgObj):
    """[summary]

    Args:
        dbConn (sqlite3.connect): Database connection
        mfgObj : Manufacture class object

    Returns:
        list:  (ResultCode, ResultText)
                ResultCode == 0: Success Add
                Resultcode <> 0: See ResultText for details[description]
            Fields which cause common errors.
            - mfgObj.mfgName must be unique in db (case insensitive).
            - mfgObj.country.id must exist in Country table in db.
            mfgObj.id is ignored
    """
    logger.debug(f"add mfg: MfgObj= {mfgObj}")
    sql = "INSERT INTO manufacture (name, country_id) VALUES (:mfgName, :cntryID)"
    theVals = {'mfgName': mfgObj.name, 'cntryID': mfgObj.country.id}
    r = _exeDML(dbConn, sql, theVals)
    if r[0] == 0:
        r[1] = f"Manufacture name: {mfgObj.name} added"
    else:
        logger.debug(f"problem with manufacture add {r}.")

    logger.debug(f"returning {r}")
    return r


def addRace(dbConn, race):
    """Adding a Race to database

    Args:
        dbConn (sqlite3.connect): Database connection
        race ([Object]): The race object to add

    Returns:
        list: ResultCode, ResultText
              ResultCode == 0 Successful
              ResultCode !=0 Unsuccessful, see ResultText
    """
    logger.debug(f"addRace: race={race}")
    logger.info(
        f"Adding race {race.name} for Race Collection {race.raceCollection.name}")
    tResult = validateRace(dbConn, race)
    if tResult[0]:  # Tests passed - Save the Race
        sql = "INSERT INTO race (name, tl_id, rc_id,racetime,weather_id,limits,type_id,notes) VALUES (:name, :trackLayoutID, :raceColID,:racetime,:weather_id, :limits, :type_id, :notes)"
        theVals = {'name': race.name,
                   'trackLayoutID': race.trackLayout.id,
                   'raceColID': race.raceCollection.id,
                   'racetime': race.racetime,
                   'weather_id': race.weather.id,
                   'limits': race.limits,
                   'type_id': race.raceType.id,
                   'notes': race.notes}
        logger.debug(f"sql={sql}")
        logger.debug(f"theVals={theVals}")
        result = _exeDML(dbConn, sql, theVals)
    else:
        logger.warning(tResult[1])
        result = (1, tResult[1])

    logger.debug(f"returning: {result}")
    return result


def addRaceCollection(dbConn, raceCollection):
    """Add a Race Collection to database

    Args:
        dbConn (sqlite3.connect): Database connection
        raceCollection : raceCollection Object

    Returns:
        list: (ResultCode, ResultText)
              ResultCode 0 = Success Add
              Resultcode <> 0 - See ResultText for details
    """
    logger.debug(f"raceCollection={raceCollection}")
    # Collection name must have a value
    if raceCollection.name == None or raceCollection.name == "":
        rtrnMsg = [1, "Collection name can not be blank"]
        logger.debug(f"Return {rtrnMsg}")
        return rtrnMsg

    # Collection name must be unique for this league
    xlist = getRaceCollectionList(dbConn, raceCollection.league.id)
    logger.debug(f"xlist={xlist}")
    for r in xlist:
        if raceCollection.name == r[1]:  # match
            rtrnMsg = [
                1, f"Collection name [{raceCollection.name}] already exists for League id [{raceCollection.league.id}]"]
            logger.debug(f"Return {rtrnMsg}")
            return rtrnMsg

    # Tests Passed
    theVals = {'colName': raceCollection.name,
               'colDesc': raceCollection.desc,
               'leagueId': raceCollection.league.id,
               'catId': raceCollection.classcat.id,
               'prize1': raceCollection.prize1,
               'prize2': raceCollection.prize2,
               'prize3': raceCollection.prize3}
    sql = "INSERT INTO race_collection (league_id, name, description, cat_id, prize1, prize2, prize3) VALUES (:leagueId, :colName, :colDesc, :catId, :prize1, :prize2, :prize3)"
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    rtrnMsg = _exeDML(dbConn, sql, theVals)
    logger.debug(f"Return {rtrnMsg}")
    return rtrnMsg


def deleteMfg(dbConn, mfgId):
    """Delete manufacture record from database

    ARGS:
        dbConn (sqlite3.connect): Database connection
        mfgId: UniqueID of Manufacture in DB(Manufacture.id)

    Returns:
        list: (ResultCode, ResultText)
                ResultCode == 0: it worked
                Resultcode <> 0: See ResultText for details
    """
    logger.debug(f"delete manufacture id={mfgId}")
    sql = "DELETE FROM manufacture WHERE id = ?"
    theVals = (mfgId,)
    result = _exeDML(dbConn, sql, theVals)
    if result[0] == 0:
        result[1] = "Manufacture Deleted"
    else:
        logger.debug(f"problem with manufacture delete {r}.")

    logger.debug(f"returning {result}")
    return result


def deleteTrack(dbConn, trackId):
    """Delete track and all related track layouts from db

    Args:
        dbConn (sqlite3.connect): Database connection
        trackId (int): UniqueID of the track in the db

    Returns:
            list: ResultCode, ResultText
                  ResultCode == 0 : successful
                  Resultcode != 0 : See ResultText for details
    """
    logger.info(
        f"Delete track trackId={trackId} and related track layouts.")
    result = (1, "method is not ready yet")
    # 1-Get and delete track_layout records for track id
    #   Get list of track_layouts for trackid
    logger.info(f"Getting track layouts for trackid {trackId}")
    trackLayouts = getLayoutList(dbConn, trackId)
    logger.info(f"track layouts to delete: {len(trackLayouts)}")
    logger.info(f"trackLayouts = {trackLayouts}")
    #   Delete each track layout
    for tLayout in trackLayouts:
        layoutId = tLayout[0]
        logger.debug(f"Deleting trackLayoutID {layoutId}: {tLayout}")
        result = deleteTrackLayout(dbConn, layoutId)
        if result[0] != 0:  # error with delete. Stop deleting
            logger.warning(
                f"problem deleting track layout id={layoutId}. See {result}.")
            return result

    # 2-If that was successfull then delete track
    sql = "DELETE FROM track WHERE id = ?"
    theVals = (trackId,)
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    result = _exeDML(dbConn, sql, theVals)
    if result[0] == 0:
        result[1] = f"track id={trackId} deleted"
    else:
        logger.warning(
            f"problem deleting track id={trackId}. See {result}.")

    return result


def deleteTrackLayout(dbConn, layoutId):
    """Delete track layout from db

    Args:
        dbConn (sqlite3.connect): Database connection
        layoutId (int): UniqueID of the track layout in the db

    Returns:
        list: ResultCode, ResultText
              ResultCode == 0 : successful
              Resultcode != 0 : See ResultText for details
    """
    logger.info(f"Delete track layout id={layoutId}.")
    result = (1, "method is not ready yet")
    sql = "DELETE FROM track_layout WHERE id = ?"
    theVals = (layoutId,)
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    result = _exeDML(dbConn, sql, theVals)
    if result[0] == 0:
        result[1] = f"track layout id={layoutId} deleted"
    else:
        logger.warning(
            f"problem deleting track layout id={layoutId}. See {result}.")

    logger.info(f"returning {result}")
    return result


def getCarCat(dbConn, id):
    """Get a Car Class Category from db

    Args:
        dbConn (sqlite3.connect): Database connection
        id (id): Clar Class Cateory ID

    Returns:
        ClassCat object
        IF ClassCat.id == 0 then ClassCat was not found
    """
    logger.info(f"Getting classCat by id: {id}")
    selectSQL = "SELECT id,name,description,sortOrder FROM category"
    whereSQL = "WHERE id = ?"
    value = id
    sql = f"{selectSQL} {whereSQL}"
    theVals = (value,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        row = cur.fetchone()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback
    dbConn.set_trace_callback(None)
    logger.debug(f"row={row}")
    if row:  # Create ClassCat object
        rtnObj = gtClass.ClassCat(
            id=row[0], name=row[1], desc=row[2])
        rtnObj.sortOrder = row[3]
    else:  # Create an empty ClassCat object
        rtnObj = gtClass.ClassCat(id=0, name="", desc="")

    logger.debug(f"rtnObj={rtnObj}")
    return rtnObj


def getCarCats(dbConn):
    """Gets all the car category/classes in db and returns as a list

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
        list(id, carClass, desc, sortorder)
        """
    logger.info("Getting list of all the car categories")
    selectSQL = "SELECT c.id as id, c.name as carClass, c.description as desc, c.sortOrder as sortorder FROM category as c ORDER BY c.sortOrder"
    sql = selectSQL
    logger.debug(f"sql = {sql}")

    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)
    logger.info(f"Returning {len(result)} rows")
    return result


def getCircuit(dbConn, key='id', value=None):
    """Get circuit record from db

    Args:
        dbConn (sqlite3.connect): Database connection
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
    # enable full sql trackback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        row = cur.fetchone()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback
    dbConn.set_trace_callback(None)
    if row:  # populate ciruit object
        logger.info(f"Circuit found")
        xCircuit = gtClass.Circuit(id=row[0], name=row[1])
    else:  # create blank ciruit object
        logger.info(f"Circuit not found")
        xCircuit = gtClass.Circuit(id=0, name=None)

    logger.debug(f"returning: {xCircuit}")
    return xCircuit


def getCircuitList(dbConn):
    """Get a list of all the circuits

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns: list(id, name)
    """
    logger.info("Getting list of Circuits")
    selectSQL = "SELECT c.id as id, c.name as name from circuit as c"
    orderbySQL = "ORDER by name"
    sql = f"{selectSQL} {orderbySQL}"
    logger.debug(f"sql = {sql}")

    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)
    logger.info(f"Returning {len(result)} rows")
    return result


def getCountry(dbConn, countryId):
    """Return a Country object from db by countryID

    Args:
        dbConn (sqlite3.connect): Database connection
        countryID (int): Unique ID for the country
    """
    logger.info(f"Getting country by countryId: {countryId}")
    selectSQL = "SELECT id AS countryId, name AS Country, alpha2, alpha3, region FROM country"
    whereSQL = "WHERE countryId = ?"
    sql = f"{selectSQL} {whereSQL}"
    theVals = (countryId,)
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        row = cur.fetchone()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)

    if row:  # Populate Country obj with db data
        logger.info(f"Found countryId: {countryId}")
        country = gtClass.Country(
            cntryID=row[0],
            cntryName=row[1],
            alpha2=row[2],
            alpha3=row[3],
            region=row[4])
    else:  # Create blank Country obj
        logger.info(f"Unable to find countryId: {countryId}")
        country = gtClass.Country(
            cntryID=0,
            cntryName=None,
            alpha2=None,
            alpha3=None,
            region=None)
    logger.info(f"Returning country={country}")
    return country


def getDriveTrains(dbConn, orderBy='code'):
    """[summary]

    Args:
        dbConn (sqlite3.connect): Database connection
        orderBy (str, optional): The field for the list to be ordered by
        Defaults to 'code'.

    Returns:
            list: (id, code, description)
    """
    logger.info(f"Getting all drive trains ordered by {orderBy} ")
    selectSQL = "select id, code, description FROM drivetrain"
    orderBySQL = f"ORDER BY {orderBy}"
    sql = f"{selectSQL} {orderBySQL}"
    logger.debug(f"sql: {sql}")

    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)
    logger.info(f"Returning {len(result)} rows")
    return result


def getLayout(dbConn, layoutId):
    """Gets a single Track Layout record from database.

    Args:
        dbConn (sqlite3.connect): Database connection
        layoutId (int): Track layoutID number to get from database.
    Returns:
        TrackLayout Object: IF TrackLayoutObject.id == 0 then nothing found
    """
    logger.info(f"Getting track layout id {layoutId}")
    sql = """SELECT id as layoutId, name as layoutName, miles, track_id, circuit_id FROM track_layout WHERE layoutId=?"""
    theVals = (layoutId,)
    # Execute the SQL
    logger.debug(f"sql: {sql}")
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        row = cur.fetchone()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)

    # Disable full sql traceback
    dbConn.set_trace_callback(None)

    if row:  # Populate trackLayout obj
        logger.info(f"Found track layout id {layoutId}")
        xTrack = getTrack(dbConn, key='trackId', value=row[3])
        xCircuit = getCircuit(dbConn, key='id', value=row[4])
        xTrackLayout = gtClass.TrackLayout(
            row[0], row[1], miles=row[2], trackObj=xTrack, circuitObj=xCircuit)

    else:  # Create blank trackLayout obj (no data returned)
        logger.info(f"Unable to find track layout id {layoutId}")
        logger.debug(f"creating empty tracklayout object")
        xCircuit = getCircuit(dbConn, key='id', value=0)
        xTrack = getTrack(dbConn, key='trackId', value=0)
        xTrackLayout = gtClass.TrackLayout(
            id=0, name=None, miles=None, trackObj=xTrack, circuitObj=xCircuit)

    logger.debug(f"returning object xTrackLayout={xTrackLayout} ")
    return xTrackLayout


def getLayoutList(dbConn, trackId):
    """Get a list of track layouts for a trackId

    Args:
        dbConn (sqlite3.connect): Database connection
        trackId (int): The trackId of the track the layout list is for
    Returns:
        list: (layoutId,layoutName)
    """
    logger.info(f"Getting track layout list: trackId={trackId}")
    selectSQL = """SELECT layoutId, layout, miles FROM vTrackLayout"""
    orderBySQL = "ORDER BY layout"
    whereSQL = "WHERE trackId = ?"
    sql = f"{selectSQL} {whereSQL} {orderBySQL}"
    theVals = (trackId,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")

    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)

    logger.info(f"Returning {len(result)} rows")
    return result


def getLeague(dbConn, key='id', value=None):
    """Get a league object from database by various fields

    Args:
        dbConn (sqlite3.connect): Database connection
        key (str, optional): The key/field to get object from db. Defaults to 'id'.
        value (required to return something): The value the key must equal to return the object.

    Returns:
        LeagueObject. If nothing found then LeagueObj.id=0
    """
    logger.info(f"Getting a League: {key}={value}")
    selectSQL = "SELECT id, name, sortord FROM league"
    whereSQL = f"WHERE {key} = ?"
    theVals = (value,)
    sql = f"{selectSQL} {whereSQL}"
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        row = cur.fetchone()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback
    dbConn.set_trace_callback(None)
    logger.debug(f"row={row}")
    if row:  # have data from db
        league = gtClass.League(id=row[0], name=row[1], sortord=row[2])
    else:  # No data from db. Create empty object
        league = gtClass.League(id=0, name="", sortord=0)
    logger.debug(f'returning: {league}')
    return league


def getLeagueList(dbConn):
    """Returns a list of all the leagues in the db.

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
        list (leagueID, leagueName)
    """
    logger.info("Getting list of Leagues")
    selectSQL = "SELECT id, name FROM league"
    orderBySQL = "ORDER BY sortord"
    sql = f"{selectSQL} {orderBySQL}"
    logger.debug(f"sql = {sql}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)
    logger.debug(f"Returning {len(result)} rows")
    return result


def getMfg(dbConn, key='mfgId', value=None):
    """
    Gets a manufacture record from the database based on the key being used.

    Args:
        dbConn (sqlite3.connect): Database connection
        value : Is the value being search for.
        key   : the column to search on. mfgId, or Make. Default is mfgid

    Returns:
        ManufactureObject. IF ManufactureObject.id = 0 then nothing found
    """
    logger.debug(f"Getting Manufacture: {key}={value}")
    selectSQL = """SELECT mfg.id as mfgId,
			mfg.name AS Make,
			country_id as cntryId
			FROM manufacture AS mfg"""

    whereSQL = f" WHERE {key} = ?"

    theVars = (value,)
    sql = f"{selectSQL} {whereSQL}"
    # Ready to execute SQL
    logger.debug(f"theVars: {theVars}")
    logger.debug(f"sql: {sql}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)

    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVars)
        row = cur.fetchone()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback
    dbConn.set_trace_callback(None)
    logger.debug(f"row={row}")
    # default Country object (blank)
    xCountry = gtClass.Country(
        cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)

    if row:  # Populate Manufacture object
        logger.debug("manufacture found.")
        if row[2]:  # We have a country. Load country object
            xCountry = getCountry(dbConn, row[2])

        xMake = gtClass.Manufacture(
            id=row[0], name=row[1], countryObj=xCountry)
        logger.debug(f"returning manufacture object")
    else:
        # Create blank Manufacture object
        logger.debug("manufacture not found.")
        xMake = gtClass.Manufacture(
            id=0, name='', countryObj=xCountry)
        logger.debug(f"returning blank manufacture object")

    logger.debug(f"Returning : {xMake}")
    return xMake


def getMfgList(dbConn):
    """Returns a list of manufactures.

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
        list: (MfgId,Make)
    """
    logger.info(f"Getting all manufactures")
    selectSQL = """SELECT mfg.id as id, mfg.name AS Make FROM manufacture AS mfg"""
    orderBySQL = f"ORDER BY mfg.id"

    sql = f"{selectSQL} {orderBySQL}"

    # Ready to execute SQL
    logger.debug(f"sql: {sql}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)
    logger.info(f"Rows being returned: {len(result)}")
    return result


def getRace(dbConn, id):
    """Get a Race object from database by raceId

    Args:
        dbConn (sqlite3.connect): Database connection
        id (int): The unique race ID

    Returns:
        Race Object: The race object.
        If race.id=0 then race was not found
    """
    logger.info(f"Getting race from db for race id: {id}")
    selectSQL = "SELECT id, name, tl_id, rc_id, weather_id, type_id, racetime, limits, notes FROM race"
    whereSQL = "WHERE id = ?"
    value = id
    theVals = (value,)
    sql = f"{selectSQL} {whereSQL}"
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        row = cur.fetchone()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)

    if row:  # Create a race object
        logger.info("Found race")
        logger.debug(f"row={row}")
        id = row[0]
        name = row[1]
        trackLayout = getLayout(dbConn, row[2])
        raceCollection = getRaceCollection(dbConn, rcId=row[3])
        weather = getWeather(dbConn, row[4])
        raceType = getRaceType(dbConn, row[5])
        racetime = row[6]
        limits = row[7]
        notes = row[8]
    else:  # create a blank racetype object
        logger.info("Race not found")
        trackLayout = getLayout(dbConn, 0)
        raceCollection = getRaceCollection(dbConn, rcId=0)
        weather = getWeather(dbConn, 0)
        raceType = getRaceType(dbConn, 0)
        id = 0
        name = None
        racetime = None
        limits = None
        notes = None

    race = gtClass.Race(id=id, name=name, trackLayout=trackLayout,
                        raceCollection=raceCollection, raceType=raceType, weather=weather)
    race.racetime = racetime
    race.limits = limits
    race.notes = notes

    logger.debug(f"race={race}")
    return race


def getRaces(dbConn, raceCollectionID):
    """Get a list of races for a Race Collection

    Args:
        dbConn (sqlite3.connect): Database connection
        raceCollectionID (int): Race Collection ID

    Returns:
        list: (raceID,raceName)
    """
    # Got to get a list of races for this race.raceCollection.id
    logger.info(f"Getting race list for collection ID={raceCollectionID}")
    selectSQL = "select r.id as raceID, r.name as RaceName FROM race as r"
    whereSQL = "WHERE r.rc_id = ?"
    orderBySQL = "ORDER BY r.name"
    sql = f"{selectSQL} {whereSQL} {orderBySQL}"
    theVals = (raceCollectionID,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback
    dbConn.set_trace_callback(None)
    logger.info(f"Returning {len(result)} rows")
    logger.debug(f"result={result}")
    return result


def getRaceCollection(dbConn, rcId):
    """Get a race collection object from database

    Args:
        dbConn (sqlite3.connect): Database connection
        rcId (int): Race collection id

    Returns:
        Race Collection object
        IF raceCollection.id == 0 then race Collection not found
    """
    logger.info(f"Getting Race Collection by id: {rcId}")
    selectSQL = "SELECT id as collectionId,name,description,league_id,cat_id,prize1,prize2,prize3 FROM race_collection"
    whereSQL = "WHERE collectionId = ?"
    value = rcId
    sql = f"{selectSQL} {whereSQL}"
    theVals = (value,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        row = cur.fetchone()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback
    dbConn.set_trace_callback(None)
    if row:  # populate the raceCollection object
        logger.debug("Found race collection")
        logger.debug(f"row={row}")

        league = getLeague(dbConn, key='id', value=row[3])
        logger.debug(f"league={league}")

        raceCollection = gtClass.RaceCollection(
            id=row[0], name=row[1], desc=row[2], leagueObj=league)

        # Getting the car class category
        catClass = getCarCat(dbConn, id=row[4])
        if catClass.id == 0:  # no catClass assigned to raceCollection
            raceCollection.classcat = gtClass.ClassCat(
                id=None, name="", desc="")
        else:
            raceCollection.classcat = catClass

    else:  # create a blank raceCollection object
        league = getLeague(dbConn, key='id', value=0)
        raceCollection = gtClass.RaceCollection(
            id=0, name=None, desc=None, leagueObj=league)

    logger.debug(f"raceCollection={raceCollection}")
    return raceCollection


def getRaceCollectionList(dbConn, leagueId):
    """Returns Race Collection list for the leagueID.

    Args:
        dbConn (sqlite3.connect): Database connection
        leagueId (int): leagueId to get race collections for

    Returns:
        list: (id,name,desc)
    """
    logger.info(
        f"Getting list of race collections for a leagueID {leagueId}")
    selectSQL = "SELECT id, name, description from race_collection"
    whereSQL = "WHERE league_id = ?"
    orderBySQL = "Order by name"
    sql = f"{selectSQL} {whereSQL} {orderBySQL}"
    theVals = (leagueId,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)
    logger.info(f"Rows being returned: {len(result)}")
    return result


def getRaceType(dbConn, id):
    """Get a Race Type from db by id

    Args:
        dbConn (sqlite3.connect): Database connection
        id (int): Race Type unique id

    Returns:
        RaceTypeObj: Race type object
    """
    selectSQL = "SELECT id, name FROM race_type"
    whereSQL = "WHERE id = ?"
    value = id
    theVals = (value,)
    sql = f"{selectSQL} {whereSQL}"
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        row = cur.fetchone()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback
    dbConn.set_trace_callback(None)
    logger.debug(f"row={row}")

    if row:  # Create a racetype object
        logger.debug("Found race type")
        logger.debug(f"row={row}")
        rt = gtClass.RaceType(id=row[0], name=row[1])
    else:  # create a blank racetype object
        rt = gtClass.RaceType(id=0, name="")

    logger.debug(f"rt={rt}")
    return rt


def getRaceTypeList(dbConn):
    """Return a list of all the race types in db

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
            list: (raceTypeid, raceTypeName)
    """
    logger.info("Getting list of race types from db")
    selectSQL = "SELECT id, name FROM race_type ORDER by name"
    sql = selectSQL
    logger.debug(f"sql = {sql}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback
    dbConn.set_trace_callback(None)
    logger.debug(f"Returning {len(result)} rows")
    return result


def getTrack(dbConn, key='trackId', value=None):
    """Gets a single Track record from database based on key and value passed.

    Args:
        dbConn (sqlite3.connect): Database connection
        key (str, optional): Column to search on. trackId, or track. Defaults to 'trackId'.
        value (optional): Value you are looking for. Defaults to None.

    Returns:
        Track Object
        if TrackObject.id == 0 then track was not found
    """
    logger.debug(f"getting track key={key}, value={value}")
    if key == 'trackId':
        whereSQL = "WHERE trackId = ?"
    elif key == 'track':
        whereSQL = "WHERE track = ?"

    sqlSelect = """SELECT id AS trackId, name AS track, country_id as countryId FROM track  """
    sql = f"{sqlSelect} {whereSQL}"
    theVals = (value,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        row = cur.fetchone()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback
    dbConn.set_trace_callback(None)
    logger.debug(f"row={row}")
    # default Country object (blank)
    xCountry = gtClass.Country(
        cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)

    if row:  # Populate the track object
        logger.info(f"Found Track")
        if row[2]:  # We have a country
            xCountry = getCountry(dbConn, row[2])

        xTrack = gtClass.Track(
            id=row[0], name=row[1], countryObj=xCountry)

    else:  # create a blank track object
        logger.debug("no track found")
        xTrack = gtClass.Track(id=0, name=None, countryObj=xCountry)

    logger.debug(f'track = {xTrack}')
    return xTrack


def getTrackList(dbConn):
    """Returns a list of all the tracks in db

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
        list: (trackId, trackName)
    """
    logger.info("Getting list of Tracks")
    selectSQL = "select id, name from track order by name"
    sql = f"{selectSQL}"
    logger.debug(f"sql = {sql}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)
    logger.info(f"Rows being returned: {len(result)}")
    return result


def getWeather(dbConn, id):
    """Return a Weather object from db by key

    Args:
        dbConn (sqlite3.connect): Database connection
        id (int): Unique weather id.

    Returns:
        Weather object
    """
    logger.info(f"Getting weather object by id: {id}")
    selectSQL = "SELECT id, name FROM weather"
    whereSQL = f"WHERE id = ?"
    theVals = (id,)
    sql = f"{selectSQL} {whereSQL}"
    logger.debug(f"{theVals}")
    logger.debug(f"sql: {sql}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        row = cur.fetchone()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback
    dbConn.set_trace_callback(None)
    logger.debug(f"row={row}")
    if row:  # have data from db
        weather = gtClass.Weather(id=row[0], name=row[1])
    else:  # No data from db. Create empty object
        weather = gtClass.Weather(id=0, name="")
    logger.debug(f'weather = {weather}')
    return weather


def getWeatherList(dbConn):
    """Returns a list of all the the Weather rows

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
        list (weatherID, weatherName)
    """
    logger.info("Getting list of weather objects")
    selectSQL = "SELECT id, name FROM weather ORDER by name"
    sql = selectSQL
    logger.debug(f"sql = {sql}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)
    logger.info(f"Rows being returned: {len(result)}")
    return result


def initDB(dbConn, scriptPath=None):
    """Create tables, views, indexes

    Args:
        dbConn (sqlite3.connect): Database connection
        scriptPath (str): path to script files
    """
    logger.info("Database to be initilized")
    logger.debug(f"scriptPath={scriptPath}")
    scripts = ['createTables.sql',
               'LoadLookUpData.sql',
               'LoadOtherData.sql']
    logger.debug(f'scripts to run: {scripts}')
    gtScripts = Path(scriptPath)
    for sFile in scripts:
        scriptFile = gtScripts / sFile
        logger.debug(f"Executing {scriptFile}")
        _exeScriptFile(dbConn, scriptFileName=f'{scriptFile}')
    logger.info("Database init completed")


def updateMfg(dbConn, mfgObj):
    """Update a manufacture record in database

    Args:
        dbConn (sqlite3.connect): Database connection
        mfgObj Manufacture object
        - Record that will be UPDATED is based on mfgObj.id.
        WARNING! - Do not change original mfgObj.id. Unexpected results will occur with sqlite

    Returns:
        list: ResultCode, ResultText
                ResultCode == 0: Success execution
                Resultcode != 0: - See ResultText for details
    """
    logger.debug(f"manufacture record update {mfgObj}")
    # Sanity check - does the mfgRecord exist in db?
    logger.debug("sanity check. confirm mfg Record exists.")
    testMfg = getMfg(dbConn, value=mfgObj.id)
    if testMfg.id == 0:  # Mfg is not in database
        result = [1, f"manufacture id {mfgObj.id} not in database."]
        logger.debug(f"returning {result}")
        return result

    logger.debug("sanity check passed. execute SQL")
    theVals = {'mfgID': mfgObj.id, 'mfgName': mfgObj.name,
               'cntryID': mfgObj.country.id}
    sql = "UPDATE manufacture SET name = :mfgName, country_id = :cntryID WHERE id = :mfgID"

    result = _exeDML(dbConn, sql, theVals)
    if result[0] == 0:
        result[1] = f"Manufacture id: {mfgObj.id} Updated"
    else:
        logger.debug(f"problem updating manufacture id: {mfgObj.id}")

    logger.info(f"returning {result}")
    return result


def updateTrack(dbConn, trackObj):
    """update track record

    Args:
        dbConn (sqlite3.connect): Database connection
        trackObj (track Object)

    Returns:
        list: ResultCode, ResultText
              ResultCode 0 = Success
              ResultCode != 0 = see ResultText for details
    """
    logger.debug(f"track record update {trackObj}")
    # Sanity check - See if tracking id exists
    testObj = getTrack(dbConn, value=trackObj.id)
    if testObj.id == 0:  # Not found in db
        return [1, f"track id {trackObj.id} not in database."]

    theVals = {'trackID': trackObj.id, 'trackName': trackObj.name,
               'cntryID': trackObj.country.id}
    sql = "UPDATE track SET name = :trackName, country_id = :cntryID WHERE id = :trackID"

    return _exeDML(dbConn, sql, theVals)


def updateTrackLayout(dbConn, uLayout):
    """Update the track layout record in database

    Args:
        dbConn (sqlite3.connect): Database connection
        uLayout (TrackLayout Object) : Updated TrackLayout Object

    Returns:
        list: ResultCode, ResultText
              ResultCode 0 = Success
              ResultCode != 0 = see ResultText for details
    """
    logger.info(f"Updating Track Layout {uLayout}")

    tResult = validateTrackLayout(dbConn, uLayout)
    if tResult[0]:  # Tests passed
        logger.info("Updating track layout id: {uLayout.id}")
        sql = "UPDATE track_layout SET name = :layoutName, miles = :miles, track_id = :trackId, circuit_id = :circuitId"
        theVals = {'layoutName': uLayout.name, 'miles': uLayout.miles,
                   'circuitId': uLayout.circuit.id, 'trackId': uLayout.track.id}
        logger.debug("sql={sql}")
        logger.debug("theVals = {theVals}")
        result = _exeDML(dbConn, sql, theVals)
    else:
        logger.warning(tResult[1])
        result = (1, tResult[1])

    logger.debug(f"returning: {result}")
    return result


def validateRace(dbConn, race):
    """Validates the Race rules and returns results

    Args:
        dbConn (sqlite3.connect): Database connection
        race (object): Race object

    Returns:
        list: (bool,msg)
        bool = False  - Race failed tests
        msg = string as to why it failed
    """
    logger.info(f"Validating race={race}")
    # Race name must contain at least one charcter
    logger.debug(
        f"Checking race name to be sure it contains at lease one character")
    if race.name == None or race.name == "":
        msg = f"Race name must contain at least one character"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Race name contains one or more characters")

    # Race name must be unique for the race_collection
    logger.debug(
        f"Checking that race name [{race.name}] is unique for race collection id {race.raceCollection.id} (case insensitve)")
    xList = getRaces(dbConn, race.raceCollection.id)
    for row in xList:
        logger.debug(f"raceId={row[0]}. checking race name: {row[1]}")
        if row[1].upper() == race.name.upper():  # layout name exist for track
            msg = f"Race name [{race.name}] for Race ID [{race.id}] already exists"
            result = (False, msg)
            logger.info(f"returning = {result}")
            return result
    logger.info(
        f"Passed: Race name is unique for race collection id {race.raceCollection.id}")

    # Weather ID must not be zero
    logger.debug(f"Checking for valid weather id")
    if race.weather.id == 0:  # Invalid Weather id
        msg = f"Race weather id must not be 0"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Weather id is greater than zero")

    # Does weather id exist
    if getWeather(dbConn, race.weather.id).id != race.weather.id:
        msg = f"The Race weather id : {race.weather.id} not found in database"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Weather id found in database")

    # TrackLayout id must not be zero
    logger.debug(f"Checking for valid Track Layout")
    if race.trackLayout.id == 0:
        msg = f"Race Track Layout id must not be 0"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Race Track layout id is greater than zero")

    # TrackLayout must exist
    if getLayout(dbConn, race.trackLayout.id).id == 0:
        msg = f"The Race track layout not found in database"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Race Track layout id found in database")

    # Race type required.
    logger.debug(f"Checking for valid racetype id")
    if race.raceType.id == 0:
        msg = f"Race type for race must not be 0"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Race type id is not 0")
    # Race type must exist
    x = getRaceTypeList(dbConn)
    logger.debug(f"RaceType List = {x}")
    logger.debug(f"race.raceType.id={race.raceType.id}")
    passed = False
    for r in x:
        if r[0] == race.raceType.id:  # Found the raceType id
            passed = True
            break
    if passed:
        logger.info("Passed. Race type found")
    else:
        msg = f"Race type for race not found in database"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result

    # Race Collection testing
    logger.debug(f"Checking for valid race collection")
    logger.debug(f"race.raceCollection.id={race.raceCollection.id}")
    # Race Collection id must not be zero
    if race.raceCollection.id == 0:
        msg = f"The race collection id for the race must not be zero"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Race collection id is not 0")

    # Race collection id must exist
    if getRaceCollection(dbConn, race.raceCollection.id).id == 0:
        msg = f"The Race collection not found in database"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Race collection found")

    msg = "Race passed tests"
    result = (True, msg)
    logger.info(f"returning = {result}")
    return result


def validateTrackLayout(dbConn, trackLayout):
    """Validates TrackLayout rules and returns results

    Args:
        dbConn (sqlite3.connect): Database connection
        trackLayout (TrackLayout object): Track Layout that is being saved

    Returns:
            list: (True/False, msg)
            True = Tests passed
            False = See msg for what did not pass
    """
    logger.debug(f"trackLayout={trackLayout}")
    # Layout name must contain at least one charcter
    logger.info(
        f"Checking layout name contains at lease one character")
    if trackLayout.name == None or trackLayout.name == "":
        msg = f"Track Layout name must contain at least one character"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result

    # Layout name must be unique for the Track
    logger.info(
        f"Checking if layout [{trackLayout.name}] already exists for track (case insensitve)")
    layoutList = getLayoutList(dbConn, trackLayout.track.id)
    for row in layoutList:
        logger.debug(f"tlayoutId={row[0]}. checking layout name: {row[1]}")
        if row[1].upper() == trackLayout.name.upper():  # layout name exist for track
            msg = f"Layout name [{trackLayout.name}] for Trackid [{trackLayout.track.id}] already exists"
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
