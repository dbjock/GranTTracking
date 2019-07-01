import logging
import sqlite3
from pathlib import Path

db_location = Path("/Users/Pops/Documents/GranTorismo/GranTTSport-Beta.db")
#db_location = ':memory:'
conn = sqlite3.connect(db_location)
c = conn.cursor()

def create_driveTrains():
    """Create the DriveTrain table"""
    logging.debug("SQL to Create DriveTrainTable")
    c.execute("""
            CREATE TABLE drivetrains (
                id INTEGER PRIMARY KEY,
                code TEXT UNIQUE NOT NULL CHECK (length(code) <= 5),
                description TEXT)
            """)
    conn.commit()
    logging.info("drivetrains table created")

def create_carCats():
    """Create the Car Classes table"""
    c.execute("""
        CREATE TABLE car_cats (
            id INTEGER PRIMARY KEY,
            title TEXT UNIQUE NOT NULL,
            description TEXT)
        """)
    conn.commit()
    logging.info("car_cats table created")

def create_cars():
    """Create the cars table. This does have foreign keys"""
    c.execute("""
            CREATE TABLE cars (
            id            INTEGER PRIMARY KEY,
            model         TEXT UNIQUE NOT NULL,
            mfg_id        INTEGER REFERENCES manufactures (id) ON DELETE RESTRICT NOT NULL,
            carcat_id     INTEGER REFERENCES car_cats (id) ON DELETE RESTRICT NOT NULL,
            drivetrain_id INTEGER NOT NULL REFERENCES drivetrains (id) ON DELETE RESTRICT NOT NULL,
            yearmade      TEXT,
            notes         TEXT
            )
        """)
    conn.commit()
    logging.info("cars table created")

def create_manufactures():
    """Create the Manufacture table"""
    c.execute("""
            CREATE TABLE manufactures (
            id INTEGER PRIMARY KEY,
            title TEXT UNIQUE NOT NULL
            )
        """)
    conn.commit()
    logging.info("manufactures table created")

def create_circuits():
    """Creates the Circuits table"""
    c.execute("""
            CREATE TABLE circuits (
            id INTEGER PRIMARY KEY,
            title TEXT UNIQUE NOT NULL
            )
        """)
    conn.commit()
    logging.info("circuits table created")

def create_tracks():
    """Creating the Track Table"""
    c.execute("""
                CREATE TABLE tracks (
                    id INTEGER PRIMARY KEY,
                    title TEXT UNIQUE NOT NULL,
                    circuit_id INTEGER REFERENCES circuits (id) ON DELETE RESTRICT NOT NULL
                    )
            """)
    conn.commit()
    logging.info("tracks table created")

def write_driveTrain(theClass):
    """Adding a record to DriveTrain table."""
    logging.debug(f"PARMS: dtID:{theClass.dtID}, code:{theClass.code}, desc:{theClass.desc}")
    if not isinstance(theClass.dtID, int):
        logging.error(f"dtID not an int. Check Parms passed to function. No Record added")
        return False

    if theClass.code == '': # Can't allow blank data in (Note.. db doesn't consider this null)
        logging.warning(f"PARMS: dtID:{theClass.dtID} code:{theClass.code} desc:{theClass.desc} : theClass.code is empty. Record not added.")
        return False

    if theClass.dtID == 0: # let db create unique theClass.dtID. DB will handle this. (Integrity will keep dupes out)
        theRecord = (theClass.code, theClass.desc)
        sql = 'INSERT INTO drivetrains (code, description) VALUES (?, ?)'
        logging.debug(f"theRecord: {theRecord}")
    else: # Add or Replace the provided data with the provided theClass.dtID.
        theRecord = (theClass.dtID, theClass.code, theClass.desc)
        sql = 'INSERT OR REPLACE INTO drivetrains (id, code, description) VALUES (?, ?, ?)'
        logging.debug(f"theRecord: {theRecord}")

    #Update the sql database
    with conn:
        try:
            c.execute(sql, theRecord)
        except sqlite3.IntegrityError as e:
            logging.warning(f"theRecord: {theRecord} sqlite integrity error: {e.args[0]}")
            return False
        except:
            logging.error('Something went wrong', exc_info = True)
            return False

    logging.info(f"theRecord: {theRecord} commited.")
    return True

def write_carCat(theClass):
    """Adding a Car category to the database"""
    logging.debug(f"PARMS: catID:{theClass.catID}, name:{theClass.name} desc:{theClass.desc}")
    if not isinstance(theClass.catID, int):
        logging.error(f"catID not an int. Check Parms passed to function. No Record added")
        return False

    if theClass.name =='': # Can't allow  blank data to db. db doesn't consider this null
        logging.warning(f"PARMS: catID:{theClass.catID}, name:{theClass.name} desc:{theClass.desc} : name is empty. Record not added")
        return False

    if theClass.catID == 0: #Just add record and have DB create unique recID (Integrity will keep dupes out)
        theRecord = (theClass.name, theClass.desc)
        sql = "INSERT INTO car_cats (title, description) Values (?, ?)"
    else: #Update database as needed.
        theRecord = (theClass.catID, theClass.name, theClass.desc)
        sql = "INSERT OR REPLACE INTO car_cats (id, title, description) Values (?, ?, ?)"

    #Update the sql database
    logging.debug(f"Sql: {sql}")
    logging.debug(f"theRecord: {theRecord}")
    with conn:
        try:
            c.execute(sql, theRecord)
        except sqlite3.IntegrityError as e:
            logging.warning(f"theRecord: {theRecord} sqlite integrity error: {e.args[0]}")
            return False
        except:
            logging.error('Something went wrong', exc_info = True)
            return False

    logging.info(f"theRecord: {theRecord} committed.")
    return True

def write_manufacture(theClass):
    """Adding a Car Manufacture to the database"""
    logging.debug(f"PARMS: mfgID:{theClass.mfgID}, name:{theClass.name}")
    if not isinstance(theClass.mfgID, int):
        logging.error(f"theClass.mfgID not an int. Check Parms passed to function. No Record added")
        return False

    if theClass.name == '': # Can't allow blank data in (Note.. db doesn't consider this null)
        logging.warning(f"PARMS: theClass.mfgID:{theClass.mfgID}, name:{theClass.name} : name is empty. Record not added")
        return False

    if theClass.mfgID == 0: #Just add the record and have DB create unique ID (Integrity will keep dupes out)
         theRecord = (theClass.name,)
         logging.debug(f"theRecord: {theRecord}")
         sql = "INSERT INTO manufactures (title) Values (?)"
    else: # Add or Replace the provided data with the provided theClass.mfgID.
         theRecord = (theClass.mfgID, theClass.name)
         logging.debug(f"theRecord: {theRecord}")
         sql = "INSERT OR REPLACE INTO manufactures (id, title) Values (?, ?)"

    # Run the sql and catch the errors
    logging.debug(f"Sql: {sql}")
    with conn:
        try:
            c.execute(sql, theRecord)
        except sqlite3.IntegrityError as e:
            logging.warning(f"theRecord: {theRecord} sqlite integrity error: {e.args[0]}")
            return False
        except:
            logging.error('Something went wrong', exc_info = True)
            return False

    logging.info(f"theRecord: {theRecord} : committed")
    return True

def write_car(theClass):
    """Adds a Car record"""
    logging.debug(f"""
        PARMS: recID:{recID}, model:{model}, mfg_id:{mfg_id}, carcat_id:{carcat_id}, drivetrain_id:{drivetrain_id}, yearmade:{yearmade},
         notes:{notes} : model is empty. Record not added""")
    if model =='':# Can't allow blank data in. db doesn't consider this null
        logging.warning(f"""
        PARMS: recID:{recID}, model:{model}, mfg_id:{mfg_id}, carcat_id:{carcat_id}, drivetrain_id:{drivetrain_id}, yearmade:{yearmade},
         notes:{notes} : model is empty. Record not added""")
        return False

    if recID == 0: #Just add record and have DB create unique recID (Integrity will be keep dupes out.)
        theRecord = (model, mfg_id, carcat_id, drivetrain_id, yearmade, notes)
        sql = "INSERT INTO cars (model, mfg_id, carcat_id, drivetrain_id, yearmade, notes) values(?, ?, ?, ?, ?, ?)"
    else: # Add or Repoace the provided data bassed on the model
        theRecord = (recID, model, mfg_id, carcat_id, drivetrain_id, yearmade, notes)
        sql = "INSERT or REPLACE INTO cars (id, model, mfg_id, carcat_id, drivetrain_id, yearmade, notes) values(?, ?, ?, ?, ?, ?, ?)"

    logging.debug(f"Sql: {sql}")
    logging.debug(f"theRecord: {theRecord}")
    with conn:
        try:
            c.execute(sql, theRecord)
        except sqlite3.IntegrityError as e:
            logging.warning(f"theRecord: {theRecord} sqlite integrity error: {e.args[0]}")
            return False
        except:
            logging.error('Something went wrong', exc_info = True)
            return False

    logging.info(f"theRecord: {theRecord} : committed")
    logging.debug("Completed")
    return True

def get_manufacture(recid: int):
    """Get recid from mfg table.
    If recid = 0 then all returned. Results will be in a list format"""
    if not isinstance(recid, int): #recid is not an int
        logging.error('recid was not an int. no processing')
        return 0

    if recid > 0:
        sql = "SELECT id, title FROM manufactures WHERE id = ?"
        logging.debug(f'Getting specific recid: {recid} SQL: {sql}')
        c.execute(sql, (recid,))
        return c.fetchall()
    else: # Get all the records
        sql = "SELECT id, title FROM manufactures"
        logging.debug(f'Getting all manufactures. SQL: {sql}')
        c.execute(sql)
        return c.fetchall()


def xwrite_car(recID: int, model: str, mfg_id: int, carcat_id: int, drivetrain_id: int, yearmade: str, notes: str):
    """Adds a Car record"""
    logging.debug(f"""
        PARMS: recID:{recID}, model:{model}, mfg_id:{mfg_id}, carcat_id:{carcat_id}, drivetrain_id:{drivetrain_id}, yearmade:{yearmade},
         notes:{notes} : model is empty. Record not added""")
    if model =='':# Can't allow blank data in. db doesn't consider this null
        logging.warning(f"""
        PARMS: recID:{recID}, model:{model}, mfg_id:{mfg_id}, carcat_id:{carcat_id}, drivetrain_id:{drivetrain_id}, yearmade:{yearmade},
         notes:{notes} : model is empty. Record not added""")
        return False

    if recID == 0: #Just add record and have DB create unique recID (Integrity will be keep dupes out.)
        theRecord = (model, mfg_id, carcat_id, drivetrain_id, yearmade, notes)
        sql = "INSERT INTO cars (model, mfg_id, carcat_id, drivetrain_id, yearmade, notes) values(?, ?, ?, ?, ?, ?)"
    else: # Add or Repoace the provided data bassed on the model
        theRecord = (recID, model, mfg_id, carcat_id, drivetrain_id, yearmade, notes)
        sql = "INSERT or REPLACE INTO cars (id, model, mfg_id, carcat_id, drivetrain_id, yearmade, notes) values(?, ?, ?, ?, ?, ?, ?)"

    logging.debug(f"Sql: {sql}")
    logging.debug(f"theRecord: {theRecord}")
    with conn:
        try:
            c.execute(sql, theRecord)
        except sqlite3.IntegrityError as e:
            logging.warning(f"theRecord: {theRecord} sqlite integrity error: {e.args[0]}")
            return False
        except:
            logging.error('Something went wrong', exc_info = True)
            return False

    logging.info(f"theRecord: {theRecord} : committed")
    logging.debug("Completed")
    return True

