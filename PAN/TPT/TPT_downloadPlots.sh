#!/bin/bash

# SPE=$1 # TP13_figure_coluzii_low

EXP=("X0001" "X2500" "X5000" "X7500" "X10000")
SPE=("gambiae_0_low" "gambiae_10_low" "gambiae_20_low" "coluzzii_0_low" "coluzzii_10_low" "coluzzii_20_low" "coluzzii_0_med" "coluzzii_10_med" "coluzzii_20_med")
for idx in "${!EXP[@]}"; do
    spe="${SPE[$idx]}"
    for idx in "${!EXP[@]}"; do
        exp="${EXP[$idx]}"
        scp -r "lab:/RAID5/marshallShare/TP13_figure_$spe/$exp/img" "/home/chipdelmal/Documents/WorkSims/TP13/2023_01/TP13_figure_$spe/$exp"
    done
done