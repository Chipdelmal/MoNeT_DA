#!/bin/bash

# argv1: USR
# argv2: DRV
# argv3: TRH

expSet=$(./YDR_selector.sh $2)
python YDR_pstTraces.py $1 $expSet $2 HLT 50 $3
python YDR_pstTraces.py $1 $expSet $2 WLD 50 $3
python YDR_pstTraces.py $1 $expSet $2 TRS 50 $3

