#   São Tomé and Príncipe

## Pipelines

### Panmictic Experiments (two nodes)

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