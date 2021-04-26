#!/bin/bash

# argv1: Folder in base dir

declare -a EXPS=("000000" "000010")

# Data analysis root (server DA) and data destiny (local DS) ------------------
BASE_DA="/RAID5/marshallShare/STP_Grid/PAN"
BASE_DS="/home/chipdelmal/Documents/WorkSims/STP_Grid/PAN"

mkdir $BASE_DS
# Go through shredding drives folders -----------------------------------------
for exp in ${EXPS[@]};do
    # Create links
    src="$BASE_DA/$exp"
    dst="$BASE_DS/$exp"
    mkdir -p $dst
    scp -r "lab:$src/$1" "$dst"
done