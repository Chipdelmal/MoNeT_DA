#!/bin/bash

PTH_I='lab:/RAID5/marshallShare'
PTH_O='/home/chipdelmal/Documents/WorkSims/TP13/2023_01'

EXP=("coluzzii_0_med" "coluzzii_10_med" "coluzzii_20_med" "gambiae_0_low" "gambiae_10_low" "gambiae_20_low" "coluzzii_0_low" "coluzzii_10_low" "coluzzii_20_low")
for idx in "${!EXP[@]}"; do
    exp="${EXP[$idx]}"
    printf "Downloading: \n\t${PTH_I}/TP13_figure_${exp} \n\t${PTH_O}\n"
    scp -r "${PTH_I}/TP13_figure_${exp}" "${PTH_O}"
done
