#!/bin/bash

SPE=$1 # TP13_figure_coluzii_low


EXP=("X0001" "X2500" "X5000" "X7500" "X10000")
for idx in "${!EXP[@]}"; do
    exp="${EXP[$idx]}"
    scp -r \
        "lab:lab:/RAID5/marshallShare/$SPE/$exp/img" \ 
        "/home/chipdelmal/Documents/WorkSims/TP13/$SPE/TP13_figure_coluzii_low/$exp"
done