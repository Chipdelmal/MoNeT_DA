#!/bin/bash

# argv[1]: USR
# argv[2]: SX

###############################################################################
# Reshape and generate output file
###############################################################################
python STP_dtaExplore.py $1 PAN HLT 50
python STP_dtaConverter.py $1 PAN HLT 50 $2
###############################################################################
# Export traces file
###############################################################################
python STP_dtaTraces.py $1 PAN HLT 50 $2
# python STP_dtaTraces.py $1 PAN ECO 50 $2
