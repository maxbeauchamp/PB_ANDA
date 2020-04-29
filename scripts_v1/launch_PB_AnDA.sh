#!/bin/bash

domain="OSMOSIS"
qsub -v "OPT=nadir","LAG=0","TYPE_OBS=mod","DOMAIN=${domain}"     submit_PB_AnDA.pbs
qsub -v "OPT=nadirswot","LAG=0","TYPE_OBS=mod","DOMAIN=${domain}" submit_PB_AnDA.pbs
qsub -v "OPT=nadir","LAG=5","TYPE_OBS=mod","DOMAIN=${domain}"     submit_PB_AnDA.pbs
qsub -v "OPT=nadirswot","LAG=5","TYPE_OBS=mod","DOMAIN=${domain}" submit_PB_AnDA.pbs
