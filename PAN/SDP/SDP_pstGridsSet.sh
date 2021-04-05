#!/bin/bash

# argv1: User

QNT="50"

python SDP_pstGrids.py $1 SDR $QNT
python SDP_pstGrids.py $1 CRS $QNT
python SDP_pstGrids.py $1 SDR $QNT
python SDP_pstGrids.py $1 IIT $QNT
python SDP_pstGrids.py $1 PGS $QNT
python SDP_pstGrids.py $1 FSR $QNT
python SDP_pstGrids.py $1 AXS $QNT
python SDP_pstGrids.py $1 SIT $QNT