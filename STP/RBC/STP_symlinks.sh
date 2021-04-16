#!/bin/bash

# declare -a EXPS=("000000" "000010")

# Data analysis root (DA) and data source root (DS) ---------------------------
BASE_DA="/RAID5/marshallShare/STP_Grid/PAN"
BASE_DS="/RAID0/STP_Grid/PAN/"

# Go through shredding drives folders -----------------------------------------
# mkdir -p "$BASE_DA"
# for exp in ${EXPS[@]};do
#     # Create links
#     src="$BASE_DS/$exp"
#     dst="$BASE_DA/$exp"
#     mkdir -p $dst
#     ln -s "$src/ANALYZED" "$dst/ANALYZED"
#     ln -s "$src/TRACE" "$dst/TRACE"
# done


find "$BASE_DS"/* -maxdepth 0 -mindepth 0 -type d | while read dir; do
    exp="$(basename $dir)"
    src="$BASE_DS/$exp"
    dst="$BASE_DA/$exp"
    mkdir -p $dst
    ln -s "$src/ANALYZED" "$dst/ANALYZED"
    ln -s "$src/TRACE" "$dst/TRACE"
done
