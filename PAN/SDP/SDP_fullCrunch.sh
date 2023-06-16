#!/bin/bash

# argv1: USR
# argv2: DRV

bash SDP_preProcessSet.sh $1
bash SDP_pstFractionSet.sh $1
bash SDP_pstProcessSet.sh $1
bash SDP_pstTracesSet.sh $1
bash SDP_dtaProcessSet.sh $1 "HLT"