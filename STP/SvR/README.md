#   Spatial Extension of the SvR BioEssays Paper (Suppression versus Replacement)


## MGDrivE Experiments Pipeline

These sets of experiments involve the transition between MGDrivE1 and MGDrivE2, so there is an additional toggle in the data analysis routines to accommodate both types of datasets.

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


##  Spatial Analysis

1. Run the [STP_geoCluster](./STP_geoCluster.py) script with the desired level of aggregation for analysis
1. Run [STP_preProcess.sh](./STP_preProcess.sh) for ECO, HLT, WLD, TRS *PREPROCESS*
1. Run [STP_preTraces.sh](./STP_preTraces.sh) for ECO, HLT, WLD, TRS *preTraces* and *preGrids* 
2. Run [STP_preVideo](./STP_preVideo.sh)

##  ASTMH Poster

* [STP_cmprReleasesASTMH](./deprecated/STP_cmprReleasesASTMH.py)