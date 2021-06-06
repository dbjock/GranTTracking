# PURPOSE: CLI to test getting data out of db. Future cli maybe.
#    GTTracking db library
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from pathlib import Path
from string import Template

# Addtional external libs
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.shortcuts import input_dialog

# App specific required
from GranT import gtdbV2 as gtdb
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
logFile = Path(gtcfg.logcfg['logDir']) / 'test-cli.log'
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
GTDBConn1 = gtdb.GTdb(gtcfg.dbcfg['dbFile'])


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

        GTDBConn1.initDB(scriptPath=_gtScripts)

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
        },
        'list': {
            'circuits': None,
            'classes': None,
            'collection': {
                'leagueId=': None
            },
            'drivetrains': None,
            'manufactures': {'orderBy=': None},
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
                pass
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
    league = GTDBConn1.getLeague(value=leagueId)
    if league.id == 0:  # League was not found
        log.warning("League not found in database")
        return [1, "League not found"]

    log.info("Getting race collection name from user")
    print_formatted_text(
        HTML(f"Enter new race collection for the <u><b>{league.name}</b></u> league"))
    rcName = prompt("   Collection Name: ")
    log.debug(f"rcName={rcName}")
    if rcName == None or rcName == "":  # User didn't provide data
        log.info("User did not provide race collection name")
        return [1, "Race collection name not provided."]

    # Validate the race collection name
    log.info(f"Checking if League already has race name: '{rcName}'")
    rcList = GTDBConn1.getRaceCollectionList(league.id)
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
    r = GTDBConn1.addRaceCollection(rCollection)
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
    else:  # No args passed
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
    # At this time not going to parse any args. Just ignoring
    cls()
    # Prompt user for Track
    x = pickTrack(text="Which track for the new race?")
    if x == None:  # no track was selected
        log.info("No track selected")
        print(
            f"No track was selected for new race")
        return
    track = GTDBConn1.getTrack(value=x)

    # Prompt user for track layout
    x = pickTrackLayout(track.id, track.name,
                        text=f'Which layout for the new race?')
    if x == None:  # no layout was selected
        log.info("No layout selected")
        print(f"No layout selected for new race on {track.name} track")
        return
    tLayout = GTDBConn1.getLayout(x)

    x = pickLeague(text="Which League for the new race?")
    if x == None:  # no league picked
        log.info("No league selected.")
        print("No league selected for new race")
        return
    log.info(f"Loading league object for leagueid={x}")
    league = GTDBConn1.getLeague(value=x)

    # Prompt user for leagues race collection
    x = pickRaceCollection(
        league.id, league.name, text=f"Which race collection for the new race?")
    if x == None:  # no race collection selected
        log.info(
            f"No race collection was selected for league ({league.id}) {league.name}")
        print("No race collection selected")
        return
    rcCollection = GTDBConn1.getRaceCollection(x)

    x = f"Track Layout   : {tLayout.track.name} - {tLayout.name} -- layout Id: {tLayout.id}"
    print(x)
    x = f"Race Collection: {rcCollection.league.name} - {rcCollection.name} -- collection Id: {rcCollection.id}"
    print(x)


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
    x = f"<b><u>Track:</u></b> ({trackObj.id}) {tName}"
    print_formatted_text(HTML(x))

    # Displaying Country info
    if trackObj.country.id == None:  # No country info
        cText = f"      {str('No country assigned to this track')[0:50].ljust(50)}"
        region = "N/A"
    else:  # Country info
        cText = f"{trackObj.country.cntryName[0:50].ljust(50)}"
        region = trackObj.country.region

    x = f"<b><u>Country:</u></b> {cText} <b>Region:</b> {region}"
    print_formatted_text(HTML(x))

    # Get track layout List
    tLayoutList = GTDBConn1.getLayoutList(trackObj.id)
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


def listAction(cmd):
    """List Action.
    This will make sure
    - the objected being listed is valid
    - and have that objected listed.

    Args:
        cmd([string]): The object and its args to list
    """
    cmd = cmd.strip()
    cls()
    # TODO: rename listObj -> obj (like what was done in addAction)
    listObj = cmd.split()[0]
    log.debug(f"listObj={listObj}")
    if listObj == 'track':
        listTrackCmd(cmd[len(listObj):].strip())
    elif listObj == 'collection':
        listRaceCollections(cmd[len(listObj):].strip())
    elif listObj == 'classes':
        displayCarCats(GTDBConn1.getCarCats())
    elif listObj == 'circuits':
        displayCircuits(GTDBConn1.getCircuitList())
    elif listObj == 'drivetrains':
        displayDriveTrains(GTDBConn1.getDriveTrains())
    elif listObj == 'leagues':
        displayLeagues(GTDBConn1.getLeagueList())
    elif listObj == 'manufactures':
        if cmd.find(' ') != -1:  # Args provided
            objArgs = cmd[cmd.find(' '):].lstrip()
            log.debug(f"objArgs: {objArgs}")
            if objArgs.split('=')[0].strip() == 'orderBy':
                orderBy = objArgs.split('=')[1].strip()
                displayMfgs(GTDBConn1.getMfgs(orderBy=orderBy))
            else:  # invalid argument for mfgs
                log.info(
                    f"Unknown list manufactures argument {objArgs.split('=')[0].strip()}")
                print_formatted_text(
                    HTML(f"<ansired>ERROR</ansired> - Unknown list manufactures argument <b>{objArgs.split('=')[0].strip()}</b>."))
        else:
            displayMfgs(GTDBConn1.getMfgs())
    else:  # Unknown object to list
        print_formatted_text(
            HTML(f'<ansired>ERROR</ansired> - Unknown <ansigreen>list</ansigreen> object <b>{listObj}</b>'))
        log.info("Unknown list object")


def listTrackCmd(args):
    """what to do when ask to list a track"""
    log.debug(f"args passed: {args}")
    log.debug(f"length of args: {len(args)}")
    if len(args) > 0 and args.find("=") > 0:  # Have valid Args
        if args.split('=')[0].strip() == 'id':
            trackId = args.split('=')[1].strip()
            log.info(f"Getting track info for track id {trackId}")
            trackRec = GTDBConn1.getTrack(key='trackId', value=trackId)
            displayTrack(trackRec)
        elif args.split('=')[0].strip() == 'name':
            tName = args.split('=')[1]
            log.info(f"Getting track info for track name {tName}")
            trackRec = GTDBConn1.getTrack(key='track', value=tName)
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
            trackRec = GTDBConn1.getTrack(key='trackId', value=result)
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
    league = GTDBConn1.getLeague(value=id)
    theList = GTDBConn1.getRaceCollectionList(id)
    displayCollections(theList, league)


def pickLeague(text='Select a League'):
    """Dialog box for user to select a League

    Returns:
        League ID user choose
    """
    log.info("Getting leagues for picklist")
    pickList = GTDBConn1.getLeagueList()
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
    picklist = GTDBConn1.getRaceCollectionList(leagueId)
    log.info(f"Displaying collections for user to choose")
    result = radiolist_dialog(title=f"Race Collections for {lName}",
                              text=text,
                              values=picklist).run()
    log.info(f"User choose collection id: {result}")
    return result


def pickTrack(text="Select a Track"):
    """Dialog box for user to select a a track
    Returns: the trackID user picked
    """
    log.info("Getting tracks for picklist")
    pickList = GTDBConn1.getTrackList()
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
    pickList = GTDBConn1.getLayoutList(trackID)
    log.info("Display track layouts for user to choose")
    result = radiolist_dialog(title=f"Track Layouts for track {trackName}",
                              text=text,
                              values=pickList).run()
    log.info(f"User choose: {result}")
    return result


if __name__ == '__main__':
    main()
