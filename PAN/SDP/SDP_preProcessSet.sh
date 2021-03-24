
#!/bin/bash

# argv1: USR
# argv2: DRV

bash ./SDP_preProcess.sh $1 SDR
bash ./SDP_preProcess.sh $1 CRS
bash ./SDP_preProcess.sh $1 SDR
bash ./SDP_preProcess.sh $1 IIT
bash ./SDP_preProcess.sh $1 PGS
bash ./SDP_preProcess.sh $1 FSR
bash ./SDP_preProcess.sh $1 AXS
bash ./SDP_preProcess.sh $1 SIT