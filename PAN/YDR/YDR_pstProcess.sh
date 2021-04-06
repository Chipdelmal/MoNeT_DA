#!/bin/bash

# argv1: User
# argv2: Gene Drive

expSet=$(./YDR_selector.sh $2)

QNT="75"
python YDR_pstProcess.py $1 $expSet $2 HLT $QNT
python YDR_pstProcess.py $1 $expSet $2 TRS $QNT
python YDR_pstProcess.py $1 $expSet $2 WLD $QNT
