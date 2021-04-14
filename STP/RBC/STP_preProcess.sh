#!/bin/bash

# argv1: User
# argv2: Land

python STP_preProcess.py $1 ECO $2
python STP_preProcess.py $1 HLT $2
python STP_preProcess.py $1 WLD $2
python STP_preProcess.py $1 TRS $2