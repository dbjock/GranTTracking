import logging
import logging.config
from pathlib import Path
import csv
import os

#App Mod
from GranT import gtcfg
from GranT import gtdb
from GranT import gtclasses as gt

logging.config.fileConfig('logging.conf', defaults=None, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def ClearScreen():
    os.system('cls')

def setup_manufacture(inputFile):
    """Populates Manufacture table.\n
        inputfile = csv filename with path
    """
    Mfg_File = Path(inputFile)
    if Mfg_File.exists():
        logging.info(f"Loading {Mfg_File}")
        with open(Mfg_File) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    logging.debug(f'First Row: {", ".join(row)}')
                    line_count += 1
                else:
                    logging.debug(f"Row: {int(row[0])}, {row[1]}")
                    ImportMfg = gt.Manufacture()
                    ImportMfg.id = int(row[0])
                    ImportMfg.name = row[1]
                    gtdb.writeMfg(myDBConn,ImportMfg.id,ImportMfg.name)
                    line_count += 1
            logging.info(f'read {line_count} lines.')
    else:
        logging.error(f"Unable to load file {Mfg_File}")

ClearScreen()
logger.info("*********Create DB")
logger.info(f"Database file: {gtcfg.dbcfg['dbFile']}")
myDBConn = gtdb.create_connection(gtcfg.dbcfg['dbFile'])

if gtdb.create_manufactures(myDBConn):
    setup_manufacture("DBInit/Manufactures.csv")

# gtdb.create_driveTrains()
# setup_drivetrain("DBInit/DriveTrainCat.csv")

#gtdb.create_carCats(myDBConn)
# setup_carCat("/Users/Pops/Documents/GranTorismo/Documentation/CarCategories.csv")

#gtdb.Create_Cars(myDBConn)
