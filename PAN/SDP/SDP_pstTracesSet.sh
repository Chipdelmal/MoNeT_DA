#!/bin/bash

# argv1: USR
# argv2: TRH

bash ./SDP_pstTraces.sh $1 SDR $2
bash ./SDP_pstTraces.sh $1 CRS $2
bash ./SDP_pstTraces.sh $1 SDR $2
bash ./SDP_pstTraces.sh $1 IIT $2
bash ./SDP_pstTraces.sh $1 PGS $2
bash ./SDP_pstTraces.sh $1 FSR $2
bash ./SDP_pstTraces.sh $1 AXS $2
bash ./SDP_pstTraces.sh $1 SIT $2