#!/bin/bash

# chmod +x YDR_preProcess.sh
if [ "$2" = "ASD" ] || [ "$2" = "XSD" ] || [ "$2" = "YSD" ]; then
	aType="homing"
fi
if [ "$2" = "AXS" ] || [ "$2" = "YXS" ]; then
	aType="shredder"
fi
python YDR_preProcess.py $1 $aType $2 ECO
python YDR_preProcess.py $1 $aType $2 HLT
python YDR_preProcess.py $1 $aType $2 WLD
python YDR_preProcess.py $1 $aType $2 TRS
