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


def _POCtest():
    print("POC Test")


def main():

    cls()
    print("enter Exit or Help for more info")
    completer = NestedCompleter.from_nested_dict({
        'help': {'exit': None, 'list': None,
                 'tracks': None},
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
                'test-GranTT > ', completer=completer, complete_while_typing=True)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        else:  # Checking for valid actions
            log.info(f"Command: {userCmd}")
            try:
                action = userCmd.split()[0]
            except IndexError:
                break
            log.debug(f"action={action}")
            if action == 'help':
                pass
            elif action == 'list':
                if userCmd.find(' ') != -1:
                    actOn = userCmd[userCmd.find(' '):]
                    listAction(actOn)
                else:
                    print("Must provide an object to list")
            elif action == 'exit':
                break
            elif action == 'secret':
                _POCtest()
            else:
                log.info('Unknown command Please enter a command')
                print_formatted_text(
                    HTML(f'Unknown command Please enter a command'))

    print('GoodBye!')


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


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
    """Print to screen the track object

    Args:
        trackObj
    """
    if trackObj.id == 0:  # No track found
        print("No Track found matching the criteria")
        print("=" * 78)
        return

    tName = trackObj.name[0:50].ljust(50)
    # rowStr = t.substitute(id=id[0:4].rjust(4),
    #   tName = tName[0:50].ljust(50))
    # print(rowStr)
    print(f"Track: ({trackObj.id}) {tName}")

    # Displaying Country info
    if trackObj.country.id == None:  # No country info
        cText = f"No country assigned to this track"
        region = "N/A"
    else:  # Country info
        cText = f"({trackObj.country.id}) {trackObj.country.cntryName[0:50].ljust(50)}"
        region = trackObj.country.region

    print(f"Country: {cText}\n Region: {region}")

    tLayoutList = GTDBConn1.getLayoutList(trackObj.id)
    print(f"Layouts:")
    # Layout id column (tlID): width 4, justification right
    # Layout name column (tlName): width 30, justification left
    # LayoutCircuitID (cID): width 4, justification right
    # LayoutCircutName(cName): width 15, justification left
    t = Template(' $tlID | $tlName | $cID | $cName')
    tlID = "ID"
    tlName = "Name"
    cID = "cID"
    cName = "Circuit Name"
    hdrStr = t.substitute(tlID=tlID[0:4].rjust(4),
                          tlName=tlName[0:30].ljust(30),
                          cID=cID[0:4].rjust(4),
                          cName=cName[0:30].ljust(30))
    print(hdrStr)
    print("-" * 78)  # header seperator
    for r in tLayoutList:
        tlID = str(r[2])
        if r[3] == None:
            tlName = "None"
        else:
            tlName = r[3]
        cID = str(r[5])
        cName = r[6]
        rowStr = t.substitute(tlID=tlID[0:4].rjust(4),
                              tlName=tlName[0:30].ljust(30),
                              cID=cID[0:4].rjust(4),
                              cName=cName[0:30].ljust(30))
        print(rowStr)

    print("=" * 78)


def help(arg):
    """Display help information

    Args:
        arg (string): command looking to get help on
    """
    if arg == 'general':
        print("Required to provide one of the following")
        print(" LIST\n CREATE\n EDIT\n DELETE")
    elif arg == 'list':
        print(""" Addtional LIST requirements
          - Tracks : list all tracks
          - Track [name of track] - list details of track
          - TrackLayout [name of TrackLayout] - list details of tracklayout""")
    else:
        pass
    sys.exit()


def listAction(cmd):
    """List Action.
    This will make sure
    - the objected being listed is valid
    - and have that objected listed.

    Args:
        cmd ([string]): The object and its args to list
    """
    cmd = cmd.strip()
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
        args ([str]): The args from the list collection command.
        These are parsed to provide complete the request
    """
    log.debug(f"args passed: {args}")
    log.debug(f"length of args: {len(args)}")
    if len(args) > 0 and args.find("=") > 0:  # Have valid Args
        if args.split('=')[0].strip() == 'leagueId':
            id = args.split('=')[1].strip()
            log.info(f"Getting collection info for league id {id}")
        else:  # unknown Args passed
            log.info(
                f"Unknown list collection argument {args.split('=')[0].strip()}")
            print_formatted_text(
                HTML(f"<ansired>ERROR</ansired> - Unknown list collection argument <b>{args.split('=')[0].strip()}</b>."))
    else:  # No args passed. Need to ask user some info
        log.info(
            "No args passed. Have user select which League to get the collection for")
        id = pickLeague()
        log.info(f"User picked league id {id}")
        if id == None:  # No League picked
            log.info(f"Cancel for Race Collection")
            print("Cancel listing of collection")
            return

    league = GTDBConn1.getLeague(value=id)
    theList = GTDBConn1.getRaceCollectionList(id)
    displayCollections(theList, league)


def pickLeague():
    """Dialog box for user to select a League

    Returns:
        League ID user choose
    """
    log.info("Getting leagues for picklist")
    pickList = GTDBConn1.getLeagueList()
    log.info("Displaying leagues for user to choose")
    result = radiolist_dialog(
        title="Leagues",
        text="Select a League",
        values=pickList
    ).run()
    log.info(f"User choose: {result}")
    return result


def pickTrack():
    """Dialog box for user to select a a track
    Returns: the trackID user picked
    """
    log.info("Getting tracks for picklist")
    pickList = GTDBConn1.getTrackList()
    log.info("display tracks for user to choose")
    result = radiolist_dialog(
        title="Tracks",
        text="Select a Track",
        values=pickList
    ).run()
    log.info(f"User choose: {result}")
    return result


def pickTrackLayout(trackID, trackName):
    """Dialog box for user to select a track layout from a track

    Args:
        trackID (int): trackID to get layouts for
        trackName (str): This is included in the text of the dialog.
              UX friendly letting them know which track its for.

    Returns:
        layoutID (int)
    """
    log.info("getting track layouts for trackID:{trackID}")
    pickList = GTDBConn1.getLayoutList(trackID)
    log.info("Display track layouts for user to choose")
    result = radiolist_dialog(title="Track Layouts",
                              text=f"Select a layout for track {trackName}",
                              values=pickList).run()
    log.info(f"User choose: {result}")
    return result


if __name__ == '__main__':
    main()
