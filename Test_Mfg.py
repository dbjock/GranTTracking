import logging
import DBFunctions as gtdb
import GTClasses as gt
from pathlib import Path
import csv
import os
myLogLvl = logging.INFO
myLogLvl = logging.DEBUG

logging.basicConfig(
    level = myLogLvl,
    format = '%(asctime)s %(levelname)s:%(module)s:%(funcName)s: %(message)s'
    )
def pMfg(xmfg):
    print(f'mfgID: {xmfg.mfgID}')
    print(f'name : {xmfg.name}')

#Adding some comments here to see how how source will see the change.

xmfg = gt.Manufacture("deleteme")
pMfg(xmfg)
print('time to play with mfg')

tmp_mfg = gtdb.get_manufacture(23)

if len(tmp_mfg) > 0:
    r = tmp_mfg[0]
    xmfg.mfgID = r[0]
    xmfg.name = r[1]

pMfg(xmfg)

print('\n going to change xmfg now')

xmfg.get(1113)
pMfg(xmfg)
# print(f'name: {xmfg.name}')
# print(f'mfgid: {xmfg.mfgID}')

# print("Get them all")
# MyList = gtdb.get_manufacture(13)
# print (f'How many rows: {len(MyList)}')
# for row in MyList:
#     print(row)
#     print(row[0])