#!/bin/bash

# argv1: USR
USR=$1
AOI=$2
QNT="50"
THS="0.1"

# bash ./SDP_pstFraction.sh $1 IIT
# bash ./SDP_pstFraction.sh $1 FSR
# bash ./SDP_pstFraction.sh $1 AXS
bash ./SDP_dtaProcess.sh $1 "PGS" $2 $QNT $THS
# bash ./SDP_dtaProcess.sh $1 "SDX" $2 $QNT $THS
# bash ./SDP_dtaProcess.sh $1 "SDY" $2 $QNT $THS
# bash ./SDP_pstFraction.sh $1 SDX
# bash ./SDP_pstFraction.sh $1 SDY
# bash ./SDP_pstFraction.sh $1 CRX
# bash ./SDP_pstFraction.sh $1 CRY