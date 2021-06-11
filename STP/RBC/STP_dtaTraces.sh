#!/bin/bash

###############################################################################
# Reshape and generate output file
###############################################################################
python STP_dtaExplore.py $1 PAN HLT 50
python STP_dtaConverted.py $1 PAN HLT 50
###############################################################################
# Export traces file
###############################################################################
python STP_dtaTraces.py $1 PAN HLT 50 SX
python STP_dtaTraces.py $1 PAN ECO 50 SX