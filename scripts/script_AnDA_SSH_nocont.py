#!/usr/bin/env python

""" script_AnDA_SSH_nocont.py: Application of MS_AnDA to spatio-temporal interpolation of SSH (sea surface height) from nadir and/or swot datasets. """

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

# get the option (nadir, swot or nadirswot)
opt	 = sys.argv[1]
lag	 = sys.argv[2]
type_obs = sys.argv[3]
start    = int(sys.argv[4])
workpath = "/home3/scratch/mbeaucha/resAnDA_"+opt+"_nadlag_"+lag+"_"+type_obs+"_dstart_"+str(start)
if not os.path.exists(workpath):
    mk_dir_recursive(workpath)     
else:
    shutil.rmtree(workpath)
    mk_dir_recursive(workpath)

			#*****************************#
			# Parameters setting for ssh  #
			#*****************************#

PR_ssh = PR()
PR_ssh.flag_scale    = True	# True: multi scale, False: one scale                    
PR_ssh.n             = 50	# dimension state 
PR_ssh.patch_r       = 20	# size of patch (patch 1°x1°)
PR_ssh.patch_c       = 20	# size of patch
PR_ssh.test_days     = 20       # num of test images: 20
PR_ssh.training_days = 365-PR_ssh.test_days # num of training images: 2012-10-01 -> 2013-09-29
PR_ssh.flag_cont     = False     # New option to deal with no continuous data (1)
PR_ssh.start_test    = start     # New option to deal with no continuous data (2)
PR_ssh.lag           = 1	# lag of time series: t -> t+lag
PR_ssh.G_PCA         = 20	# N_eof for global PCA

# Input dataset
PR_ssh.var		= "ssh_"+type_obs  # Variable to assimilate
# Directory of ssh data
if opt=="nadir":
    PR_ssh.path_X	= datapath+'/data/gridded_data_swot_wocorr/dataset_nadir_'+lag+'d.nc'
elif opt=="swot":
    PR_ssh.path_X       = datapath+'/data/gridded_data_swot_wocorr/dataset_swot.nc'   	
else:
    PR_ssh.path_X       = datapath+'/data/gridded_data_swot_wocorr/dataset_nadir_'+lag+'d_swot.nc'
PR_ssh.path_mod 	= datapath+'/maps/NATL60-CJM165_ssh_y2013.1y.nc' # Directory of ssh NATL60 maps
PR_ssh.path_OI 		= datapath+'/oi/ssh_NATL60_4nadir.nc'	 # Directory of OI product 

# Dataset automatically created during execution
PR_ssh.path_X_lr 		= workpath+'/ssh_lr.nc'
PR_ssh.path_dX_PCA		= workpath+'/dX_pca.nc'
PR_ssh.path_index_patches 	= workpath+'/list_pos.pickle'
PR_ssh.path_neighbor_patches 	= workpath+'/pair_pos.pickle'

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
#AF_ssh.regression 	= 'local_linear' # forecasting strategies select among:\
					 # locally_constant, increment, local_linear
AF_ssh.regression       = 'optimal_interpolation'
AF_ssh.sampling 	= 'gaussian' 
AF_ssh.B 		= 0.0001 # variance of initial state error
if type_obs=="mod":
    AF_ssh.R 		= 0.0001 # variance of observation error
    AF_ssh.Runiq        = True
if type_obs=="obs":
    AF_ssh.Runiq        = False
    if AF_ssh.Runiq == True:
        AF_ssh.R        = 0.001 # variance of observation error (25-36cm, cf. discussion with M.Ballarotta CLS)

"""  Loading data  """
VAR_ssh = VAR()
print('Loading Data...')
VAR_ssh = Load_data(PR_ssh) 
print('...Done')

if AF_ssh.Runiq == False:
    ## *** Fit nadir variance *** ##
    print('Fit nadir error variance coefficients...')
    # estimate the coefficients
    AF_ssh.coeff    = fit_Rvar(VAR_ssh.Obs_train,VAR_ssh.Mod_train,VAR_ssh.timelag_train,2)
    AF_ssh.R        = np.polyval(AF_ssh.coeff,VAR_ssh.timelag_test)
    # plot
    plotFit_Rvar(VAR_ssh.Obs_train,VAR_ssh.Mod_train,VAR_ssh.timelag_train,2,\
                 workpath+"/boxplot_error_lag.pdf")
    print('...Done')

			#***************#
			# Assimilation  #
			#***************#
r_start = 0
c_start = 0
r_length = 10*20
c_length = 10*20
lon = np.arange(-65,-65+((1/20)*r_length),1/20)
lat = np.arange(30,30+((1/20)*c_length),1/20)
extent_=[np.min(lon),np.max(lon),np.min(lat),np.max(lat)]
level = 20 	# 20 patches executed simultaneously

saved_path =  workpath+'/saved_path.pickle'

# To compare with MS-AnDA
print('Start MS-VE-DINEOF...')
itrp_dineof = MS_VE_Dineof(PR_ssh, VAR_ssh.dX_orig+VAR_ssh.X_lr,\
                           VAR_ssh.Optimal_itrp+VAR_ssh.X_lr[PR_ssh.training_days:],\
                           VAR_ssh.Obs_test+VAR_ssh.X_lr[PR_ssh.training_days:],20,50)
itrp_dineof = itrp_dineof[:,:r_length,:c_length]
print('...Done')

print('Start assimilation...')
AnDA_ssh_1 = AnDA_result()
MS_AnDA_ssh = MS_AnDA(VAR_ssh, PR_ssh, AF_ssh)
AnDA_ssh_1 = MS_AnDA_ssh.multi_patches_assimilation(level, r_start, r_length, c_start, c_length)
print('...Done')

			#****************#
			# Postprocessing #
			#****************#

print('Start Post-processing...')
# remove block artifact (do PCA twice gives perfect results) 
Pre_filtered = np.copy(VAR_ssh.dX_orig[:PR_ssh.training_days,r_start:r_start+r_length,c_start:c_start+c_length]+VAR_ssh.X_lr[:PR_ssh.training_days,r_start:r_start+r_length,c_start:c_start+c_length])
Pre_filtered = np.concatenate((Pre_filtered,AnDA_ssh_1.itrp_AnDA),axis=0)
AnDA_ssh_1.itrp_postAnDA = Post_process(Pre_filtered,len(VAR_ssh.Obs_test),17,15) 
print('... Done 1st step')
Pre_filtered = np.copy(VAR_ssh.dX_orig[:PR_ssh.training_days,r_start:r_start+r_length,c_start:c_start+c_length]+VAR_ssh.X_lr[:PR_ssh.training_days,r_start:r_start+r_length,c_start:c_start+c_length])
Pre_filtered = np.concatenate((Pre_filtered,AnDA_ssh_1.itrp_postAnDA),axis=0)
AnDA_ssh_1.itrp_postAnDA = Post_process(Pre_filtered,len(VAR_ssh.Obs_test),13,15)      
print('... Done 2nd step')
X_initialization = np.copy(VAR_ssh.X_lr[:,r_start:r_start+r_length,c_start:c_start+c_length]+VAR_ssh.dX_orig[:,r_start:r_start+r_length,c_start:c_start+c_length])
X_initialization[PR_ssh.training_days:,:,:] = AnDA_ssh_1.itrp_postAnDA 
X_lr = LR_perform(X_initialization,'',100)
AnDA_ssh_1.itrp_postAnDA = X_lr[PR_ssh.training_days:,:,:]
print('...Done')
                
# Save AnDA result         
with open(saved_path, 'wb') as handle:
    pickle.dump([AnDA_ssh_1, itrp_dineof], handle)
    

