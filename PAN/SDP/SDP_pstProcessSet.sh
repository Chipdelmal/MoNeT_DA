#!/bin/bash

# argv1: USR

bash ./SDP_pstProcess.sh $1 SDR
bash ./SDP_pstProcess.sh $1 CRS
bash ./SDP_pstProcess.sh $1 SDR
bash ./SDP_pstProcess.sh $1 IIT
bash ./SDP_pstProcess.sh $1 PGS
bash ./SDP_pstProcess.sh $1 FSR
bash ./SDP_pstProcess.sh $1 AXS
bash ./SDP_pstProcess.sh $1 SIT