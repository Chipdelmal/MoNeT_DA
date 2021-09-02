
#!/bin/bash
# argv1: USR

bash ./SDP_preTraces.sh $1 SIT
bash ./SDP_preTraces.sh $1 IIT
bash ./SDP_preTraces.sh $1 FSR
bash ./SDP_preTraces.sh $1 PGS
bash ./SDP_preTraces.sh $1 AXS
bash ./SDP_preTraces.sh $1 CRS
bash ./SDP_preTraces.sh $1 CRX
bash ./SDP_preTraces.sh $1 CRY
bash ./SDP_preTraces.sh $1 SDR
bash ./SDP_preTraces.sh $1 SDX
bash ./SDP_preTraces.sh $1 SDY

bash ./SDP_preGridsSet.sh $1
