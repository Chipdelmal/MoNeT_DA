#!/bin/bash

# argv1: USR
# argv2: DRV
# argv3: TRH

expSet=$(./YDR_selector.sh $2)

QNT="50"
python YDR_pstTraces.py $1 $expSet $2 HLT $QNT $3
python YDR_pstTraces.py $1 $expSet $2 WLD $QNT $3
python YDR_pstTraces.py $1 $expSet $2 TRS $QNT $3
