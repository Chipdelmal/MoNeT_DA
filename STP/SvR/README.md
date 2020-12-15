#   Spatial Extension of the SvR BioEssays Paper


## MGDrivE Experiments Pipeline

These sets of experiments involve the transition between MGDrivE1 and MGDrivE2, so 

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