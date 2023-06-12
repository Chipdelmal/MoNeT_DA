#!/bin/bash

USR=$1

###############################################################################
# Setup Path
###############################################################################
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
###############################################################################
# Launch Scripts
###############################################################################
for lnd in "UpperRiver"
do
    bash GOP_preProcess.sh $USR $lnd "PGS"
    bash GOP_preProcessEpi.sh $USR $lnd "HUM"
done