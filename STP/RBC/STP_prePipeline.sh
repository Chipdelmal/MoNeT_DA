#!/bin/bash

# argv1: User
# argv2: Land

./STP_symlinks.sh
./STP_preProcess.sh srv PAN 
./STP_preTraces.sh srv PAN 