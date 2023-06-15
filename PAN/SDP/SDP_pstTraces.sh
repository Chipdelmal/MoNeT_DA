#!/bin/bash

# argv1: USR
# argv2: DRV
# argv3: TRH


QNT="50"
THS="0.1"

python SDP_pstTraces.py $1 $2 HLT $QNT $THS
python SDP_pstTraces.py $1 $2 WLD $QNT $THS
python SDP_pstTraces.py $1 $2 TRS $QNT $THS

python SDP_pstGrids.py $1 $2 $QNT