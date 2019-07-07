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
                    gtdb.writeDriveTrain(myDBConn,drvTrainID,drvTrainCode,drvTrainDesc)
                    line_count += 1
            logger.info(f'read {line_count} lines.')
    else:
        logger.error(f"Unable to load file {Mfg_File}")

os.system('cls')
logger.info("*********Create DB")
logger.info(f"Database file: {gtcfg.dbcfg['dbFile']}")
myDBConn = gtdb.create_connection(gtcfg.dbcfg['dbFile'])

if create_manufactures(myDBConn):
    setup_manufacture("DBInit/Manufactures.csv")

# if gtdb.create_driveTrains(myDBConn):
#     setup_DriveTrain("DBInit/DriveTrainCat.csv")

