#!/bin/bash

PTH_I='lab:/RAID5/marshallShare'
PTH_O='/home/chipdelmal/Documents/WorkSims/TP13/2023_01'


EXP=("gambiae_0_low" "gambiae_10_low" "gambiae_20_low" "coluzzii_0_low" "coluzzii_10_low" "coluzzii_20_low" "coluzzii_10_med")
for idx in "${!EXP[@]}"; do
    exp="${EXP[$idx]}"
    # echo "${PTH_I}/${exp}"
    # echo "${PTH_O}"
    scp -r "${PTH_I}/${exp}" "${PTH_O}"
done
