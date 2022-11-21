#!/bin/bash

DRIVES=("LDR" "SDR")
SPATIAL=("265_DF" "265_DP" "265_DR" "265_DS" "265_SF" "265_SP" "265_SR" "265_SS")
###############################################################################
# Download Geo
###############################################################################
if true; then
    echo "--------- Downloading GEO ---------"
    scp -r \
        "lab:/RAID5/marshallShare/STP_Grid/GEO"  \
        "/home/chipdelmal/Documents/WorkSims/STP_new/"
    scp -r \
        "lab:/RAID5/marshallShare/STP_Grid/GEO_v2_Debug"  \
        "/home/chipdelmal/Documents/WorkSims/STP_new/"
fi
###############################################################################
# Download Panmictic
###############################################################################
if false; then
    for idx in "${!DRIVES[@]}"; do
        drive="${DRIVES[$idx]}"
        echo "--------- Downloading ${drive}:PAN ---------"
        scp -r \
            "lab:/RAID5/marshallShare/STP_Grid/$drive/PAN/000000/img/preTraces"  \
            "/home/chipdelmal/Documents/WorkSims/STP_new/$drive/PAN/000000/img"
        scp -r \
            "lab:/RAID5/marshallShare/STP_Grid/$drive/PAN/000000/img/dtaTraces"  \
            "/home/chipdelmal/Documents/WorkSims/STP_new/$drive/PAN/000000/img"
        scp -r \
            "lab:/RAID5/marshallShare/STP_Grid/$drive/PAN/ML/img/" \
            "/home/chipdelmal/Documents/WorkSims/STP_new/$drive/PAN/ML"
    done
fi
###############################################################################
# Download Spatial
###############################################################################
if true; then
    for idx in "${!DRIVES[@]}"; do
        drive=${DRIVES[$idx]} 
        for jdx in "${!SPATIAL[@]}"; do
            spatial=${SPATIAL[$idx]} 
            echo "--------- Downloading ${drive}:${spatial} ---------"
            scp -r \
                "lab:/RAID5/marshallShare/STP_Grid/$drive/SPA/$spatial/img/preTraces/*.png"  \
                "/home/chipdelmal/Documents/WorkSims/STP_new/$drive/SPA/$spatial/img/preTraces/"
            scp -r \
                "lab:/RAID5/marshallShare/STP_Grid/$drive/SPA/$spatial/img/pstTraces/*.png"  \
                "/home/chipdelmal/Documents/WorkSims/STP_new/$drive/SPA/$spatial/img/pstTraces/"
        done
    done
fi

