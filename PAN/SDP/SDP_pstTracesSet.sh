#!/bin/bash

# argv1: USR
# argv2: TRH


QNT="75"
bash ./SDP_pstTraces.sh $1 IIT $2
bash ./SDP_pstTraces.sh $1 FSR $2
bash ./SDP_pstTraces.sh $1 PGS $2
bash ./SDP_pstTraces.sh $1 AXS $2
bash ./SDP_pstTraces.sh $1 CRX $2
bash ./SDP_pstTraces.sh $1 CRY $2
bash ./SDP_pstTraces.sh $1 SDX $2
bash ./SDP_pstTraces.sh $1 SDY $2

# bash ./SDP_pstGridsSet.sh $1