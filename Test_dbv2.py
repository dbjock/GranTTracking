import logging
import logging.config
from pathlib import Path
import os
# Application required modules
from GranT import gtdbV2
from GranT import gtcfg

logging.config.fileConfig('logging.conf', defaults=None,
                          disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def test_createInit(dbName=None):
    """Testing ability to create database, and all scripts for data loading
    PARMS - all required
    dbName : The path and name of the database
    """
    logger.info(f"TESTING Initiziting database: {dbName}")
    GranTdb = gtdbV2.GTdb(name=dbName)
    scripts = ['./GranT/createTables.sql',
               './GranT/LoadLookUpData.sql', './GranT/LoadOtherData.sql']

    for scriptFile in scripts:
        logger.info(f"Executing {scriptFile}")
        GranTdb.exeScriptFile(scriptFileName=scriptFile)

    logger.info("Initiziting database complete")


def NOTRDY_test_mfg_CreatingRec(dbFile):
    """Testing ability to get all mfg Records"""
    logger.info(f"*" * 50)
    logger.info(f"Testing writeMfg with new records, and getAllMfg to return")
    logger.info(f"*" * 50)
    deldb(dbFile)
    dbConn = gtdb.create_connection(dbFile)
    gtdb.create_manufactures(dbConn)
    gtdb.writeMfg(dbConn, 0, "TheTest")
    gtdb.writeMfg(dbConn, 0, "TheTest1")
    gtdb.writeMfg(dbConn, 0, "TheTest2")
    dbConn.close  # Force write
    dbConn = gtdb.create_connection(dbFile)
    result = gtdb.getAllMfg(dbConn)
    dbConn.close  # Force write
    if len(result) < 3:
        logger.error(f"Test Failed")
    else:
        logger.info(f"Test Passed")
        return True


def test_getAllMfg(dbObj):
    """Going to return all manufacture/makes via db object

    PARM
    dbObj : Gran Turismo database object
    """
    logger.info("Getting all Manufacture/Make records")
    print(dbObj.getAllMfg(orderBy='Make'))


def test_getMfg(dbObj):
    """Get a manufactore via DB

    PARM
    dbObj : Gran Turiso Database Object
    """
    logger.info("Getting data on Manufacture/Make. ID = 1")
    print(dbObj.getMfg(key='recID', value=1))
    logger.info("Getting data on Manufacture/Make. ID = 1")
    print(dbObj.getMfg(key='Make', value='JaGUar'))


def mainTest():
    os.system('cls')
    logger.info("************Getter Done testing***********")
    # test_createInit(dbName='./data/testdb.db')
    GranTdb = gtdbV2.GTdb(name='./data/testdb.db')
    # test_getMfg(GranTdb)
    test_getAllMfg(GranTdb)


if __name__ == '__main__':
    mainTest()
