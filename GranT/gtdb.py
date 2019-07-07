import logging
import sqlite3

#App modules
from GranT import gtcfg

logger = logging.getLogger(__name__)

def create_connection(dbfile):
    """
    Create a connection to the sqlite3 database\n
    dbfile : filepath and name (:memory: for in memory)
    *If dbfile does not exist it will be created with an empty database
    """
    logger.debug(f"Creating Connection to {dbfile}")
    conn = sqlite3.connect(dbfile)
    return conn

def writeMfg(dbConn,recID,mfgName):
    """
    Writes/Creates a manufacture record.
    All PARMS requried.
    dbConn : DB Connection object
    recID : 0 = Attempt to Create Record
            !0 Record will update/create as needed
    mfgName : mfgName/name of the manufacture (Must not be None,null,blank)
    Returns True if successful. Else Nothing
    """
    logger.debug(f"PARMS: recID: {recID}, mfgName: {mfgName}")
    if not isinstance(recID, int):
        logger.error(f"recID is not an integer. No Add/Update")
        return None

    # Can't allow blank data in (Note.. db doesn't consider this null)
    if mfgName is None or mfgName == '':
        logger.error(f"mfgName must contain a value. No Add/Update")
        return None

    #Setting up SQL for Create or Update
    if recID == 0: #Add record. If mfgName unique, will add with unique recID
        logger.debug(f"Creating record for mfgName: {mfgName}")
        theVars = (mfgName,)
        sql = "INSERT INTO manufactures (mfgName) Values (?)"
    else: #Add/replace record with provided data based on recID
        logger.debug(f"Create/Update record")
        theVars = (recID, mfgName)
        sql = "INSERT OR REPLACE INTO manufactures (id, mfgName) Values (?, ?)"

    # Execute SQL
    logger.debug(f"Sql: {sql}")
    try:
        dbcursor = dbConn.cursor()
        dbcursor.execute(sql, theVars)
    except sqlite3.IntegrityError as e:
        logger.error(f"theVars: {theVars} sqlite integrity error: {e.args[0]}")
        return None
    except:
        logger.critical(f'Unexpected error executing sql: {sql}', exc_info = True)
        return None

    dbConn.commit()
    logger.info(f"Values: {theVars} : committed")
    return True

def getMfg(dbConn,value,key='recID'):
    """
    Gets the manufacture record from the database based on the key being used.\n
    dbConn = sqlite3 connection object
    value : Is the value being search for.
    key   : the column name to search on. recID, or mfgName. Default is recID\n
    Returns : [(recID, mfgName)] of False if nothing is found?
    """
    logger.info(f"Getting Manufacture value={value} key={key}")
    if key == 'recID':
        if not isinstance(value, int):
            logger.error(f"recID must be an integer value")
            return None

        sql = "SELECT id, mfgName FROM manufactures WHERE id = ?"
        theVars = (value,)
        logger.debug(f'Getting specific recID: {value} SQL: {sql}')
    elif key == 'mfgName':
        sql = "SELECT id, mfgName FROM manufactures WHERE mfgName = ?"
        theVars = (value,)
        logger.debug(f'Getting specific recID: {value} SQL: {sql}')
    else:
        logger.error(f'key {key} does not exist')
        return None

    try:
        dbCursor = dbConn.cursor()
        dbCursor.execute(sql, theVars)
        result = dbCursor.fetchone()
        logger.info("Return Manufacture results")
        return result
    except:
        logger.critical(f'Unexpected error executing sql: {sql}', exc_info = True)
        return None

def getAllMfg(dbConn):
    """
    Gets all records from the Manufacturing table
    return: Returns : [(recID, mfgName),...]
    """
    logger.info(f'Getting all manufactures')
    dbCursor = dbConn.cursor()
    sql = "SELECT id, mfgName FROM manufactures"
    try:
        dbCursor.execute(sql)
        logger.debug(f"sql: {sql}")
        return dbCursor.fetchall()
    except:
        logger.critical(f'Unexpected error executing sql: {sql}', exc_info = True)
        return None

def create_manufactures(dbConn):
    """Create the Manufacture table"""
    logger.info("Creating Manufacture Table")
    sql = "CREATE TABLE manufactures (id INTEGER PRIMARY KEY, mfgName TEXT UNIQUE NOT NULL)"
    dbCursor = dbConn.cursor()
    try:
        dbCursor.execute(sql)
    except:
        logger.critical(f'Unexpected error when executing sql: {sql}', exc_info = True)
        return None

    dbConn.commit()
    logger.info("Manufactures table has been created")
    return True

def create_tracks(dbConn):
    """Creating the Track Table"""
    logger.info("Creating tracks table")
    sql = "CREATE TABLE tracks (id INTEGER PRIMARY KEY, trkName TEXT UNIQUE NOT NULL, circuit_id INTEGER REFERENCES circuits (id) ON DELETE RESTRICT NOT NULL)"
    dbCursor = dbConn.cursor()
    try:
        dbCursor.execute(sql)
        dbConn.commit()
    except:
        logger.critical(f'Unexpected error when executing sql: {sql}', exc_info = True)
        return None

    logger.info("tracks table created")
    return True

def create_driveTrains(dbConn):
    """Create the DriveTrain table"""
    logger.info("Creating drivetrains Table")
    sql = "CREATE TABLE drivetrains (id INTEGER PRIMARY KEY,code TEXT UNIQUE NOT NULL CHECK (length(code) <= 5), description TEXT)"
    dbCursor = dbConn.cursor()
    try:
        dbCursor.execute(sql)
        dbConn.commit()
    except:
        logger.critical(f'Unexpected error when executing sql: {sql}', exc_info = True)
        return None

    logger.info("drivetrains table created")
    return True

def create_circuits(dbConn):
    """Creates the Circuits Table"""
    logger.info("Creating circuits table")
    sql = "CREATE TABLE circuits (id INTEGER PRIMARY KEY, circuitName TEXT UNIQUE NOT NULL)"
    dbCursor = dbConn.cursor()
    try:
        dbCursor.execute(sql)
        dbConn.commit()
    except:
        logger.critical(f'Unexpected error when executing sql: {sql}', exc_info = True)
        return None

    logger.info("Circuits table created")
    return True

def create_cars(dbConn):
    """Creates the Cars table"""
    logger.info("Creating cars table")
    sql ="CREATE TABLE cars (id            INTEGER PRIMARY KEY,model         TEXT UNIQUE NOT NULL,mfg_id        INTEGER REFERENCES manufactures (id) ON DELETE RESTRICT NOT NULL,carcat_id     INTEGER REFERENCES car_cats (id) ON DELETE RESTRICT NOT NULL,drivetrain_id INTEGER NOT NULL REFERENCES drivetrains (id) ON DELETE RESTRICT NOT NULL,yearmade      TEXT,notes         TEXT)"
    dbCursor = dbConn.cursor()
    try:
        dbCursor.execute(sql)
        dbConn.commit()
    except:
        logger.critical(f'Unexpected error when executing sql: {sql}', exc_info = True)
        return None

    logger.info("Circuits cars created")
    return True

def create_carCats(dbConn):
    """Creats car_cats table"""
    logger.info("Creating the car_cats table")
    sql = "CREATE TABLE car_cats (id INTEGER PRIMARY KEY, catName TEXT UNIQUE NOT NULL, description TEXT)"
    dbCursor = dbConn.cursor()
    try:
        dbCursor.execute(sql)
        dbConn.commit()
    except:
        logger.critical(f'Unexpected error when executing sql: {sql}', exc_info = True)
        return None

    logger.info("car_cats table created")
    return True
