#!/bin/bash

# argv1: USR
# argv2: DRV

python SDP_pstProcess.py $1 $2 HLT 50
python SDP_pstProcess.py $1 $2 WLD 50
python SDP_pstProcess.py $1 $2 TRS 50

python SDP_pstProcess.py $1 $2 HLT 75
python SDP_pstProcess.py $1 $2 WLD 75
python SDP_pstProcess.py $1 $2 TRS 75

python SDP_pstProcess.py $1 $2 HLT 90
python SDP_pstProcess.py $1 $2 WLD 90
python SDP_pstProcess.py $1 $2 TRS 90