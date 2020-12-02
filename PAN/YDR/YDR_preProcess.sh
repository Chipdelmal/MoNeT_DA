#!/bin/bash

# chmod +x YDR_preProcess.sh
python YDR_preProcess.py $1 $2 $3 ECO
python YDR_preProcess.py $1 $2 $3 HLT
python YDR_preProcess.py $1 $2 $3 WLD
python YDR_preProcess.py $1 $2 $3 TRS
