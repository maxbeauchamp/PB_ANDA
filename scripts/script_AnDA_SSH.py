#!/usr/bin/env python

""" script_AnDA_SSH.py: Application of MS_AnDA to spatio-temporal interpolation of SSH (sea surface height) from nadir and/or swot datasets. """

__author__ = "Maxime Beauchamp"
__version__ = "2.0"
__date__ = "2019-12-10"
__email__ = "maxime.beauchamp76@gmail.com"

from pb_anda import *
np.random.seed(1)

respath=""

			#*****************************#
			# Parameters setting for ssh  #
			#*****************************#

PR_ssh = PR()
PR_ssh.flag_scale    = True	# True: multi scale, False: one scale                    
PR_ssh.n             = 50	# dimension state (number of EOF coefficients ?)
PR_ssh.patch_r       = 20	# size of patch (patch 1°x1°)
PR_ssh.patch_c       = 20	# size of patch
PR_ssh.training_days = 365-50	# num of training images: 2012-10-01 -> 2013-09-29
PR_ssh.test_days     = 50	# num of test images: 2015
PR_ssh.lag           = 1	# lag of time series: t -> t+lag
PR_ssh.G_PCA         = 20	# N_eof for global PCA

# Input dataset
PR_ssh.var		= "ssh_mod"					 # Variable to assimilate
PR_ssh.path_X 		= datapath+'/data/dataset_nadir_swot.nc'	 # Directory of ssh data
PR_ssh.path_mod 	= datapath+'/maps/NATL60-CJM165_sst_y2013.1y.nc' # Directory of ssh NATL60 maps
PR_ssh.path_OI 		= datapath+'/oi/ssh_NATL60_swot_4nadir.nc'	 # Directory of OI product 
#PR_ssh.path_mask 	= './metop_mask.nc'				 # Directory of observation Mask

# Dataset automatically created during execution
PR_ssh.path_X_lr 		= './ssh_lr.nc'
PR_ssh.path_dX_PCA		= './dX_pca.nc'
PR_ssh.path_index_patches 	= './list_pos.pickle'
PR_ssh.path_neighbor_patches 	= './pair_pos.pickle'

			#*****************************#
			# Parameters setting for ssh  #
			#*****************************#

AF_ssh = General_AF()
AF_ssh.flag_reduced 	= False # True: Reduced version of Local Linear AF
AF_ssh.flag_cond 	= False # True: use Obs at t+lag as condition to select successors,\
				# False: no condition in analog forecasting
AF_ssh.flag_model 	= False # True: Use gradient, velocity as additional regressors in AF
AF_ssh.flag_catalog 	= True 	# True: each catalog for each patch position
                    		# False: only one catalog for all positions
AF_ssh.cluster 		= 1     # clusterized version AF
AF_ssh.k 		= 200 	# number of analogs
AF_ssh.k_initial 	= 200 	# retrieving k_initial nearest neighbors, then using condition to retrieve k analogs 
AF_ssh.neighborhood 	= np.ones([PR_ssh.n,PR_ssh.n]) # global analogs
AF_ssh.regression 	= 'local_linear' # forecasting strategies select among:\
					 # locally_constant, increment, local_linear
AF_ssh.sampling 	= 'gaussian' 
AF_ssh.B 		= 0.0001 # variance of initial state error
AF_ssh.R 		= 0.0001 # variance of observation error

"""  Loading data  """
VAR_ssh = VAR()
VAR_ssh = Load_data(PR_ssh) 

			#***************#
			# Assimilation  #
			#***************#
r_start = 0
c_start = 0
r_length = 100
c_length = 100
level = 100 	# 100 patches executed simultaneously

saved_path =  'saved_path.pickle'
AnDA_ssh_1 = AnDA_result()
MS_AnDA_ssh = MS_AnDA(VAR_ssh, PR_ssh, AF_ssh)
AnDA_ssh_1 = MS_AnDA_ssh.multi_patches_assimilation(level, r_start, r_length, c_start, c_length)

			#****************#
			# Postprocessing #
			#****************#

# remove block artifact (do PCA twice gives perfect results) 
Pre_filtered = np.copy(VAR_ssh.dX_orig[:PR_ssh.training_days,r_start:r_start+r_length,c_start:c_start+c_length]+VAR_ssh.X_lr[:PR_ssh.training_days,r_start:r_start+r_length,c_start:c_start+c_length])
Pre_filtered = np.concatenate((Pre_filtered,AnDA_ssh_1.itrp_AnDA),axis=0)
AnDA_ssh_1.itrp_postAnDA = Post_process(Pre_filtered,len(VAR_ssh.Obs_test),17) 
Pre_filtered = np.copy(VAR_ssh.dX_orig[:PR_ssh.training_days,r_start:r_start+r_length,c_start:c_start+c_length]+VAR_ssh.X_lr[:PR_ssh.training_days,r_start:r_start+r_length,c_start:c_start+c_length])
Pre_filtered = np.concatenate((Pre_filtered,AnDA_ssh_1.itrp_postAnDA),axis=0)
AnDA_ssh_1.itrp_postAnDA = Post_process(Pre_filtered,len(VAR_ssh.Obs_test),13)          
X_initialization = np.copy(VAR_ssh.X_lr[:,r_start:r_start+r_length,c_start:c_start+c_length]+VAR_ssh.dX_orig[:,r_start:r_start+r_length,c_start:c_start+c_length])
X_initialization[PR_ssh.training_days:,:,:] = AnDA_ssh_1.itrp_postAnDA 
X_lr = LR_perform(X_initialization,'',100)
AnDA_ssh_1.itrp_postAnDA = X_lr[PR_ssh.training_days:,:,:]

# Save AnDA result         
with open(saved_path, 'wb') as handle:
    pickle.dump(AnDA_ssh_1, handle)
    
# Reload saved AnDA result
with open(saved_path, 'rb') as handle:
    AnDA_ssh_1 = pickle.load(handle)    

			#*****************#
			# Display results #
			#*****************#

resssh = 0.25
for i in range(165,len(AnDA_ssh_1.GT)):
    day=datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=i),"%Y-%m-%d")

    ## Maps
    resfile=respath+"/results_AnDA_maps_"+day+".pdf"
    # Load data
    gt 			= AnDA_ssh_1.GT[i,:,:]
    obs 		= AnDA_ssh_1.Obs[i,:,:]
    AnDA 		=  AnDA_ssh_1.itrp_AnDA[i,:,:]
    OI 			= AnDA_ssh_1.itrp_OI[i,:,:]
    Post_AnDA 		= AnDA_ssh_1.itrp_postAnDA[i,:,:]
    Grad_gt 		= Gradient(gt,2)
    Grad_AnDA 		= Gradient(AnDA,2)
    Grad_Post_AnDA 	= Gradient(Post_AnDA,2)
    Grad_OI 		= Gradient(OI,2)
    # Display figures
    var=['gt','obs','Grad_gt','OI','AnDA',\
         'Post_AnDA','Grad_AnDA','Grad_OI','Grad_Post_AnDA']
    title=['GT','Obs',r"$\nabla_{GT}$",'OI','AnDA',\
           'Post_AnDA',r"$\nabla_{AnDA}$",r"$\nabla_{OI}$",]
    plt.figure() # open the figure
    for j in range(0,len(var)):
        plt.subplot(3,3,j+1)
        if (var[j])[0:4]=="Grad":
            vmin = np.nanmin(Grad_gt) ; vmax = np.nanmax(Grad_gt)
        else:
            vmin = np.nanmin(gt) ; vmax = np.nanmax(gt)
        plt.imshow(get(var[j]),aspect='auto',cmap='jet',vmin=vmin,vmax=vmax)
        plt.colorbar()
        plt.title('GT')
    plt.save(resfile)	# save the figure
    plt.close()		# close the figure

    ## Radial Power Spectrum (RAPS)
    resfile=respath+"/results_AnDA_RAPS_"+day+".pdf"
    f0, Pf_AnDA  	= raPsd2dv1(AnDA_ssh_1.itrp_AnDA[i,:,:],resssh,True)
    f1, Pf_postAnDA 	= raPsd2dv1(AnDA_ssh_1.itrp_postAnDA[i,:,:],resssh,True)
    f2, Pf_GT    	= raPsd2dv1(AnDA_ssh_1.GT[i,:,:],resssh,True)
    f3, Pf_OI    	= raPsd2dv1(AnDA_ssh_1.itrp_OI[i,:,:],resssh,True)
    wf1         	= 1/f1
    wf2         	= 1/f2
    wf3         	= 1/f3
    plt.figure()
    plt.loglog(wf2,Pf_GT,label='GT')
    plt.loglog(wf3,Pf_OI,label='OI')
    plt.loglog(wf1,Pf_AnDA,label='AnDA')
    plt.loglog(wf2,Pf_postAnDA,label='postAnDA')
    plt.gca().invert_xaxis()
    plt.legend()
    plt.save(resfile)	# save the figure
    plt.close()		# close the figure




