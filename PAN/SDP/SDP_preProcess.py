
import sys
import YDR_aux as aux
import YDR_gene as drv
import YDR_land as lnd
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed

if monet.isNotebook():
    (USR, DRV, AOI) = ('dsk', 'PGS', 'HLT')
    (OVW, JOB) = (True, 4)
else:
    (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
    (OVW, JOB) = (True, 8)