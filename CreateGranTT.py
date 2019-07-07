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
                    gtdb.writeMfg(myDBConn,mfgid,mfgname)
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

if gtdb.create_manufactures(myDBConn):
    setup_manufacture("DBInit/Manufactures.csv")

if gtdb.create_driveTrains(myDBConn):
    setup_DriveTrain("DBInit/DriveTrainCat.csv")

