#!/bin/bash

declare -a FLDRS=("pgSIT" "ifegenia" "IIT" "RIDL" "fsRIDL")
for fName in ${FLDRS[@]}; do
    ln -s "/RAID0/fem_pgSIT/$fName/ANALYZED" "/RAID5/marshallShare/fem_pgSIT/$fName/ANALYZED";
    ln -s "/RAID0/fem_pgSIT/$fName/TRACE" "/RAID5/marshallShare/fem_pgSIT/$fName/TRACE";
done