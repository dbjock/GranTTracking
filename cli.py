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


def main():
    print("enter Exit or Help for more info")
    completer = NestedCompleter.from_nested_dict({
        'help': {'exit': None, 'list': None,
                 'tracks': None},
        'list': {
            'circuits': None,
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
        else:
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
            else:
                log.info('Unknown command Please enter a command')
                print_formatted_text(
                    HTML(f'Unknown command Please enter a command'))

    print('GoodBye!')


def listAction(cmd):
    """List Action.
    example, list track information for trackid 1
    list track id=1

    Args:
        cmd ([string]): The object and its args
    """
    cmd = cmd.strip()
    listObj = cmd.split()[0]
    log.debug(f"listObj={listObj}")
    if listObj == 'track':
        if cmd.find(' ') != -1:  # Args provided
            objArgs = cmd[cmd.find(' '):].lstrip()
            log.debug(f"objArgs: {objArgs}")
            if objArgs.split('=')[0].strip() == 'id':
                trackId = objArgs.split('=')[1].strip()
                log.info(f"Getting track info for track id {trackId}")
                trackRec = GTDBConn1.getTrack(key='trackId', value=trackId)
                displayTrack(trackRec)
            elif objArgs.split('=')[0].strip() == 'name':
                tName = objArgs.split('=')[1]
                log.info(f"Getting track info for track name {tName}")
                trackRec = GTDBConn1.getTrack(key='track', value=tName)
                displayTrack(trackRec)

            else:
                log.info(
                    f"Unknown list track argument {objArgs.split('=')[0].strip()}")
                print_formatted_text(
                    HTML(f"<ansired>ERROR</ansired> - Unknown list track argument <b>{objArgs.split('=')[0].strip()}</b>."))
        else:  # Missing required track args
            log.info("Missing required args for track action")
            print_formatted_text(
                HTML(f'<ansired>ERROR</ansired> - id= or name= are required.'))
    elif listObj == 'circuits':
        displayCircuits()
    else:
        print_formatted_text(
            HTML(f'<ansired>ERROR</ansired> - Unknown <ansigreen>list</ansigreen> object <b>{listObj}</b>'))
        log.info("Unknown list object")


def displayCircuits():
    """Display all the circuits"""
    cList = GTDBConn1.getCircuits()
    print(f"Number of circuits: {len(cList)}")
    t = Template(' $id | $cName')
    id = "ID"
    cName = "Circuit"
    hdrStr = t.substitute(id=id[0:4].rjust(4),
                          cName=cName[0:30].ljust(30))
    print(hdrStr)
    print("-" * 78)  # header seperator
    for r in cList:
        id = str(r[0])
        cName = r[1]
        rowStr = t.substitute(id=id[0:4].rjust(4),
                              cName=cName[0:30].ljust(30))
        print(rowStr)
    print("=" * 78)


def displayTrack(trackObj):
    """Print to screen the track object

    Args:
        trackObj
    """
    if trackObj.id == 0:  # No track found
        print("No Track found matching the criteria")
        return

    t = Template('Track: $tName ID: $id')
    id = str(trackObj.id)
    tName = trackObj.name
    rowStr = t.substitute(id=id[0:4].rjust(4),
                          tName=tName[0:50].ljust(50))
    print(rowStr)
    print(
        f" Country: ({trackObj.country.id}) {trackObj.country.cntryName[0:50].ljust(50)}")
    print(f" Region: {trackObj.country.region}")
    tLayoutList = GTDBConn1.getLayoutList(key='trackId', value=trackObj.id)
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


if __name__ == '__main__':
    main()
