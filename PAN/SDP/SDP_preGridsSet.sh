

#!/bin/bapy

# argv1: USR

python SDP_preGrids.py $1 SDR
python SDP_preGrids.py $1 CRS
python SDP_preGrids.py $1 SDR
python SDP_preGrids.py $1 IIT
python SDP_preGrids.py $1 PGS
python SDP_preGrids.py $1 FSR
python SDP_preGrids.py $1 AXS
python SDP_preGrids.py $1 SIT