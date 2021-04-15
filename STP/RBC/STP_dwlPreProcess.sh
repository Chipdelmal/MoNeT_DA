#!/bin/bash

declare -a EXPS=("000" "001" "002")

# Data analysis root (server DA) and data destiny (local DS) ------------------
BASE_DA="/RAID5/marshallShare/STP_Grid/PAN"
BASE_DS="/home/chipdelmal/Documents/WorkSims/STP_Grid"

# Go through shredding drives folders -----------------------------------------
for exp in ${EXPS[@]};do
    # Create links
    src="$BASE_DA/$exp"
    dst="$BASE_DS/$exp"
    mkdir -p $dst
    scp -r "lab:$src/PREPROCESS" "$dst"
done