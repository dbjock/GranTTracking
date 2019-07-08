import logging
import logging.config
from pathlib import Path
import csv
import os

#App Mod
from GranT import gtcfg
from GranT import gtdb

logging.config.fileConfig('logging.conf', defaults=None, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

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

def addMfg(dbConn,recID,mfgName):
    """
    Adds a manufacture record.
    All PARMS requried.
    dbConn : DB Connection object
    mfgName : mfgName/name of the manufacture (Must not be None,null,blank)
    """
    logger.debug(f"Adding Manufacture to DB. mfgnam={mfgName}")
    if mfgName is None or mfgName == '':
        logger.error(f"mfgName must contain a value. No Add/Update")
        return False

    theVals = (recID, mfgName)
    sql = "INSERT OR REPLACE INTO manufactures (id, mfgName) Values (?, ?)"
    # Execute SQL
    logger.debug(f"Sql: {sql}")
    try:
        dbcursor = dbConn.cursor()
        dbcursor.execute(sql, theVals)
    except:
        logger.critical(f'Unexpected error executing sql: {sql}', exc_info = True)
        quit()

    dbConn.commit()
    logger.debug(f"Values: {theVals} : committed")

def addDriveTrain(dbConn,recID,dtCode,dtDesc):
    """
    Adds a DriveTrain record.
    ALL PARMS requried.
    dbConn : DB Connection object\n
    recID : must !0\n
    dtCode : DriveTrain Code must contain a value\n
    dtDesc : Full Description of the type of Drive Train\n
    Returns True if successfull
    """
    logger.debug(f"PARMS: recID:{recID}, dtCode:{dtCode}, dtDesc:{dtDesc}")
    if not isinstance(recID, int):
        logger.error(f"recID is not an integer. No Add")
        return False

    if recID == 0:
        logger.error(f"recID must not equal zero")
        return False

    #Drive Code (dtCode) can't be blank or none. (Note.. sqlite doesn't consider this null)
    if dtCode is None or dtCode == '':
        logger.error(f"dtCode must contain a value. No Add")
        return False

    #Setting up SQL for Create or Update
    theVals = (recID, dtCode, dtDesc)
    sql = "INSERT INTO drivetrains (id, code, description) Values (?, ?, ?)"

    #Executing SQL
    logger.debug(f"Sql: {sql}")
    try:
        dbcursor = dbConn.cursor()
        dbcursor.execute(sql, theVals)
    except:
        logger.critical(f'Unexpected error executing sql: {sql} - Values: {theVals}', exc_info = True)
        return False

    dbConn.commit()
    logger.debug(f"Values: {theVals} : committed")
    return True

def addCarCat(dbConn,recID,carCat,catDesc):
    """Adds a car_cats record.
    ALL PARMS requried.
    dbConn : DB Connection object\n
    recID : must !0\n
    carCat : Catagory Code must contain a value\n
    catDesc : Catagory Description of the type of Drive Train\n
    Returns True if successfull
    """
    logger.debug(f"PARMS: recID:{recID}, carCat:{carCat}, catDesc:{catDesc}")
    if not isinstance(recID, int):
        logger.error(f"recID is not an integer. No Add")
        return False

    if recID == 0:
        logger.error(f"recID must not equal zero")
        return False

    #Car Category (carCat) can't be blank or none. (Note.. sqlite doesn't consider this null)
    if carCat is None or carCat == '':
        logger.error(f"carCat must contain a value. No Add")
        return False

    #Setting up SQL for Create or Update
    theVals = (recID, carCat, catDesc)
    sql = "INSERT INTO car_cats (id, catName, description) Values (?, ?, ?)"

    #Executing SQL
    logger.debug(f"Sql: {sql}")
    try:
        dbcursor = dbConn.cursor()
        dbcursor.execute(sql, theVals)
    except:
        logger.critical(f'Unexpected error executing sql: {sql} - Values: {theVals}', exc_info = True)
        return False

    dbConn.commit()
    logger.debug(f"Values: {theVals} : committed")
    return True

def setup_manufacture(inputFile):
    """Populates Manufacture table.\n
       inputfile = csv filename with path
    """
    Mfg_File = Path(inputFile)
    if Mfg_File.exists():
        logger.info(f"Loading {Mfg_File}")
        with open(Mfg_File) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    logger.debug(f'First Row: {", ".join(row)}')
                    line_count += 1
                else:
                    logger.debug(f"Row: {int(row[0])}, {row[1]}")
                    mfgid = int(row[0])
                    mfgname = row[1]
                    addMfg(myDBConn,mfgid,mfgname)
                    line_count += 1
            logger.info(f'read {line_count} lines.')
    else:
        logger.error(f"Unable to load file {Mfg_File}")

def setup_DriveTrain(inputFile):
    """Populates the DriveTrain table.\n
    inputfile = csv filename with path"""
    inFile = Path(inputFile)
    if inFile.exists():
        logger.info(f"Loading {inputFile}")
        with open(inFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    logger.debug(f'First Row: {", ".join(row)}')
                    line_count += 1
                else:
                    logger.debug(f"Row: {int(row[0])}, {row[1]}, {row[2]}")
                    drvTrainID = int(row[0])
                    drvTrainCode = row[1]
                    drvTrainDesc = row[2]
                    addDriveTrain(myDBConn,drvTrainID,drvTrainCode,drvTrainDesc)
                    line_count += 1
            logger.info(f'read {line_count} lines.')
    else:
        logger.error(f"Unable to load file {inFile}")

def setup_carCats(inputFile):
    """Populates the car_cats table.\n
    inputfile = csv filename with path"""
    inFile = Path(inputFile)
    if inFile.exists():
        logger.info(f"Loading {inputFile}")
        with open(inFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    logger.debug(f'First Row: {", ".join(row)}')
                    line_count += 1
                else:
                    logger.debug(f"Row: {int(row[0])}, {row[1]}, {row[2]}")
                    recID = int(row[0])
                    carCat = row[1]
                    catDesc = row[2]
                    addCarCat(myDBConn,recID,carCat,catDesc)
                    line_count += 1
            logger.info(f'read {line_count} lines.')
    else:
        logger.error(f"Unable to load file {inFile}")

def deldb(theFile):
    """Deletes the dbfile"""
    logger.info(f"Deleting File: {theFile}")
    exists = os.path.isfile(theFile)
    if exists:
        os.remove(theFile)
        logger.info(f"{theFile} deleted")
    else:
        logger.info(f"{theFile} Not found")

os.system('cls')
logger.info("*********Create DB")
logger.info(f"Database file: {gtcfg.dbcfg['dbFile']}")
deldb(gtcfg.dbcfg['dbFile'])
myDBConn = gtdb.create_connection(gtcfg.dbcfg['dbFile'])

if create_manufactures(myDBConn):
    setup_manufacture("DBInit/Manufactures.csv")

if create_driveTrains(myDBConn):
    setup_DriveTrain("DBInit/DriveTrainCat.csv")

if create_carCats(myDBConn):
    setup_carCats("DBInit\CarCategories.csv")