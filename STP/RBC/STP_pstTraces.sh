#!/bin/bash

# argv1: User
# argv2: Land

QNT='90'
THS='0.75'
python STP_pstTraces.py $1 HLT $2 $QNT $THS
python STP_pstTraces.py $1 WLD $2 $QNT $THS
python STP_pstTraces.py $1 TRS $2 $QNT $THS

python STP_pstGrids.py $1 $2 $QNT