#!/usr/bin/env python3

import fileinput


template = '/home/chipdelmal/Documents/WorkSims/STP/SPA/106/img/106_template.svg'
(_, i_rer, i_ren, i_rsg, i_fic, i_gsv, i_aoi) = (
    '0025000000', '03', '0000000000',
    '0000000000', '0000000000', '0000000000',
    'HLT'
)
ptrn = 'E_{}_{}_{}_{}_{}-{}_{}'

pth = "/home/chipdelmal/Documents/WorkSims/STP/SPA/106/img/preTraces/E_0025000000_03_0000000000_0000000000_0000000000-HLT_003.png"
# Replace string
imgRef = pth.split('/')
(imgPth, imgNme) = ('/'.join(imgRef[:-1]), imgRef[-1])
ptrn.format(i_rer, i_ren, i_rsg, i_fic, i_gsv, i_aoi, imgNme[-7:])

