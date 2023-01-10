#!/bin/bash

for drv in "ifegenia_3" "ifegenia_4" "ifegenia_5" "pgSIT" # "IIT" "RIDL" "fsRIDL" 
do
    scp -r "lab:/RAID5/marshallShare/fem_pgSIT/${drv}/ML/img/heat" "/home/chipdelmal/Documents/WorkSims/fem_pgSIT/${drv}/"
    scp -r "lab:/RAID5/marshallShare/fem_pgSIT/${drv}/img/dtaTraces" "/home/chipdelmal/Documents/WorkSims/fem_pgSIT/${drv}"
    scp -r "lab:/RAID5/marshallShare/fem_pgSIT/${drv}/img/preTraces" "/home/chipdelmal/Documents/WorkSims/fem_pgSIT/${drv}"
done 
