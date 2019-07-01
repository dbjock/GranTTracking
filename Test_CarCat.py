import logging
import DBFunctions as gtdb
import GTClasses as gt
from pathlib import Path
import csv
import os
myLogLvl = logging.INFO
#myLogLvl = logging.DEBUG

def displayCarCat(theCarCat):
    print(f'Catname----: {theCarCat.name}')
    print(f'CatID------: {theCarCat.catID}')
    print(f'Description: {theCarCat.desc}')


def Setup_CarCat(inputFile):
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
                    gtdb.Add_CarCat(importCar)
                    line_count += 1
            logging.info(f'Processed {line_count} lines.')
    else:
        logging.warning(f"Unable to load file {CarCat_File}")

logging.basicConfig(
    level = myLogLvl,
    format = '%(asctime)s %(levelname)s:%(module)s:%(funcName)s: %(message)s'
    )
gtdb.Create_CarCats()
Setup_CarCat("/Users/Pops/Documents/GranTorismo/Documentation/CarCategories.csv")
#testing the use of classes in the db functions
#Using the car category to test.
testCarCat = gt.Category('Cat number 12')
testCarCat.catID = 12
testCarCat.desc = 'I have changed this to 12'
displayCarCat(testCarCat)
gtdb.Add_CarCat(testCarCat)