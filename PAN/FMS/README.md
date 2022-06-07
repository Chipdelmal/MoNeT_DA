# pgSIT & Femaless

One-node analysis of pgSIT efficacy as compared to other sterile insect techniques. Drive codes are:

* `PGS`: pgSIT
* `FML`: Femaless


Original path for the experiments is: `/RAID0/pgSIT`. Where the experiments' filename key is `E_ren_rer_...` with:

* `ren`: number of releases
* `rer`: size of the releases


## Symlinks on Server

```bash
declare -a StringArray=("pgSIT" )

for fName in ${StringArray[@]}; do
    ln -s "/RAID0/fem_pgSIT/{$fName}/ANALYZED" "/RAID5/marshallShare/fem_pgSIT/{$fName}/ANALYZED";
    ln -s "/RAID0/fem_pgSIT/{$fName}/TRACE" "/RAID5/marshallShare/fem_pgSIT/{$fName}/TRACE";
done
```