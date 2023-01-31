#!/bin/bash

PTH_I='lab:/RAID5/marshallShare/GambiaOP'
PTH_O='/home/chipdelmal/Documents/WorkSims/GambiaOP'

EXP=("Brikama" "UpperRiver")
for idx in "${!EXP[@]}"; do
    exp="${EXP[$idx]}"
    printf "Downloading: \n\t${PTH_I}/${exp} \n\t${PTH_O}\n"
    scp -r "${PTH_I}/${exp}" "${PTH_O}"
done
