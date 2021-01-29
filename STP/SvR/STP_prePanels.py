#!/usr/bin/env python3

import re
import sys
import subprocess
from os import path, system
from datetime import datetime
from itertools import product
import MoNeT_MGDrivE as monet
import STP_aux as aux
import STP_functions as fun


(USR, AOI, REL, LND) = ('dsk', 'HLT', '265', 'SPA')
# (USR, AOI, REL, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
FIC = ('0000000000', '0100000000')
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, REL)
monet.makeFolder(path.join(PT_IMG, 'panels'))
###############################################################################
# Template layout
###############################################################################
template = path.join(PT_IMG, REL+'_template.svg')
with open(template, 'r') as file :
    filedata = file.read()
###############################################################################
# Replacements
###############################################################################
PTRN = 'E_{}_{}_{}_{}_{}-{}'
# Find original ids -----------------------------------------------------------
p = re.compile('E_.*png', re.IGNORECASE)
pats = re.findall(p, filedata)
img_org = list({i[:-8] for i in pats})
print(img_org)
# Replacement ids -------------------------------------------------------------
uids = fun.getExperimentsIDSets(path.join(PT_IMG, 'preTraces/'), skip=-1)
uids[2] = uids[2][1:]   # Delete the zero releases entry
expSets = set(list(product(*uids[1:-1])))
print(expSets)
###############################################################################
# Iterate
###############################################################################
tS = datetime.now()
monet.printExperimentHead(PT_ROT, PT_IMG, tS, 'UCIMI PrePanels '+AOI)
(xpNum, digs) = monet.lenAndDigits(expSets)
i = 0
exp = sorted(list(expSets))[-18]
for (i, exp) in enumerate(sorted(list(expSets))):
    monet.printProgress(i+1, xpNum, digs)
    # Get exp ids -------------------------------------------------------------
    (i_rer, i_ren, i_rsg, i_fic, i_gsv) = exp
    fn = PTRN.format(i_rer, i_ren, i_rsg, 'X', i_gsv, AOI)
    # print(fn)
    img_new = (
        PTRN.format(i_rer, i_ren, i_rsg, FIC[0], i_gsv, AOI),
        PTRN.format(i_rer, i_ren, i_rsg, FIC[1], i_gsv, AOI)
    )
    # Replace and export SVG --------------------------------------------------
    fd = filedata.replace(img_org[0], img_new[0])
    fd = fd.replace(img_org[1], img_new[1])
    with open(path.join(path.join(PT_IMG, fn+'.svg')), "w") as text_file:
        text_file.write(fd)
    ###########################################################################
    # Export PNG from SVG
    ###########################################################################
    cmd = [
        'inkscape', 
        '--export-type=png', 
        '--export-dpi=300', 
        path.join(PT_IMG, fn+'.svg'), 
        '--export-filename='+path.join(PT_IMG, 'panels', fn)
    ]
    subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)