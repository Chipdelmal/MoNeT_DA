
import cv2
import numpy as np
from glob import glob
from os import path
import MoNeT_MGDrivE as monet
import TRP_aux as aux

if monet.isNotebook():
    (EXP_FNAME, TRAPS_NUM) = ('BASE-100', 1)
    (PT_DTA, PT_GA, PT_IMG) = aux.selectPaths('dsk')
else:
    (EXP_FNAME, TRAPS_NUM) = (argv[1], int(argv[2]))
    (PT_DTA, PT_GA, PT_IMG) = aux.selectPaths(argv[3])
###############################################################################
# Load and concatenate images
############################################################################### 
homFiles = sorted(glob(path.join(PT_IMG, EXP_FNAME+'*HOM*')))
hetFiles = sorted(glob(path.join(PT_IMG, EXP_FNAME+'*HET*')))
i=1
for i in range(2): # range(len(homFiles)):
    (homImg, hetImg) = (
        cv2.imread(homFiles[i]),
        cv2.imread(hetFiles[i])
    )
    im_v = cv2.hconcat([homImg, hetImg])
    fName = homFiles[i].split('/')[-1]
    fName = fName.replace('-HOM', '')
    cv2.imwrite(path.join(PT_IMG, fName), im_v)