# pgSIT & Femaless

One-node analysis of pgSIT efficacy as compared to other sterile insect techniques. Drive codes are:

* `PGS`: pgSIT
* `FML`: Femaless


Original path for the experiments is: `/RAID0/pgSIT`. Where the experiments' filename key is `E_ren_rer_...` with:

* `ren`: number of releases
* `rer`: size of the releases


## Symlinks on Server

```bash
ln -s /RAID0/fem_pgSIT/pgSIT/ANALYZED /RAID5/marshallShare/fem_pgSIT/pgSIT/ANALYZED;\
ln -s /RAID0/fem_pgSIT/pgSIT/TRACE /RAID5/marshallShare/fem_pgSIT/pgSIT/TRACE;
```