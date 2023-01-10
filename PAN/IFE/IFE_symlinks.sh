#!/bin/bash

declare -a FLDRS=("fsRIDL") #"pgSIT" "ifegenia" "IIT" "RIDL" "fsRIDL" "ifegenia_3" "ifegenia_4" "ifegenia_5" "ifegenia_6")
for fName in ${FLDRS[@]}; do
    ln -s "/RAID0/fem_pgSIT/$fName/ANALYZED" "/RAID5/marshallShare/fem_pgSIT/$fName/ANALYZED";
    ln -s "/RAID0/fem_pgSIT/$fName/TRACE" "/RAID5/marshallShare/fem_pgSIT/$fName/TRACE";
done