#!/bin/bash

# argv1: Imageset folder

declare -a EXPS=("000000" "000010")

# Data analysis root (server DA) and data destiny (local DS) ------------------
BASE_DA="/RAID5/marshallShare/STP_Grid/PAN"
BASE_DS="/home/chipdelmal/Documents/WorkSims/STP_Grid/PAN"

# Go through shredding drives folders -----------------------------------------
for exp in ${EXPS[@]};do
    # Create links
    src="$BASE_DA/$exp"
    dst="$BASE_DS/$exp"
    mkdir -p $dst
    scp -r "lab:$src/img/$1" "$dst/img/"
done