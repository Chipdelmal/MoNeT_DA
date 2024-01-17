# Target Product Profile (TPP)

## Pipeline

To generate the whole set of analysis, the following set of bash scripts needs to be run in order.

1. Run [`bash TPP_fullCrunch.sh USR MOS_BOOL HUM_BOOL THS`](./TPP_fullCrunch.sh) to generate base analysis files.
    1. [`bash TPP_preCrunch.sh USR MOS_BOOL HUM_BOOL`](./TPP_preCrunch.sh)
        1. [`TPP_preProcess.py`](./TPP_preProcess.py)
        2. [`TPP_preTraces.py`](./TPP_preTraces.py)
        3. [`TPP_preProcessEpi.py`](./TPP_preProcessEpi.py)
    2. [`bash TPP_pstCrunch.sh USR MOS_BOOL HUM_BOOL`](./TPP_pstCrunch.sh)
        1. [`TPP_pstFraction.py`](./TPP_pstFraction.py)
        2. [`TPP_pstProcess.py`](./TPP_pstProcess.py)
    3. [`bash TPP_clsCrunch.sh USR MOS_BOOL HUM_BOOL THS`](./TPP_clsCrunch.sh)
        1. [`TPP_clsCompile.py`](./TPP_clsCompile.py)
        2. [`TPP_clsUnify.py`](./TPP_clsUnify.py)
        3. [`TPP_dtaExplore.py`](./TPP_dtaExplore.py)
        4. [`TPP_dtaTraces.py`](./TPP_dtaTraces.py)
2. Run [`bash TPP_mlrCrunch.sh USR MOS_BOOL HUM_BOOL THS`](./TPP_mlrCrunch.sh) to train Keras models.
    1. [`TPP_mlrTrainKeras.py`](./TPP_mlrTrainKeras.py)
3. Run [`bash TPP_mlrHeatmaps.sh USR MOS_BOOL HUM_BOOL THS`](./TPP_mlrHeatmaps.sh) to generate heatmaps.
    1. [`TPP_mlrHeatmaps.py`](./TPP_mlrHeatmaps.py)
4. Download files and data from server to local with [`bash TPP_download.sh`](./TPP_download.sh) (paths are hard-coded for convenience).