#!/bin/bash

for drv in "ifegenia_3" "ifegenia_4" "ifegenia_5" "pgSIT" # "IIT" "RDL" "RDF" 
do
    scp -r "lab:/RAID5/marshallShare/fem_pgSIT/${drv}/ML/img" "/home/chipdelmal/Documents/WorkSims/fem_pgSIT/${drv}"
    scp -r "lab:/RAID5/marshallShare/fem_pgSIT/${drv}/img/dtaTraces" "/home/chipdelmal/Documents/WorkSims/fem_pgSIT/${drv}"
done 