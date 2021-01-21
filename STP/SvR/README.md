#   Spatial Extension of the SvR BioEssays Paper (Suppression versus Replacement)


## MGDrivE Experiments Pipeline

These sets of experiments involve the transition between MGDrivE1 and MGDrivE2, so there is an additional toggle in the data analysis routines to accommodate both types of datasets.

### Spatial Experiments and Preprocess

Setup the factorial experiment in the [Rscript](https://github.com/Chipdelmal/MGDrivE/tree/master/Main/STP) and run the following command:

```bash
./STP_simAndPreProcess.sh srv 265 SPA v1 True
```

This should auto-run the factorial and place the results in the RAID5 drive. After running the sims, it should startup the [preProcess](./STP_preProcess.py) followed by the [preTraces](./STP_preTraces.py) and [preGrids](./STP_preGrids.py) (these two are optional).

####  Spatial Analysis Breakdown

1. Run the [STP_geoCluster.py](./STP_geoCluster.py) script with the desired level of aggregation for analysis
1. Run [STP_preProcess.sh](./STP_preProcess.sh) for ECO, HLT, WLD, TRS *PREPROCESS*
1. Run [STP_preTraces.sh](./STP_preTraces.sh) for ECO, HLT, WLD, TRS *preTraces* and *preGrids* 
2. Run [STP_preVideo.sh](./STP_preVideo.sh) for desired videos (probably HLT)

##  Classifier

To put all the data through the ML classification pipeline, run:

```bash
chmod +x STP_clsPipeline.sh
./STP_clsPipeline.sh
```

which launches the following scripts in order:

1. [STP_clsPreUnify](./STP_clsPreUnify.py)
1. [STP_clsPreprocess](./STP_clsPreprocess.py)
1. [STP_clsTrain](./STP_clsTrain.py)


##  ASTMH Poster

* [STP_cmprReleasesASTMH](./deprecated/STP_cmprReleasesASTMH.py)