import sys
import logging
import sqlite3
from pathlib import Path

# Custom App modules
from GranT import GTClasses as gtClass

logger = logging.getLogger(__name__)


def create_connection(dbLoc=":memory:"):
    """Create a connection to a sqlite3 db.
    Note: This will NOT init db with the schema.

    Args:
        dbLoc ([str]): dbFile to connect to
        Default value is ":memory:"

    Returns:
        sqlite3.connect [object]: Connection to database
    """
    logger.debug(f"dbLoc = {dbLoc}")
    if dbLoc:
        logger.info(f"Connecting to {dbLoc}")
        try:
            conn = sqlite3.connect(
                dbLoc, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        except Exception as err:
            logger.critical(f"Unable to connect to {dbLoc}")
            logger.critical(f"Error:  {err}", exc_info=True)
            sys.exit(1)

        logger.info(f"Successful connection to {dbLoc}")
        logger.debug(f"sqlite3 version {sqlite3.version}")
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = on;")
        cur.execute("PRAGMA database_list;")
        xtmp = cur.fetchall()
        logger.debug(f"database_list={xtmp}")
        return conn
    else:  # Critical exit
        logger.critical('dbLoc must contain a value')
        sys.exit(1)
    sys.exit(1)


def _addLayoutRec(dbConn, tLayout):
    """Internal use only. Add layout rec to db with no checks

    Args:
        dbConn (sqlite3.connect): Database connection
        tLayout (TrackLayout Object)

    Returns:
        list: ResultCode, ResultText
        ResultCode = 0 Successfull
        ResultCode != 0 See ResultText for details
    """
    logger.debug(f"trackobj = {tLayout}")
    theVals = {'layoutName': tLayout.name, 'miles': tLayout.miles,
               'circuitId': tLayout.circuit.id, 'trackId': tLayout.track.id}
    sql = 'INSERT INTO track_layout (name, miles, track_id, circuit_id) VALUES (:layoutName, :miles, :trackId, :circuitId)'
    return _exeDML(dbConn, sql, theVals)


def _exeDML(dbConn, sql, theVals):
    """Executes DML commands, INSERT, DELETE, UPDATE sql.

    Args:
        dbConn (sqlite3.connect): Database connection
        sql (string): Sql to execute
        theVals : Values to be sanitized
    Returns:
        list (ResultCode, ResultText)
        ResultCode == 0 Success. ResultText will have cursor.lastrowid
        ResultCode != 0 - See ResultText for details
    """
    logger.debug(f"Passed sql={sql}")
    logger.debug(f"Passed Vals={theVals}")
    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        rowID = cur.lastrowid
        logger.debug(f"RowID = {rowID}")
        dbConn.commit()
    except sqlite3.IntegrityError as e:
        logger.warning(f"sqlite integrity error: {e.args[0]}")
        # Disable full sql traceback to logger.debug
        dbConn.set_trace_callback(None)
        retVal = [2, f"sqlite integrity error: {e.args[0]}"]
        logger.debug(f"Returning {retVal}")
        return retVal
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)

    rowCount = cur.rowcount
    logger.debug(f"successful commit of sql, Rows affected={rowCount}")
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)
    retVal = [0, f"Commit successful rowID={rowID} rowCount={rowCount}"]
    logger.debug(f"Returning {retVal}")
    return retVal


def _exeScriptFile(dbConn, scriptFileName=None):
    """ INTERNAL USE Only. executes a Script file.

    Args:
        dbConn (sqlite3.connect): Database connection
        scriptFileName : SQL script file to run. Defaults to None.
    """
    logger.debug(f"loading script {scriptFileName} to memory")
    scriptFile = open(scriptFileName, 'r')
    script = scriptFile.read()
    scriptFile.close()
    try:
        cur = dbConn.cursor()
        cur.executescript(script)
    except:
        logger.critical(
            f"Unexpected Error running script {scriptFileName}", exc_info=True)
        sys.exit(1)

    dbConn.commit()
    logger.debug(f"script commited")


def addTrack(dbConn, layout):
    """Adding a Track and a Layout for it

    Args:
        dbConn (sqlite3.connect): Database connection
        layout : Track layout object

    Returns:
            list: ResultCode, ResultText
            ResultCode = 0 Successfull
            ResultCode != 0 See ResultText for details
    """
    logger.info(f"Adding a new track {layout}")
    xtrack = getTrack(dbConn, key='track', value=layout.track.name)
    if xtrack.id != 0:  # track with same name exists - ReturnCode 100
        msg = f"Unable to save. Track name already in db. Track name = {layout.track.name}"
        logger.warning(msg)
        result = (100, msg)
        logger.debug(f"returning: {result}")
        return result
    else:
        logger.info("Confirmed track doesn't exist")

    xcircuit = getCircuit(dbConn, key='id', value=layout.circuit.id)
    if xcircuit.id == 0:  # circuit does not exist -ReturnCode 102
        msg = f'Unable to save. Circuit does not exist'
        logger.warning(msg)
        result = (102, msg)
        logger.debug(f"returning: {result}")
        return result
    else:
        logger.info("Confirmed circuit exists")

    if not layout.miles:  # Miles must have a value - ReturnCode 103.
        msg = f"Unable to save. Invalid miles value {layout.miles}"
        logger.warning(msg)
        result = (103, msg)
        logger.debug(f"returning: {result}")
        return result
    else:
        logger.info("Confirmed miles has a value")

    # Tests Passed. Now we add records
    # Add track record
    logger.info("Saving new track record")
    theVals = {'trackName': layout.track.name,
               'cntryID': layout.track.country.id}
    sql = "INSERT INTO track (name, country_id) VALUES (:trackName, :cntryID)"
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    result = _exeDML(dbConn, sql, theVals)
    if result[0] == 2:  # integrity error
        msg = f"error saving track record. error: {result}"
        logger.error(msg)
        result = (104, msg)
        logger.debug(f"returning: {result}")
        return result
    else:
        # Get new track.id from db to update layout object
        logger.debug("Getting new track.id")
        uTrack = getTrack(dbConn, key="track", value=layout.track.name)
        logger.info(f"Successfully saved new track record {uTrack}")
        logger.debug(
            "update trackLayout object with new track.id {uTrack.id}")
        layout.track.id = uTrack.id

    # Add track layout record
    logger.info("Saving track_layout record")
    result = _addLayoutRec(dbConn, layout)
    if result[0] == 2:  # integrity error
        msg = f"error saving track_layout record. error: {result}"
        logger.error(msg)
        result = (105, msg)
        logger.debug(f"returning: {result}")
        return result
    else:
        logger.info("Successfully saved new track_layout record")

    logger.debug(f"returning: {result}")
    return result


def addCar(dbConn, car):
    """Adds a Car record to database

    Args:
        dbConn (sqlite3.connect): Database connection
        car : Car object to be added

    Returns:
        list: ResultCode, ResultText
              ResultCode 0 = Success
              ResultCode != 0 = see ResultText for details
    """
    logger.info(f"Adding {car}")
    # Go validate and see what happens
    valResult = validateCar(dbConn, car)
    if valResult[0]:
        logger.info("All validation passed. Saving Car")
        sql = "INSERT INTO car (model, mfg_id, cat_id, drivetrain_id, year) VALUES (:model, :mfgId, :catId, :dtId, :year)"
        theVals = {'model': car.model,
                   'year': car.year,
                   'mfgId': car.manufacture.id,
                   'catId': car.catclass.id,
                   'dtId': car.driveTrain.id}
        result = _exeDML(dbConn, sql, theVals)
        logger.debug(f"save result: {result}")
        if result[0] == 0:
            return(0, f"Car added. {result[1]}")
        else:
            return(1, f"Unable to save: {result[1]}")
    else:  # Validation failed
        logger.debug(f"Validation did not pass: {valResult}")
        return (1, valResult[1])


def addCarSetting(dbConn, carSetting):
    """Adds a Car Setting record to db

    Args:
        dbConn (sqlite3.connect): Database connection
        carSetting : CustCarSettings Object

    Returns:
        list: ResultCode, ResultText
              ResultCode = 0 Success
              ResultCode != 0 see ResultText for details
    """
    logger.debug(f'carSetting={carSetting.__dict__}')
    logger.info(
        f"Request to add custom car setting name={carSetting.name} for car id={carSetting.car_id}")
    logger.info('Validating data')
    valResult = validateCarSetting(dbConn, carSetting)
    if valResult[0]:  # validation passed
        logger.info("All validation passed. Saving custom car settings")
        insertSQL = "INSERT INTO car_setting (car_id,cat_id,name,max_power,max_torque,power_ratio,traction_control,brake_balance,top_speed,gear_1,gear_2,gear_3,gear_4,gear_5,gear_6,gear_7,final_gear,weight,weight_reduction,tire_code,accel,braking,max_speed,cornering,stability)"
        valuesSQL = "VALUES (:car_id,:cat_id,:name,:max_power,:max_torque,:power_ratio,:traction_control,:brake_balance,:top_speed,:gear_1,:gear_2,:gear_3,:gear_4,:gear_5,:gear_6,:gear_7,:final_gear,:weight,:weight_reduction,:tire_code,:accel,:braking,:max_speed,:cornering,:stability)"
        sql = f"{insertSQL} {valuesSQL}"
        theVals = {'car_id': carSetting.car_id,'cat_id': carSetting.cat_id,'name': carSetting.name,'max_power': carSetting.max_power,'max_torque': carSetting.max_torque,'power_ratio': carSetting.power_ratio,'traction_control': carSetting.traction_control,'brake_balance': carSetting.brake_balance,'top_speed': carSetting.top_speed,'gear_1': carSetting.gear_1,'gear_2': carSetting.gear_2,'gear_3': carSetting.gear_3,'gear_4': carSetting.gear_4,'gear_5': carSetting.gear_5,'gear_6': carSetting.gear_6,'gear_7': carSetting.gear_7,'final_gear': carSetting.final_gear,'weight': carSetting.weight,'weight_reduction': carSetting.weight_reduction,'tire_code': carSetting.tire_code,'accel': carSetting.accel,'braking': carSetting.braking,'max_speed': carSetting.max_speed,'cornering': carSetting.cornering,'stability': carSetting.stability}
        result = _exeDML(dbConn, sql, theVals)
        logger.debug(f"save result: {result}")
        if result[0] == 0:
            return(0, f"Custom car settings added. {result[1]}")
        else:
            return(1, f"Unable to add: {result[1]}")
    else:  # validation failed
        logger.warning(valResult[1])
        result = (1, valResult[1])
        return result


def addLayout(dbConn, trackLayout):
    """Adds a Track Layout record

    Args:
        dbConn (sqlite3.connect): Database connection
        trackLayout : TrackLayout Object

    Returns:
        list: ResultCode, ResultText
              ResultCode 0 = Success
              ResultCode != 0 = see ResultText for details
    """
    logger.debug(f"addTrackLayout: trackLayout={trackLayout}")
    logger.info(
        f"Adding track layout {trackLayout.name} for track {trackLayout.track.name}.")
    tResult = validateTrackLayout(dbConn, trackLayout)
    if tResult[0]:  # Tests passed
        result = _addLayoutRec(dbConn, trackLayout)
    else:
        logger.warning(tResult[1])
        result = (1, tResult[1])

    logger.debug(f"returning: {result}")
    return result


def addMfg(dbConn, mfgObj):
    """[summary]

    Args:
        dbConn (sqlite3.connect): Database connection
        mfgObj : Manufacture class object

    Returns:
        list:  (ResultCode, ResultText)
                ResultCode == 0: Success Add
                Resultcode <> 0: See ResultText for details[description]
            Fields which cause common errors.
            - mfgObj.mfgName must be unique in db (case insensitive).
            - mfgObj.country.id must exist in Country table in db.
            mfgObj.id is ignored
    """
    logger.debug(f"add mfg: MfgObj= {mfgObj}")
    sql = "INSERT INTO manufacture (name, country_id) VALUES (:mfgName, :cntryID)"
    theVals = {'mfgName': mfgObj.name, 'cntryID': mfgObj.country.id}
    r = _exeDML(dbConn, sql, theVals)
    if r[0] == 0:
        r[1] = f"Manufacture name: {mfgObj.name} added"
    else:
        logger.debug(f"problem with manufacture add {r}.")

    logger.debug(f"returning {r}")
    return r


def addRace(dbConn, race):
    """Adding a Race to database

    Args:
        dbConn (sqlite3.connect): Database connection
        race ([Object]): The race object to add

    Returns:
        list: ResultCode, ResultText
              ResultCode == 0 Successful
              ResultCode !=0 Unsuccessful, see ResultText
    """
    logger.debug(f"addRace: race={race}")
    logger.info(
        f"Adding race {race.name} for Race Collection {race.raceCollection.name}")
    tResult = validateRace(dbConn, race)
    if tResult[0]:  # Tests passed - Save the Race
        sql = "INSERT INTO race (name, tl_id, rc_id,racetime,weather_id,limits,type_id,notes) VALUES (:name, :trackLayoutID, :raceColID,:racetime,:weather_id, :limits, :type_id, :notes)"
        theVals = {'name': race.name,
                   'trackLayoutID': race.trackLayout.id,
                   'raceColID': race.raceCollection.id,
                   'racetime': race.racetime,
                   'weather_id': race.weather.id,
                   'limits': race.limits,
                   'type_id': race.raceType.id,
                   'notes': race.notes}
        logger.debug(f"sql={sql}")
        logger.debug(f"theVals={theVals}")
        result = _exeDML(dbConn, sql, theVals)
    else:
        logger.warning(tResult[1])
        result = (1, tResult[1])

    logger.debug(f"returning: {result}")
    return result


def addRaceCollection(dbConn, raceCollection):
    """Add a Race Collection to database

    Args:
        dbConn (sqlite3.connect): Database connection
        raceCollection : raceCollection Object

    Returns:
        list: (ResultCode, ResultText)
              ResultCode 0 = Success Add
              Resultcode <> 0 - See ResultText for details
    """
    logger.debug(f"raceCollection={raceCollection}")
    # Collection name must have a value
    if raceCollection.name == None or raceCollection.name == "":
        rtrnMsg = [1, "Collection name can not be blank"]
        logger.debug(f"Return {rtrnMsg}")
        return rtrnMsg

    # Collection name must be unique for this league
    xlist = getRaceCollectionList(dbConn, raceCollection.league.id)
    logger.debug(f"xlist={xlist}")
    for r in xlist:
        if raceCollection.name == r[1]:  # match
            rtrnMsg = [
                1, f"Collection name [{raceCollection.name}] already exists for League id [{raceCollection.league.id}]"]
            logger.debug(f"Return {rtrnMsg}")
            return rtrnMsg

    # Tests Passed
    theVals = {'colName': raceCollection.name,
               'colDesc': raceCollection.desc,
               'leagueId': raceCollection.league.id,
               'catId': raceCollection.classcat.id,
               'prize1': raceCollection.prize1,
               'prize2': raceCollection.prize2,
               'prize3': raceCollection.prize3}
    sql = "INSERT INTO race_collection (league_id, name, description, cat_id, prize1, prize2, prize3) VALUES (:leagueId, :colName, :colDesc, :catId, :prize1, :prize2, :prize3)"
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    rtrnMsg = _exeDML(dbConn, sql, theVals)
    logger.debug(f"Return {rtrnMsg}")
    return rtrnMsg

def deleteCarSetting(dbConn,id):
    """Delete car setting record from database

    Args:
        dbConn (sqlite3.connect): Database connection
        id ([int]): UniqueID assigned to the car setting

    Returns:
        list: (ResultCode, ResultText)
                ResultCode == 0: it worked
                Resultcode <> 0: See ResultText for details
    """
    logger.debug(f"delete CarSettingID={id}")
    sql = "DELETE FROM car_setting WHERE id = ?"
    theVals=(id,)
    result = _exeDML(dbConn, sql, theVals)

    if result[0] == 0: #Sql successfully commited
        #Need to parse to get rowcount. Expecting rowCount=nnn
        srchFor = 'ROWCOUNT'
        rowCount=None
        for x in result[1].split(' '):
            if x.upper().find(srchFor) == 0: # found it
                xTmp = x.split('=')
                rowCount=int(xTmp[1])
                break

        if rowCount > 0:
            result = [0, f'Deleted {rowCount} row(s)']
        else:
            result = [1, 'No rows were deleted']

    logger.debug(f"returning {result}")
    return result


def deleteMfg(dbConn, mfgId):
    """Delete manufacture record from database

    ARGS:
        dbConn (sqlite3.connect): Database connection
        mfgId: UniqueID of Manufacture in DB(Manufacture.id)

    Returns:
        list: (ResultCode, ResultText)
                ResultCode == 0: it worked
                Resultcode <> 0: See ResultText for details
    """
    logger.debug(f"delete manufacture id={mfgId}")
    sql = "DELETE FROM manufacture WHERE id = ?"
    theVals = (mfgId,)
    result = _exeDML(dbConn, sql, theVals)
    if result[0] == 0:
        result[1] = "Manufacture Deleted"
    else:
        logger.debug(f"problem with manufacture delete {result}.")

    logger.debug(f"returning {result}")
    return result


def deleteTrack(dbConn, trackId):
    """Delete track and all related track layouts from db

    Args:
        dbConn (sqlite3.connect): Database connection
        trackId (int): UniqueID of the track in the db

    Returns:
            list: ResultCode, ResultText
                  ResultCode == 0 : successful
                  Resultcode != 0 : See ResultText for details
    """
    logger.info(
        f"Delete track trackId={trackId} and related track layouts.")
    result = (1, "method is not ready yet")
    # 1-Get and delete track_layout records for track id
    #   Get list of track_layouts for trackid
    logger.info(f"Getting track layouts for trackid {trackId}")
    trackLayouts = getLayoutList(dbConn, trackId)
    logger.info(f"track layouts to delete: {len(trackLayouts)}")
    logger.info(f"trackLayouts = {trackLayouts}")
    #   Delete each track layout
    for tLayout in trackLayouts:
        layoutId = tLayout[0]
        logger.debug(f"Deleting trackLayoutID {layoutId}: {tLayout}")
        result = deleteTrackLayout(dbConn, layoutId)
        if result[0] != 0:  # error with delete. Stop deleting
            logger.warning(
                f"problem deleting track layout id={layoutId}. See {result}.")
            return result

    # 2-If that was successfull then delete track
    sql = "DELETE FROM track WHERE id = ?"
    theVals = (trackId,)
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    result = _exeDML(dbConn, sql, theVals)
    if result[0] == 0:
        result[1] = f"track id={trackId} deleted"
    else:
        logger.warning(
            f"problem deleting track id={trackId}. See {result}.")

    return result


def deleteTrackLayout(dbConn, layoutId):
    """Delete track layout from db

    Args:
        dbConn (sqlite3.connect): Database connection
        layoutId (int): UniqueID of the track layout in the db

    Returns:
        list: ResultCode, ResultText
              ResultCode == 0 : successful
              Resultcode != 0 : See ResultText for details
    """
    logger.info(f"Delete track layout id={layoutId}.")
    result = (1, "method is not ready yet")
    sql = "DELETE FROM track_layout WHERE id = ?"
    theVals = (layoutId,)
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    result = _exeDML(dbConn, sql, theVals)
    if result[0] == 0:
        result[1] = f"track layout id={layoutId} deleted"
    else:
        logger.warning(
            f"problem deleting track layout id={layoutId}. See {result}.")

    logger.info(f"returning {result}")
    return result


def getCar(dbConn, id):
    """Get a Car from db

    Args:
        dbConn (sqlite3.connect): Database connection
        id (int): Unique id assigned in the db to the car

    Returns:
        Car Object
        IF CarObject.id == 0 then nothing found
    """
    logger.info(f"Getting car object id={id}")
    selectSQL = "SELECT id, model, mfg_id, cat_id, drivetrain_id, year"
    fromSQL = "FROM car"
    whereSQL = "WHERE id=?"
    sql = f"{selectSQL} {fromSQL} {whereSQL}"
    theVals = (id,)
    # Execute the SQL
    results = directSql(dbConn, sql, theVals)
    if results:  # have data
        logger.info(f"Found carid: {id}. Converting to car Object")
        xMaker = getMfg(dbConn, value=results[0][2])
        xClassCat = getCarCat(dbConn, results[0][3])
        xDriveTrain = getDriveTrain(dbConn, results[0][4])
        xCar = gtClass.Car(results[0][0], results[0]
                           [1], xMaker, xDriveTrain, xClassCat)
        xCar.year = results[0][5]

    else:  # Create blank car
        logger.info(f"Unable to find carid: {id}. Creating empty car object")
        xCountry = gtClass.Country(
            cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)
        xMaker = gtClass.Manufacture(0, None, xCountry)
        xDriveTrain = gtClass.DriveTrain(0, code=None, desc=None)
        xClassCat = gtClass.ClassCat(0, name=None, desc=None)
        xCar = gtClass.Car(0, None, xMaker, xDriveTrain, xClassCat)

    logger.debug(f"Returning : {xCar}")
    return xCar

def getCarSetting(dbConn,id):
    """Get a Car Setting from db

    Args:
        dbConn (sqlite3.connect): Database connection
        id (int): Unique id assigned in the db to the car setting

    Returns:
        CustCarSetting Object
        IF CustCarSetting.id == 0 then nothing found
    """
    logger.info(f"Getting car setting object id={id}")
    selectSQL="SELECT id,car_id,cat_id,name,max_power,max_torque,power_ratio,traction_control,brake_balance,top_speed,gear_1,gear_2,gear_3,gear_4,gear_5,gear_6,gear_7,final_gear,weight,weight_reduction,tire_code,accel,braking,max_speed,cornering,stability"
    fromSQL="FROM car_setting"
    whereSQL = "WHERE id=?"
    sql = f"{selectSQL} {fromSQL} {whereSQL}"
    theVals = (id,)
    # Execute the SQL
    results = directSql(dbConn, sql, theVals)
    if results: # Have data
        logger.info(f"Found carSettingID={id}. Converting to carSetting Object")
        logger.debug(f"results={results}")
        carSetting=gtClass.CustCarSettings(id=results[0][0],
        car_id=results[0][1],
        cat_id=results[0][2],
        name=results[0][3])
        carSetting.max_power=results[0][4]
        carSetting.max_torque=results[0][5]
        carSetting.power_ratio=results[0][6]
        carSetting.traction_control=results[0][7]
        carSetting.brake_balance=results[0][8]
        carSetting.top_speed=results[0][9]
        carSetting.gear_1=results[0][10]
        carSetting.gear_2=results[0][11]
        carSetting.gear_3=results[0][12]
        carSetting.gear_4=results[0][13]
        carSetting.gear_5=results[0][14]
        carSetting.gear_6=results[0][15]
        carSetting.gear_7=results[0][16]
        carSetting.final_gear=results[0][17]
        carSetting.weight=results[0][18]
        carSetting.weight_reduction=results[0][19]
        carSetting.tire_code=results[0][20]
        carSetting.accel=results[0][21]
        carSetting.braking=results[0][22]
        carSetting.cornering=results[0][23]
        carSetting.max_speed=results[0][24]
        carSetting.stability=results[0][25]
    else: # Create blank car settings object
        logger.info(f"Unable to find carSettingID={id}. Creating empty carSetting Object")
        carSetting=gtClass.CustCarSettings(id=0,car_id=0,name="Not found",cat_id=0)

    logger.debug(f"carSettingObj={carSetting.__dict__}")
    return carSetting

def getCarSettingList(dbConn,carId):
    """Returns a list of car settings for carId

    Args:
        dbConn (sqlite3.connect): Database connection
        carId : The car.id to get all the settings for
    Returns:
        list(id, custSettingName)
        The list will be sorted by custSettingName
    """
    logger.info(f"Getting list of car settings for carId={carId}")
    selectSQL="SELECT cset.id, cset.name"
    fromSQL="FROM car_setting AS cset INNER JOIN car ON cset.car_id = car.id"
    orderBySQL="ORDER BY cset.name"
    whereSQL = "WHERE car.id = ?"
    sql = f"{selectSQL} {fromSQL} {whereSQL} {orderBySQL}"
    theVals = (carId,)
    result = directSql(dbConn, sql, theVals)
    logger.info(f"Returning {len(result)} rows")
    return result


def getCarCat(dbConn, id):
    """Get a Car Class Category from db

    Args:
        dbConn (sqlite3.connect): Database connection
        id (id): Car Class Cateory ID

    Returns:
        ClassCat object
        IF ClassCat.id == 0 then ClassCat was not found
    """
    logger.info(f"Getting classCat by id: {id}")
    selectSQL = "SELECT id,name,description,sortOrder FROM category"
    whereSQL = "WHERE id = ?"
    value = id
    sql = f"{selectSQL} {whereSQL}"
    theVals = (value,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")
    row = directSql(dbConn, sql, theVals)
    logger.debug(f"row={row}")
    if row:  # Create ClassCat object
        rtnObj = gtClass.ClassCat(
            id=row[0][0], name=row[0][1], desc=row[0][2])
        rtnObj.sortOrder = row[0][3]
    else:  # Create an empty ClassCat object
        rtnObj = gtClass.ClassCat(id=0, name="", desc="")

    logger.debug(f"rtnObj={rtnObj}")
    return rtnObj


def getCarCatList(dbConn):
    """Gets all the car category/classes in db and returns as a list

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
        list(id, carClass, desc, sortorder)
        """
    logger.info("Getting list of all the car categories")
    selectSQL = "SELECT c.id as id, c.name as carClass, c.description as desc, c.sortOrder as sortorder FROM category as c ORDER BY c.sortOrder"
    sql = selectSQL
    logger.debug(f"sql = {sql}")
    theVals = ()
    result = directSql(dbConn, sql, theVals)
    logger.info(f"Returning {len(result)} rows")
    return result


def getCarList(dbConn, mfgID, sortBy="year"):
    """Get a list of cars for mfgID sorted by <sortBy>

    Args:
        dbConn (sqlite3.connect): Database connection
        mfgID (int): Manufacture unique ID
        sortBy (str, optional): List sorted by. Defaults to "year". (not case sensitive)
            name = Sorted by car name
            year = Sorted by the year, name
            ClassCat = Sorted by the class category text (not id), name
            drivetrain = Sorted by the drive train name (not id), name

    """
    logger.debug(f"mfgID={mfgID} sortBy={sortBy} ")
    selectSQL = "SELECT car.mfg_id, model, year, cat.name as class, dt.code"
    fromSQL = "FROM car JOIN drivetrain AS dt ON car.drivetrain_id = dt.id JOIN category as cat on car.cat_id = cat.id"
    whereSQL = "WHERE mfg_id = :mfgID"
    vals = {'mfgID': mfgID}

    if sortBy.lower() == 'classcat':  # Sort by the ClassCat.name
        orderSQL = "ORDER BY cat.name"
    elif sortBy.lower() == 'drivetrain':
        orderSQL = "ORDER BY dt.code"
    elif sortBy.lower() == 'name':
        orderSQL = "ORDER BY model"
    elif sortBy.lower() == 'year':
        orderSQL = "ORDER BY year"
    else:
        logger.warning(
            f"Unknown sortBy value passed. Setting no orderby")
        orderSQL = ""

    sql = f"{selectSQL} {fromSQL} {whereSQL} {orderSQL}"
    results = directSql(dbConn=dbConn, sql=sql, theVals=vals)
    logger.info(f"Returning {len(results)} rows")
    return results


def getCircuit(dbConn, key='id', value=None):
    """Get circuit record from db

    Args:
        dbConn (sqlite3.connect): Database connection
        key (str): key to search for value.
            'id' or 'name'
        value : Value to search for in key

    Returns:
        CircuitObject
    """
    logger.info(f"Getting a circuit key={key}, value={value}")
    selectSQL = "SELECT c.id as circuitId, c.name AS Circuit FROM circuit AS c"

    if key == 'id':
        whereSQL = "WHERE c.id = ?"
    elif key == 'name':
        whereSQL = "WHERE c.name = ?"
    else:  # no key passed
        logger.critical("Invalid or missing key value passed.")
        sys.exit(1)

    sql = f"{selectSQL} {whereSQL}"
    theVals = (value,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")
    row = directSql(dbConn, sql, theVals)
    if row:  # populate ciruit object
        logger.info(f"Circuit found")
        xCircuit = gtClass.Circuit(id=row[0][0], name=row[0][1])
    else:  # create blank ciruit object
        logger.info(f"Circuit not found")
        xCircuit = gtClass.Circuit(id=0, name=None)

    logger.debug(f"returning: {xCircuit}")
    return xCircuit


def getCircuitList(dbConn):
    """Get a list of all the circuits

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns: list(id, name)
    """
    logger.info("Getting list of Circuits")
    selectSQL = "SELECT c.id as id, c.name as name from circuit as c"
    orderbySQL = "ORDER by name"
    sql = f"{selectSQL} {orderbySQL}"
    theVals = ()
    logger.debug(f"sql = {sql}")
    result = directSql(dbConn, sql, theVals)
    logger.info(f"Returning {len(result)} rows")
    return result


def getCountry(dbConn, countryId):
    """Return a Country object from db by countryID

    Args:
        dbConn (sqlite3.connect): Database connection
        countryID (int): Unique ID for the country
    """
    logger.info(f"Getting country by countryId: {countryId}")
    selectSQL = "SELECT id AS countryId, name AS Country, alpha2, alpha3, region FROM country"
    whereSQL = "WHERE countryId = ?"
    sql = f"{selectSQL} {whereSQL}"
    theVals = (countryId,)
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    row = directSql(dbConn, sql, theVals)
    if row:  # Populate Country obj with db data
        logger.info(f"Found countryId: {countryId}")
        country = gtClass.Country(
            cntryID=row[0][0],
            cntryName=row[0][1],
            alpha2=row[0][2],
            alpha3=row[0][3],
            region=row[0][4])
    else:  # Create blank Country obj
        logger.info(f"Unable to find countryId: {countryId}")
        country = gtClass.Country(
            cntryID=0,
            cntryName=None,
            alpha2=None,
            alpha3=None,
            region=None)
    logger.info(f"Returning country={country}")
    return country


def getDriveTrain(dbConn, id):
    """Get a Drive Train from the database

    Args:
        dbConn (sqlite3.connect): Database connection
        id (int): Unique ID for the drivetrain in db

    Returns:
        DriveTrain object
        IF DriveTrain.id == 0 then no drive train found
    """
    logger.info(f"Getting drivetrain object id={id}")
    selectSQL = "SELECT id, code, description"
    fromSQL = "FROM drivetrain"
    whereSQL = "WHERE id=?"
    sql = f"{selectSQL} {fromSQL} {whereSQL}"
    theVals = (id,)
    # Execute the SQL
    results = directSql(dbConn, sql, theVals)

    if results:  # Create DriveTrain object
        xObj = gtClass.DriveTrain(results[0][0], results[0][1], results[0][2])
    else:  # Create empty DriveTrain object
        xObj = gtClass.DriveTrain(0, None, None)

    logger.debug(f"Returning : {xObj}")
    return xObj


def getDriveTrainList(dbConn, orderBy='code'):
    """[summary]

    Args:
        dbConn (sqlite3.connect): Database connection
        orderBy (str, optional): The field for the list to be ordered by
        Defaults to 'code'.

    Returns:
            list: (id, code, description)
    """
    logger.info(f"Getting all drive trains ordered by {orderBy} ")
    selectSQL = "select id, code, description FROM drivetrain"
    orderBySQL = f"ORDER BY {orderBy}"
    sql = f"{selectSQL} {orderBySQL}"
    logger.debug(f"sql: {sql}")
    theVals = ()
    result = directSql(dbConn, sql, theVals)
    logger.info(f"Returning {len(result)} rows")
    return result

def getGarageMfgList(dbConn):
    """Get a list of all manufactures that have cars in the garage

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
        list: (MfgId,Make)
    """
    logger.info(f"Getting list of manufactures that have cars in the garage")
    selectSQL="SELECT mfg.id AS id,mfg.name AS Make"
    fromSQL="FROM manufacture AS mfg JOIN car ON car.mfg_id = mfg.id"
    groupBySQL ="GROUP BY mfg.id, mfg.name"
    orderBySQL = f"ORDER BY mfg.name"
    sql = f"{selectSQL} {fromSQL} {groupBySQL} {orderBySQL}"
    theVals = ()
    logger.debug(f"sql: {sql}")
    results = directSql(dbConn, sql, theVals)
    logger.info(f"Rows being returned: {len(results)}")
    return results


def getLayout(dbConn, layoutId):
    """Gets a single Track Layout record from database.

    Args:
        dbConn (sqlite3.connect): Database connection
        layoutId (int): Track layoutID number to get from database.
    Returns:
        TrackLayout Object: IF TrackLayoutObject.id == 0 then nothing found
    """
    logger.info(f"Getting track layout id {layoutId}")
    sql = """SELECT id as layoutId, name as layoutName, miles, track_id, circuit_id FROM track_layout WHERE layoutId=?"""
    theVals = (layoutId,)
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    row = directSql(dbConn, sql, theVals)
    if row:  # Populate trackLayout obj
        logger.info(f"Found track layout id {layoutId}")
        xTrack = getTrack(dbConn, key='trackId', value=row[0][3])
        xCircuit = getCircuit(dbConn, key='id', value=row[0][4])
        xTrackLayout = gtClass.TrackLayout(
            row[0][0], row[0][1], miles=row[0][2], trackObj=xTrack, circuitObj=xCircuit)

    else:  # Create blank trackLayout obj (no data returned)
        logger.info(f"Unable to find track layout id {layoutId}")
        logger.debug(f"creating empty tracklayout object")
        xCircuit = getCircuit(dbConn, key='id', value=0)
        xTrack = getTrack(dbConn, key='trackId', value=0)
        xTrackLayout = gtClass.TrackLayout(
            id=0, name=None, miles=None, trackObj=xTrack, circuitObj=xCircuit)

    logger.debug(f"returning object xTrackLayout={xTrackLayout} ")
    return xTrackLayout


def getLayoutList(dbConn, trackId):
    """Get a list of track layouts for a trackId

    Args:
        dbConn (sqlite3.connect): Database connection
        trackId (int): The trackId of the track the layout list is for
    Returns:
        list: (layoutId, layout,Miles,Races)
    """
    logger.info(f"Getting track layout list: trackId={trackId}")
    selectSQL = "SELECT tl.id AS layoutId, tl.name AS layout, tl.miles AS Miles, count(race.tl_id) AS Races"
    fromSQL = "FROM track_layout AS tl LEFT JOIN race ON tl.id = race.tl_id"
    groupBySQL = "GROUP BY tl.id HAVING tl.track_id = ?"
    orderBySQL = "ORDER BY layout"
    sql = f"{selectSQL} {fromSQL} {groupBySQL} {orderBySQL}"
    theVals = (trackId,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")
    results = directSql(dbConn, sql, theVals)
    logger.info(f"Returning {len(results)} rows")
    return results


def getLeague(dbConn, key='id', value=None):
    """Get a league object from database by various fields

    Args:
        dbConn (sqlite3.connect): Database connection
        key (str, optional): The key/field to get object from db. Defaults to 'id'.
        value (required to return something): The value the key must equal to return the object.

    Returns:
        LeagueObject. If nothing found then LeagueObj.id=0
    """
    logger.info(f"Getting a League: {key}={value}")
    selectSQL = "SELECT id, name, sortord FROM league"
    whereSQL = f"WHERE {key} = ?"
    theVals = (value,)
    sql = f"{selectSQL} {whereSQL}"
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    row = directSql(dbConn, sql, theVals)
    if row:  # have data from db
        league = gtClass.League(
            id=row[0][0], name=row[0][1], sortord=row[0][2])
    else:  # No data from db. Create empty object
        league = gtClass.League(id=0, name="", sortord=0)
    logger.debug(f'returning: {league}')
    return league


def getLeagueList(dbConn):
    """Returns a list of all the leagues in the db.

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
        list (leagueID, leagueName)
    """
    logger.info("Getting list of Leagues")
    selectSQL = "SELECT id, name FROM league"
    orderBySQL = "ORDER BY sortord"
    sql = f"{selectSQL} {orderBySQL}"
    logger.debug(f"sql = {sql}")
    theVals = ()
    results = directSql(dbConn, sql, theVals)
    logger.debug(f"Returning {len(results)} rows")
    return results


def getMfg(dbConn, key='mfgId', value=None):
    """
    Gets a manufacture record from the database based on the key being used.

    Args:
        dbConn (sqlite3.connect): Database connection
        value : Is the value being search for.
        key   : the column to search on. mfgId, or Make. Default is mfgid

    Returns:
        ManufactureObject. IF ManufactureObject.id = 0 then nothing found
    """
    logger.debug(f"Getting Manufacture: {key}={value}")
    selectSQL = "SELECT mfg.id as mfgId, mfg.name AS Make, country_id as cntryId FROM manufacture AS mfg"
    whereSQL = f" WHERE {key} = ?"
    theVals = (value,)
    sql = f"{selectSQL} {whereSQL}"
    # Ready to execute SQL
    logger.debug(f"theVars: {theVals}")
    logger.debug(f"sql: {sql}")
    row = directSql(dbConn, sql, theVals)
    logger.debug(f"row={row}")
    # default Country object (blank)
    xCountry = gtClass.Country(
        cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)

    if row:  # Populate Manufacture object
        logger.debug("manufacture found.")
        if row[0][2]:  # We have a country. Load country object
            xCountry = getCountry(dbConn, row[0][2])

        xMake = gtClass.Manufacture(
            id=row[0][0], name=row[0][1], countryObj=xCountry)
        logger.debug(f"returning manufacture object")
    else:
        # Create blank Manufacture object
        logger.debug("manufacture not found.")
        xMake = gtClass.Manufacture(
            id=0, name='', countryObj=xCountry)
        logger.debug(f"returning blank manufacture object")

    logger.debug(f"Returning : {xMake}")
    return xMake


def getMfgList(dbConn):
    """Returns a list of manufactures.

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
        list: (MfgId,Make)
    """
    logger.info(f"Getting all manufactures")
    selectSQL = """SELECT mfg.id as id, mfg.name AS Make FROM manufacture AS mfg"""
    orderBySQL = f"ORDER BY mfg.name"
    sql = f"{selectSQL} {orderBySQL}"
    theVals = ()
    logger.debug(f"sql: {sql}")
    results = directSql(dbConn, sql, theVals)
    logger.info(f"Rows being returned: {len(results)}")
    return results


def getRace(dbConn, id):
    """Get a Race object from database by raceId

    Args:
        dbConn (sqlite3.connect): Database connection
        id (int): The unique race ID

    Returns:
        Race Object: The race object.
        If race.id=0 then race was not found
    """
    logger.info(f"Getting race from db for race id: {id}")
    selectSQL = "SELECT id, name, tl_id, rc_id, weather_id, type_id, racetime, limits, notes FROM race"
    whereSQL = "WHERE id = ?"
    value = id
    theVals = (value,)
    sql = f"{selectSQL} {whereSQL}"
    logger.debug(f"sql={sql}")
    logger.debug(f"theVals={theVals}")
    row = directSql(dbConn, sql, theVals)
    if row:  # Create a race object
        logger.info("Found race")
        logger.debug(f"row={row}")
        id = row[0][0]
        name = row[0][1]
        trackLayout = getLayout(dbConn, row[0][2])
        raceCollection = getRaceCollection(dbConn, rcId=row[0][3])
        weather = getWeather(dbConn, row[0][4])
        raceType = getRaceType(dbConn, row[0][5])
        racetime = row[0][6]
        limits = row[0][7]
        notes = row[0][8]
    else:  # create a blank racetype object
        logger.info("Race not found")
        trackLayout = getLayout(dbConn, 0)
        raceCollection = getRaceCollection(dbConn, rcId=0)
        weather = getWeather(dbConn, 0)
        raceType = getRaceType(dbConn, 0)
        id = 0
        name = None
        racetime = None
        limits = None
        notes = None

    race = gtClass.Race(id=id, name=name, trackLayout=trackLayout,
                        raceCollection=raceCollection, raceType=raceType, weather=weather)
    race.racetime = racetime
    race.limits = limits
    race.notes = notes

    logger.debug(f"race={race}")
    return race


def getRaceList(dbConn, raceCollectionID):
    """Get a list of races for a Race Collection

    Args:
        dbConn (sqlite3.connect): Database connection
        raceCollectionID (int): Race Collection ID

    Returns:
        list: (raceID,raceName)
    """
    # Got to get a list of races for this race.raceCollection.id
    logger.info(f"Getting race list for collection ID={raceCollectionID}")
    selectSQL = "select r.id as raceID, r.name as RaceName FROM race as r"
    whereSQL = "WHERE r.rc_id = ?"
    orderBySQL = "ORDER BY r.name"
    sql = f"{selectSQL} {whereSQL} {orderBySQL}"
    theVals = (raceCollectionID,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")
    results = directSql(dbConn, sql, theVals)
    logger.info(f"Returning {len(results)} rows")
    logger.debug(f"result={results}")
    return results


def getRaceCollection(dbConn, rcId):
    """Get a race collection object from database

    Args:
        dbConn (sqlite3.connect): Database connection
        rcId (int): Race collection id

    Returns:
        Race Collection object
        IF raceCollection.id == 0 then race Collection not found
    """
    logger.info(f"Getting Race Collection by id: {rcId}")
    selectSQL = "SELECT id as collectionId,name,description,league_id,cat_id,prize1,prize2,prize3 FROM race_collection"
    whereSQL = "WHERE collectionId = ?"
    value = rcId
    sql = f"{selectSQL} {whereSQL}"
    theVals = (value,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")
    row = directSql(dbConn, sql, theVals)
    if row:  # populate the raceCollection object
        logger.debug("Found race collection")
        logger.debug(f"row={row}")

        league = getLeague(dbConn, key='id', value=row[0][3])
        logger.debug(f"league={league}")
        raceCollection = gtClass.RaceCollection(
            id=row[0][0], name=row[0][1], desc=row[0][2], leagueObj=league)

        # Getting the car class category
        catClass = getCarCat(dbConn, id=row[0][4])
        if catClass.id == 0:  # no catClass assigned to raceCollection
            raceCollection.classcat = gtClass.ClassCat(
                id=None, name="", desc="")
        else:
            raceCollection.classcat = catClass

        # Prize money
        raceCollection.prize1 = row[0][5]
        raceCollection.prize2 = row[0][6]
        raceCollection.prize3 = row[0][7]

    else:  # create a blank raceCollection object
        league = getLeague(dbConn, key='id', value=0)
        raceCollection = gtClass.RaceCollection(
            id=0, name=None, desc=None, leagueObj=league)

    logger.debug(f"raceCollection={raceCollection}")
    return raceCollection


def getRaceCollectionList(dbConn, leagueId):
    """Returns Race Collection list for the leagueID.

    Args:
        dbConn (sqlite3.connect): Database connection
        leagueId (int): leagueId to get race collections for

    Returns:
        list: (id,name,desc,catClass, Prize1, Prize2, Prize3,raceCount)
    """
    logger.info(
        f"Getting list of race collections for a leagueID {leagueId}")
    selectSQL = "SELECT rc.id, rc.name, rc.description, cat.name as catClass, rc.prize1,  rc.prize2, rc.prize3,Count(race.id) AS races"
    fromSQL = "FROM race_collection AS rc LEFT JOIN category AS cat ON rc.cat_id = cat.id LEFT JOIN race ON race.rc_id = rc.id"
    groupBySQL = "GROUP BY rc.id HAVING rc.league_id=?"
    orderBySQL = "ORDER BY rc.name"
    sql = f"{selectSQL} {fromSQL} {groupBySQL} {orderBySQL}"
    theVals = (leagueId,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")
    results = directSql(dbConn, sql, theVals)
    logger.info(f"Rows being returned: {len(results)}")
    return results


def getRaceType(dbConn, id):
    """Get a Race Type from db by id

    Args:
        dbConn (sqlite3.connect): Database connection
        id (int): Race Type unique id

    Returns:
        RaceTypeObj: Race type object
        If RaceTypeObj.id=0 then race type was not found
    """
    selectSQL = "SELECT id, name FROM race_type"
    whereSQL = "WHERE id = ?"
    value = id
    sql = f"{selectSQL} {whereSQL}"
    theVals = (value,)
    row = directSql(dbConn, sql, theVals)
    logger.debug(f"row={row}")
    if row:  # Create a racetype object
        logger.debug("Found race type")
        logger.debug(f"row={row}")
        rt = gtClass.RaceType(id=row[0][0], name=row[0][1])
    else:  # create a blank racetype object
        rt = gtClass.RaceType(id=0, name="")

    logger.debug(f"rt={rt}")
    return rt


def getRaceTypeList(dbConn):
    """Return a list of all the race types in db

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
            list: (raceTypeid, raceTypeName)
    """
    logger.info("Getting list of race types from db")
    selectSQL = "SELECT id, name FROM race_type ORDER by name"
    sql = selectSQL
    theVals = ()
    logger.debug(f"sql = {sql}")
    results = directSql(dbConn, sql, theVals)
    logger.debug(f"Returning {len(results)} rows")
    return results


def getTireList(dbConn):
    """Return a list of all the tire type in db

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
        list: (TireCode, description)

    """
    logger.info("Getting list of race types from db")
    sql = "SELECT code, description from tire ORDER BY code"
    theVals = ()
    logger.debug(f"sql = {sql}")
    results = directSql(dbConn, sql, theVals)
    logger.debug(f"Returning {len(results)} rows")
    return results


def getTrack(dbConn, key='trackId', value=None):
    """Gets a single Track record from database based on key and value passed.

    Args:
        dbConn (sqlite3.connect): Database connection
        key (str, optional): Column to search on. trackId, or track. Defaults to 'trackId'.
        value (optional): Value you are looking for. Defaults to None.

    Returns:
        Track Object
        if TrackObject.id == 0 then track was not found
    """
    logger.debug(f"getting track key={key}, value={value}")
    if key == 'trackId':
        whereSQL = "WHERE trackId = ?"
    elif key == 'track':
        whereSQL = "WHERE track = ?"

    sqlSelect = """SELECT id AS trackId, name AS track, country_id as countryId FROM track"""
    sql = f"{sqlSelect} {whereSQL}"
    theVals = (value,)
    logger.debug(f"sql = {sql}")
    logger.debug(f"theVals = {theVals}")
    row = directSql(dbConn, sql, theVals)
    logger.debug(f"row={row}")
    # default Country object (blank)
    xCountry = gtClass.Country(
        cntryID=0, cntryName=None, alpha2=None, alpha3=None, region=None)

    if row:  # Populate the track object
        logger.info(f"Found Track")
        if row[0][2]:  # We have a country
            xCountry = getCountry(dbConn, row[0][2])
        xTrack = gtClass.Track(
            id=row[0][0], name=row[0][1], countryObj=xCountry)

    else:  # create a blank track object
        logger.debug("no track found")
        xTrack = gtClass.Track(id=0, name=None, countryObj=xCountry)

    logger.debug(f'track = {xTrack}')
    return xTrack


def getTrackList(dbConn):
    """Returns a list of all the tracks and the number of layouts for each track

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
        list: (trackId, trackName, numLayouts)
    """
    logger.info("Getting list of Tracks")
    selectSQL = "SELECT tl.track_id,t.name,count(tl.id) as layouts"
    fromSQL = "FROM track as t LEFT join track_layout as tl ON t.id = tl.track_id GROUP BY tl.track_id"
    orderBySQL = "ORDER BY t.name"
    sql = f"{selectSQL} {fromSQL} {orderBySQL}"
    theVals = ()
    logger.debug(f"sql = {sql}")
    results = directSql(dbConn, sql, theVals)
    logger.info(f"Rows being returned: {len(results)}")
    return results


def getWeather(dbConn, id):
    """Return a Weather object from db by key

    Args:
        dbConn (sqlite3.connect): Database connection
        id (int): Unique weather id.

    Returns:
        Weather object
        if WeatherObject.id == 0 then weather was not found

    """
    logger.info(f"Getting weather object by id: {id}")
    selectSQL = "SELECT id, name FROM weather"
    whereSQL = f"WHERE id = ?"
    theVals = (id,)
    sql = f"{selectSQL} {whereSQL}"
    logger.debug(f"{theVals}")
    logger.debug(f"sql: {sql}")
    row = directSql(dbConn, sql, theVals)
    logger.debug(f"row={row}")
    if row:  # have data from db
        weather = gtClass.Weather(id=row[0][0], name=row[0][1])
    else:  # No data from db. Create empty object
        weather = gtClass.Weather(id=0, name="")
    logger.debug(f'weather = {weather}')
    return weather


def getWeatherList(dbConn):
    """Returns a list of all the the Weather rows

    Args:
        dbConn (sqlite3.connect): Database connection

    Returns:
        list (weatherID, weatherName)
    """
    logger.info("Getting list of weather objects")
    selectSQL = "SELECT id, name FROM weather ORDER by name"
    sql = selectSQL
    logger.debug(f"sql = {sql}")
    theVals = ()
    results = directSql(dbConn, sql, theVals)
    logger.info(f"Rows being returned: {len(results)}")
    return results


def initDB(dbConn, scriptPath=None):
    """Create tables, views, indexes

    Args:
        dbConn (sqlite3.connect): Database connection
        scriptPath (str): path to script files
    """
    logger.info("Database to be initilized")
    logger.debug(f"scriptPath={scriptPath}")
    scripts = ['createTables.sql',
               'LoadLookUpData.sql',
               'LoadOtherData.sql']
    logger.debug(f'scripts to run: {scripts}')
    gtScripts = Path(scriptPath)
    for sFile in scripts:
        scriptFile = gtScripts / sFile
        logger.debug(f"Executing {scriptFile}")
        _exeScriptFile(dbConn, scriptFileName=f'{scriptFile}')
    logger.info("Database init completed")

def updateCarSetting(dbConn,carSetting):
    valResult = validateCarSetting(dbConn,carSetting)
    if not valResult[0]: # is not valid
        logger.warning(valResult[1])
        return (1,valResult[1])

    updateSQL = "UPDATE car_setting"
    setSQL = "SET car_id=:car_id, cat_id=:cat_id, name=:name, max_power=:max_power, max_torque=:max_torque, power_ratio=:power_ratio, traction_control=:traction_control, brake_balance=:brake_balance, top_speed=:top_speed, gear_1=:gear_1, gear_2=:gear_2, gear_3=:gear_3, gear_4=:gear_4, gear_5=:gear_5, gear_6=:gear_6, gear_7=:gear_7, final_gear=:final_gear, weight=:weight, weight_reduction=:weight_reduction, tire_code=:tire_code"

    whereSQL = "WHERE id = :id"

    theVals = {'id': carSetting.id,'car_id': carSetting.car_id,'cat_id': carSetting.cat_id,'name': carSetting.name,'max_power': carSetting.max_power,'max_torque': carSetting.max_torque,'power_ratio': carSetting.power_ratio,'traction_control': carSetting.traction_control,'brake_balance': carSetting.brake_balance,'top_speed': carSetting.top_speed,'gear_1': carSetting.gear_1,'gear_2': carSetting.gear_2,'gear_3': carSetting.gear_3,'gear_4': carSetting.gear_4,'gear_5': carSetting.gear_5,'gear_6': carSetting.gear_6,'gear_7': carSetting.gear_7,'final_gear': carSetting.final_gear,'weight': carSetting.weight,'weight_reduction': carSetting.weight_reduction,'tire_code': carSetting.tire_code}

    sql = f"{updateSQL} {setSQL} {whereSQL}"
    logger.info(f"Updating carSetting {carSetting.id}")
    return _exeDML(dbConn, sql, theVals)


def updateMfg(dbConn, mfgObj):
    """Update a manufacture record in database

    Args:
        dbConn (sqlite3.connect): Database connection
        mfgObj Manufacture object
        - Record that will be UPDATED is based on mfgObj.id.
        WARNING! - Do not change original mfgObj.id. Unexpected results will occur with sqlite

    Returns:
        list: ResultCode, ResultText
                ResultCode == 0: Success execution
                Resultcode != 0: - See ResultText for details
    """
    logger.debug(f"manufacture record update {mfgObj}")
    # Sanity check - does the mfgRecord exist in db?
    logger.debug("sanity check. confirm mfg Record exists.")
    testMfg = getMfg(dbConn, value=mfgObj.id)
    if testMfg.id == 0:  # Mfg is not in database
        result = [1, f"manufacture id {mfgObj.id} not in database."]
        logger.debug(f"returning {result}")
        return result

    logger.debug("sanity check passed. execute SQL")
    theVals = {'mfgID': mfgObj.id, 'mfgName': mfgObj.name,
               'cntryID': mfgObj.country.id}
    sql = "UPDATE manufacture SET name = :mfgName, country_id = :cntryID WHERE id = :mfgID"

    result = _exeDML(dbConn, sql, theVals)
    if result[0] == 0:
        result[1] = f"Manufacture id: {mfgObj.id} Updated"
    else:
        logger.debug(f"problem updating manufacture id: {mfgObj.id}")

    logger.info(f"returning {result}")
    return result


def updateTrack(dbConn, trackObj):
    """update track record

    Args:
        dbConn (sqlite3.connect): Database connection
        trackObj (track Object)

    Returns:
        list: ResultCode, ResultText
              ResultCode 0 = Success
              ResultCode != 0 = see ResultText for details
    """
    logger.debug(f"track record update {trackObj}")
    # Sanity check - See if tracking id exists
    testObj = getTrack(dbConn, value=trackObj.id)
    if testObj.id == 0:  # Not found in db
        return [1, f"track id {trackObj.id} not in database."]

    theVals = {'trackID': trackObj.id, 'trackName': trackObj.name,
               'cntryID': trackObj.country.id}
    sql = "UPDATE track SET name = :trackName, country_id = :cntryID WHERE id = :trackID"

    return _exeDML(dbConn, sql, theVals)


def updateTrackLayout(dbConn, uLayout):
    """Update the track layout record in database

    Args:
        dbConn (sqlite3.connect): Database connection
        uLayout (TrackLayout Object) : Updated TrackLayout Object

    Returns:
        list: ResultCode, ResultText
              ResultCode 0 = Success
              ResultCode != 0 = see ResultText for details
    """
    logger.info(f"Updating Track Layout {uLayout}")

    tResult = validateTrackLayout(dbConn, uLayout)
    if tResult[0]:  # Tests passed
        logger.info("Updating track layout id: {uLayout.id}")
        sql = "UPDATE track_layout SET name = :layoutName, miles = :miles, track_id = :trackId, circuit_id = :circuitId"
        theVals = {'layoutName': uLayout.name, 'miles': uLayout.miles,
                   'circuitId': uLayout.circuit.id, 'trackId': uLayout.track.id}
        logger.debug("sql={sql}")
        logger.debug("theVals = {theVals}")
        result = _exeDML(dbConn, sql, theVals)
    else:
        logger.warning(tResult[1])
        result = (1, tResult[1])

    logger.debug(f"returning: {result}")
    return result


def validateCar(dbConn, car):
    """Validates the car object

    Args:
        dbConn ([type]): [description]
        car ([type]): [description]

    Returns:
        list: (Bool,msg)
        Bool = True/False if passed. If False see msg as to why
        msg = string as to why it failed
    """
    # Model name is unique for the manufacture
    logger.info("Checking for valid model name")
    if car.model:
        # Get a list of all car models for the manufacture
        pass
    else:  # car.model must have a value
        result = (False, f"Model must have a value")
        logger.info(f"{result}")
        return result
    logger.info("Passed: Model name is valid")

    # Validate Manufacture Id
    logger.info("Checking for valid manufacture id")
    if car.manufacture.id == 0:
        result = (
            False, f"Manufacture id {car.manufacture.id} must not be zero")
        logger.info(f"{result}")
        return result
    xObj = getMfg(dbConn, value=car.manufacture.id)
    if xObj.id == 0:
        result = (
            False, f"Manufacture id {car.manufacture.id} not found")
        logger.info(f"{result}")
        return result
    logger.info("Passed: manufacture id valid")

    # driveTrain id exists
    logger.info("Checking for valid drive train id")
    if car.driveTrain.id == 0:
        result = (False, f"Drivetrain id must not be zero")
        logger.info(f"{result}")
        return result
    xObj = getDriveTrain(dbConn, car.driveTrain.id)
    if xObj.id == 0:
        result = (False, f"Drivetrain id {car.driveTrain.id} not found")
        logger.info(f"{result}")
        return result
    logger.info("Passed: drive train id valid")

    # catClass Id exists
    logger.info("Checking for valid Class category id")
    if car.catclass.id == 0:
        result = (False, f"Class category must not be zero")
        logger.info(f"{result}")
        return result
    xObj = getCarCat(dbConn, car.catclass.id)
    if xObj.id == 0:
        result = (False, f"ClassCat id {car.catclass.id} not found")
        logger.info(f"{result}")
        return result

    # Year value can be null/none OR int
    logger.info("Checking to see if year has a valid entry")
    if car.year:
        if type(car.year) != int:
            result = (
                False, f"Invalid year value. Year={car.year}. Must be null or an integer")
            logger.info(f"{result}")
            return result

    return (True, "Car validation passed")


def validateCarSetting(dbConn, custCarSettings):
    """Validates the custom Car Settings objects.

    Args:
        dbConn (sqlite3.connect): Database connection
        custCarSettings (CustCarSettings object): CustCarSettings that are being validated

    Returns:
        list: (True/False, msg)
        True = Tests passed
        False = See msg for what did not pass

    """
    logger.info(f"Validating custom car settings = {custCarSettings.__dict__}")

    # The following tests access db.
    # Last tests as no need to access db if validation fails
    logger.debug("Check car_id exists")
    car = getCar(dbConn, custCarSettings.car_id)
    if car.id == 0:
        result = (
            False, f"Car id does not exist. car_id={custCarSettings.car_id}")
        logger.info(f"{result}")
        return result

    logger.debug("Check cat_id exists")
    carCat = getCarCat(dbConn, custCarSettings.cat_id)
    if carCat.id == 0:
        result = (
            False, f"Category id does not exist. cat_id={custCarSettings.cat_id}")
        logger.info(f"{result}")
        return result

    logger.debug("Check tire_code exists")
    if custCarSettings.tire_code:
        x = getTireList(dbConn)
        found = False
        for chk in x:
            logger.debug(f"{chk[0]}")
            if chk[0].upper() == custCarSettings.tire_code.upper():
                found = True
        if not found:
            result = (
                False, f"Tire code does not exist. tire_code={custCarSettings.tire_code}")
            logger.info(f"{result}")
            return result

    # name must be unique for the car_id
    logger.debug(
        f"Checking name is unique for the car. carid = {custCarSettings.car_id}")
    selectSQL = "SELECT id, name, car_id"
    fromSQL = "FROM car_setting"
    whereSQL = "WHERE car_id=:carID and name=:csName"
    theVals = {'carID': custCarSettings.car_id,
               'csName': custCarSettings.name.strip()}
    sql = f"{selectSQL} {fromSQL} {whereSQL}"
    results = directSql(dbConn, sql, theVals)
    logger.debug(f"results={results}")
    if results:
        logger.debug(
            f"Name is not unique for car. customCarSettingID={results[0][0]}, for carid={results[0][2]}")
        result = (
            False, f"Car setting name already exists for car id {custCarSettings.car_id}")
        logger.info(f"{result}")
        return result

    result = (True, "Tests passed")
    logger.info(f"{result}")
    return result


def validateRace(dbConn, race):
    """Validates the Race rules and returns results

    Args:
        dbConn (sqlite3.connect): Database connection
        race (object): Race object

    Returns:
        list: (bool,msg)
        bool = False  - Race failed tests
        msg = string as to why it failed
    """
    logger.info(f"Validating race={race}")
    # Race name must contain at least one charcter
    logger.debug(
        f"Checking race name to be sure it contains at lease one character")
    if not race.name:
        msg = f"Race name must contain at least one character"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Race name contains one or more characters")

    # Race name must be unique for the race_collection
    logger.debug(
        f"Checking that race name [{race.name}] is unique for race collection id {race.raceCollection.id} (case insensitve)")
    xList = getRaceList(dbConn, race.raceCollection.id)
    for row in xList:
        logger.debug(f"raceId={row[0]}. checking race name: {row[1]}")
        if row[1].upper() == race.name.upper():  # layout name exist for track
            msg = f"Race name [{race.name}] for race collection id {race.raceCollection.id} already exists. The race name must be unique."
            result = (False, msg)
            logger.info(f"returning = {result}")
            return result
    logger.info(
        f"Passed: Race name is unique for race collection id {race.raceCollection.id}")

    # Weather ID must not be zero
    logger.debug(f"Checking for valid weather id")
    if race.weather.id == 0:  # Invalid Weather id
        msg = f"Race weather id must not be 0"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Weather id is greater than zero")

    # Does weather id exist
    if getWeather(dbConn, race.weather.id).id != race.weather.id:
        msg = f"The Race weather id : {race.weather.id} not found in database"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Weather id found in database")

    # TrackLayout id must not be zero
    logger.debug(f"Checking for valid Track Layout")
    if race.trackLayout.id == 0:
        msg = f"Race Track Layout id must not be 0"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Race Track layout id is greater than zero")

    # TrackLayout must exist
    if getLayout(dbConn, race.trackLayout.id).id == 0:
        msg = f"The Race track layout not found in database"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Race Track layout id found in database")

    # Race type required.
    logger.debug(f"Checking for valid racetype id")
    if race.raceType.id == 0:
        msg = f"Race type for race must not be 0"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Race type id is not 0")
    # Race type must exist
    x = getRaceTypeList(dbConn)
    logger.debug(f"RaceType List = {x}")
    logger.debug(f"race.raceType.id={race.raceType.id}")
    passed = False
    for r in x:
        if r[0] == race.raceType.id:  # Found the raceType id
            passed = True
            break
    if passed:
        logger.info("Passed. Race type found")
    else:
        msg = f"Race type for race not found in database"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result

    # Race Collection testing
    logger.debug(f"Checking for valid race collection")
    logger.debug(f"race.raceCollection.id={race.raceCollection.id}")
    # Race Collection id must not be zero
    if race.raceCollection.id == 0:
        msg = f"The race collection id for the race must not be zero"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Race collection id is not 0")

    # Race collection id must exist
    if getRaceCollection(dbConn, race.raceCollection.id).id == 0:
        msg = f"The Race collection not found in database"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result
    else:
        logger.info("Passed: Race collection found")

    msg = "Race passed tests"
    result = (True, msg)
    logger.info(f"returning = {result}")
    return result


def validateTrackLayout(dbConn, trackLayout):
    """Validates TrackLayout rules and returns results

    Args:
        dbConn (sqlite3.connect): Database connection
        trackLayout (TrackLayout object): Track Layout that is being validated

    Returns:
        list: (True/False, msg)
        True = Tests passed
        False = See msg for what did not pass
    """
    logger.debug(f"trackLayout={trackLayout}")
    # Layout name must contain at least one charcter
    logger.info(
        f"Checking layout name contains at lease one character")
    if trackLayout.name == None or trackLayout.name == "":
        msg = f"Track Layout name must contain at least one character"
        result = (False, msg)
        logger.info(f"returning = {result}")
        return result

    # Layout name must be unique for the Track
    logger.info(
        f"Checking if layout [{trackLayout.name}] already exists for track (case insensitve)")
    layoutList = getLayoutList(dbConn, trackLayout.track.id)
    for row in layoutList:
        logger.debug(f"tlayoutId={row[0]}. checking layout name: {row[1]}")
        if row[1].upper() == trackLayout.name.upper():  # layout name exist for track
            msg = f"Layout name [{trackLayout.name}] for Trackid [{trackLayout.track.id}] already exists"
            result = (False, msg)
            logger.info(f"returning = {result}")
            return result

    # Miles is not a string. (Null is allowed in this test)
    logger.info(f"Checking miles [{trackLayout.miles}] is not a string")
    if isinstance(trackLayout.miles, str):  # miles is a string
        result = (False, f"Miles must not contain letters")
        logger.info(f"returning = {result}")
        return result
    # Miles is not null. not tested. DB should provide integrity error: NOT NULL constraint failed
    # Circuit ID existance not tested. DB should provide integrity error: FOREIGN KEY constraint failed
    # Track ID existance not tested. DB should provide integrity error: FOREIGN KEY constraint failed
    # All tests passed
    result = (True, "Track Layout Tests Passed")
    logger.info(f"returning = {result}")
    return result


def directSql(dbConn, sql, theVals):
    """Execute hand crafted sql.

    Args:
        dbConn (sqlite3.connect): Database connection
        sql (str): SQL to run
        theVals (list,dict): Values to be sanitized

    Returns:
        list: results for the SQL
    """
    logger.debug(f"DIRECTsql = {sql}")
    logger.debug(f"DIRECTVals = {theVals}")

    # Enabling full sql traceback to logger.debug
    dbConn.set_trace_callback(logger.debug)
    try:
        cur = dbConn.cursor()
        cur.execute(sql, theVals)
        result = cur.fetchall()
    except:
        logger.critical(
            f'Unexpected error executing sql: {sql}', exc_info=True)
        sys.exit(1)
    # Disable full sql traceback to logger.debug
    dbConn.set_trace_callback(None)

    logger.info(f"Returning {len(result)} rows")
    return result
