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
    if row:  # have data from db
        league = gtClass.League(id=row[0], name=row[1], sortord=row[2])
    else:  # No data from db. Create empty object
        league = gtClass.League(id=0, name="", sortord=0)
    logger.debug(f'returning: {league}')
    return league


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
