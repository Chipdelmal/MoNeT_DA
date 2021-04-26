#!/bin/bash

# declare -a EXPS=("000" "002" "004" "006" "008")
declare -a EXPS=("001")
declare -a HMS=("xLinked" "yLinked" "autosomal")
declare -a SHR=("autosomal" "yLinked" "CRISPR")

# Data analysis root (DA) and data source root (DS)
# BASE_DA="/RAID5/marshallShare/yLinked"
# BASE_DS="/RAID0/yLinked"
BASE_DA="/RAID5/marshallShare/yLinked2"
BASE_DS="/RAID0/yLinked2"

# Go through shredding drives folders -----------------------------------------
mkdir -p "$BASE_DA/shredder/"
for fldr in ${SHR[@]};do
    mkdir -p "$BASE_DA/shredder/$fldr"
    for exp in ${EXPS[@]};do
        # Create links
        src="$BASE_DS/shredder/$fldr/$exp"
        dst="$BASE_DA/shredder/$fldr/$exp"
	      mkdir -p $dst
        ln -s "$src/ANALYZED" "$dst/ANALYZED"
        ln -s "$src/TRACE" "$dst/TRACE"
	# unlink "$dst/TRACES"
    done
done

# Go through shredding drives folders -----------------------------------------
mkdir -p "$BASE_DA/homing/"
for fldr in ${HMS[@]};do
    mkdir -p "$BASE_DA/homing/$fldr"
    for exp in ${EXPS[@]};do
        # Create links
        src="$BASE_DS/homing/$fldr/$exp"
        dst="$BASE_DA/homing/$fldr/$exp"
	    mkdir -p $dst
        ln -s "$src/ANALYZED" "$dst/ANALYZED"
        ln -s "$src/TRACE" "$dst/TRACE"
	# unlink "$dst/TRACES"
    done
done

