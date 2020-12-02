#!/bin/bash

# chmod +x YDR_preProcess.sh
expSet=$(./YDR_selector.sh $2)
python YDR_preProcess.py $1 $aType $2 ECO
python YDR_preProcess.py $1 $aType $2 HLT
python YDR_preProcess.py $1 $aType $2 WLD
python YDR_preProcess.py $1 $aType $2 TRS
