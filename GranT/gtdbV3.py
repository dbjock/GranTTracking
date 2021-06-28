import sys
import logging
import sqlite3
from pathlib import Path

# Custom App modules
from GranT import GTClasses as gtClass

logger = logging.getLogger(__name__)

# """Create a connection to Sqlite3 db

# Args:
#   dbfile : database file to connect
# Returns:
#   Sqlite3 connection object or None
# """


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
    Order will be by the sortorder in db

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
        cur.execute(sql, theVals)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)
    logger.debug(f"Returning {len(result)} rows")
    return result


def getTrack(dbConn, key='trackId', value=None):
    """Gets a single Track record from database based on key and value passed.

    Args:
        dbConn ([type]): [description]
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


def initDB(dbConn, scriptPath=None):
    """Create tables, views, indexes

    PARM
    scriptPath : path to script files *Required
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
