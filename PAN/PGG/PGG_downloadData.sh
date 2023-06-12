#!/bin/bash

PTH_I='lab:/RAID5/marshallShare/pgSIT_gFLE/'
PTH_O='/home/chipdelmal/Documents/WorkSims/PGG'
# PTH_O='/Users/sanchez.hmsc/Desktop/GOP'

EXP=("UpperRiver") # "Brikama")
for idx in "${!EXP[@]}"; do
    exp="${EXP[$idx]}"
    printf "Downloading: \n\t${PTH_I}/${exp} \n\t${PTH_O}\n"
    scp -r "${PTH_I}/${exp}" "${PTH_O}"
done
