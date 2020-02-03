# tar plots for beamer
tar zvcf /home3/scratch/mbeaucha/eftp/figs.tar.gz /home3/scratch/mbeaucha/RES_MOD_NOCONT/compare_AnDA_nadlag_mod/TS_AnDA_nadir_nadlag.png /home3/scratch/mbeaucha/RES_MOD_NOCONT/compare_AnDA_nadlag_mod/TS_AnDA_nadirswot_nadlag.png /home3/scratch/mbeaucha/RES_MOD_NOCONT/scores_AnDA_nadlag_0_mod/TS_AnDA_nRMSE.png /home3/scratch/mbeaucha/RES_MOD_NOCONT/scores_AnDA_nadlag_0_mod/results_AnDA_maps_2013-05-13.png /home3/scratch/mbeaucha/RES_MOD_NOCONT/scores_AnDA_nadlag_0_mod/results_AnDA_grads_2013-05-13.png /home3/scratch/mbeaucha/RES_MOD_NOCONT/scores_AnDA_nadlag_0_mod/Taylor_diagram_maps_2013-05-13.png /home3/scratch/mbeaucha/RES_MOD_NOCONT/scores_AnDA_nadlag_0_mod/results_AnDA_RAPS_2013-05-13.png /home3/scratch/mbeaucha/RES_OBS_NOCONT/compare_AnDA_nadlag_obs/TS_AnDA_nadir_nadlag.png /home3/scratch/mbeaucha/RES_OBS_NOCONT/compare_AnDA_nadlag_obs/TS_AnDA_nadirswot_nadlag.png /home3/scratch/mbeaucha/RES_OBS_NOCONT/scores_AnDA_nadlag_5_obs/TS_AnDA_nRMSE.png /home3/scratch/mbeaucha/RES_OBS_NOCONT/scores_AnDA_nadlag_5_obs/results_AnDA_maps_2013-05-13.png /home3/scratch/mbeaucha/RES_OBS_NOCONT/scores_AnDA_nadlag_5_obs/results_AnDA_grads_2013-05-13.png /home3/scratch/mbeaucha/RES_OBS_NOCONT/scores_AnDA_nadlag_5_obs/Taylor_diagram_maps_2013-05-13.png /home3/scratch/mbeaucha/RES_OBS_NOCONT/scores_AnDA_nadlag_5_obs/results_AnDA_RAPS_2013-05-13.png 

# copy plots for animate beamer
mkdir /home3/scratch/mbeaucha/figs_animate
cp -rf /home3/scratch/mbeaucha/RES_MOD_NOCONT/resAnDA*/*maps*png /home3/scratch/mbeaucha/RES_OBS_NOCONT/resAnDA*/*maps*png /home3/scratch/mbeaucha/RES_MOD_NOCONT/resAnDA*/*grads*png /home3/scratch/mbeaucha/RES_OBS_NOCONT/resAnDA*/*grads*png --parents /home3/scratch/mbeaucha/figs_animate
mv -f /home3/scratch/mbeaucha/figs_animate/home3/scratch/mbeaucha/* /home3/scratch/mbeaucha/figs_animate/
rm -rf /home3/scratch/mbeaucha/figs_animate/home3
cd /home3/scratch/mbeaucha/figs_animate
for tt in 'OBS' 'MOD' ; do
  cd RES_${tt}_NOCONT
  for lag in `seq 0 5` ; do
    for data in 'swot' 'nadir' 'nadirswot' ; do
      cd resAnDA_${data}_nadlag_${lag}_${tt,,}
      for var in 'maps' ; do
        lfile=($(ls *${var}*))
        N=${#lfile[*]}
        for ifile in `seq 0 $((N-1))` ; do
          mv -f ${lfile[$ifile]} ${lfile[$ifile]::-15}_${ifile}.png
        done
      done
      cd ..
    done
  done
  cd ..
done
tar zvcf /home3/scratch/mbeaucha/eftp/figs_animate.tar.gz /home3/scratch/mbeaucha/figs_animate/*

