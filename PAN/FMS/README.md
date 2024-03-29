# pgSIT & Femaless

These scripts run the pipelines for the datasets generated by [Ifegenia & pgSIT MGDrivE simulations](https://github.com/Chipdelmal/MGDrivE/tree/master/Main/pgSIT_Femaless).

## Drive Codes

One-node analysis of pgSIT efficacy as compared to other sterile insect techniques. Drive codes are:

* `PGS`: pgSIT
* `FML3`: Ifegenia (1 target site)
* `FML4`: Femaless (2 target site)
* `FML5`: Femaless (3 target site)
* `IIT`: Incompatible Insect Technique
* `RDF`: Female-Specific RIDL Technique
* `RDL`: RIDL

## Experimental Setup

The experiments' filename key is `E_ren_rer_...` with:

* `ren (1e0, 2)`: number of releases
* `rer (1e3, 4)`: size of the releases

## Data Paths

Base directories for output and analysis:

* Data: `/RAID0/fem_pgSIT/{drive}/`
* Analysis: `/RAID5/marshallShare/fem_pgSIT/{drive}/`

With the symlinked paths being:

* `/RAID5/marshallShare/fem_pgSIT/{drive}/ANALYZED` to `/RAID0/fem_pgSIT/{drive}/ANALYZED`
* `/RAID5/marshallShare/fem_pgSIT/{drive}/TRACE` to `/RAID0/fem_pgSIT/{drive}/TRACE`


## Pipelines

For the full data pipeline on all the drives, run:

```bash
./FMS_fullPipe.sh srv 50 0.1
```

This will launch all the required analyses for all drives, namely:

```bash
bash FMS_preCrunch.sh $USR $drv
bash FMS_pstCrunch.sh $USR $drv $QNT
bash FMS_clsCrunch.sh $USR $drv $QNT HLT $THS
bash FMS_dtaTraces.sh $USR $drv $QNT HLT $THS HLT
```

### PreProcess

```bash
./FMS_preCrunch.sh srv PGS
./FMS_preCrunch.sh srv FMS3
./FMS_preCrunch.sh srv FMS4
./FMS_preCrunch.sh srv FMS5
```

### PstProcess

```bash
./FMS_pstCrunch.sh srv PGS 50
./FMS_pstCrunch.sh srv FMS3 50
./FMS_pstCrunch.sh srv FMS4 50
./FMS_pstCrunch.sh srv FMS5 50
```

### ClsProcess

```bash
./FMS_clsCrunch.sh srv PGS 50 HLT 0.1
./FMS_clsCrunch.sh srv FMS3 50 HLT 0.1
./FMS_clsCrunch.sh srv FMS4 50 HLT 0.1
./FMS_clsCrunch.sh srv FMS5 50 HLT 0.1
```



## Download Results

```bash
scp -r lab:/RAID5/marshallShare/fem_pgSIT/ifegenia_5/img '/home/chipdelmal/Documents/WorkSims/fem_pgSIT/2022_08/ifegenia_5'
scp -r lab:/RAID5/marshallShare/fem_pgSIT/ifegenia_3/ML/img/heat '/home/chipdelmal/Documents/WorkSims/fem_pgSIT/2022_08/ifegenia_3/img'
```