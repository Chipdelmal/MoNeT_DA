
#!/bin/bash

# argv1: USR

# bash ./SDP_preProcess.sh $1 SIT
# bash ./SDP_preProcess.sh $1 IIT
# bash ./SDP_preProcess.sh $1 FSR
bash ./SDP_preProcess.sh $1 PGS
# bash ./SDP_preProcess.sh $1 AXS
bash ./SDP_preProcess.sh $1 CRX
bash ./SDP_preProcess.sh $1 CRY
bash ./SDP_preProcess.sh $1 SDX
bash ./SDP_preProcess.sh $1 SDY
