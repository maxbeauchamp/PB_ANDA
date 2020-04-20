#!/bin/bash

qsub -v "OPT=swot","LAG=0","TYPE_OBS=mod"      submit_PB_AnDA.pbs
qsub -v "OPT=nadir","LAG=0","TYPE_OBS=mod"     submit_PB_AnDA.pbs
qsub -v "OPT=nadirswot","LAG=0","TYPE_OBS=mod" submit_PB_AnDA.pbs
qsub -v "OPT=nadir","LAG=1","TYPE_OBS=mod"     submit_PB_AnDA.pbs
qsub -v "OPT=nadirswot","LAG=1","TYPE_OBS=mod" submit_PB_AnDA.pbs
qsub -v "OPT=nadir","LAG=2","TYPE_OBS=mod"     submit_PB_AnDA.pbs
qsub -v "OPT=nadirswot","LAG=2","TYPE_OBS=mod" submit_PB_AnDA.pbs
qsub -v "OPT=nadir","LAG=3","TYPE_OBS=mod"     submit_PB_AnDA.pbs
qsub -v "OPT=nadirswot","LAG=3","TYPE_OBS=mod" submit_PB_AnDA.pbs
qsub -v "OPT=nadir","LAG=4","TYPE_OBS=mod"     submit_PB_AnDA.pbs
qsub -v "OPT=nadirswot","LAG=4","TYPE_OBS=mod" submit_PB_AnDA.pbs
qsub -v "OPT=nadir","LAG=5","TYPE_OBS=mod"     submit_PB_AnDA.pbs
qsub -v "OPT=nadirswot","LAG=5","TYPE_OBS=mod" submit_PB_AnDA.pbs
