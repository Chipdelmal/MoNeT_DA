#!/bin/bash

# argv1: USR
# argv2: DRV

QNT="75"
python SDP_pstProcess.py $1 $2 HLT $QNT
python SDP_pstProcess.py $1 $2 WLD $QNT
python SDP_pstProcess.py $1 $2 TRS $QNT

