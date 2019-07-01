import logging
from GranT import DBFunctions as gtdb
from GranT import GTClasses as gt
from pathlib import Path
import csv
import os
def ClearScreen():
    os.system('cls')

myLogLvl = logging.INFO
#myLogLvl = logging.DEBUG

logging.basicConfig(
    level = myLogLvl,
    format = '%(asctime)s %(levelname)s:%(module)s:%(funcName)s: %(message)s'
    )

logging.info(f"Db location is {gtdb.db_location}")

def setup_manufacture(inputFile):
    """Populates Manufacture table from a file.\n
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
                    logging.debug(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    logging.debug(f"id = {int(row[0])} name = {row[1]}")
                    ImportMfg = gt.Manufacture(row[1])
                    ImportMfg.mfgID = int(row[0])
                    gtdb.write_manufacture(ImportMfg)
                    line_count += 1
            logging.info(f'read {line_count} lines.')
    else:
        logging.warning(f"Unable to load file {Mfg_File}")

def setup_carCat(inputFile):
    """Populates Car Category table from a file.\n
        inputfile = csv filename with path
    """
    CarCat_File = Path(inputFile)
    if CarCat_File.exists():
        logging.info(f"Loading {CarCat_File}")
        with open(CarCat_File) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    logging.debug(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    logging.debug(f'{row[0]} : {row[1]} : {row[2]}.')
                    importCar = gt.Category(row[1])
                    importCar.catID = int(row[0])
                    importCar.desc = row[2]
                    gtdb.write_carCat(importCar)
                    line_count += 1
            logging.info(f'read {line_count} lines.')
    else:
        logging.warning(f"Unable to load file {CarCat_File}")

def setup_drivetrain(inputFile):
    """Populates DriveTrain table from a file.\n
    inputFile = csv filename with path
    """
    DriveTrain_File = Path(inputFile)
    if DriveTrain_File.exists():
        logging.info(f"Loading {DriveTrain_File}")
        with open(DriveTrain_File) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    logging.debug(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    logging.debug(f'{int(row[0])} : {row[1]} : {row[2]}.')
                    importDriveTrain = gt.DriveTrain(row[1])
                    importDriveTrain.dtID = int(row[0])
                    importDriveTrain.desc = row[2]
                    gtdb.write_driveTrain(importDriveTrain)
                    line_count += 1
            logging.info(f'Processed {line_count} lines.')
    else:
        logging.warning(f"Unable to load file {DriveTrain_File}")

gtdb.create_manufactures()
setup_manufacture("/Users/Pops/Documents/GranTorismo/Documentation/Manufactures.csv")
gtdb.create_driveTrains()
setup_drivetrain("/Users/Pops/Documents/GranTorismo/Documentation/DriveTrainCat.csv")

gtdb.create_carCats()
setup_carCat("/Users/Pops/Documents/GranTorismo/Documentation/CarCategories.csv")

# gtdb.Create_Cars()