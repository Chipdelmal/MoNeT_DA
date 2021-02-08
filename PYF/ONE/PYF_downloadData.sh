
#!/bin/bash

# argv1: LND
# argv2: Data bool
# argv3: Plots bool

BASE="/home/chipdelmal/Documents/WorkSims"

if [ "$2" = "True" ]; then
    scp -r "lab:/RAID5/marshallShare/pyf/${1}/PREPROCESS" "${BASE}/PYF/Onetahi/sims/${1}/"
    scp -r "lab:/RAID5/marshallShare/pyf/${1}/POSTPROCESS" "${BASE}/PYF/Onetahi/sims/${1}/"
    scp -r "lab:/RAID5/marshallShare/pyf/${1}/SUMMARY" "${BASE}/PYF/Onetahi/sims/${1}/"
fi

if [ "$3" = "True" ]; then
    scp -r "lab:/RAID5/marshallShare/pyf/${1}/img/preTraces" "${BASE}/PYF/Onetahi/sims/${1}/img/"
    scp -r "lab:/RAID5/marshallShare/pyf/${1}/img/pstTraces" "${BASE}/PYF/Onetahi/sims/${1}/img/"
    scp -r "lab:/RAID5/marshallShare/pyf/${1}/img/pstHeatmap" "${BASE}/PYF/Onetahi/sims/${1}/img/"
fi