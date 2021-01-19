#!/usr/bin/env python3

# 'inkscape --export-type="png" --export-dpi="300" --export-background="ffffffff" 106_template.svg --export-filename="test.png"'

import re


PTRN = 'E_{}_{}_{}_{}_{}-{}'

###############################################################################
# Template layout
###############################################################################
template = '/home/chipdelmal/Documents/WorkSims/STP/SPA/106/img/106_template.svg'
with open(template, 'r') as file :
  filedata = file.read()
###############################################################################
# Replacements
###############################################################################
# Find original ids -----------------------------------------------------------
p = re.compile('E_.*png', re.IGNORECASE)
pats = re.findall(p, filedata)
img_org = {i[:-8] for i in pats}

(_, i_rer, i_ren, i_rsg, i_fic, i_gsv, i_aoi) = (
    '0025000000', '03', '0000000000',
    '0000000000', ('0000000000', '0100000000'), '0000000000',
    'HLT'
)
img_new = (
    PTRN.format(i_rer, i_ren, i_rsg, i_fic[0], i_gsv, i_aoi),
    PTRN.format(i_rer, i_ren, i_rsg, i_fic[1], i_gsv, i_aoi)
)
fd = filedata.replace(img_org[0], img_new[0])
fd = fd.replace(img_org[1], img_new[1])

i_fic

pth = "/home/chipdelmal/Documents/WorkSims/STP/SPA/106/img/preTraces/E_0025000000_03_0000000000_0000000000_0000000000-HLT_003.png"
# Replace string
imgRef = pth.split('/')
(imgPth, imgNme) = ('/'.join(imgRef[:-1]), imgRef[-1])
ptrn.format(i_rer, i_ren, i_rsg, i_fic[0], i_gsv, i_aoi, imgNme[-7:])
ptrn.format(i_rer, i_ren, i_rsg, i_fic[1], i_gsv, i_aoi, imgNme[-7:])


