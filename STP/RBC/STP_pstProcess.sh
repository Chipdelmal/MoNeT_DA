#!/bin/bash

QNT='90'
python STP_pstProcess.py $1 HLT $2 $QNT
python STP_pstProcess.py $1 WLD $2 $QNT
python STP_pstProcess.py $1 TRS $2 $QNT