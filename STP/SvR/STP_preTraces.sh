#!/bin/bash

python STP_preTraces.py $1 ECO $2 $3
python STP_preTraces.py $1 HLT $2 $3
python STP_preTraces.py $1 TRS $2 $3
python STP_preTraces.py $1 WLD $2 $3