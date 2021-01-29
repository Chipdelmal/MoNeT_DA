#!/bin/bash

# python STP_pstFraction.py 'srv' 'HLT' '106' 'SPA'
python STP_pstFraction.py $1 HLT $2 $3
python STP_pstFraction.py $1 TRS $2 $3
python STP_pstFraction.py $1 WLD $2 $3

python STP_pstProcess.py $1 HLT $2 $3
python STP_pstProcess.py $1 TRS $2 $3
python STP_pstProcess.py $1 WLD $2 $3


if [ "$4" = "True" ]; then
    ./STP_pstTraces.sh "$@"
fi
