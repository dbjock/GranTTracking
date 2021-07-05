# PURPOSE: CLI to test getting data out of db. Future cli maybe.
#    GTTracking db library
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import html
from pathlib import Path

# Addtional external libs
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.shortcuts import input_dialog

# App specific required
from GranT import gtdbV3 as gtdb
from GranT import GTClasses as GT
from GranT import gtcfg

_gtPath = Path.cwd()
_gtScripts = _gtPath / 'Scripts'


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
logFile = Path(gtcfg.logcfg['logDir']) / 'cli.log'
print(logFile)

log_fh = RotatingFileHandler(
    logFile, mode='a', maxBytes=1048576, backupCount=2)
extFMT = logging.Formatter(
    '%(asctime)s %(levelname)-8s:%(name)s.%(funcName)s: %(message)s')
log_fh.setFormatter(extFMT)
log_fh.setLevel(logging.DEBUG)
# Add logging filehander log_fh to the logger
log.addHandler(log_fh)
print(f"Logging to {logFile}")
print(f"Connecting to db {gtcfg.dbcfg['dbFile']}")

dbC1 = gtdb.create_connection(gtcfg.dbcfg['dbFile'])


def _sortTuple(tup, key):
    """Returns a tuple sorted by the key

    Args:
        tup (tuple list): example [(1,"zzd"),(3,"azd")]
        key (int): The key/index to sort.
            example: 1 for results: [(3,"azd"),(1,"zzd")]
    """
    return(sorted(tup, key=lambda x: x[key]))


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
        gtdb.initDB(dbC1, scriptPath=_gtScripts)

        x = f'<ansired><b>Database initilization complete</b></ansired>'
        print_formatted_text(HTML(x))


def main():

    cls()
    print("enter Exit or Help for more info")
    completer = NestedCompleter.from_nested_dict({
        'help': {
            'exit': None,
            'list': None,
            'tracks': None,
            'dbinit': None
        },
        'add': {
            'collection': {
                'leagueId=': None
            },
            'race': None
        },
        'list': {
            'circuits': None,
            'classes': None,
            'collection': {
                'leagueId=': None
            },
            'drivetrains': None,
            'manufactures': {'orderBy=': None},
            'race': None,
            'track': {
                'id=': None,
                'name=': None
            },
        },
        'exit': None,
    })

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
            elif action == 'secret':
                _POCtest()
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
    else:  # Unknown object
        print_formatted_text(
            HTML(f'<ansired>ERROR</ansired> - Unknown <ansigreen>add</ansigreen> object <b>{obj}</b>'))
        log.info("Unknown object for add action")


def addCollection(leagueId):
    """Add a race collection

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
    # Now to prepare object for saving to the database
    log.debug("creating rCollection")
    rCollection = GT.RaceCollection(
        id=0, name=rcName, desc=rcDesc, leagueObj=league)
    log.debug(f"Saving {rCollection}")
    r = gtdb.addRaceCollection(dbC1, rCollection)
    log.debug(f'result from adding racecollection: {r}')
    return r


def addCollectionCmd(args):
    """What to do when asked to add a collection"""
    log.debug(f"args passed: {args}")
    log.debug(f"length of args: {len(args)}")
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

    r = addCollection(id)
    if r[0] != 0:  # Save was not successful
        x = f'  <ansiyellow>Unable to add Race Collection. Return Code: {r[0]} Desc: {r[1]}</ansiyellow>'
        print_formatted_text(HTML(x))
        log.info(
            f"Unable to add Race Collection. Return Code: {r[0]} Desc: {r[1]}")
        return
    else:  # Race collection added
        x = f'  <ansigreen>Race Collection Added</ansigreen>'
        print_formatted_text(HTML(x))
        log.info(f"Race Collection Added")


def addRaceCmd(args):
    log.debug(f"args passed: {args}")
    log.debug(f"length of args: {len(args)}")
    # At this time not going to parse any args
    # Prompt user for League
    x = pickLeague(text="Which League for the new race?")
    if x == None:  # no league picked
        log.info("No league selected.")
        print("No league selected for new race")
        return
    log.info(f"Loading league object for leagueid={x}")
    league = gtdb.getLeague(dbC1, value=x)
    # tlName = r[1][0:30].ljust(30)
    x = f"League         : {league.name[0:30].ljust(30)}"
    print(x)

    # Prompt user for leagues race collection
    x = pickRaceCollection(
        league.id, league.name, text=f"Which race collection for the new race?")
    if x == None:  # no race collection selected
        log.info(
            f"No race collection was selected for league ({league.id}) {league.name}")
        print("No race collection selected")
        return
    rcCollection = gtdb.getRaceCollection(dbC1, x)
    x = f"Race Collection: {rcCollection.name[0:30].ljust(30)}"
    print(x)

    # Prompt user for Track
    x = pickTrack(text="Which track for the new race?")
    if x == None:  # no track was selected
        log.info("No track selected")
        print(
            f"No track was selected for new race")
        return
    track = gtdb.getTrack(dbC1, value=x)
    x = f"Track          : {track.name[0:30].ljust(30)}"

    # Prompt user for track layout
    x = pickTrackLayout(track.id, track.name,
                        text=f'Which layout for the new race?')
    if x == None:  # no layout was selected
        log.info("No layout selected")
        print(f"No layout selected for new race on {track.name} track")
        return
    tLayout = gtdb.getLayout(dbC1, x)
    x = f"Layout         : {tLayout.name[0:30].ljust(30)}"
    print_formatted_text(HTML(x))

    # Prompt user for weather type
    x = pickWeather()
    if x == None:  # User did not choose a weather type
        log.info(f"No weather type choosen")
        print("No weather type choosen")
        return
    weather = gtdb.getWeather(dbC1, x)
    x = f"Weather        : {weather.name[0:30].ljust(30)}"

    # Prompt user for Race type
    x = pickRaceType()
    if x == None:  # User did not choose a race type
        log.info(f"No race type choosen")
        print("No race type choosen")
        return
    raceType = gtdb.getRaceType(dbC1, id=x)
    x = f"Race type      : {raceType.name[0:30].ljust(30)}"
    print(x)

    log.info("Getting race name from user")
    name = prompt("   Race Name (Enter to cancel): ")
    log.debug(f"name={name}")
    if name == None or name == "":  # User didn't provide data
        log.info("User did not provide race name")
        return [1, "Race name not provided."]

    xRace = GT.Race(id=0, name=name, trackLayout=tLayout,
                    raceCollection=rcCollection, raceType=raceType, weather=weather)
    print(gtdb.addRace(dbC1, xRace))


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


def displayCollections(theList, leagueObj):
    print(f"Race Collections for League: ({leagueObj.id}) {leagueObj.name}")
    for r in theList:
        print(r)


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
    # TODO: More stuff to put in here
    # League and collection info
    htmlLeague = html.escape(
        f'{race.raceCollection.league.name}')
    htmlCollection = html.escape(
        f"{race.raceCollection.name}")
    print_formatted_text(HTML(
        f"<b>League     :</b> <ansigreen>{htmlLeague}</ansigreen> ({race.raceCollection.league.id}) - <ansigreen>{htmlCollection}</ansigreen> ({race.raceCollection.id})"))
    # Race info and type
    htmlData = html.escape(f'{race.name}')
    print_formatted_text(
        HTML(f'<b>Race       :</b> <ansigreen>{htmlData}</ansigreen> ({race.id})   <b>Type: </b> <ansigreen>{race.raceType.name}</ansigreen>'))
    # Track and Layout
    htmlData = html.escape(
        f"{race.trackLayout.track.name} - {race.trackLayout.name}")
    print_formatted_text(HTML(f"  <ansigreen>{htmlData}</ansigreen>"))
    # Prizes
    p1 = f"1st"[0:7].ljust(7)
    p2 = f"2nd"[0:7].ljust(7)
    p3 = f"3rd"[0:7].ljust(7)
    print(f"  {p1} |{p2} |{p3} |")
    print(f"  {'-'*27}")
    p1 = f"{race.prize1:,d}"[0:7].rjust(7)
    p2 = f"{race.prize2:,d}"[0:7].rjust(7)
    p3 = f"{race.prize3:,d}"[0:7].rjust(7)
    print_formatted_text(HTML(
        f"  <ansigreen>{p1}</ansigreen> |<ansigreen>{p2}</ansigreen> |<ansigreen>{p3}</ansigreen> |"))

    # Weather and miles
    print_formatted_text(
        HTML(f"  <b>Miles :</b> <ansigreen>{race.trackLayout.miles}</ansigreen> <b>Weather : </b><ansigreen>{race.weather.name}</ansigreen>"))

    if race.racetime:
        racetime = race.racetime
    else:
        racetime = "-- Nothing Entered --"
    print(f"  Race Time  :{racetime}")
    if race.limits:
        limits = race.limits
    else:
        limits = "-- Nothing Entered --"
    #         Weather    :
    print(f"  Limits     : {limits}")
    if race.notes:
        notes = race.notes
    else:
        notes = "-- Nothing Entered --"
    print(f"  Notes      : {notes}")

    print("** Got more work **")


def displayTrack(trackObj):
    """Display track information

    Args:
        trackObj
    """
    if trackObj.id == 0:  # No track found
        print("No Track found matching the criteria")
        print("=" * 78)
        return

    tName = trackObj.name[0:50].ljust(50)
    print(f"Track: ({trackObj.id}) {tName}")

    # Displaying Country info
    if trackObj.country.id == 0:  # No country info
        cText = f"      {str('No country assigned to this track')[0:50].ljust(50)}"
        region = "N/A"
    else:  # Country info
        cText = f"{trackObj.country.cntryName[0:50].ljust(50)}"
        region = trackObj.country.region

    print(f"Country: {cText} Region: {region}")

    # Get track layout List
    tLayoutList = gtdb.getLayoutList(dbC1, trackObj.id)
    print(f"Layouts:")
    tlID = "ID"
    tlName = "Name".ljust(30)
    tlMiles = "Miles"
    rowStr = f" {tlID} | {tlName} | {tlMiles} |"
    print(rowStr)
    print("-" * 80)  # header seperator
    # display track layouts
    for r in tLayoutList:
        tlID = str(r[0])[0:2].rjust(2)
        tlName = r[1][0:30].ljust(30)
        tlMiles = "{:.2f}".format(r[2]).rjust(5)
        rowStr = f" {tlID} | {tlName} | {tlMiles} |"
        print(rowStr)

    print("=" * 80)


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
        displayCarCats(gtdb.getCarCats(dbC1))
    elif listObj == 'circuits':
        displayCircuits(gtdb.getCircuitList(dbC1))
    elif listObj == 'drivetrains':
        displayDriveTrains(gtdb.getDriveTrains(dbC1))
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
    theList = gtdb.getRaceCollectionList(dbC1, id)
    displayCollections(theList, league)


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
    """
    log.info("getting track layouts for trackID:{trackID}")
    pickList = gtdb.getLayoutList(dbC1, trackID)
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
