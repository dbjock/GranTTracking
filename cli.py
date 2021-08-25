# PURPOSE: CLI to test getting data out of db. Future cli maybe.
#    GTTracking db library
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import html
from pathlib import Path
from datetime import datetime

# Addtional external libs
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.validation import Validator
from prompt_toolkit.completion import NestedCompleter, WordCompleter
from prompt_toolkit.shortcuts import radiolist_dialog, input_dialog

# App specific required
from GranT import gtdbV3 as gtdb
from GranT import GTClasses as GT
from GranT import gtcfg

# _gtPath = Path.cwd()
# _gtScripts = _gtPath / 'Scripts'
gtcfg.curcfg['gtPath'] = Path.cwd()
gtcfg.curcfg['gtScripts'] = gtcfg.curcfg['gtPath'] / 'Scripts'
gtcfg.curcfg['layoutUpdated'] = True
gtcfg.curcfg['version'] = '1.alpha'
# Log Formatters
smlFMT = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s')
extFMT = logging.Formatter(
    '%(asctime)s %(levelname)-8s:%(name)s.%(funcName)s: %(message)s')
# Log Handlers
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.CRITICAL)
console.setFormatter(smlFMT)
# Initilizing logging (This is the root logger now)
log = logging.getLogger('')
log.setLevel(logging.DEBUG)
log.addHandler(console)
# create log folder if it does not exists
Path(gtcfg.logcfg['logDir']).mkdir(parents=True, exist_ok=True)

logFile = Path(gtcfg.logcfg['logDir']) / 'cli.log'

log_fh = RotatingFileHandler(
    logFile, mode='a', maxBytes=1048576, backupCount=2)
extFMT = logging.Formatter(
    '%(asctime)s %(levelname)-8s:%(name)s.%(funcName)s: %(message)s')
log_fh.setFormatter(extFMT)
log_fh.setLevel(logging.DEBUG)
# Add logging filehander log_fh to the logger
log.addHandler(log_fh)
linePrmpt = '  system> '
print(f"{linePrmpt} Logging to: {logFile}")
log.info(f"CLI app version : {gtcfg.curcfg['version']} starting")
# create Path to database if it does not exists
Path(Path(gtcfg.dbcfg['dbFile']).parent).mkdir(parents=True, exist_ok=True)
print(f"{linePrmpt} Database  : {gtcfg.dbcfg['dbFile']}")
if not Path(gtcfg.dbcfg['dbFile']).exists():
    newDB = True
    log.info(f"Db file not found: newDB={newDB}")
else:
    newDB = False
    log.info(f"Db found: newDB={newDB}")

# sqlite will create a database file if it does not exist.
dbC1 = gtdb.create_connection(gtcfg.dbcfg['dbFile'])

if newDB:
    log.info(f"Initializing new database: {gtcfg.dbcfg['dbFile']}")
    print(f"{linePrmpt} Initializing new database")
    gtdb.initDB(dbC1, scriptPath=gtcfg.curcfg['gtScripts'])
    log.info(f"Creating User Tables")
    gtdb._exeScriptFile(
        dbC1, scriptFileName=gtcfg.curcfg['gtScripts'] / 'createUserTables.sql')


def _sortTuple(tup, key):
    """Returns a tuple sorted by the key

    Args:
        tup (tuple list): example [(1,"zzd"),(3,"azd")]
        key (int): The key/index to sort.
            example: 1 for results: [(3,"azd"),(1,"zzd")]
    """
    return(sorted(tup, key=lambda x: x[key]))


def _isNum(text):
    """Used for validation to ensure numbers are provided"""
    return text.isdigit()


def _isNumOrNull(text):
    if len(text) == 0:
        return True

    return text.isdigit()


def _YorN(text):
    for validChar in ['Y', 'N']:
        if text.upper() == validChar:
            return True

    return False


def _valTime(text):
    """Used to validate if text is time"""
    timeformat = "%H:%M"
    try:
        validtime = datetime.strptime(text, timeformat)
        return True
    except ValueError:
        return False


def dbInit():
    "Database initization"
    x = f'<ansired><b>WARNING!! All Data in db will be erased</b></ansired>'
    print_formatted_text(HTML(x))
    usrText = prompt("  Confirm by typing YES >>>> ")
    if usrText == None or usrText != "YES":  # Not confirmed
        log.info("db init not confirmed")
        print("db init not confirmed. Canceled")
    else:
        log.warning("db init confirmed")
        x = f'<ansired><b>Database being initiliazed</b></ansired>'
        print_formatted_text(HTML(x))
        gtdb.initDB(dbC1, scriptPath=gtcfg.curcfg['gtScripts'])

        x = f'<ansired><b>Database initilization complete</b></ansired>'
        print_formatted_text(HTML(x))


def main():
    print("enter Exit or Help for more info")
    cmdHelper = {
        'help': {
            'exit': None,
            'list': None,
            'tracks': None,
            'dbinit': None
        },
        'add': {
            'car': {'mfgid=': None},
            'collection': {'leagueId=': None},
            'race': {'collectionId=': None}
        },
        'list': {
            'circuits': None,
            'classes': None,
            'collection': {
                'leagueId=': None,
                'id=': None
            },
            'drivetrains': None,
            'manufactures': {'orderBy=': None},
            'race': {
                'id=': None
            },
            'track': {
                'id=': None,
                'name=': None,
                'layoutId=': None
            },
            'tracks': None,
        },
        'exit': None,
    }
    completer = NestedCompleter.from_nested_dict(cmdHelper)

    session = PromptSession()

    while True:
        try:
            userCmd = session.prompt(
                '  GranTT > ', completer=completer, complete_while_typing=True)
        except KeyboardInterrupt:
            log.info("Keyboard Interrupt. Exiting Application")
            break
        except EOFError:  # No sure why this is here
            log.info("EOFError. Exiting application")
            break
        else:  # Checking for valid actions
            log.info(f"Command: {userCmd}")
            try:  # User entered a command
                action = userCmd.split()[0]
            except IndexError:
                break
            log.debug(f"action={action}")
            if action == 'help':
                if userCmd.find(' ') != -1:
                    objCmd = userCmd[userCmd.find(' '):]
                    helpAction(objCmd.strip())
                else:
                    log.info("help command not complete")
                    print(" Please provde which command you want help for.")
            elif action == 'add':
                if userCmd.find(' ') != -1:
                    objCmd = userCmd[userCmd.find(' '):]
                    addAction(objCmd)
                else:
                    log.info("add command not complete")
                    print("Please provde an object for the add command.")
            elif action == 'cls' or action == 'clear':
                cls()
            elif action == 'list':
                if userCmd.find(' ') != -1:
                    objCmd = userCmd[userCmd.find(' '):]
                    listAction(objCmd)
                else:
                    log.info("list command not complete")
                    print("Please provide an object for the list command")
            elif action == 'exit':
                log.info("Exiting application")
                break
            elif action == 'dbinit':
                dbInit()
            else:
                log.info('Unknown command Please enter a command')
                print_formatted_text(
                    HTML(f'Unknown command Please enter a command'))

    print('GoodBye!')


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def addAction(cmd):
    """Add Action.
    This will make sure
    - the objected being listed is valid
    - and have that objected listed.

    Args:
        cmd ([string]): The object and its args
    """
    cmd = cmd.strip()
    obj = cmd.split()[0]
    log.debug(f"obj={obj}")
    if obj == "collection":
        addCollectionCmd(cmd[len(obj):].strip())
    elif obj == "race":
        addRaceCmd(cmd[len(obj):].strip())
    elif obj == "car":
        addCarCmd(cmd[len(obj):].strip())
    elif obj == "carSettings":
        pass
    else:  # Unknown object
        print_formatted_text(
            HTML(f'<ansired>ERROR</ansired> - Unknown <ansigreen>add</ansigreen> object <b>{obj}</b>'))
        log.info("Unknown object for add action")


def addCarCmd(args):
    """Add car to database.

    Args:
        args (str): All the args passed from the command
    """
    log.debug(f"args passed: {args}")
    mfgId = None
    classId = None
    driveTrainId = None
    for setting in args.split():
        if setting.split("=")[0].upper() == 'MFGID':
            mfgId = setting.split("=")[1]
        elif setting.split("=")[0].upper() == 'CLASSID':
            classId = setting.split("=")[1]
        elif setting.split("=")[0].upper() == 'DRIVETRAINID':
            driveTrainId = setting.split("=")[1]

    log.debug(f"mfgId={mfgId} classId={classId} driveTrainId={driveTrainId}")

    if mfgId:
        log.info(f"Validating mfgId {mfgId}")
        mfg = gtdb.getMfg(dbC1, key='mfgId', value=mfgId)
        if mfg.id == 0:  # mfg not found
            log.info(f"mfgId={mfgId} no found. Prompt user for manufacture")
            mfgId = pickMfg(
                text='Invalid mfgId provided. Please select a manufacture for the new car')
            if mfgId == None:  # no mfg picked
                log.info("No manufacture picked")
                print("No manufacture provided")
                return
            else:  # mfg picked
                log.info(f"Loading manufacture object mfgId={mfgId}")
                mfg = gtdb.getMfg(dbC1, key='mfgId', value=mfgId)
        else:  # mfg validated
            log.info(f"mfgId {mfgId} validated and loaded")
    else:  # Prompt user for Mfg
        log.info(f"mfgId not provided. Prompt user for manufacture")
        mfgId = pickMfg(text='Please select a manufacture for the new car')
        if mfgId == None:  # no mfg picked
            log.info("No manufacture picked")
            return
        else:  # mfg picked
            log.info(f"Loading manufacture object mfgId={mfgId}")
            mfg = gtdb.getMfg(dbC1, key='mfgId', value=mfgId)

    if classId:
        log.info(f"Validating classId {classId}")
        carClass = gtdb.getCarCat(dbC1, classId)
        if carClass.id == 0:  # carClass not found
            log.info(
                f"classId={classId} not found. Prompt user for class/category")
            classId = pickCarCategory(
                text='Invalid classId provided. Please select a car class category for the new car')
            if classId == None:  # no carClass picked
                log.info("No class/category picked")
                return
            else:  # carClass picked
                log.info(f"Loading class/category object classId={classId}")
                carClass = gtdb.getCarCat(dbC1, classId)
        else:  # carClass validated
            log.info(f"classId {classId} validated and loaded")
    else:  # Prompt user for carClass
        log.info(f"classId not provided. Prompt user for class/category")
        classId = pickCarCategory(
            text='Please select a car class category for the new car')
        if classId == None:  # no carClass picked
            log.info("No class/category picked")
            return
        else:  # carClass picked
            log.info(f"Loading class/category object classId={classId}")
            carClass = gtdb.getCarCat(dbC1, classId)

    if driveTrainId:
        log.info(f"Validating driveTrainId {driveTrainId}")
        driveTrain = gtdb.getDriveTrain(dbC1, driveTrainId)
        if driveTrain.id == 0:  # Drivetrain not found
            log.info(
                f"driveTrainId={driveTrainId} not found. Prompt user for a drivetrain")
            driveTrainId = pickDriveTrain(
                text="Invalid driveTrainID provided. Please select a drivetrain for the new car")
            if driveTrainId:  # User choose
                driveTrain = gtdb.getDriveTrain(dbC1, driveTrainId)
                log.info(
                    f"Loading drivetrain object driveTrainId={driveTrainId} ")
                driveTrain = gtdb.getDriveTrain(dbC1, driveTrainId)
            else:  # Bail out
                log.info(f"No drivetrainId provided")
                print(f"No drivetrain selected")
                return
    else:  # get drivetrainid from user prompt
        log.info(f"driveTrainID not provided. Prompt user for driveTrainID ")
        driveTrainId = pickDriveTrain(
            text="Select a drivetrain for the new car")
        if driveTrainId:  # User provided choice
            driveTrain = gtdb.getDriveTrain(dbC1, driveTrainId)
            log.info(f"Loading drivetrain object driveTrainId={driveTrainId} ")
            driveTrain = gtdb.getDriveTrain(dbC1, driveTrainId)
        else:  # Bail out
            log.info(f"No drivetrainId provided")
            print(f"No drivetrain selected")
            return

    # Display new car info user select
    cls()
    print_formatted_text(HTML(f"<b>Adding a car to the garage</b>"))
    displayCarMfg(mfg.id)

    # Display command to use if adding another
    print_formatted_text(HTML(
        f"   >> add car mfgId={mfg.id} classId={carClass.id} driveTrainId={driveTrain.id}"))

    print()
    print_formatted_text(HTML(
        f"      Class: <ansigreen>{html.escape(carClass.name)}</ansigreen>"))
    print_formatted_text(HTML(
        f"Drive Train: <ansigreen>{html.escape(driveTrain.code)} - {html.escape(driveTrain.desc)}</ansigreen>"))

    # Now to get the user typed in details
    validator = Validator.from_callable(_isNumOrNull,
                                        error_message='Input must be a number or blank',
                                        move_cursor_to_end=True)

    enterYear = prompt("  Model Year > ", validator=validator)
    if enterYear:
        enterYear = int(enterYear)

    log.info(f"User enter {enterYear} for year")
    enterName = prompt("  Model Name > ")
    log.info(f"User enter {enterName} for name")

    # Prompt if car is to be saved
    validator = Validator.from_callable(_YorN,
                                        error_message='Y or N',
                                        move_cursor_to_end=True)
    xTmp = prompt("Do you wish to save this car? (Y or N) > ",
                  validator=validator)
    if xTmp.upper() == "N":
        log.info("User does not want to save car")
        print("Car will not be saved")
    elif xTmp.upper() == "Y":
        # Attempting to save car
        car = GT.Car(id=0, model=enterName, Manufacture=mfg,
                     DriveTrain=driveTrain, ClassCat=carClass)
        car.year = enterYear
        log.info(f"car={car}")
        result = gtdb.addCar(dbC1, car)
        if result[0] == 0:
            x = f'  <ansigreen>Car added to garage</ansigreen>'
            print_formatted_text(HTML(x))
            log.info(f"Car added to garage")
            # TODO: Display the cars by mfg
            displayCarMfg(mfg.id)
        else:
            x = f'  <ansired>Unable to add car to garage. Return Code: {result[0]} Desc: {result[1]}</ansired>'
            print_formatted_text(HTML(x))
            log.info(
                f"Unable to add car to garage. Return Code: {result[0]} Desc: {result[1]}")


def addCollection(leagueId):
    """Add a race collection dialog with user

    Args:
        leagueId (int): The league ID to add the race collection to

    Returns:
        list: (ResultCode,ResultDesc)
        if ResultCode !=0 then not successfull. See ResultDesc
    """

    log.info(f"getting league object for league id {leagueId}")
    league = gtdb.getLeague(dbC1, value=leagueId)
    if league.id == 0:  # League was not found
        log.warning("League not found in database")
        return [1, "League not found"]

    log.info("Getting race collection name from user")
    print_formatted_text(
        HTML(f"Enter new race collection for the <u><b>{league.name}</b></u> league"))
    rcName = prompt("   Collection Name (Enter to cancel): ")
    log.debug(f"rcName={rcName}")
    if rcName == None or rcName == "":  # User didn't provide data
        log.info("User did not provide race collection name")
        return [1, "Race collection name not provided."]

    # Validate the race collection name
    log.info(f"Checking if League already has race name: '{rcName}'")
    rcList = gtdb.getRaceCollectionList(dbC1, league.id)
    for r in rcList:
        log.debug(
            f"checking userEntry.upper {rcName.upper()} to list {r[1].upper()}")
        if rcName.upper() == r[1].upper():
            log.warning(f"Race collection name already exists for league.")
            return [1, "Race collection name already exists for this League."]

    # Get description info from user
    log.info("Getting race collection desc from user")
    rcDesc = prompt(
        f"   Description: ")

    rCollection = GT.RaceCollection(
        id=0, name=rcName, desc=rcDesc, leagueObj=league)

    # What car class category is this restricted to
    log.info("Getting car class category")
    rCollection.classcat.id = pickCarCategory(
        text="Which car class category is this restricted to?")
    if rCollection.classcat.id:  # A car class has been selected
        selCarClass = gtdb.getCarCat(dbC1, rCollection.classcat.id)
        xTmp = f"{selCarClass.name} {selCarClass.desc}"
    else:  # No car class selected
        xTmp = f" "
    x = f"   Car Class Category: {xTmp.ljust(50)}"
    print_formatted_text(HTML(x))

    log.info(f"User picked car Cat id {rCollection.classcat.id}")

    # Prize info
    numCheck = Validator.from_callable(_isNum,
                                       error_message='This input contains non-numeric characters',
                                       move_cursor_to_end=True)
    log.info(f"Getting prize info from user")
    rCollection.prize1 = prompt(
        f"   1st Prize: ", validator=numCheck)
    rCollection.prize2 = prompt(
        f"   2nd Prize: ", validator=numCheck)
    rCollection.prize3 = prompt(
        f"   3rd Prize: ", validator=numCheck)
    # Save object to database
    log.debug(f"Saving {rCollection}")
    r = gtdb.addRaceCollection(dbC1, rCollection)
    log.debug(f'result from adding racecollection: {r}')
    return r


def addCollectionCmd(args):
    """What to do when asked to add a collection"""
    log.debug(f"args passed: {args}")
    if len(args) > 0 and args.find("=") > 0:  # Have valid args
        if args.split('=')[0].strip() == 'leagueId':
            id = args.split('=')[1].strip()
        else:  # Unknown args passed
            log.info(
                f"Unknown add collection argument {args.split('=')[0].strip()}")
            print_formatted_text(
                HTML(f"<ansired>ERROR</ansired> - Unknown add collection argument <b>{args.split('=')[0].strip()}</b>."))
            return
    else:  # Get user to choose a league
        log.info("No args passed. Getting user to select a league")
        id = pickLeague(text="Add a race collection to which league?")
        log.info(f"User picked league id {id}")
        if id == None:  # No League picked
            log.info("No league select. Cancel add collection")
            print("Canceled add collection")
            return
        log.info(
            f"Get user input for adding a race collection to league id = {id}")

    # Now ask all the questions to the user
    r = addCollection(id)
    if r[0] != 0:  # Save was not successful
        x = f'  <ansired>Unable to add Race Collection. Return Code: {r[0]} Desc: {r[1]}</ansired>'
        print_formatted_text(HTML(x))
        log.info(
            f"Unable to add Race Collection. Return Code: {r[0]} Desc: {r[1]}")
        return
    else:  # Race collection added
        x = f'  <ansigreen>Race Collection Added</ansigreen>'
        print_formatted_text(HTML(x))
        log.info(f"Race Collection Added")


def addRaceCmd(args):
    """Check and see what args have been passed before
    before drilling down on the questions to ask to add a Race"""
    log.debug(f"args passed: {args}")
    log.debug(f"length of args: {len(args)}")
    collectionId = None
    layoutId = None
    weatherId = None
    raceTypeId = None
    for setting in args.split():
        if setting.split("=")[0].upper() == 'COLLECTIONID':
            collectionId = setting.split("=")[1]
        elif setting.split("=")[0].upper() == 'LAYOUTID':
            layoutId = setting.split("=")[1]
        elif setting.split("=")[0].upper() == 'WEATHERID':
            weatherId = setting.split("=")[1]
        elif setting.split("=")[0].upper() == 'RACETYPEID':
            raceTypeId = setting.split("=")[1]

    log.debug(
        f"collectionId={collectionId}: layoutId={layoutId}: weatherId={weatherId}: raceTypeId={raceTypeId}")

    if collectionId:
        log.info(f"Validating collectionId {collectionId}")
        rcCollection = gtdb.getRaceCollection(dbC1, collectionId)
        if rcCollection.id == 0:  # Race Collection not found
            log.info(
                f"collectionId:{collectionId} was not found. Prompt user to get.")
            x = pickLeague(
                text=f"The collectionId {collectionId} was not found. Please select a League")
            if x == None:  # no league picked
                log.info("No league selected")
                print("Unable to get a collectionId for the new race")
                return
            else:  # League picked. Get collectionId for the league from user.
                log.info(f"Loading league object for leagueid={x}")
                league = gtdb.getLeague(dbC1, value=x)
                # Prompt user to select collection from the league
                log.info("Prompting user for race collection id")
                collectionId = pickRaceCollection(
                    league.id, league.name, text=f"Which race collection for the new race?")
                if collectionId == None:  # no race collection selected
                    log.info(
                        f"No race collection selected for leagueId={league.id}")
                    print("Unable to get a collectionId for the new race")
                    return
        else:  # Race Collection found
            pass
    else:  # Need to get info from user
        log.info(f"No collectionId provided. Prompting user to get the id")
        x = pickLeague(
            text="No collectionId was provided. Please select a League")
        if x == None:  # no leauge picked
            log.info("No league selected.")
            print("Unable to get a collection id for the new race")
            return
        else:  # Get collectionId for the league from user.
            log.info(f"Loading league object for leagueid={x}")
            league = gtdb.getLeague(dbC1, value=x)
            # Prompt user to select collection from the league
            log.info("Prompting user for race collection id")
            collectionId = pickRaceCollection(
                league.id, league.name, text=f"Which race collection for the new race?")
            if collectionId == None:  # no race collection selected
                log.info(
                    f"No race collection was selected for league ({league.id}) {league.name}")
                print("Unable to get a collection id for the new race")
                return

    if layoutId:
        log.info(f"Validating layoutId {layoutId}")
        tLayout = gtdb.getLayout(dbC1, layoutId)
        if tLayout.id == 0:  # TrackLayout not found
            log.info(f"layoutId:{layoutId} was not found. Prompt user for it")
            # Prompt user for Track
            x = pickTrack(
                text=f"The layoutId {layoutId} was not found. Please select a Track")
            if x == None:  # no track was selected
                log.info("No track selected")
                print(f"Unable to get a layoutId for new race")
                return
            else:  # Track was selected. Get layout from user.
                log.info(f"Loading track object for trackId={x}")
                track = gtdb.getTrack(dbC1, value=x)
                log.info(f"Prompting user for layout id")
                layoutId = pickTrackLayout(track.id, track.name,
                                           text=f'Which layout for the new race?')
                if layoutId == None:  # no layout was selected
                    log.info(f"No layout selected for trackId {track.id}")
                    print(f"Unable to get a layoutId for new race")
                    return
        else:  # TrackLayout found
            pass
    else:  # Need to get info from user
        log.info(f"No layoutId provided. Prompting user to get it.")
        x = pickTrack(text=f"No layoutId was provided. Please select a Track")
        if x == None:  # no track selected
            log.info("No track selected.")
            print("Unable to get a layoutId for new race")
            return
        else:  # Track selected. Get layout from user
            log.info(f"Loading track object for trackId={x}")
            track = gtdb.getTrack(dbC1, value=x)
            log.info(f"Prompting user for layout id")
            layoutId = pickTrackLayout(track.id, track.name,
                                       text=f'Which layout for the new race?')
            if layoutId == None:  # no layout was selected
                log.info(f"No layout selected for trackId {track.id}")
                print(f"Unable to get a layoutId for new race")
                return

    if weatherId:
        log.info(f"Validating weatherId {weatherId}")
        weather = gtdb.getWeather(dbC1, weatherId)
        if weather.id == 0:  # Not found, get info from user
            log.info(
                f"weatherId:{weatherId} was not found. Prompt user for it")
            weatherId = pickWeather(
                text=f"The weatherId {weatherId} was not found. Please select Weather")
            if weatherId == None:  # User not choose weather
                log.info(f"No weather selected")
                print(f"Unable to get a weatherId for new race")
                return
    else:  # Need to get info from user
        log.info(
            f"weatherId:{weatherId} not provided. Prompting user for it")
        weatherId = pickWeather(
            text=f"No weatherId provided. Please select Weather")
        if weatherId == None:  # User not choose weather
            log.info(f"No weather selected")
            print(f"Unable to get a weatherId for new race")
            return

    if raceTypeId:
        log.info(f"Validating raceTypeId {raceTypeId}")
        raceType = gtdb.getRaceType(dbC1, raceTypeId)
        if raceType.id == 0:  # Not found. Prompt user for info
            log.info(
                f"raceTypeId: {raceTypeId} was not found. Prompt user for it")
            raceTypeId = pickRaceType(
                text=f"The raceTypeId {raceTypeId} was not found. Please select a race type")
            if raceTypeId == None:  # User didn't choose
                log.info(f"No race type selected")
                print(f"Unable to get a raceTypeId for new race")
                return
        else:  # Good
            pass
    else:  # Need to get info from user
        log.info(
            f"raceTypeId: {raceTypeId} not provided. Prompt user for it")
        raceTypeId = pickRaceType(
            text=f"No raceTypeId was provided. Please select a race type")
        if raceTypeId == None:  # User didn't choose
            log.info(f"No race type selected")
            print(f"Unable to get a raceTypeId for new race")
            return

    # Getting required objects from database
    log.info("Getting race collection object from database")
    rcCollection = gtdb.getRaceCollection(dbC1, collectionId)
    log.info("Getting track layout object from database")
    tLayout = gtdb.getLayout(dbC1, layoutId)
    log.info("Getting weather object from database")
    weather = gtdb.getWeather(dbC1, weatherId)
    log.info("Getting weather object from database")
    raceType = gtdb.getRaceType(dbC1, raceTypeId)

    # Display what user selected
    cls()
    print("Adding a Race")

    displayCollection(rcCollection)
    # Display track layout
    htmltrackNlayout = html.escape(
        f"{tLayout.track.name} ({tLayout.track.id}) : {tLayout.name} ({tLayout.id})")
    htmlLine = f"Track and Layout: <ansigreen>{htmltrackNlayout}</ansigreen>"
    print_formatted_text(HTML(htmlLine))
    # Display Weather and race type
    htmlLine = f"Weather: <ansigreen>{weather.name}</ansigreen> Race type: <ansigreen>{raceType.name}</ansigreen>"
    print_formatted_text(HTML(htmlLine))
    htmlLine = f" >> add race collectionId={rcCollection.id} layoutId={tLayout.id} weatherId={weather.id} raceTypeId={raceType.id}"
    print_formatted_text(HTML(htmlLine))

    # Prompt user for Race Number
    log.info("Getting race number from user")
    numCheck = Validator.from_callable(_isNum,
                                       error_message='This input contains non-numeric characters',
                                       move_cursor_to_end=True)
    raceNum = prompt("  Race number for this collection >> ",
                     validator=numCheck)
    log.debug(f"raceNum={raceNum}")
    if int(raceNum) == 0:  # User didn't provide data
        log.info("User did not provide a race number")
        print("Invalid race number provided")
        return
    # Now have all the required data to create the Race Object
    name = f"Race {raceNum}"
    xRace = GT.Race(id=0, name=name, trackLayout=tLayout,
                    raceCollection=rcCollection, raceType=raceType, weather=weather)

    # Prompt user for Race time
    log.info("Getting Race time from user")
    validator = Validator.from_callable(
        _valTime, error_message='Not a valid time format', move_cursor_to_end=True)
    raceTime = prompt(f"   Time of Day for race (HH:MM) >> ",
                      validator=validator)
    log.debug(f"raceTime={raceTime}")
    xRace.racetime = raceTime

    # Prompt user for limits i.e. lap/max time restrictions
    log.info("Getting lap/max time limits from user")
    xRace.limits = prompt(f"    Limits >> ")
    log.debug(f"limits={xRace.limits}")

    # Prompt user for any notes about race
    log.info("Getting notes about race from user")
    xRace.notes = prompt(f"    Notes >> ")
    log.debug(f"notes={xRace.notes}")

    # Saving race object to database
    log.info(f"Saving: {xRace}")
    result = gtdb.addRace(dbC1, xRace)
    if result[0] != 0:  # Save was not successful
        log.info(
            f"Unable to add Race. Return Code: {result[0]} Desc: {result[1]}")
        htmlLine = f'  <b><ansired>Unable to add Race. Return Code: {result[0]} Desc: {result[1]}</ansired></b>'
        print_formatted_text(HTML(htmlLine))
    else:
        log.info(f"Race added")
        htmlLine = f'  <ansigreen>Race Added</ansigreen>'
        displayCollection(rcCollection)

    return


def displayCarMfg(mfgId):
    """Display all cars in garage for mfgId

    Args:
        mfgId (int): Manufacture ID
    """
    mfg = gtdb.getMfg(dbC1, key='mfgId', value=mfgId)
    print_formatted_text(HTML(
        f"Cars in your garage for manufacture: <ansigreen>{html.escape(mfg.name)}</ansigreen>"))
    print()

    # header line
    carId = f' ID'
    modName = f'Model Name'.ljust(60)
    mYear = f'Year'.ljust(4)
    carClassN = f'Class'.ljust(6)
    mDT = f'Drive'

    print(
        f" {carId} | {modName} | {mYear} | {carClassN} | {mDT}")
    print("-" * 104)  # header seperator
    # Getting and display cars
    selectSQL = "SELECT car.id, model, year, cat.name as class, dt.code"
    fromSQL = "FROM car JOIN drivetrain AS dt ON car.drivetrain_id = dt.id JOIN category as cat on car.cat_id = cat.id"
    whereSQL = "WHERE mfg_id = :mfgID"
    orderBy = "ORDER BY model"
    sql = f"{selectSQL} {fromSQL} {whereSQL} {orderBy}"
    vals = {'mfgID': mfgId}
    results = gtdb.directSql(dbC1, sql, vals)
    for row in results:
        carId = f"{row[0]:d}".rjust(3)
        modName = html.escape(row[1].ljust(60))
        if row[2]:  # year as a value
            mYear = f"{row[2]:d}".rjust(4)
        else:  # year has no value
            mYear = "    "
        carClassN = html.escape(row[3].ljust(6))
        mDT = html.escape(row[4].ljust(4))

        htmlText = f" <ansigreen>{carId}</ansigreen> | <ansigreen>{modName}</ansigreen> | <ansigreen>{mYear}</ansigreen> | <ansigreen>{carClassN}</ansigreen> | <ansigreen>{mDT}</ansigreen>"
        print_formatted_text(HTML(htmlText))
    print("-" * 104)  # header seperator


def displayCarCats(theList):
    """Display all the Car Categories/Classes"""
    for r in theList:
        print(r)


def displayCircuits(theList):
    """Display all the circuits"""
    print(f"Number of circuits: {len(theList)}")
    print(f"  ID  | Circuit")
    print("-" * 78)  # header seperator

    for r in theList:
        # {r[0]:>4} -- This means the value of r[0] will be right justified with 4 spaces
        print(f" {r[0]:>4} | {r[1][0:30].ljust(30)}")

    print("=" * 78)


def displayCollection(raceColObj):
    """Display race info for a race collection

    Args:
        raceColObj : Race Collection object
    """
    # League and collection info
    log.info(f"Displaying information for race collection id {raceColObj.id}")
    htmlLeague = html.escape(
        f'{raceColObj.league.name}')
    htmlCollection = html.escape(
        f"{raceColObj.name}")
    print_formatted_text(HTML(
        f"League     : <ansigreen>{htmlLeague} ({raceColObj.league.id})</ansigreen>  Collection: <ansigreen>{htmlCollection} ({raceColObj.id})</ansigreen> "))
    # Race collection description
    htmlText = f"Description : <ansigreen>{html.escape(raceColObj.desc)}</ansigreen>"
    print_formatted_text(HTML(htmlText))
    # Prizes and Class
    prize1 = f"{raceColObj.prize1:,d}"[0:7].ljust(7)
    prize2 = f"{raceColObj.prize2:,d}"[0:7].ljust(7)
    prize3 = f"{raceColObj.prize3:,d}"[0:7].ljust(7)
    htmlText = f" Class : <ansigreen>{raceColObj.classcat.name}</ansigreen>  1st: <ansigreen>{prize1}</ansigreen> 2nd: <ansigreen>{prize2}</ansigreen> 3rd: <ansigreen>{prize3}</ansigreen>"
    print_formatted_text(HTML(htmlText))

    print("\nRaces:")
    id = f"ID".rjust(3)
    rName = "Name".ljust(7)
    trackNlayout = "Track (id): Layout (id)"
    limits = f"Limit".ljust(11)
    startTime = "Start"
    weather = "Weather"
    print_formatted_text(
        HTML(f"{id} | {rName} | {trackNlayout[0:65].ljust(65)} | {limits} | {startTime} | {weather}"))

    print("-" * 118)  # header seperator
    for x in gtdb.getRaceList(dbC1, raceColObj.id):
        race = gtdb.getRace(dbC1, x[0])
        id = f"{race.id:d}".rjust(3)
        rName = html.escape(race.name[0:7].ljust(7))
        trackNlayout = html.escape(
            f"{race.trackLayout.track.name} ({race.trackLayout.track.id}): {race.trackLayout.name} ({race.trackLayout.id})")
        limit = f"{race.limits}".rjust(3)
        limits = f"{limit} {race.raceType.name}".ljust(11)
        startTime = html.escape(race.racetime.ljust(5))
        weather = html.escape(race.weather.name)
        print_formatted_text(
            HTML(f"<ansigreen>{id}</ansigreen> | <ansigreen>{rName}</ansigreen> | <ansigreen>{trackNlayout[0:65].ljust(65)}</ansigreen> | <ansigreen>{limits}</ansigreen> | <ansigreen>{startTime}</ansigreen> | <ansigreen>{weather}</ansigreen>"))
    print("=" * 118)  # End of display


def displayCollections(leagueObj):
    """Display race collections for the league

    Args:
        leagueObj : League object
    """
    theList = gtdb.getRaceCollectionList(dbC1, leagueObj.id)
    print_formatted_text(
        HTML(f"Race Collections for League: <ansigreen>{html.escape(leagueObj.name)}</ansigreen> ({leagueObj.id})"))
    # Header
    colID = f' ID'
    colName = f'Collection Name'.ljust(40)
    carClass = f'Class'.ljust(6)
    prize1 = f'1st ~'.ljust(10)
    prize2 = f'2nd ~'.ljust(10)
    prize3 = f'3rd ~'.ljust(10)
    races = f'Races'
    print(
        f"  {colID} | {colName} | {carClass} | {prize1} | {prize2} | {prize3} | {races}")
    print("-" * 104)  # header seperator
    # Data
    # list: (id,name,desc,catClass, Prize1, Prize2, Prize3,raceCount)
    for row in theList:
        # print(row)
        colID = f"{row[0]:d}".rjust(3)
        colName = html.escape(row[1].ljust(40))
        if row[3]:  # Car Class Cat has a value
            xcarClass = row[3]
        else:  # Car Class Cat has no value
            xcarClass = ""
        carClass = html.escape(xcarClass.ljust(6))  # catClass
        # prizes
        prize1 = html.escape(f'{row[4]:,}'.rjust(10))
        prize2 = html.escape(f'{row[5]:,}'.rjust(10))
        prize3 = html.escape(f'{row[6]:,}'.rjust(10))
        races = f"{row[7]:d}".rjust(4)
        print_formatted_text(
            HTML(f"  <ansigreen>{colID}</ansigreen> | <ansigreen>{colName}</ansigreen> | <ansigreen>{carClass}</ansigreen> | <ansigreen>{prize1}</ansigreen> | <ansigreen>{prize2}</ansigreen> | <ansigreen>{prize3}</ansigreen> | <ansigreen>{races}</ansigreen>"))
    print("=" * 104)


def displayDriveTrains(theList):
    for r in theList:
        print(r)


def displayLeagues(theList):
    print("Here are the leagues")
    for r in theList:
        print(r)


def displayMfgs(theList):
    for r in theList:
        print(r)


def displayRace(race):
    """Display race information

    Args:
        race (object): The race class object
    """
    # League and collection info
    htmlLeague = html.escape(
        f'{race.raceCollection.league.name}')
    htmlCollection = html.escape(
        f"{race.raceCollection.name}")
    htmlRaceName = html.escape(f'{race.name}')
    print_formatted_text(HTML(
        f"League : <ansigreen>{htmlLeague} ({race.raceCollection.league.id})</ansigreen>  Collection: <ansigreen>{htmlCollection} ({race.raceCollection.id})</ansigreen> Race: <ansigreen>{htmlRaceName} ({race.id})</ansigreen>"))
    # Race collection description
    htmlText = f" <ansigreen>{html.escape(race.raceCollection.desc)}</ansigreen>"
    print_formatted_text(HTML(htmlText))
    # Prizes and Class
    prize1 = f"{race.raceCollection.prize1:,d}"[0:7].ljust(7)
    prize2 = f"{race.raceCollection.prize2:,d}"[0:7].ljust(7)
    prize3 = f"{race.raceCollection.prize3:,d}"[0:7].ljust(7)
    htmlText = f" Class : <ansigreen>{race.raceCollection.classcat.name}</ansigreen>  1st: <ansigreen>{prize1}</ansigreen> 2nd: <ansigreen>{prize2}</ansigreen> 3rd: <ansigreen>{prize3}</ansigreen>"
    print_formatted_text(HTML(htmlText))
    # Track Layout and miles long
    htmltrackNlayout = html.escape(
        f"{race.trackLayout.track.name} ({race.trackLayout.track.id}) : {race.trackLayout.name} ({race.trackLayout.id})")

    htmlLine = f"  Track and Layout: <ansigreen>{htmltrackNlayout}</ansigreen>"
    print_formatted_text(HTML(htmlLine))

    # Race Start Time, Weather and Limits
    startTime = html.escape(race.racetime.ljust(5))
    print_formatted_text(
        HTML(f"  Start Time: <ansigreen>{startTime}</ansigreen>  Weather: <ansigreen>{race.weather.name}</ansigreen> Limit: <ansigreen>{race.limits} {race.raceType.name}</ansigreen>"))

    # If lap type race.. show total race length
    if race.raceType.id == 1:
        ttlRaceLen = race.trackLayout.miles * float(race.limits)
        print_formatted_text(
            HTML(f"  Race Length: <ansigreen>{ttlRaceLen:.2f} Miles</ansigreen>"))

    # Race Notes
    if race.notes:
        notes = html.escape(f"{race.notes}")
    else:
        notes = "-- Nothing Entered --"
    print_formatted_text(HTML(f"Notes: <ansigreen>{notes}</ansigreen>"))
    print_formatted_text(HTML(f"Race Results:"))
    print("-" * 123)
    print("=" * 123)


def displayTrack(trackObj):
    """Display track information

    Args:
        trackObj
    """
    if trackObj.id == 0:  # No track found
        log.info("Track was not found")
        print_formatted_text(
            HTML(f"<ansired> ERROR </ansired> <b>Track not found</b>"))
        return

    log.info("Displaying information for trackID: {trackObj.id}")
    htmltName = html.escape(f"{trackObj.name}")
    print_formatted_text(
        HTML(f"Track  : <ansigreen>{htmltName}</ansigreen> ({trackObj.id})"))

    # Displaying Country info
    if trackObj.country.id == 0:  # No country info
        xtext = f"{str('None selected')[0:50].ljust(50)}"
        region = "N/A"
    else:  # Country info
        xtext = html.escape(f"{trackObj.country.cntryName}")
        region = html.escape(f"{trackObj.country.region}")

    print_formatted_text(HTML(
        f"Country: <ansigreen>{xtext}</ansigreen> (<ansigreen>{region}</ansigreen>)"))

    # Get track layout List
    tLayoutList = gtdb.getLayoutList(dbC1, trackObj.id)
    print(f"Layouts:")
    tlID = "ID"
    tlName = "Name".ljust(30)
    tlMiles = "Miles"
    races = "Races"
    rowStr = f" {tlID} | {tlName} | {tlMiles} | {races}"
    print(rowStr)
    print("-" * 55)  # header seperator
    # display track layouts
    for r in tLayoutList:
        tlID = str(r[0])[0:2].rjust(2)
        tlName = html.escape(r[1][0:30].ljust(30))
        tlMiles = "{:.2f}".format(r[2]).rjust(5)
        races = f"{r[3]:d}".rjust(4)
        rowStr = HTML(
            f" <ansigreen>{tlID}</ansigreen> | <ansigreen>{tlName}</ansigreen> | <ansigreen>{tlMiles}</ansigreen> | <ansigreen>{races}</ansigreen>")
        print_formatted_text(rowStr)

    print("=" * 55)


def displayTracks():
    """Displays table of track info
    """
    log.info("Getting list of tracks")
    theList = gtdb.getTrackList(dbC1)
    print_formatted_text(
        HTML(f"Number of Tracks: <ansigreen>{len(theList)}</ansigreen>"))
    # Header
    tID = f" ID"
    tName = f"Track Name"[0:30].ljust(30)
    region = f"Region"[0:10].ljust(10)
    country = f"Country"[0:54].ljust(54)
    layouts = f"Layouts"
    print_formatted_text(
        HTML(f"{tID} | {tName} | {region} | {country} | {layouts}"))
    print("-" * 117)
    # Details
    for row in theList:
        log.info(f"Getting track detail for trackid {row[0]}")
        track = gtdb.getTrack(dbC1, key='trackId', value=row[0])
        tID = str(row[0])[0:2].rjust(2)
        tName = html.escape(track.name[0:30].ljust(30))
        # Displaying Country info
        if track.country.id == 0:  # No country info
            country = str('----')[0:54].ljust(54)
            region = "N/A"[0:10].ljust(10)
        else:  # Country info
            country = html.escape(track.country.cntryName[0:54]).ljust(54)
            region = html.escape(track.country.region[0:10].ljust(10))
        layouts = str(row[2])[0:2].rjust(2)
        print_formatted_text(
            HTML(f" <ansigreen>{tID}</ansigreen> | <ansigreen>{tName}</ansigreen> | <ansigreen>{region}</ansigreen> | <ansigreen>{country}</ansigreen> | <ansigreen>{layouts}</ansigreen>"))

    print("=" * 117)


def displayTrackLayout(trackLayout):
    """Display Track Layout information

    Args:
        trackLayout ([type]): track Layout object
    """
    if trackLayout.id == 0:
        log.info("Track Layout was not found")
        print_formatted_text(
            HTML(f"<ansired> ERROR </ansired> <b>Track Layout not found</b>"))
        return
    log.info(
        f"Displaying track layout info for trackLayoutId: {trackLayout.id}")
    # Formatting header data
    trackNlayout = html.escape(
        f"{trackLayout.track.name} ({trackLayout.track.id}): {trackLayout.name} ({trackLayout.id})")
    htmlCountry = html.escape(
        f"{trackLayout.track.country.cntryName} ({trackLayout.track.country.region})")
    miles = "{:.2f}".format(trackLayout.miles).rjust(5)
    # Print the Track and Layout info
    htmlLine = f"Track Layout Info for: <ansigreen>{trackNlayout}</ansigreen>"
    print_formatted_text(HTML(htmlLine))
    htmlLine = f"Miles: <ansigreen>{miles}</ansigreen>  Country: <ansigreen>{htmlCountry}</ansigreen>"
    print_formatted_text(HTML(htmlLine))
    print_formatted_text(HTML("Races"))
    # Race Header line
    raceID = " ID"
    rName = "Race".ljust(7)
    leagueNcollection = "League (id) - Collection (id)".ljust(70)
    carClass = f'Class'.ljust(6)
    prize1 = f'1st ~'.ljust(10)
    prize2 = f'2nd ~'.ljust(10)
    prize3 = f'3rd ~'.ljust(10)
    limits = f"Limit".ljust(11)
    weather = "Weather"
    print_formatted_text(HTML(
        f"{raceID} | {rName} | {leagueNcollection} | {carClass} | {prize1} | {prize2} | {prize3} | {limits} | {weather}"))
    print("-" * 163)
    # Race detail info
    log.info(f"Getting race detail info for {trackLayout.id}")
    selectSQL = "SELECT r.id, r.name, l.name || ' (' || l.id || ') - ' || rc.name || ' (' || rc.id || ')' AS wtf, carcat.name AS Class, r.limits, rc.prize1, rc.prize2, rc.prize3, rt.name type, w.name AS weather"
    fromSQL = "FROM race AS r JOIN track_layout AS tl ON r.tl_id = tl.id JOIN race_type AS rt ON r.type_id = rt.id JOIN weather AS w ON r.weather_id = w.id JOIN race_collection AS rc ON r.rc_id = rc.id JOIN league AS l ON rc.league_id = l.id JOIN category as carcat ON rc.cat_id = carcat.id"
    whereSQL = "WHERE tl.id = ?"
    orderBySQL = "ORDER BY l.name, rc.name"
    # Getting the details
    for row in gtdb.directSql(dbC1, f"{selectSQL} {fromSQL} {whereSQL} {orderBySQL}", (trackLayout.id,)):
        raceID = f"{row[0]:d}".rjust(3)
        rName = html.escape(row[1][0:7].ljust(7))
        leagueNcollection = html.escape(row[2].ljust(70))
        carClass = row[3].ljust(6)
        racetime = html.escape(row[4].ljust(5))
        prize1 = f'{int(row[5]):,}'.rjust(10)
        prize2 = f'{int(row[6]):,}'.rjust(10)
        prize3 = f'{int(row[7]):,}'.rjust(10)
        limit = f"{row[4]}".rjust(3)
        limits = f"{limit} {row[8]}".ljust(11)
        weather = f'{row[9]}'

        print_formatted_text(HTML(
            f"<ansigreen>{raceID}</ansigreen> | <ansigreen>{rName}</ansigreen> | <ansigreen>{leagueNcollection}</ansigreen> | <ansigreen>{carClass}</ansigreen> | <ansigreen>{prize1}</ansigreen> | <ansigreen>{prize2}</ansigreen> | <ansigreen>{prize3}</ansigreen> | <ansigreen>{limits}</ansigreen> | <ansigreen>{weather}</ansigreen>"))
    print("=" * 163)
    return


def help(arg):
    """Display help information

    Args:
        arg(string): command looking to get help on
    """
    if arg == 'general':
        print("Required to provide one of the following")
        print(" LIST\n CREATE\n EDIT\n DELETE")
    elif arg == 'list':
        print(""" Addtional LIST requirements
          - Tracks: list all tracks
          - Track[name of track] - list details of track
          - TrackLayout[name of TrackLayout] - list details of tracklayout""")
    else:
        pass
    sys.exit()


def helpAction(cmd=None):
    """Display the help for a cmd
    """
    log.info(f"Providing help for the command {cmd}")
    if cmd.lower() == "list":
        print_formatted_text(HTML('<b>list</b>'))
        print_formatted_text(HTML(' <b><u>Car things</u></b>'))
        print_formatted_text(
            HTML(' classes - Lists all the car classes a car can be.'))
        print_formatted_text(
            HTML(' drivetrains - List all the drive trains a car can have.'))
        print_formatted_text(
            HTML(' manufactures - List all the manufactures for the cars.'))
        print_formatted_text(HTML('<b><u>Track things</u></b>'))
        print_formatted_text(
            HTML(' circuits - Lists all circuits tracks can use.'))
        print_formatted_text(HTML(
            ' collection - Lists all the race collections for a league. Select a league, or enter a leagueId'))
        print_formatted_text(HTML(' leagues - Lists all the Leagues'))
        print_formatted_text(HTML(
            ' track - List all the information about a single track. You can list by TrackID or name, or just select a track.'))

    elif cmd.lower() == "dbinit":
        pass
    else:
        pass


def listAction(cmd):
    """List Action.
    This will make sure
    - the objected being listed is valid
    - and have that objected listed.

    Args:
        cmd([string]): The object and its args to list
    """
    cmd = cmd.strip()
    # TODO: rename listObj -> obj (like what was done in addAction)
    listObj = cmd.split()[0]
    log.debug(f"listObj={listObj}")
    if listObj == 'track':
        listTrackCmd(cmd[len(listObj):].strip())
    elif listObj == 'collection':
        listRaceCollections(cmd[len(listObj):].strip())
    elif listObj == 'classes':
        displayCarCats(gtdb.getCarCatList(dbC1))
    elif listObj == 'circuits':
        displayCircuits(gtdb.getCircuitList(dbC1))
    elif listObj == 'drivetrains':
        displayDriveTrains(gtdb.getDriveTrainList(dbC1))
    elif listObj == 'leagues':
        displayLeagues(gtdb.getLeagueList(dbC1))
    elif listObj == 'manufactures':
        if cmd.find(' ') != -1:  # Args provided
            objArgs = cmd[cmd.find(' '):].lstrip()
            log.debug(f"objArgs: {objArgs}")
            if objArgs.split('=')[0].strip() == 'orderBy':
                orderBy = objArgs.split('=')[1].strip()
                displayMfgs(gtdb.getMfgs(dbC1, orderBy=orderBy))
            else:  # invalid argument for mfgs
                log.info(
                    f"Unknown list manufactures argument {objArgs.split('=')[0].strip()}")
                print_formatted_text(
                    HTML(f"<ansired>ERROR</ansired> - Unknown list manufactures argument <b>{objArgs.split('=')[0].strip()}</b>."))
        else:
            displayMfgs(gtdb.getMfgList(dbC1))
    elif listObj == 'race':
        listRaceCmd(cmd[len(listObj):].strip())
    elif listObj == 'tracks':
        displayTracks()
    else:  # Unknown object to list
        print_formatted_text(
            HTML(f'<ansired>ERROR</ansired> - Unknown <ansigreen>list</ansigreen> object <b>{listObj}</b>'))
        log.info("Unknown list object")


def listRaceCmd(args):
    """What to do when ask to list a Race"""
    log.debug(f"args passed: {args}")
    log.debug(f"length of args: {len(args)}")
    if len(args) > 0 and args.find("=") > 0:  # Have Args
        if args.split('=')[0].strip() == 'id':
            raceId = args.split('=')[1].strip()
            log.info(f"Getting race info for race id {raceId}")
            race = gtdb.getRace(dbC1, raceId)
            if race.id == 0:
                print("Race not found")
            else:
                displayRace(race)
        else:  # invalid Args passed
            log.info(
                f"Unknown list race argument {args.split('=')[0].strip()}")
            print_formatted_text(
                HTML(f"<ansired>ERROR</ansired> - Unknown list track argument <b>{args.split('=')[0].strip()}</b>."))
    else:  # No args passed
        print("I will need to ask some questions to find the race you are looking for")


def listTrackCmd(args):
    """what to do when ask to list a track"""
    log.debug(f"args passed: {args}")
    log.debug(f"length of args: {len(args)}")
    if len(args) > 0 and args.find("=") > 0:  # Have Args
        if args.split('=')[0].strip() == 'id':
            trackId = args.split('=')[1].strip()
            log.info(f"Getting track info for track id {trackId}")
            trackRec = gtdb.getTrack(dbC1, key='trackId', value=trackId)
            displayTrack(trackRec)
        elif args.split('=')[0].strip() == 'name':
            tName = args.split('=')[1]
            log.info(f"Getting track info for track name {tName}")
            trackRec = gtdb.getTrack(dbC1, key='track', value=tName)
            displayTrack(trackRec)
        elif args.split('=')[0].strip() == 'layoutId':
            layoutId = args.split('=')[1].strip()
            log.info(
                f"Getting track layout info for track layout id {layoutId}")
            trackLayout = gtdb.getLayout(dbC1, layoutId)
            displayTrackLayout(trackLayout)
        else:  # invalid Args passed
            log.info(
                f"Unknown list track argument {args.split('=')[0].strip()}")
            print_formatted_text(
                HTML(f"<ansired>ERROR</ansired> - Unknown list track argument <b>{args.split('=')[0].strip()}</b>."))
    else:  # No args passed
        log.info("No args passed. Have user select a track to get info")
        result = pickTrack()
        log.debug(f"result={result}")
        if result != None:  # User selected a track
            trackRec = gtdb.getTrack(dbC1, key='trackId', value=result)
            displayTrack(trackRec)


def listRaceCollections(args):
    """Get a list, and display, race collections for a League

    Args:
        args([str]): The args from the list collection command.
        These are parsed to provide complete the request
    """
    log.debug(f"args passed: {args}")
    log.debug(f"length of args: {len(args)}")
    if len(args) > 0 and args.find("=") > 0:  # Have valid Args
        if args.split('=')[0].strip() == 'leagueId':
            id = args.split('=')[1].strip()
            league = gtdb.getLeague(dbC1, value=id)
            if league.id != 0:
                displayCollections(league)
            else:
                print_formatted_text(
                    HTML(f"<ansired> ERROR </ansired> <b>League not found</b>"))
            return
        if args.split('=')[0].strip() == 'id':
            id = args.split('=')[1].strip()
            rCollection = gtdb.getRaceCollection(dbC1, id)
            if rCollection.id != 0:
                displayCollection(rCollection)
            else:
                print_formatted_text(
                    HTML(f"<ansired> ERROR </ansired> <b>Collection id not found</b>"))
            return
        else:  # unknown Args passed
            log.info(
                f"Unknown list collection argument {args.split('=')[0].strip()}")
            print_formatted_text(
                HTML(f"<ansired>ERROR</ansired> - Unknown list collection argument <b>{args.split('=')[0].strip()}</b>."))
            return
    else:  # No args passed. Need to ask user some info
        log.info(
            "No args passed. Getting user to select a league")
        id = pickLeague()
        log.info(f"User picked league id {id}")
        if id == None:  # No League picked
            log.info(f"Cancel for Race Collection")
            print("Cancel listing of collection")
            return

    log.info(f"Getting collection info for league id {id}")
    league = gtdb.getLeague(dbC1, value=id)
    displayCollections(league)


def pickCar(text='Select a Car', mfgId=0):
    """Dialog box for user to select a car from a manufacture

    Args:
        text (str, optional): [description]. Defaults to 'Select a Car'.
        mfgId (int, optional): [description]. Defaults to 0.

    Returns:
        Car.id user chose
    """
    log.info("Getting cars for mfgId={mfgId}")
    selectSQL = "SELECT id, model"
    fromSQL = "FROM car"
    whereSQL = "WHERE mfg_id = :mfgID"
    orderBy = "ORDER BY model"
    sql = f"{selectSQL} {fromSQL} {whereSQL} {orderBy}"
    vals = {'mfgID': mfgId}
    pickList = gtdb.directSql(dbC1, sql, vals)
    log.info("Displaying cars for use to select")
    result = radiolist_dialog(
        title="Cars",
        text=text,
        values=pickList
    ).run()
    log.info(f"User choose: {result}")
    return result


def pickCarCategory(text='Select a Car Class Category'):
    """Dialbog box for user to select a car class category

    Returns:
        ClassCat.id user choose
    """
    log.info("Getting car class categories for picklist")
    pickList = gtdb.getCarCatList(dbC1)
    log.info("Displaying Car Class Categories to user to choose")
    result = radiolist_dialog(
        title="Class Categories",
        text=text,
        values=pickList
    ).run()
    log.info(f"user choose id: {result}")
    return result


def pickDriveTrain(text="Select a Drivetrain"):
    """Dialog box for user to select a drivetrain from

    Args:
        text (str, optional): [description]. Defaults to "Select a Drivetrain".

    Returns:
        int : the drivetrain id user choose. (None if there was not a choice)
    """
    log.info("Getting list of drivetrains")
    pickList = gtdb.getDriveTrainList(dbC1)
    log.info("Display drivetrain dialog box for user to choose")
    result = radiolist_dialog(title="Drivetrains",
                              text=text,
                              values=pickList
                              ).run()
    log.info(f"User choose {result}")
    return result


def pickLeague(text='Select a League'):
    """Dialog box for user to select a League

    Returns:
        League ID user choose
    """
    log.info("Getting leagues for picklist")
    pickList = gtdb.getLeagueList(dbC1)
    log.info("Displaying leagues for user to choose")
    result = radiolist_dialog(
        title="Leagues",
        text=text,
        values=pickList
    ).run()
    log.info(f"User choose leagueId: {result}")
    return result


def pickMfg(text='Select manufacture'):
    """Dialog box for picking a manufacture/make

    Args:
        text (str, optional): Text in dialog box for user. Defaults to 'Select manufacture'.
    """
    log.info("Getting list of manufactures for user to select")
    pickList = gtdb.getMfgList(dbC1)
    log.info("Display dialog")
    result = radiolist_dialog(title="Manufactures",
                              text=text,
                              values=pickList).run()
    log.info(f"User choose mfgId: {result}")
    return result


def pickRaceCollection(leagueId, lName, text='Select one'):
    log.info(f"Getting race collections for ({leagueId}) {lName} league")
    picklist = gtdb.getRaceCollectionList(dbC1, leagueId)
    log.info(f"Displaying collections for user to choose")
    result = radiolist_dialog(title=f"Race Collections for {lName}",
                              text=text,
                              values=picklist).run()
    log.info(f"User choose collection id: {result}")
    return result


def pickRaceType(text="Select a Race type"):
    """Dialog box for user to select a Race Type

    Args:
        text (str, optional): [description]. Defaults to "Select a Race type".

    Returns:
        RaceTypeID (int): The choosen Racetype id
    """
    log.info("Getting Race Types for picklist")
    pickList = gtdb.getRaceTypeList(dbC1)
    log.info("Displaying race types for use to choose")
    result = radiolist_dialog(
        title="Race Types",
        text=text,
        values=pickList
    ).run()
    log.info(f"User choose RaceTypeId: {result}")
    return result


def pickTrack(text="Select a Track"):
    """Dialog box for user to select a track
    Returns: the trackID user picked
    """
    log.info("Getting tracks for picklist")
    pickList = gtdb.getTrackList(dbC1)
    log.info("display tracks for user to choose")
    result = radiolist_dialog(
        title="Tracks",
        text=text,
        values=pickList
    ).run()
    log.info(f"User choose: {result}")
    return result


def pickTrackLayout(trackID, trackName, text='Select one'):
    """Dialog box for user to select a track layout from a track

    Args:
        trackID(int): trackID to get layouts for
        trackName(str): This is included in the text of the dialog.
              UX friendly letting them know which track its for.

    Returns:
        layoutID(int)

    If there is only one track layout, this will automaticly return
    that layouts id, thus not prompting use to choose.
    """
    log.info(f"getting track layouts for trackID:{trackID}")
    pickList = gtdb.getLayoutList(dbC1, trackID)
    if len(pickList) == 1:
        result = pickList[0][0]
        log.info(f"Only one to choose. returning {result}")
    else:
        log.info("Display track layouts for user to choose")
        result = radiolist_dialog(title=f"Track Layouts for track {trackName}",
                                  text=text,
                                  values=pickList).run()
        log.info(f"User choose: {result}")
    return result


def pickWeather(text='Select type of Weather'):
    """Dialog box for user to select weather type.

    Args:
        text (str, optional): Text to appear on dialog box. Defaults to 'Select type of Weather'.

    Returns:
        int: The unique id of the Weather
    """
    log.info("Getting list of weather choices")
    pickList = gtdb.getWeatherList(dbC1)
    log.info('Displaying weather types for user to choose')
    result = radiolist_dialog(
        title="Weather Types",
        text=text,
        values=pickList
    ).run()
    log.info(f"User choose: {result}")
    return result


if __name__ == '__main__':
    main()
