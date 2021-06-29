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
    logger.info("Attempting to safe the race collection")
    theVals = {'colName': raceCollection.name, 'colDesc': raceCollection.desc,
               'leagueId': raceCollection.league.id}
    sql = "INSERT INTO race_collection (league_id, name, description) VALUES (:leagueId, :colName, :colDesc)"
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    rtrnMsg = _exeDML(dbConn, sql, theVals)
    logger.debug(f"Return {rtrnMsg}")
    return rtrnMsg


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


def getRaceCollection(dbConn, rcId):
    """Get a race collection object from database

    Args:
        dbConn (sqlite3.connect): Database connection
        rcId (int): Race collection id

    Returns:
        Race Collection objection
        IF raceCollection.id == 0 then race Collection not found
    """
    logger.info(f"Getting Race Collection by id: {rcId}")
    selectSQL = "SELECT id as collectionId, name, description, league_id FROM race_collection"
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
