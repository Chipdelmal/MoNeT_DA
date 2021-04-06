#!/bin/bash

# argv1: USR
# argv2: DRV
# argv3: TRH

QNT="50"
expSet=$(./YDR_selector.sh $2)
python YDR_pstTraces.py $1 $expSet $2 HLT $QNT $3
python YDR_pstTraces.py $1 $expSet $2 WLD $QNT $3
python YDR_pstTraces.py $1 $expSet $2 TRS $QNT $3

python YDR_pstGrids.py $1 $expSet $2 $QNT

# bash ./YDR_preGrids.sh $1 $2