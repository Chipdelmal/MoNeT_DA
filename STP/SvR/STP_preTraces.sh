#!/bin/bash

python STP_preTraces.py $1 ECO $2 $3 $4
python STP_preTraces.py $1 HLT $2 $3 $4
python STP_preTraces.py $1 TRS $2 $3 $4
python STP_preTraces.py $1 WLD $2 $3 $4

python STP_preGrids.py $1 $2 $3
