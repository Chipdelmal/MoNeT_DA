#!/bin/bash

# argv1: USR
# argv2: DRV
# argv3: TRH


QNT="75"
python SDP_pstTraces.py $1 $2 HLT 50 $3
python SDP_pstTraces.py $1 $2 WLD 50 $3
python SDP_pstTraces.py $1 $2 TRS 50 $3

python SDP_pstTraces.py $1 $2 HLT 75 $3
python SDP_pstTraces.py $1 $2 WLD 75 $3
python SDP_pstTraces.py $1 $2 TRS 75 $3

python SDP_pstTraces.py $1 $2 HLT 90 $3
python SDP_pstTraces.py $1 $2 WLD 90 $3
python SDP_pstTraces.py $1 $2 TRS 90 $3

bash ./SDP_pstGrids.sh $1 $QNT