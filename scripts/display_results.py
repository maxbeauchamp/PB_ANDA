#!/usr/bin/env python

""" display_results.py: script to display maps, taylors diagrams and radially averaged power spectrums from MS-PB-AnDA and MS-VE-DINEOF with three different datasets (nadir / swot / nadirswot) """

__author__ = "Maxime Beauchamp"
__version__ = "0.1"
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
    
# Reload saved AnDA result
file_results_nadir='/home3/scratch/mbeaucha/resAnDA_nadir/saved_path.pickle'
with open(file_results_nadir, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadir = AnDA_ssh_1  
    itrp_dineof_nadir = itrp_dineof
file_results_swot='/home3/scratch/mbeaucha/resAnDA_swot/saved_path.pickle'
with open(file_results_swot, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_swot = AnDA_ssh_1  
    itrp_dineof_swot = itrp_dineof
file_results_nadirswot='/home3/scratch/mbeaucha/resAnDA_nadirswot/saved_path.pickle'
with open(file_results_nadirswot, 'rb') as handle:
    AnDA_ssh_1, itrp_dineof = pickle.load(handle)
    AnDA_ssh_1_nadirswot = AnDA_ssh_1  
    itrp_dineof_nadirswot = itrp_dineof

			#*****************#
			# Display results #
			#*****************#

resssh = 0.25
for i in range(0,len(AnDA_ssh_1.GT)):
    day=datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=PR_ssh.training_days+i),"%Y-%m-%d")

    ## Maps
    resfile1=workpath+"/results_AnDA_maps_"+day+".pdf"
    resfile1=workpath+"/results_AnDA_grads_"+day+".pdf"
    # Load data
    gt 				= AnDA_ssh_1.GT[i,:,:]
    Grad_gt             	= Gradient(gt,2)
    OI           		= AnDA_ssh_1.itrp_OI[i,:,:]
    Grad_OI             	= Gradient(OI,2)
    # nadir
    obs_nadir 			= AnDA_ssh_1_nadir.Obs[i,:,:]
    VE_DINEOF_nadir           	= itrp_dineof_nadir[i,:,:]
    Grad_VE_DINEOF_nadir 	= Gradient(VE_DINEOF_nadir,2)
    AnDA_nadir 		 	= AnDA_ssh_1_nadir.itrp_AnDA[i,:,:]
    Grad_AnDA_nadir          	= Gradient(AnDA_nadir,2)
    Post_AnDA_nadir 		= AnDA_ssh_1_nadir.itrp_postAnDA[i,:,:]
    Grad_Post_AnDA_nadir	= Gradient(Post_AnDA_nadir,2)
    # swot
    obs_swot 			= AnDA_ssh_1_swot.Obs[i,:,:]
    VE_DINEOF_swot           	= itrp_dineof_swot[i,:,:]
    Grad_VE_DINEOF_swot 	= Gradient(VE_DINEOF_swot,2)
    AnDA_swot 		 	= AnDA_ssh_1_swot.itrp_AnDA[i,:,:]
    Grad_AnDA_swot          	= Gradient(AnDA_swot,2)
    Post_AnDA_swot 		= AnDA_ssh_1_swot.itrp_postAnDA[i,:,:]
    Grad_Post_AnDA_swot		= Gradient(Post_AnDA_swot,2)
    # nadirswot
    obs_nadirswot 			= AnDA_ssh_1_nadirswot.Obs[i,:,:]
    VE_DINEOF_nadirswot           	= itrp_dineof_nadirswot[i,:,:]
    Grad_VE_DINEOF_nadirswot 		= Gradient(VE_DINEOF_nadirswot,2)
    AnDA_nadirswot 		 	= AnDA_ssh_1_nadirswot.itrp_AnDA[i,:,:]
    Grad_AnDA_nadirswot          	= Gradient(AnDA_nadirswot,2)
    Post_AnDA_nadirswot 		= AnDA_ssh_1_nadirswot.itrp_postAnDA[i,:,:]
    Grad_Post_AnDA_nadirswot		= Gradient(Post_AnDA_nadirswot,2)

    # Display maps
    var=['obs_nadir','obs_swot','obs_nadirswot',\
         'OI','OI','OI',\
         'AnDA_nadir','AnDA_swot','AnDA_nadirswot',\
         'Post_AnDA_nadir','Post_AnDA_swot','Post_AnDA_nadirswot',\
         'VE_DINEOF_nadir','VE_DINEOF_swot','VE_DINEOF_nadirswot',]
    title=['Obs (nadir)','Obs (swot)','Obs (nadir+swot)',\
           'OI (nadir)','OI (nadir)','OI (nadir)',\
           'AnDA (nadir)','AnDA (swot)','AnDA (nadir+swot)',\
           'Post_AnDA (nadir)','Post_AnDA (swot)','Post_AnDA (nadir+swot)',\
           'VE-DINEOF (nadir)','VE-DINEOF (swot)','VE-DINEOF (nadir+swot)']
    fig, ax = plt.subplots(5,4,
                          subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=0.0)))
    # display GT (reference)
    vmin = np.nanmin(gt) ; vmax = np.nanmax(gt)
    cmap="coolwarm"
    plot(ax,0,0,lon,lat,gt,'GT',\
             extent=extent_,cmap=cmap,vmin=vmin,vmax=vmax)
    for ivar in range(0,len(var)):
        i = int(np.floor(ivar/3)) ; j = (ivar%3)+1
        plot(ax,i,j,lon,lat,eval(var[ivar]),title[ivar],\
             extent=extent_,cmap=cmap,vmin=vmin,vmax=vmax)
    plt.subplots_adjust(hspace=0.85,wspace=0.85)
    plt.savefig(resfile1)	# save the figure
    plt.close()			# close the figure

    # Display gradients
    var=['obs_nadir','obs_swot','obs_nadirswot',\
         'Grad_OI','Grad_OI','Grad_OI',\
         'Grad_AnDA_nadir','Grad_AnDA_swot','Grad_AnDA_nadirswot',\
         'Grad_Post_AnDA_nadir','Grad_Post_AnDA_swot','Grad_Post_AnDA_nadirswot',\
         'Grad_VE_DINEOF_nadir','Grad_VE_DINEOF_swot','Grad_VE_DINEOF_nadirswot']
    title=['Obs (nadir)','Obs (swot)','Obs (nadir+swot)',\
           r"$\nabla_{OI}$ (nadir)",r"$\nabla_{OI}$ (nadir)",r"$\nabla_{OI}$ (nadir)",\
           r"$\nabla_{AnDA}$ (nadir)",r"$\nabla_{AnDA}$ (swot)",r"$\nabla_{AnDA} (nadir+swot)$",\
           r"$\nabla_{Post_AnDA}$ (nadir)",r"$\nabla_{Post_AnDA} (swot)$",r"$\nabla_{Post_AnDA} (nadir+swot)$",\
           r"$\nabla_{VE-DINEOF}$ (nadir)",r"$\nabla_{VE-DINEOF} (swot)$",r"$\nabla_{VE-DINEOF} (nadir+swot)$",]
    fig, ax = plt.subplots(5,4,
                          subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=0.0)))
    vmin = np.nanmin(Grad_gt) ; vmax = np.nanmax(Grad_gt)
    cmap="viridis"
    plot(ax,0,0,lon,lat,Grad_gt,r"$\nabla_{GT}$",\
             extent=extent_,cmap=cmap,vmin=vmin,vmax=vmax)
    for ivar in range(0,len(var)):
        i = int(np.floor(ivar/3)) ; j = (ivar%3)+1
        plot(ax,i,j,lon,lat,eval(var[ivar]),title[ivar],\
             extent=extent_,cmap=cmap,vmin=vmin,vmax=vmax)
    plt.subplots_adjust(hspace=0.85,wspace=0.85)
    plt.savefig(resfile2)	# save the figure
    plt.close()			# close the figure

    ## Taylor diagrams (rough variables)
    resfile=workpath+"/Taylor_diagram_maps_"+day+".pdf"
    title=['GT',\
           r"$\nabla_{OI}$",\
           r"$\nabla_{AnDA}$ (nadir)",r"$\nabla_{AnDA}$ (swot)",r"$\nabla_{AnDA} (nadir+swot)$",\
           r"$\nabla_{Post_AnDA}$ (nadir)",r"$\nabla_{Post_AnDA} (swot)$",r"$\nabla_{Post_AnDA} (nadir+swot)$",\
           r"$\nabla_{VE-DINEOF}$ (nadir)",r"$\nabla_{VE-DINEOF} (swot)$",r"$\nabla_{VE-DINEOF} (nadir+swot)$",]
    series={'gt':gt,
            'OI':OI,
            'AnDA_nadir':AnDA_nadir,'AnDA_swot':AnDA_swot,'AnDA_nadirswot':AnDA_nadirswot,
            'Post_AnDA_nadir':Post_AnDA_nadir,'Post_AnDA_swot':Post_AnDA_swot,'Post_AnDA_nadirswot':Post_AnDA_nadirswot,
            'VE_DINEOF_nadir':VE_DINEOF_nadir,'VE_DINEOF_swot':VE_DINEOF_swot,'VE_DINEOF_nadirswot':VE_DINEOF_nadirswot}
    Taylor_diag(series,label,\
                styles=['s','p','p','p','h','h','h','D','D','D'],\
                colors=['y','r','g','b','r','g','b','r','g','b'])
    plt.savefig(resfile)
    plt.close()

    ## Taylor diagrams (gradients)
    resfile=workpath+"/Taylor_diagram_maps_"+day+".pdf"
    label=['GT',\
           'OI',\
           'AnDA (nadir)','AnDA (swot)','AnDA (nadir+swot)',\
           'Post_AnDA (nadir)','Post_AnDA (swot)','Post_AnDA (nadir+swot)',\
           'VE-DINEOF (nadir)','VE-DINEOF (swot)','VE-DINEOF (nadir+swot)']
    series={'gt':gt,
            'Grad_OI':OI,
            'Grad_AnDA_nadir':AnDA_nadir,'Grad_AnDA_swot':AnDA_swot,'Grad_AnDA_nadirswot':AnDA_nadirswot,
            'Grad_Post_AnDA_nadir':Post_AnDA_nadir,'Grad_Post_AnDA_swot':Post_AnDA_swot,'Grad_Post_AnDA_nadirswot':Post_AnDA_nadirswot,
            'Grad_VE_DINEOF_nadir':VE_DINEOF_nadir,'Grad_VE_DINEOF_swot':VE_DINEOF_swot,'Grad_VE_DINEOF_nadirswot':VE_DINEOF_nadirswot}
    Taylor_diag(series,label,\
                styles=['s','p','p','p','h','h','h','D','D','D'],\
                colors=['y','r','g','b','r','g','b','r','g','b'])
    plt.savefig(resfile)
    plt.close()

    ## Radial Power Spectrum (RAPS)
    resfile=workpath+"/results_AnDA_RAPS_"+day+".pdf"
    f_ref, Pf_GT    			= raPsd2dv1(GT,resssh,True)
    f0, Pf_OI 		 		= raPsd2dv1(OI,resssh,True)
    f1_nadir, Pf_AnDA_nadir  		= raPsd2dv1(AnDA_nadir,resssh,True)
    f1_swot, Pf_AnDA_swot  		= raPsd2dv1(AnDA_swot,resssh,True)
    f1_nadirswot, Pf_AnDA_nadirswot  	= raPsd2dv1(AnDA_nadirswot,resssh,True)
    f1_nadir, Pf_AnDA_nadir  		= raPsd2dv1(AnDA_nadir,resssh,True)
    f1_swot, Pf_AnDA_swot  		= raPsd2dv1(AnDA_swot,resssh,True)
    f1_nadirswot, Pf_AnDA_nadirswot  	= raPsd2dv1(AnDA_nadirswot,resssh,True)
    f2_nadir, Pf_postAnDA_nadir 	= raPsd2dv1(Post_AnDA_nadir,resssh,True)
    f2_swot, Pf_postAnDA_swot 		= raPsd2dv1(Post_AnDA_swot,resssh,True)
    f2_nadirswot, Pf_postAnDA_nadirswot = raPsd2dv1(Post_AnDA_nadirswot,resssh,True)
    f3_nadir, Pf_VE_DINEOF_nadir   	= raPsd2dv1(VE_DINEOF_nadir,resssh,True)
    f3_swot, Pf_VE_DINEOF_swot  	= raPsd2dv1(VE_DINEOF_swot,resssh,True)
    f3_nadirswot,Pf_VE_DINEOF_nadirswot = raPsd2dv1(VE_DINEOF_nadirswot,resssh,True)
    wf_ref	        = 1/f_ref
    wf0	        	= 1/f0
    wf1_nadir        	= 1/f1_nadir
    wf1_swot        	= 1/f1_swot
    wf1_nadirswot       = 1/f1_nadirswot
    wf2_nadir         	= 1/f2_nadir
    wf2_swot         	= 1/f2_swot
    wf2_nadirswot       = 1/f2_nadirswot
    wf3_nadir         	= 1/f3_nadir
    wf3_swot         	= 1/f3_swot
    wf3_nadirswot       = 1/f3_nadirswot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(wf_ref,Pf_GT,label='GT','k')
    ax.plot(wf0,Pf_OI,label='OI','y-')
    ax.plot(wf1_nadir,Pf_AnDA_nadir,label='AnDA (nadir)','r-')
    ax.plot(wf1_swot,Pf_AnDA_swot,label='AnDA (swot)','g-')
    ax.plot(wf1_nadirswot,Pf_AnDA_nadirswot,label='AnDA (nadir+swot)','b-')
    ax.plot(wf2_nadir,Pf_postAnDA_nadir,label='postAnDA (nadir)','r--')
    ax.plot(wf2_swot,Pf_postAnDA_swot,label='postAnDA (swot)','g--')
    ax.plot(wf2_nadirswot,Pf_postAnDA_nadirswot,label='postAnDA (nadir+swot)','g--')
    ax.plot(wf3_nadir,Pf_VE_DINEOF_nadir,label='VE-DINEOF (nadir)','ro-')
    ax.plot(wf3_swot,Pf_VE_DINEOF_swot,label='VE-DINEOF(swot)','go-')
    ax.plot(wf3_nadirswot,Pf_VE_DINEOF_nadirswot,label='VE-DINEOF (nadir+swot)','bo-')
    ax.set_xlabel("Wavenumber", fontweight='bold')
    ax.set_ylabel("Power spectral density (m2/(cy/km))", fontweight='bold')
    ax.set_xscale('log') ; ax.set_yscale('log')
    plt.legend(loc='best')
    plt.xticks([50, 100, 200, 500, 1000], ["50km", "100km", "200km", "500km", "1000km"])
    ax.invert_xaxis()
    plt.grid(which='both', linestyle='--')
    plt.savefig(resfile)        # save the figure
    plt.close()         	# close the figure
