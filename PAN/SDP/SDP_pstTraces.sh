#!/bin/bash

# argv1: USR
# argv2: DRV
# argv3: TRH


QNT="50"
python SDP_pstTraces.py $1 $2 HLT $QNT $3
# python SDP_pstTraces.py $1 $2 WLD $QNT $3
# python SDP_pstTraces.py $1 $2 TRS $QNT $3

python SDP_pstGrids.py $1 $2 $QNT