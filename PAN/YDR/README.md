
# Y-Drive 

## Gene Drive Constructs

* [ASD: Autosomal Split-Drive](https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-SplitDriveMF.R)
* [XSD: X-Linked Split-Drive](https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-SplitDriveX.R)
* [YSD: Y-Linked Split-Drive](https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-SplitDriveY.R)
* [ASD: Autosomal X-Shredder](https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-ShredderMF.R)
* [YXS: Y-Linked X-Shredder](https://github.com/Chipdelmal/MGDrivE/blob/master/MGDrivE/R/Cube-ShredderY.R)

## Scripts

Add your USR id to the [YDR_aux](./YDR_aux.py) file to run the scripts.

### PreProcess bash scripts

Bash scripts to do the whole pre-processing pipeline:

```bash
# Runs the whole pre-process analysis workflow (with preTraces and preGrids)
./preTraces.sh USR DRV True
# Runs the preProcess section only
./preProcess.sh USR DRV False
```

To generate the preTraces with grids:

```bash
./preTraces.sh USR DRV 
```

To run the grids of all the experiments (after doing their traces):

```bash
./preGrids.sh USR 
```

And the grids

```bash
./preGrids.sh USR DRV
```

## Authors

* Héctor M. Sánchez C.
* Jared B. Bennett


