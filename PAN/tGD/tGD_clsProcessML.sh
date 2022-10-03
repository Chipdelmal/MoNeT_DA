
#!/bin/bash
USR=$1
QNT=$2
THS=$3

###############################################################################
# Launch Scripts (ML)
###############################################################################
for aoi in "HLT" "CST" "WLD" "TRS"
    for mtr in "WOP" "CPT" "TTI" "TTO" "MNX"
    do
        python PGS_clsCompileML.py $USR $DRV $aoi $mtr
    done
    python PGS_clsUnifyML.py $USR $DRV $aoi $THS 
done