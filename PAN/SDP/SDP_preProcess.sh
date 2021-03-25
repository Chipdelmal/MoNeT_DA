#!/bin/bash

# argv1: USR
# argv2: DRV

python SDP_preProcess.py $1 $2 ECO
python SDP_preProcess.py $1 $2 HLT
python SDP_preProcess.py $1 $2 WLD
python SDP_preProcess.py $1 $2 TRS