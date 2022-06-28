#!/bin/bash

USR=$1
QNT=$2
THS=$3

###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
for drv in "IIT" "RDL" "RDF" "PGS" "FMS3" "FMS4" "FMS5"
do
    bash FMS_preCrunch.sh $USR $drv
    bash FMS_pstCrunch.sh $USR $drv $QNT
    bash FMS_clsCrunch.sh $USR $drv $QNT HLT $THS
done