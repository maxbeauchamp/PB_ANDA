#!/usr/bin/env python

""" launch_4periods_ANDA.py: Application of MS_AnDA to spatio-temporal interpolation of SSH (sea surface height) from nadir and/or swot datasets on 4 periods and merging. """

__author__ = "Maxime Beauchamp"
__version__ = "2.0"
__date__ = "2019-12-10"
__email__ = "maxime.beauchamp76@gmail.com"

from pb_anda import *
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

opt = sys.argv[1]
lag = sys.argv[2]
type_obs = sys.argv[3]

# wait for the results
workpath="/home3/scratch/mbeaucha/resAnDA_"+opt+"_nadlag_"+lag+"_"+type_obs+"_dstart_60"
saved_path1=workpath+'/saved_path.pickle'
workpath="/home3/scratch/mbeaucha/resAnDA_"+opt+"_nadlag_"+lag+"_"+type_obs+"_dstart_140"
saved_path2=workpath+'/saved_path.pickle'
workpath="/home3/scratch/mbeaucha/resAnDA_"+opt+"_nadlag_"+lag+"_"+type_obs+"_dstart_220"
saved_path3=workpath+'/saved_path.pickle'
workpath="/home3/scratch/mbeaucha/resAnDA_"+opt+"_nadlag_"+lag+"_"+type_obs+"_dstart_300"
saved_path4=workpath+'/saved_path.pickle'

if  ( not os.path.exists(saved_path1) ):
    bashCommand="qsub -v 'OPT="+opt+"','LAG="+lag+"','TYPE_OBS="+type_obs+"','START=60'      /home3/datahome/mbeaucha/algo/submit_PB_AnDA_nocont.pbs"
    os.popen(bashCommand)
if  ( not os.path.exists(saved_path2) ):
    bashCommand="qsub -v 'OPT="+opt+"','LAG="+lag+"','TYPE_OBS="+type_obs+"','START=140'      /home3/datahome/mbeaucha/algo/submit_PB_AnDA_nocont.pbs"
    os.popen(bashCommand)
if  ( not os.path.exists(saved_path3) ):
    bashCommand="qsub -v 'OPT="+opt+"','LAG="+lag+"','TYPE_OBS="+type_obs+"','START=220'      /home3/datahome/mbeaucha/algo/submit_PB_AnDA_nocont.pbs"
    os.popen(bashCommand)
if  ( not os.path.exists(saved_path4) ):
    bashCommand="qsub -v 'OPT="+opt+"','LAG="+lag+"','TYPE_OBS="+type_obs+"','START=300'      /home3/datahome/mbeaucha/algo/submit_PB_AnDA_nocont.pbs"
    os.popen(bashCommand)

# wait for the results
while ( not (os.path.exists(saved_path1) and \
        os.path.exists(saved_path2) and \
        os.path.exists(saved_path3) and \
        os.path.exists(saved_path4)) ):
    time.sleep(10)
    print('Wainting for the 4 periods runs to finish...')
    print('...Done')

# Reload saved AnDA result (period #1)
with open(saved_path1, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_p1, itrp_dineof_p1 = AnDA_ssh_1, itrp_dineof
# Reload saved AnDA result (period #2)
with open(saved_path2, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_p2, itrp_dineof_p2 = AnDA_ssh_1, itrp_dineof
# Reload saved AnDA result (period #3)
with open(saved_path3, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_p3, itrp_dineof_p3 = AnDA_ssh_1, itrp_dineof
# Reload saved AnDA result (period #4)
with open(saved_path4, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_p4, itrp_dineof_p4 = AnDA_ssh_1, itrp_dineof

# Merge all the results
itrp_dineof		= np.concatenate([itrp_dineof_p1,itrp_dineof_p2,itrp_dineof_p3,itrp_dineof_p4])
AnDA_ssh_1.GT 		= np.concatenate([AnDA_ssh_1_p1.GT,AnDA_ssh_1_p2.GT,\
                               AnDA_ssh_1_p3.GT,AnDA_ssh_1_p4.GT])
AnDA_ssh_1.Obs 		= np.concatenate([AnDA_ssh_1_p1.Obs,AnDA_ssh_1_p2.Obs,\
                               AnDA_ssh_1_p3.Obs,AnDA_ssh_1_p4.Obs])
AnDA_ssh_1.itrp_OI	= np.concatenate([AnDA_ssh_1_p1.itrp_OI,AnDA_ssh_1_p2.itrp_OI,\
                               AnDA_ssh_1_p3.itrp_OI,AnDA_ssh_1_p4.itrp_OI])
AnDA_ssh_1.itrp_AnDA 	= np.concatenate([AnDA_ssh_1_p1.itrp_AnDA,AnDA_ssh_1_p2.itrp_AnDA,\
                               AnDA_ssh_1_p3.itrp_AnDA,AnDA_ssh_1_p4.itrp_AnDA])
AnDA_ssh_1.itrp_postAnDA = np.concatenate([AnDA_ssh_1_p1.itrp_postAnDA,AnDA_ssh_1_p2.itrp_postAnDA,\
                               AnDA_ssh_1_p3.itrp_postAnDA,AnDA_ssh_1_p4.itrp_postAnDA])

# Display all the results
lday1=[ datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=60+i),"%Y-%m-%d") for i in range(20) ]
lday2=[ datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=140+i),"%Y-%m-%d") for i in range(20) ]
lday3=[ datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=220+i),"%Y-%m-%d") for i in range(20) ]
lday4=[ datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=300+i),"%Y-%m-%d") for i in range(20) ]
lday = np.concatenate([lday1,lday2,lday3,lday4])

workpath = "/home3/scratch/mbeaucha/resAnDA_"+opt+"_nadlag_"+lag+"_"+type_obs
if not os.path.exists(workpath):
    mk_dir_recursive(workpath)
else:
    shutil.rmtree(workpath)
    mk_dir_recursive(workpath)
saved_path = workpath+'/saved_path.pickle'

# Save AnDA result         
with open(saved_path, 'wb') as handle:
    pickle.dump([AnDA_ssh_1, itrp_dineof], handle)

# Reload saved AnDA result
with open(saved_path, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)    

			#*****************#
			# Display results #
			#*****************#

resssh = 0.25
r_start = 0
c_start = 0
r_length = 10*20
c_length = 10*20
lon = np.arange(-65,-65+((1/20)*r_length),1/20)
lat = np.arange(30,30+((1/20)*c_length),1/20)
extent_=[np.min(lon),np.max(lon),np.min(lat),np.max(lat)]
for i in range(80):

    day=lday[i]
    print(day)
    ## Maps
    resfile=workpath+"/results_AnDA_maps_"+day+".png"
    # Load data
    gt 			= AnDA_ssh_1.GT[i,:,:]
    Grad_gt             = Gradient(gt,2)
    obs 		= AnDA_ssh_1.Obs[i,:,:]
    OI                  = AnDA_ssh_1.itrp_OI[i,:,:]
    Grad_OI             = Gradient(OI,2)
    VE_DINEOF           = itrp_dineof[i,:,:]
    Grad_VE_DINEOF      = Gradient(VE_DINEOF,2)
    AnDA 		= AnDA_ssh_1.itrp_AnDA[i,:,:]
    Grad_AnDA           = Gradient(AnDA,2)
    Post_AnDA 		= AnDA_ssh_1.itrp_postAnDA[i,:,:]
    Grad_Post_AnDA     = Gradient(Post_AnDA,2)

    # Display figures
    var=['gt','obs','OI','AnDA','VE_DINEOF',\
         'Post_AnDA','Grad_gt','Grad_OI','Grad_AnDA','Grad_VE_DINEOF','Grad_Post_AnDA']
    title=['GT','Obs','OI','AnDA','VE-DINEOF',\
           'Post_AnDA',r"$\nabla_{GT}$",r"$\nabla_{OI}$",\
            r"$\nabla_{AnDA}$",r"$\nabla_{VE-DINEOF}$",r"$\nabla_{Post_AnDA}$"]
    fig, ax = plt.subplots(4,3,figsize=(15,15),
                          subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=0.0)))
    for ivar in range(0,len(var)):
        i = int(np.floor(ivar/3)) ; j = ivar%3
        if (var[ivar])[0:4]=="Grad":
            vmin = np.nanmin(Grad_gt) ; vmax = np.nanmax(Grad_gt)
            cmap="viridis"
        else:
            vmin = np.nanmin(gt) ; vmax = np.nanmax(gt)
            #vmin=-2 ; vmax=2
            cmap="coolwarm"
        plot(ax,i,j,lon,lat,eval(var[ivar]),title[ivar],\
             extent=extent_,cmap=cmap,vmin=vmin,vmax=vmax)
    plt.subplots_adjust(hspace=0.85,wspace=0.85)
    plt.savefig(resfile)	# save the figure
    plt.close()		# close the figure

    ## Taylor diagrams
    resfile=workpath+"/Taylor_diagram_"+day+".png"
    var=['gt','OI','AnDA','Post_AnDA','VE_DINEOF']
    label = ['GT','OI','AnDA','Post_AnDA','VE_DINEOF']
    series={'gt':gt,
            'OI':OI,
            'AnDA':AnDA,
            'Post_AnDA':Post_AnDA,
            'VE_DINEOF':VE_DINEOF}
    Taylor_diag(series,label,['o','o','o','o','o'],plt.matplotlib.cm.jet(np.linspace(0,1,5)))
    plt.savefig(resfile)
    plt.close()

    ## Radial Power Spectrum (RAPS)
    resfile=workpath+"/results_AnDA_RAPS_"+day+".png"
    f0, Pf_AnDA  	= raPsd2dv1(AnDA,resssh,True)
    f1, Pf_postAnDA 	= raPsd2dv1(Post_AnDA,resssh,True)
    f2, Pf_GT    	= raPsd2dv1(gt,resssh,True)
    f3, Pf_OI    	= raPsd2dv1(OI,resssh,True)
    wf0			= 1/f0
    wf1         	= 1/f1
    wf2         	= 1/f2
    wf3         	= 1/f3
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(wf2,Pf_GT,label='GT')
    ax.plot(wf3,Pf_OI,label='OI')
    ax.plot(wf0,Pf_AnDA,label='AnDA')
    ax.plot(wf2,Pf_postAnDA,label='postAnDA')
    ax.set_xlabel("Wavenumber", fontweight='bold')
    ax.set_ylabel("Power spectral density (m2/(cy/km))", fontweight='bold')
    ax.set_xscale('log') ; ax.set_yscale('log')
    plt.legend(loc='best')
    plt.xticks([50, 100, 200, 500, 1000], ["50km", "100km", "200km", "500km", "1000km"])
    ax.invert_xaxis()
    plt.grid(which='both', linestyle='--')
    plt.savefig(resfile)	# save the figure
    plt.close()		# close the figure


