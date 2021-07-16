#!/bin/bash

TYP=$1
##############################################################################
# ML csvs
##############################################################################
if [[ "$TYP" = "ML" ]]; then
    scp -r lab:/RAID5/marshallShare/STP_Grid/LDR/PAN/ML/*.csv /home/chipdelmal/Documents/WorkSims/STP_Grid/LDR/PAN/ML
fi
##############################################################################
# ML csvs
##############################################################################
if [[ "$TYP" = "DICE" ]]; then
    scp -r lab:/RAID5/marshallShare/STP_Grid/LDR/PAN/ML/img/*.png /home/chipdelmal/Documents/WorkSims/STP_Grid/LDR/PAN/ML/img
fi
##############################################################################
# ML csvs
##############################################################################
if [[ "$TYP" = "PRE" ]]; then
    scp -r lab:/RAID5/marshallShare/STP_Grid/LDR/PAN/000000/img/preTraces/ /home/chipdelmal/Documents/WorkSims/STP_Grid/LDR/PAN/000000/img/
fi
##############################################################################
# ML csvs
##############################################################################
if [[ "$TYP" = "DTA" ]]; then
    scp -r lab:/RAID5/marshallShare/STP_Grid/LDR/PAN/000000/img/dtaTraces/ /home/chipdelmal/Documents/WorkSims/STP_Grid/LDR/PAN/000000/img/
fi