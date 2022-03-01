# São Tomé and Príncipe

Information about all the routines needed for the paper.

<hr>

## Simulations

The scripts required to generate the datasets for these experiments can be found at:

* Panmictic [LDR](https://github.com/Chipdelmal/MGDrivE/blob/master/Main/STP/STP_Grid_LDR.R) and [SDR](https://github.com/Chipdelmal/MGDrivE/blob/master/Main/STP/STP_Grid_SDR.R)
* Spatial [LDR](https://github.com/Chipdelmal/MGDrivE/blob/master/Main/STP/STP_Spatial_LDR.R) and [SDR](https://github.com/Chipdelmal/MGDrivE/blob/master/Main/STP/STP_Spatial_SDR.R)

With the gene-cubes being [LDR drive](https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-CRISPR2MF.R) and [SDR drive](https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-SplitDriveMF.R).

These scripts export data to the following directories on the server:

* Panmictic raw data: `/RAID0/STP_Space_{LDR,SDR}/`
* Spatial raw data: `/RAID0/STP_Grid/{LDR,SDR}/PAN/000000/`

Which are symlinked from these locations for data analysis:

* Panmictic analysis: `/RAID5/marshallShare/STP_Grid/{LDR,SDR}/SPA/265_{S,D}{F,P,S}/`
* Spatial analysis: `/RAID5/marshallShare/STP_Grid/{LDR,SDR}/PAN/000000`

Where the first ID is: `{S: South releases, D: Study sites}`; and the second one: `{P: two clusters,  S: fifteen clusters (for plots), F: seventy-five clusters (for videos)}`.

## Data Analysis

To run the PRE phases of the DA pipelines (HLT only), use the following bash script:

```bash
./STP_crunchDataset.sh $USR "LDR" "PAN" $DCE
./STP_crunchDataset.sh $USR "SDR" "PAN" $DCE
./STP_crunchDataset.sh $USR "LDR" "SPA" $DCE
./STP_crunchDataset.sh $USR "SDR" "SPA" $DCE
```

Note that if `$DCE` is `True` it might take a while to export the plots (depending on the selected sampling fraction).

If WLD, ECO, HLT, and TRS, run:

```bash
./STP_preProcess.sh $USR $LND $DRV
```

All of the heatmaps used for publication are generated through the following commands:

```bash
./STP_dtaHeatmap.sh $USR "LDR"
./STP_dtaHeatmap.sh $USR "SDR"
```

exporting the results to the `[DATA SOURCE]/../ML/img/heat/` directories. Whereas all the accompanying releases curves are generated through:

```bash
python STP_dtaRelCompare.py $USR "PAN" "HLT" "LDR" 50
python STP_dtaSexCompare.py $USR "PAN" "HLT" "LDR" 50
python STP_dtaRelCompare.py $USR "PAN" "HLT" "SDR" 50
python STP_dtaSexCompare.py $USR "PAN" "HLT" "SDR" 50
```

which export the data at `[DATA SOURCE]/../ML/img/`. 

## PstTraces for Spatial

To generate all the `pstTraces` sets (HLT, WLD, TRS) run:

```bash
./STP_preProcess.sh $USR $LND $DRV
./STP_pstFraction.sh $USR $LND $DRV
./STP_pstProcess.sh $USR $LND $DRV
./STP_pstTraces.sh $USR $LND $DRV
```

with the `SUBSAMPLE` value set to `1` in order to plot every trace.

## Classifier (ML)

For the full classifier routine run:

```bash
./STP_clsPipeline.sh $USR LDR 50 True
./STP_clsPipeline.sh $USR SDR 50 True
```

after having the `STP_crunchDataset.sh` run for both SDR and LDR, PAN sets. This will generate the model, plots and summaries (feature importance) needed for the analysis.

<hr>

## Namefile

`E_sex_ren_res_rsg_gsv_fch_fcb_fcr_hrm_hrf`

## Inputs

* `sex (1e00)`: released mosquitos sex
  * `sxm`: male
  * `sxg`: gravid female (mixed)
  * `sxn`: non-gravid female (mixed)
* `ren (1e00)`: releases number
* `res (1e03)`: releases size
* `rsg (1e10)`: resistance generation
* `gsv (1e10)`: genetic standing variation
* `fch (1e05)`: fitness cost on drive
* `fcb (1e05)`: fitness cost on out-of-frame resistance
* `fcr (1e05)`: fitness cost on in-frame resistance
* `hrm (1e05)`: homing rate male
* `hrt (1e05)`: homing rate female

## Outputs

* `CPT`: Cumulative fraction of mosquitoes divided by time
* `TTI`: Time to introgression
* `TTO`: Time to outrogression
* `WOP`: Window of protection
* `POE`: Probability of elimination/fixation
* `MIN`: Minimum of mosquitoes
* `RAP`: Fraction of mosquites at timepoint

<hr>