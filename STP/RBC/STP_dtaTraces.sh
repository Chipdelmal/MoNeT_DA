#!/bin/bash

# argv[1]: USR
# argv[2]: SX
# argv[3]: DRV

###############################################################################
# Reshape and generate output file
###############################################################################
python STP_dtaExplore.py $1 PAN HLT $3 50
python STP_dtaConverter.py $1 PAN HLT $3 50 $2 HLT
###############################################################################
# Export traces file
###############################################################################
python STP_dtaTraces.py $1 PAN HLT $3 50 HLT
# python STP_dtaTraces.py $1 PAN ECO 50 $2
 