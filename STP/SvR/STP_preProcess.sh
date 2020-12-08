#!/bin/bash

python STP_preProcess.py $1 ECO $2 $3 $4
python STP_preProcess.py $1 HLT $2 $3 $4
python STP_preProcess.py $1 TRS $2 $3 $4
python STP_preProcess.py $1 WLD $2 $3 $4

if [ "$4" = "True" ]; then
    ./STP_preTraces.sh "$@"
fi