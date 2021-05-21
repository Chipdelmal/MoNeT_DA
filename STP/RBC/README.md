#   São Tomé and Príncipe

## Variables Key

### Inputs

* `sex`: released mosquitos sex
  * `sxm`: male
  * `sxg`: gravid female
  * `sxn`: non-gravid female  
* `ren`: releases number
* `res`: releases size
* `rsg`: resistance generation
* `gsv`: genetic standing variation
* `fcf`: fertility fitness cost
* `mfm`: mating fitness homozygous
* `mft`: mating fitness heterozygous
* `hrm`: homing rate male
* `hrt`: homing rate female

### Outputs

* `CPT`: Cumulative fraction of mosquitoes divided by time
* `TTI`: Time to introgression
* `TTO`: Time to outrogression
* `WOP`: Window of protection
* `POE`: Probability of elimination/fixation
* `MIN`: Minimum of mosquitoes
* `RAP`: Fraction of mosquites at timepoint

## Pipelines

### Panmictic Experiments (one node)

To run the **pre** end of the DA (*run on server only*):

```bash
./STP_symlinks.sh
./STP_preProcess.sh srv PAN
./STP_preTraces.sh srv PAN
```

alternative, run the `./STP_prePipeline.sh` script for the three steps above to be auto-launched.

Downloading **pre** data and images:

```bash
./STP_dwlDataset.sh PREPROCESS
./STP_dwlImg.sh preGrids
```

For the **pst** DA:

```bash
./STP_pstFraction.sh dsk PAN
./STP_pstProcess.sh dsk PAN
./STP_pstTraces.sh dsk PAN
```


## Some References

* https://github.com/parrt/random-forest-importances
* https://explained.ai/rf-importance/index.html
* https://github.com/parrt/random-forest-importances/blob/master/src/rfpimp.py
* https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance_multicollinear.html#sphx-glr-auto-examples-inspection-plot-permutation-importance-multicollinear-py
* https://pdpbox.readthedocs.io/en/latest/pdp_plot.html
* https://github.com/blent-ai/ALEPython
* https://towardsdatascience.com/explaining-feature-importance-by-example-of-a-random-forest-d9166011959e