#!/bin/bash

i=0
# for tdata in 'swot' 'nadir' 'nadirswot'; do
for tdata in 'nadir' 'nadirswot'; do
  for lag in '0' '1' '2' '3' '4' '5' ; do
    for tobs in 'mod' 'obs' ; do
      previousJob="Job"${i}
      i=$((i+1))
      Job="Job"${i}  
      if [ $i == 1 ] ; then
        qsub -N ${Job} -v "OPT=${tdata}","LAG=${lag}","TYPE_OBS=${tobs}"  submit_PB_AnDA_merge_nocont.pbs 
      else 
        JobID=`qselect -N ${previousJob} -u $USER`
        JobID=${JobID:0:7}
        qsub -N ${Job} -v "OPT=${tdata}","LAG=${lag}","TYPE_OBS=${tobs}" -W depend=afterany:${JobID} submit_PB_AnDA_merge_nocont.pbs
      fi
    done
  done
done

