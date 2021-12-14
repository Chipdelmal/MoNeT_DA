#!/bin/bash

USR=$1
XID=$2
LND=$3
TRP=$4

./SXK_SexLandscape.sh $USR $XID $LND $TRP
./SXK_SexGA.sh $USR $XID $LND $TRP
./SXK_SexPlot.sh $USR $XID $LND $TRP
./SXK_SexStack.sh $USR $XID $LND $TRP
