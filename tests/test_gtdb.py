import logging
import logging.config
from pathlib import Path
import os
#Application required modules
from GranT import gtdb
from GranT import gtcfg

logging.config.fileConfig('logging.conf', defaults=None, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def deldb(theFile):
    """Deletes the dbfile"""
    logger.info(f"Deleting File: {theFile}")
    exists = os.path.isfile(theFile)
    if exists:
        os.remove(theFile)
        logger.info(f"{theFile} deleted")
    else:
        logger.info(f"{theFile} Not found")

def test_mfg_CreatingRec(dbFile):
    """Testing ability to get all records from dbFile"""
    logger.info(f"*" * 50)
    logger.info(f"Testing writeMfg with new records, and getAllMfg to return")
    logger.info(f"*" * 50)
    deldb(dbFile)
    dbConn = gtdb.create_connection(dbFile)
    gtdb.create_manufactures(dbConn)
    gtdb.writeMfg(dbConn,0,"TheTest")
    gtdb.writeMfg(dbConn,0,"TheTest1")
    gtdb.writeMfg(dbConn,0,"TheTest2")
    dbConn.close #Force write
    dbConn = gtdb.create_connection(dbFile)
    result = gtdb.getAllMfg(dbConn)
    dbConn.close #Force write
    if len(result) < 3:
        logger.error(f"Test Failed")
    else:
        logger.info(f"Test Passed")
        return True

def test_mfg_UpdatingRec(dbFile):
    """Testing ability to get all records from dbFile"""
    logger.info(f"*" * 50)
    logger.info(f"Testing writeMfg to update, and getMfg to verify the update")
    logger.info(f"*" * 50)
    deldb(dbFile)
    dbConn = gtdb.create_connection(dbFile)
    gtdb.create_manufactures(dbConn)
    gtdb.writeMfg(dbConn,2,"TheTest2")
    dbConn.close
    dbConn = gtdb.create_connection(dbFile)
    logger.info(f"Getting records by recID - Before Change")
    theOrginal = gtdb.getMfg(dbConn,2,key='recID')
    gtdb.writeMfg(dbConn,2,"TheTest2a")
    dbConn.close
    dbConn = gtdb.create_connection(dbFile)
    theNew = gtdb.getMfg(dbConn,2,key='recID')
    dbConn.close
    if theOrginal[0] == theNew[0] and theOrginal[1] != theNew[1]:
        logger.info(f"Testing passed")
        return True
    else:
        logger.error(f"Testing Failed. Values are not different")

def mainTest():
    os.system('cls')
    logger.info("Getter Done testing")
    dbTestFile = "C:/Users/Pops/Code/GTurismoTracking/tests/testdb.db"
    logger.info(f"Testing using database: {dbTestFile} ")
    FailCount = 0
    TestCount = 0
    if not test_mfg_CreatingRec(dbTestFile):
        FailCount +=1

    if not test_mfg_UpdatingRec(dbTestFile):
        FailCount +=1

    if FailCount > 0:
        logger.error(f"Fail count: {FailCount}")
        print(f"Fail count: {FailCount}")
    else:
        print("All Test Passed")


if __name__ == '__main__':
    mainTest()

