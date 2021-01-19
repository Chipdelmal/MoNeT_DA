#!/usr/bin/env python3

# 'inkscape --export-type="png" --export-dpi="300" --export-background="ffffffff" 106_template.svg --export-filename="test.png"'

import re
from os import path
import  subprocess
import STP_aux as aux
import STP_functions as fun
import MoNeT_MGDrivE as monet


PTRN = 'E_{}_{}_{}_{}_{}-{}'

(USR, LND, REL) = ('dsk', 'SPA', '106')
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, REL)
monet.makeFolder(path.join(PT_IMG, 'panels'))
###############################################################################
# Template layout
###############################################################################
template = path.join(PT_IMG, '106_template.svg')
with open(template, 'r') as file :
    filedata = file.read()
###############################################################################
# Replacements
###############################################################################
# Find original ids -----------------------------------------------------------
p = re.compile('E_.*png', re.IGNORECASE)
pats = re.findall(p, filedata)
img_org = list({i[:-8] for i in pats})
# Replacement ids -------------------------------------------------------------
uids = fun.getExperimentsIDSets(PT_PRE, skip=-1)
(i_rer, i_ren, i_rsg, i_fic, i_gsv, i_aoi) = (
    '0025000000', '03', '0000000000',
    ('0000000000', '0100000000'), 
    uids[5][1], 'WLD'
)
fn = PTRN.format(i_rer, i_ren, i_rsg, 'X', i_gsv, i_aoi)
print(fn)
img_new = (
    PTRN.format(i_rer, i_ren, i_rsg, i_fic[0], i_gsv, i_aoi),
    PTRN.format(i_rer, i_ren, i_rsg, i_fic[1], i_gsv, i_aoi)
)
# Replace and export SVG ------------------------------------------------------
fd = filedata.replace(img_org[0], img_new[0])
fd = fd.replace(img_org[1], img_new[1])
with open(path.join(path.join(PT_IMG, fn+'.svg')), "w") as text_file:
    text_file.write(fd)
###############################################################################
# Export PNG from SVG
###############################################################################
cmd = [
    'inkscape', '--export-type="png"', 
    '--export-dpi="300"', '--export-background="ffffffff"',
    path.join(PT_IMG, fn+'.svg'), 
    '--export-filename='+path.join(PT_IMG, 'panels', fn)
]
os.system(' '.join(cmd))