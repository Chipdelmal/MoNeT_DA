#!/bin/bash

declare -a EXPS=("000" "002" "004" "006" "008")
declare -a HMS=("autosomal" "xLinked" "yLinked")
declare -a SHR=("autosomal" "yLinked" "CRISPR")

# Data analysis root (DA) and data source root (DS)
BASE_DA="/RAID5/marshallShare/yLinked"
BASE_DS="/RAID0/yLinked"

# BASE_DA="/home/chipdelmal/Desktop/yDrive"
# BASE_DS="./yDrive"

# Go through shredding drives folders -----------------------------------------
mkdir -p "$BASE_DA/shredding/"
for fldr in ${SHR[@]};do
    mkdir -p "$BASE_DA/shredding/$fldr"
    for exp in ${EXPS[@]};do
        # Create links
        src="$BASE_DS/shredding/$fldr/$exp"
        dst="$BASE_DA/shredding/$fldr/$exp"
        ln -s "$src/ANALYZED" "$dst/ANALYZED"
        ln -s "$src/TRACES" "$dst/TRACES"
    done
done

# Go through homing drives folders --------------------------------------------
# mkdir -p "$BASE_DA/homing/"
# for fldr in ${HMS[@]};do
#     mkdir -p "$BASE_DA/homing/$fldr"
#     for exp in ${EXPS[@]};do
#         # Create links
#         src="$BASE_DS/homing/$fldr/$exp"
#         dst="$BASE_DA/homing/$fldr/$exp"
#         ln -s "$src/ANALYZED" "$dst/ANALYZED"
#         ln -s "$src/TRACES" "$dst/TRACES"
#     done
# done

