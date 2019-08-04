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
    conn = sqlite3.connect(dbfile,detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row #Ability to get column names (.keys())
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON") #Turning on foreign_key enforcement
    return conn

def add_Mfg(dbConn,mfgName):
    """
    Adds a manufacture record.
    All PARMS requried.
    dbConn : DB Connection object
    mfgName : mfgName/name of the manufacture (Must not be None,null,blank)
    Returns : True if successfull
    """
    logger.debug(f"Adding Manufacture to DB. mfgnam={mfgName}")
    if mfgName is None or mfgName == '':
        logger.error(f"mfgName must contain a value. No Add/Update")
        return False

    theVals = (mfgName,)
    sql = "INSERT INTO manufactures (mfgName) Values (?)"
    # Execute SQL
    logger.debug(f"Sql: {sql}")
    try:
        dbcursor = dbConn.cursor()
        dbcursor.execute(sql, theVals)
    except sqlite3.IntegrityError as e:
        logger.error(f"sqlite integrity error: {e.args[0]}")
        return False
    except:
        logger.critical(f'Unexpected error executing sql: {sql}', exc_info = True)
        return False

    dbConn.commit()
    logger.debug(f"Values: {theVals} : committed")
    return getMfg(dbConn,mfgName,key="mfgName")

def update_Mfg(dbConn,recID,mfgName):
    """
    Updates mfgName in manufacture record.
    All PARMS requried.
    dbConn : DB Connection object
    recID : int of record to update
    mfgName : mfgName value (Must not be None,null,blank)
    Returns True if successful.
    """
    logger.debug(f"PARMS: recID: {recID}, mfgName: {mfgName}")
    if not isinstance(recID, int):
        logger.error(f"recID is not an integer.")
        raise ValueError(f"recID is not an integer.")

    # Can't allow blank data in (Note.. db doesn't consider this null)
    if mfgName is None or mfgName == '':
        logger.error(f"mfgName must contain a value.")
        raise ValueError(f"mfgName must contain a value.")

    #Setting up SQL Update
    theVals = (mfgName,recID)
    sql = "UPDATE manufactures SET mfgName = ? WHERE id = ?"

    # Execute SQL
    logger.debug(f"Sql: {sql}")
    try:
        dbcursor = dbConn.cursor()
        dbcursor.execute(sql, theVals)
    except sqlite3.IntegrityError as e:
        logger.error(f"theVals: {theVals} sqlite integrity error: {e.args[0]}")
    except:
        logger.critical(f'Unexpected error executing sql: {sql}', exc_info = True)

    dbConn.commit()
    logger.info(f"Values: {theVals} : committed")
    return True

def getMfg(dbConn,value,key='recID'):
    """
    Gets the manufacture record from the database based on the key being used.\n
    dbConn = sqlite3 connection object
    value : Is the value being search for.
    key   : the column name to search on. recID, or mfgName. Default is recID\n
    Returns : [(recID, mfgName)] or False if nothing is found?
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

    #Ready to execute SQL
    try:
        logger.debug(f"sql: {sql}")
        dbCursor = dbConn.cursor()
        dbCursor.execute(sql, theVars)
        result = dbCursor.fetchone()
        logger.info("Return Manufacture results")
        return result
    except:
        logger.critical(f'Unexpected error executing sql: {sql}', exc_info = True)
        return None

def getDriveTrain(dbConn,value,key='recID'):
    """
    Gets the DriveTrain record from the database based on the key being used.\n
    dbConn = sqlite3 connection object
    value : Is the value being search for.
    key   : the column name to search on. recID, dtCode. Default is recID\n
    Returns : [(recID, dtCode, dtDesc)] or False if nothing is found?
    """
    logger.info(f"Getting DriveTrain value={value}, key={key}")
    if key == 'recID':
        if not isinstance(value, int):
            logger.error(f"recID must be an integer value")
            return None

        theVals = (value,)
        sql = "SELECT id, code, description FROM drivetrains WHERE id = ?"
    elif key =='dtCode':
        theVals = (value,)
        sql = f"SELECT id, code, description FROM drivetrains WHERE code = ?"

    #Execute SQL
    try:
        logger.debug(f"sql: {sql}")
        dbCursor = dbConn.cursor()
        dbCursor.execute(sql, theVals)
        result = dbCursor.fetchone()
        logger.info("Return DriveTrain results")
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
