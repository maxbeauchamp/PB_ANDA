#!/usr/bin/env python

""" compare_AnDA_nadlag.py: script to compare AnDA results according the nadir lag period (0-5)"""

__author__ = "Maxime Beauchamp"
__version__ = "0.1"
__date__ = "2020-12-01"
__email__ = "maxime.beauchamp76@gmail.com"

from pb_anda import *
import matplotlib.dates as mdates
np.random.seed(1)

# function to create recursive paths
def mk_dir_recursive(dir_path):
    if os.path.isdir(dir_path):
        return
    h, t = os.path.split(dir_path)  # head/tail
    if not os.path.isdir(h):
        mk_dir_recursive(h)

    new_path = join_paths(h, t)
    if not os.path.isdir(new_path):
        os.mkdir(new_path)

type_obs = sys.argv[1]
workpath = "/home3/scratch/mbeaucha/compare_AnDA_nadlag_"+type_obs
if not os.path.exists(workpath):
    mk_dir_recursive(workpath)
else:
    shutil.rmtree(workpath)
    mk_dir_recursive(workpath)    

## Reload saved AnDA result
# NADLAG = 0
file_results_nadir='/home3/scratch/mbeaucha/resAnDA_nadir_nadlag_0_'+type_obs+'/saved_path.pickle'
with open(file_results_nadir, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadir_0 = AnDA_ssh_1  
file_results_nadirswot='/home3/scratch/mbeaucha/resAnDA_nadirswot_nadlag_0_'+type_obs+'/saved_path.pickle'
with open(file_results_nadirswot, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadirswot_0 = AnDA_ssh_1  
# NADLAG = 1
file_results_nadir='/home3/scratch/mbeaucha/resAnDA_nadir_nadlag_1_'+type_obs+'/saved_path.pickle'
with open(file_results_nadir, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadir_1 = AnDA_ssh_1
file_results_nadirswot='/home3/scratch/mbeaucha/resAnDA_nadirswot_nadlag_1_'+type_obs+'/saved_path.pickle'
with open(file_results_nadirswot, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadirswot_1 = AnDA_ssh_1
# NADLAG = 2
file_results_nadir='/home3/scratch/mbeaucha/resAnDA_nadir_nadlag_2_'+type_obs+'/saved_path.pickle'
with open(file_results_nadir, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadir_2 = AnDA_ssh_1
file_results_nadirswot='/home3/scratch/mbeaucha/resAnDA_nadirswot_nadlag_2_'+type_obs+'/saved_path.pickle'
with open(file_results_nadirswot, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadirswot_2 = AnDA_ssh_1
# NADLAG = 3
file_results_nadir='/home3/scratch/mbeaucha/resAnDA_nadir_nadlag_3_'+type_obs+'/saved_path.pickle'
with open(file_results_nadir, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadir_3 = AnDA_ssh_1
file_results_nadirswot='/home3/scratch/mbeaucha/resAnDA_nadirswot_nadlag_3_'+type_obs+'/saved_path.pickle'
with open(file_results_nadirswot, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadirswot_3 = AnDA_ssh_1
# NADLAG = 4
file_results_nadir='/home3/scratch/mbeaucha/resAnDA_nadir_nadlag_4_'+type_obs+'/saved_path.pickle'
with open(file_results_nadir, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadir_4 = AnDA_ssh_1
file_results_nadirswot='/home3/scratch/mbeaucha/resAnDA_nadirswot_nadlag_4_'+type_obs+'/saved_path.pickle'
with open(file_results_nadirswot, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadirswot_4 = AnDA_ssh_1
# NADLAG = 5
file_results_nadir='/home3/scratch/mbeaucha/resAnDA_nadir_nadlag_5_'+type_obs+'/saved_path.pickle'
with open(file_results_nadir, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadir_5 = AnDA_ssh_1
file_results_nadirswot='/home3/scratch/mbeaucha/resAnDA_nadirswot_nadlag_5_'+type_obs+'/saved_path.pickle'
with open(file_results_nadirswot, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadirswot_5 = AnDA_ssh_1


			#*****************#
			# Display results #
			#*****************#

## Init variables for temporal analysis
nrmse_Post_AnDA_nadir_0=np.zeros(len(AnDA_ssh_1.GT))
nrmse_Post_AnDA_nadirswot_0=np.zeros(len(AnDA_ssh_1.GT))
nrmse_Post_AnDA_nadir_1=np.zeros(len(AnDA_ssh_1.GT))
nrmse_Post_AnDA_nadirswot_1=np.zeros(len(AnDA_ssh_1.GT))
nrmse_Post_AnDA_nadir_2=np.zeros(len(AnDA_ssh_1.GT))
nrmse_Post_AnDA_nadirswot_2=np.zeros(len(AnDA_ssh_1.GT))
nrmse_Post_AnDA_nadir_3=np.zeros(len(AnDA_ssh_1.GT))
nrmse_Post_AnDA_nadirswot_3=np.zeros(len(AnDA_ssh_1.GT))
nrmse_Post_AnDA_nadir_4=np.zeros(len(AnDA_ssh_1.GT))
nrmse_Post_AnDA_nadirswot_4=np.zeros(len(AnDA_ssh_1.GT))
nrmse_Post_AnDA_nadir_5=np.zeros(len(AnDA_ssh_1.GT))
nrmse_Post_AnDA_nadirswot_5=np.zeros(len(AnDA_ssh_1.GT))
## Observations spatial coverage
nadcov_0=np.zeros(len(AnDA_ssh_1.GT))
nadswotcov_0=np.zeros(len(AnDA_ssh_1.GT))
nadcov_1=np.zeros(len(AnDA_ssh_1.GT))
nadswotcov_1=np.zeros(len(AnDA_ssh_1.GT))
nadcov_2=np.zeros(len(AnDA_ssh_1.GT))
nadswotcov_2=np.zeros(len(AnDA_ssh_1.GT))
nadcov_3=np.zeros(len(AnDA_ssh_1.GT))
nadswotcov_3=np.zeros(len(AnDA_ssh_1.GT))
nadcov_4=np.zeros(len(AnDA_ssh_1.GT))
nadswotcov_4=np.zeros(len(AnDA_ssh_1.GT))
nadcov_5=np.zeros(len(AnDA_ssh_1.GT))
nadswotcov_5=np.zeros(len(AnDA_ssh_1.GT))

# list of dates
lday1=[ datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=60+i),"%Y-%m-%d") for i in range(20) ]
lday2=[ datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=140+i),"%Y-%m-%d") for i in range(20) ]
lday3=[ datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=220+i),"%Y-%m-%d") for i in range(20) ]
lday4=[ datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=300+i),"%Y-%m-%d") for i in range(20) ]
lday = np.concatenate([lday1,lday2,lday3,lday4])

## Spatial analysis
for i in range(0,len(AnDA_ssh_1.GT)):

    day=lday[i]
    print(day)

    # Load data
    gt 			= AnDA_ssh_1.GT[i,:,:]
    obs_nadir_0 	= AnDA_ssh_1_nadir_0.Obs[i,:,:]
    Post_AnDA_nadir_0 	= AnDA_ssh_1_nadir_0.itrp_postAnDA[i,:,:]
    obs_nadir_1         = AnDA_ssh_1_nadir_1.Obs[i,:,:]
    Post_AnDA_nadir_1   = AnDA_ssh_1_nadir_1.itrp_postAnDA[i,:,:]
    obs_nadir_2         = AnDA_ssh_1_nadir_2.Obs[i,:,:]
    Post_AnDA_nadir_2   = AnDA_ssh_1_nadir_2.itrp_postAnDA[i,:,:]
    obs_nadir_3         = AnDA_ssh_1_nadir_3.Obs[i,:,:]
    Post_AnDA_nadir_3   = AnDA_ssh_1_nadir_3.itrp_postAnDA[i,:,:]
    obs_nadir_4         = AnDA_ssh_1_nadir_4.Obs[i,:,:]
    Post_AnDA_nadir_4   = AnDA_ssh_1_nadir_4.itrp_postAnDA[i,:,:]
    obs_nadir_5         = AnDA_ssh_1_nadir_5.Obs[i,:,:]
    Post_AnDA_nadir_5   = AnDA_ssh_1_nadir_5.itrp_postAnDA[i,:,:]
    # nadirswot
    obs_nadirswot_0 		= AnDA_ssh_1_nadirswot_0.Obs[i,:,:]
    Post_AnDA_nadirswot_0 	= AnDA_ssh_1_nadirswot_0.itrp_postAnDA[i,:,:]
    obs_nadirswot_1 	   	= AnDA_ssh_1_nadirswot_1.Obs[i,:,:]
    Post_AnDA_nadirswot_1 	= AnDA_ssh_1_nadirswot_1.itrp_postAnDA[i,:,:]
    obs_nadirswot_2     	= AnDA_ssh_1_nadirswot_2.Obs[i,:,:]
    Post_AnDA_nadirswot_2 	= AnDA_ssh_1_nadirswot_2.itrp_postAnDA[i,:,:]
    obs_nadirswot_3     	= AnDA_ssh_1_nadirswot_3.Obs[i,:,:]
    Post_AnDA_nadirswot_3 	= AnDA_ssh_1_nadirswot_3.itrp_postAnDA[i,:,:]
    obs_nadirswot_4     	= AnDA_ssh_1_nadirswot_4.Obs[i,:,:]
    Post_AnDA_nadirswot_4 	= AnDA_ssh_1_nadirswot_4.itrp_postAnDA[i,:,:]
    obs_nadirswot_5     	= AnDA_ssh_1_nadirswot_5.Obs[i,:,:]
    Post_AnDA_nadirswot_5 	= AnDA_ssh_1_nadirswot_5.itrp_postAnDA[i,:,:]

    ## Compute spatial coverage
    nadcov_0[i]		= len(np.argwhere(np.isfinite(obs_nadir_0.flatten())))/len(obs_nadir_0.flatten())
    nadswotcov_0[i]	= len(np.argwhere(np.isfinite(obs_nadirswot_0.flatten())))/len(obs_nadirswot_0.flatten())
    nadcov_1[i]         = len(np.argwhere(np.isfinite(obs_nadir_1.flatten())))/len(obs_nadir_1.flatten())
    nadswotcov_1[i]     = len(np.argwhere(np.isfinite(obs_nadirswot_1.flatten())))/len(obs_nadirswot_1.flatten())
    nadcov_2[i]         = len(np.argwhere(np.isfinite(obs_nadir_2.flatten())))/len(obs_nadir_2.flatten())
    nadswotcov_2[i]     = len(np.argwhere(np.isfinite(obs_nadirswot_2.flatten())))/len(obs_nadirswot_2.flatten())
    nadcov_3[i]         = len(np.argwhere(np.isfinite(obs_nadir_3.flatten())))/len(obs_nadir_3.flatten())
    nadswotcov_3[i]     = len(np.argwhere(np.isfinite(obs_nadirswot_3.flatten())))/len(obs_nadirswot_3.flatten())
    nadcov_4[i]         = len(np.argwhere(np.isfinite(obs_nadir_4.flatten())))/len(obs_nadir_4.flatten())
    nadswotcov_4[i]     = len(np.argwhere(np.isfinite(obs_nadirswot_4.flatten())))/len(obs_nadirswot_4.flatten())
    nadcov_5[i]         = len(np.argwhere(np.isfinite(obs_nadir_5.flatten())))/len(obs_nadir_5.flatten())
    nadswotcov_5[i]     = len(np.argwhere(np.isfinite(obs_nadirswot_5.flatten())))/len(obs_nadirswot_5.flatten())
    ## Compute NRMSE statistics (i.e. RMSE/stdev(gt) )
    nrmse_Post_AnDA_nadir_0[i]  	= (np.sqrt(np.nanmean(((gt-np.nanmean(gt))-(Post_AnDA_nadir_0-np.nanmean(Post_AnDA_nadir_0)))**2)))/np.nanstd(gt)
    nrmse_Post_AnDA_nadirswot_0[i] 	= (np.sqrt(np.nanmean(((gt-np.nanmean(gt))-(Post_AnDA_nadirswot_0-np.nanmean(Post_AnDA_nadirswot_0)))**2)))/np.nanstd(gt)
    nrmse_Post_AnDA_nadir_1[i]          = (np.sqrt(np.nanmean(((gt-np.nanmean(gt))-(Post_AnDA_nadir_1-np.nanmean(Post_AnDA_nadir_1)))**2)))/np.nanstd(gt)
    nrmse_Post_AnDA_nadirswot_1[i]      = (np.sqrt(np.nanmean(((gt-np.nanmean(gt))-(Post_AnDA_nadirswot_1-np.nanmean(Post_AnDA_nadirswot_1)))**2)))/np.nanstd(gt)
    nrmse_Post_AnDA_nadir_2[i]          = (np.sqrt(np.nanmean(((gt-np.nanmean(gt))-(Post_AnDA_nadir_2-np.nanmean(Post_AnDA_nadir_2)))**2)))/np.nanstd(gt)
    nrmse_Post_AnDA_nadirswot_2[i]      = (np.sqrt(np.nanmean(((gt-np.nanmean(gt))-(Post_AnDA_nadirswot_2-np.nanmean(Post_AnDA_nadirswot_2)))**2)))/np.nanstd(gt)
    nrmse_Post_AnDA_nadir_3[i]          = (np.sqrt(np.nanmean(((gt-np.nanmean(gt))-(Post_AnDA_nadir_3-np.nanmean(Post_AnDA_nadir_3)))**2)))/np.nanstd(gt)
    nrmse_Post_AnDA_nadirswot_3[i]      = (np.sqrt(np.nanmean(((gt-np.nanmean(gt))-(Post_AnDA_nadirswot_3-np.nanmean(Post_AnDA_nadirswot_3)))**2)))/np.nanstd(gt)
    nrmse_Post_AnDA_nadir_4[i]          = (np.sqrt(np.nanmean(((gt-np.nanmean(gt))-(Post_AnDA_nadir_4-np.nanmean(Post_AnDA_nadir_4)))**2)))/np.nanstd(gt)
    nrmse_Post_AnDA_nadirswot_4[i]      = (np.sqrt(np.nanmean(((gt-np.nanmean(gt))-(Post_AnDA_nadirswot_4-np.nanmean(Post_AnDA_nadirswot_4)))**2)))/np.nanstd(gt)
    nrmse_Post_AnDA_nadir_5[i]          = (np.sqrt(np.nanmean(((gt-np.nanmean(gt))-(Post_AnDA_nadir_5-np.nanmean(Post_AnDA_nadir_5)))**2)))/np.nanstd(gt)
    nrmse_Post_AnDA_nadirswot_5[i]      = (np.sqrt(np.nanmean(((gt-np.nanmean(gt))-(Post_AnDA_nadirswot_5-np.nanmean(Post_AnDA_nadirswot_5)))**2)))/np.nanstd(gt)

## Plot time series (nadir)
N = len(lday)
print(N)
# first axis with nRMSE time series
col = plt.matplotlib.cm.jet(np.linspace(0,1,6))
plt.plot(range(N),nrmse_Post_AnDA_nadir_0,color=col[0],linewidth=.5,label='post-AnDA (nadir, lag=0)')
plt.plot(range(N),nrmse_Post_AnDA_nadir_1,color=col[1],linewidth=.5,label='post-AnDA (nadir, lag=1)')
plt.plot(range(N),nrmse_Post_AnDA_nadir_2,color=col[2],linewidth=.5,label='post-AnDA (nadir, lag=2)')
plt.plot(range(N),nrmse_Post_AnDA_nadir_3,color=col[3],linewidth=.5,label='post-AnDA (nadir, lag=3)')
plt.plot(range(N),nrmse_Post_AnDA_nadir_4,color=col[4],linewidth=.5,label='post-AnDA (nadir, lag=4)')
plt.plot(range(N),nrmse_Post_AnDA_nadir_5,color=col[5],linewidth=.5,label='post-AnDA (nadir, lag=5)')
plt.ylabel('nRMSE')
plt.xlabel('Time (days)')
# add vertical bar to divide the 4 periods
plt.axvline(x=19)
plt.axvline(x=39)
plt.axvline(x=59)
# graphical options
plt.ylabel('nRMSE')
plt.xlabel('Time (days)')
plt.xticks([0,20,40,60],\
           [lday[0],lday[20],lday[40],lday[60]],\
           rotation=45, ha='right')
plt.margins(x=0)
plt.grid(True,alpha=.3)
plt.legend(loc='upper left',prop=dict(size='small'),frameon=False,bbox_to_anchor=(0,1.02,1,0.2),ncol=2,mode="expand")
# second axis with spatial coverage
axes2 = plt.twinx()
width=0.75
p1 = axes2.bar(range(N), nadcov_0, width,color=col[0],alpha=0.25)
p2 = axes2.bar(range(N), nadcov_1, width, bottom=nadcov_0, color=col[1], alpha=0.25)
p3 = axes2.bar(range(N), nadcov_2, width, bottom=nadcov_1, color=col[2], alpha=0.25)
p4 = axes2.bar(range(N), nadcov_3, width, bottom=nadcov_2, color=col[3], alpha=0.25)
p5 = axes2.bar(range(N), nadcov_4, width, bottom=nadcov_3, color=col[4], alpha=0.25)
p6 = axes2.bar(range(N), nadcov_5, width, bottom=nadcov_4, color=col[5], alpha=0.25)
axes2.set_ylim(0, 1)
axes2.set_ylabel('Spatial Coverage (%)')
axes2.margins(x=0)
resfile=workpath+"/TS_AnDA_nadir_nadlag.png"
plt.savefig(resfile,bbox_inches="tight")    # save the figure
plt.close()         			    # close the figure

## Plot time series (nadir+swot)
N = len(lday)
print(N)
# first axis with nRMSE time series
col = plt.matplotlib.cm.jet(np.linspace(0,1,6))
plt.plot(range(N),nrmse_Post_AnDA_nadirswot_0,color=col[0],linewidth=.5,label='post-AnDA (nadir, lag=0)')
plt.plot(range(N),nrmse_Post_AnDA_nadirswot_1,color=col[1],linewidth=.5,label='post-AnDA (nadir, lag=1)')
plt.plot(range(N),nrmse_Post_AnDA_nadirswot_2,color=col[2],linewidth=.5,label='post-AnDA (nadir, lag=2)')
plt.plot(range(N),nrmse_Post_AnDA_nadirswot_3,color=col[3],linewidth=.5,label='post-AnDA (nadir, lag=3)')
plt.plot(range(N),nrmse_Post_AnDA_nadirswot_4,color=col[4],linewidth=.5,label='post-AnDA (nadir, lag=4)')
plt.plot(range(N),nrmse_Post_AnDA_nadirswot_5,color=col[5],linewidth=.5,label='post-AnDA (nadir, lag=5)')
plt.ylabel('nRMSE')
plt.xlabel('Time (days)')
# add vertical bar to divide the 4 periods
plt.axvline(x=19)
plt.axvline(x=39)
plt.axvline(x=59)
# graphical options
plt.ylabel('nRMSE')
plt.xlabel('Time (days)')
plt.xticks([0,20,40,60],\
           [lday[0],lday[20],lday[40],lday[60]],\
           rotation=45, ha='right')
plt.margins(x=0)
plt.grid(True,alpha=.3)
plt.legend(loc='upper left',prop=dict(size='small'),frameon=False,bbox_to_anchor=(0,1.02,1,0.2),ncol=2,mode="expand")
# second axis with spatial coverage
axes2 = plt.twinx()
width=0.75
p1 = axes2.bar(range(N), nadswotcov_0, width,color=col[0],alpha=0.25)
p2 = axes2.bar(range(N), nadswotcov_1, width, bottom=nadswotcov_0, color=col[1], alpha=0.25)
p3 = axes2.bar(range(N), nadswotcov_2, width, bottom=nadswotcov_1, color=col[2], alpha=0.25)
p4 = axes2.bar(range(N), nadswotcov_3, width, bottom=nadswotcov_2, color=col[3], alpha=0.25)
p5 = axes2.bar(range(N), nadswotcov_4, width, bottom=nadswotcov_3, color=col[4], alpha=0.25)
p6 = axes2.bar(range(N), nadswotcov_5, width, bottom=nadswotcov_4, color=col[5], alpha=0.25)
axes2.set_ylim(0, 1)
axes2.set_ylabel('Spatial Coverage (%)')
axes2.margins(x=0)
resfile=workpath+"/TS_AnDA_nadirswot_nadlag.png"
plt.savefig(resfile,bbox_inches="tight")    # save the figure
plt.close()                                 # close the figure
