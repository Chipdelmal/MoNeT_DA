#!/bin/bash

# argv1: User
# argv2: Land

./STP_pstFraction.sh $1 $2
./STP_pstProcess.sh $1 $2
./STP_pstTraces.sh $1 $2