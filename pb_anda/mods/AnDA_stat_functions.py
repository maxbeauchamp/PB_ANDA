#!/usr/bin/env python

""" AnDA_stat_functions.py: Collection of statistical functions used in AnDA. """

__author__ = "Phi Huynh Viet"
__version__ = "2.0"
__date__ = "2017-08-01"
__email__ = "phi.huynhviet@telecom-bretagne.eu"

from .AnDA_transform_functions import Imputing_NaN
import numpy as np
import mpl_toolkits.axisartist.grid_finder as GF
import mpl_toolkits.axisartist.floating_axes as FA
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.projections import PolarAxes
import netCDF4
import pandas as pd

def fit_Rvar(obs,mod,lag,deg):
    """ Fit the polynomial coefficients of function f,
        var(obs-mod)=f(timelag)
    """

    obs = obs.flatten()
    mod = mod.flatten()
    lag = lag.flatten()

    idx = ~np.isnan(obs)  
    obs = obs[idx]
    mod = mod[idx]
    err=obs-mod
    lag = lag[idx]

    dfr = pd.DataFrame(np.transpose(np.asarray([err,lag])),columns=['error','lag'])
    var= dfr.groupby("lag").error.agg(np.var)
    var.index = np.arange(1,len(var)+1)
    coeff = np.polyfit(np.unique(lag), var, deg)
    
    return coeff

def plotFit_Rvar(obs,mod,lag,deg,ofile):
    """ Plot the polynomial coefficients fitting of function f,
        var(obs-mod)=f(timelag)
    """

    obs = obs.flatten()
    mod = mod.flatten()
    lag = lag.flatten()

    idx = ~np.isnan(obs)
    obs = obs[idx]
    mod = mod[idx]
    err=obs-mod
    lag = lag[idx]

    dfr = pd.DataFrame(np.transpose(np.asarray([err,lag])),columns=['error','lag'])
    var= dfr.groupby("lag").error.agg(np.var)
    var.index = np.arange(1,len(var)+1)
    coeff = np.polyfit(np.unique(lag), var, deg)

    fig, ax = plt.subplots(figsize=(10,7))
    fit = pd.Series(np.polyval(coeff, np.unique(lag)))
    fit.index = np.arange(1,len(var)+1)
    ax.plot(fit,'k-',linewidth=2,label=r"$\mathrm{\widehat{Var}}[y-Hx | lag]=f(lag)$")
    ax.plot(var,'r--',linewidth=1.25,label=r"$\mathrm{Var}[y-Hx | lag]$")
    # boxplot
    bp = dfr.boxplot(column="error",by="lag", showfliers=False,ax=ax, rot=45) 
    ticks = ax.xaxis.get_ticklocs()
    ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
    ax.xaxis.set_ticks(ticks[::10])
    ax.xaxis.set_ticklabels(ticklabels[::10])
    ax.set_ylim([-0.25,0.25])
    ax.legend()
    plt.title('')
    fig.suptitle('')
    plt.savefig(ofile)
    plt.close()


def AnDA_RMSE(a,b):
    """ Compute the Root Mean Square Error between 2 n-dimensional vectors. """
    if (a.ndim==1):
        a = a[np.newaxis]
    if (a.ndim>2):
        a = a.reshape(a.shape[0],-1)
    if (b.ndim==1):
        b = b[np.newaxis]    
    if (b.ndim>2):
        b = b.reshape(b.shape[0],-1)
    return np.sqrt(np.nanmean((a-b)**2,1))

    
def AnDA_CRMSE(a,b):
    """ Compute the Root Mean Square Error between 2 n-dimensional vectors. """
    if (a.ndim==1):
        a = a[np.newaxis]
    if (a.ndim>2):
        a = a.reshape(a.shape[0],-1)
    if (b.ndim==1):
        b = b[np.newaxis]
    if (b.ndim>2):
        b = b.reshape(b.shape[0],-1)
    abar = np.nanmean(a)
    bbar = np.nanmean(b)
    return np.sqrt(np.nanmean(((a-abar)-(b-bbar))**2,1))
    
def AnDA_correlate(a,b):
    """ Compute the Correlation between 2 n-dimensional vectors. """
    if (a.ndim==1):
        a = a[np.newaxis]
    if (a.ndim>2):
        a = a.reshape(a.shape[0],-1)
    if (b.ndim==1):
        b = b[np.newaxis] 
    if (b.ndim>2):
        b = b.reshape(b.shape[0],-1)
    a = a - np.nanmean(a,1)[np.newaxis].T
    b = b - np.nanmean(b,1)[np.newaxis].T
    r = np.nansum((a*b),1) / np.sqrt(np.nansum((a*a),1) * np.nansum((b*b),1))
    return r   

def AnDA_Taylor_stats(a,b):
    """ Compute the Taylor Statistics between 2 n-dimensional vectors. """
    abar = np.nanmean(a)
    bbar = np.nanmean(b)
    crmsd = np.sqrt(np.nanmean(((a-abar)-(b-bbar))**2))
    sd    = np.sqrt(np.nanmean((a-abar)**2))
    a = a - np.nanmean(a)
    b = b - np.nanmean(b)
    corr = np.nansum((a*b)) / np.sqrt(np.nansum((a*a)) * np.nansum((b*b)))
    return [crmsd, corr, sd]

def Taylor_diag(series,names,styles,colors):
    """ Taylor Diagram : obs is reference data sample
        in a full diagram (0 --> npi)
        --------------------------------------------------------------------------
        Input: series     - dict with all time series (lists) to analyze  
               series[0]  - is the observation, the reference by default.
    """
    from matplotlib.projections import PolarAxes
    taylor_stats = np.array([AnDA_Taylor_stats(series[i],series[list(series.keys())[0]]) for i in series.keys()])
    crmsd, corr, std = taylor_stats.T
    ref = std[0]
    rlocs = np.concatenate((np.arange(0,10,0.25),[0.95,0.99]))
    str_rlocs = np.concatenate((np.arange(0,10,0.25),[0.95,0.99]))
    tlocs = np.arccos(rlocs)        # Conversion to polar angles
    gl1 = GF.FixedLocator(tlocs)    # Positions
    tf1 = GF.DictFormatter(dict(zip(tlocs, map(str,rlocs))))   
    str_locs2 = np.arange(0,11,0.5)
    tlocs2 =  np.arange(0,11,0.5)      # Conversion to polar angles  
    g22 = GF.FixedLocator(tlocs2)  
    tf2 = GF.DictFormatter(dict(zip(tlocs2, map(str,str_locs2))))
    tr = PolarAxes.PolarTransform()
    smin = 0
    smax = (120/100)*np.max(std)
    ghelper = FA.GridHelperCurveLinear(tr,
                                           extremes=(0,np.pi/2, # 1st quadrant
                                                     smin,smax),
                                           grid_locator1=gl1,
                                           #grid_locator2=g11,
                                           tick_formatter1=tf1,
                                           tick_formatter2=tf2,
                                           )
    fig = plt.figure(figsize=(10,5), dpi=100)
    ax = FA.FloatingSubplot(fig, 111, grid_helper=ghelper)
    fig.add_subplot(ax)
    ax.axis["top"].set_axis_direction("bottom") 
    ax.axis["top"].toggle(ticklabels=True, label=True)
    ax.axis["top"].major_ticklabels.set_axis_direction("top")
    ax.axis["top"].label.set_axis_direction("top")
    ax.axis["top"].label.set_text("Correlation Coefficient")
    ax.axis["left"].set_axis_direction("bottom") 
    ax.axis["left"].label.set_text("Standard Deviation")
    ax.axis["right"].set_axis_direction("top") 
    ax.axis["right"].toggle(ticklabels=True, label=True)
    ax.axis["right"].set_visible(True)
    ax.axis["right"].major_ticklabels.set_axis_direction("bottom")
    ax.axis["right"].label.set_text("Standard Deviation")
    ax.axis["bottom"].set_visible(False) 
    ax.grid(True)
    ax = ax.get_aux_axes(tr)
    t = np.linspace(0, np.pi/2)
    r = np.zeros_like(t) + ref
    ax.plot(t,r, 'k--', label='_')
    rs,ts = np.meshgrid(np.linspace(smin,smax),
                            np.linspace(0,np.pi/2))
    rms = np.sqrt(ref**2 + rs**2 - 2*ref*rs*np.cos(ts))
    CS =ax.contour(ts, rs,rms,cmap=cm.bone)
    plt.clabel(CS, inline=1, fontsize=10)
    ax.plot(np.arccos(0.9999),ref,'k',marker='*',ls='', ms=10)
    aux = range(1,len(corr))
    #colors = plt.matplotlib.cm.jet(np.linspace(0,1,len(corr)))
    for i in reversed(aux):
        ax.plot(np.arccos(corr[i]), std[i],c=colors[i],alpha=0.7,marker=styles[i],label="%s" %names[i])
        #ax.text(np.arccos(corr[i]), std[i],"%s"%i)
    # inset axes....
    '''axins = ax.inset_axes([1.1, 0, 0.3, 0.3])
    def pol2cart(phi, rho):
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return(x, y)
    x = np.empty(len(aux))
    y = np.empty(len(aux))
    for i in reversed(aux):
        x[i-1], y[i-1] = pol2cart(np.arccos(corr[i]), std[i]) 
        axins.plot(x[i-1], y[i-1], c=colors[i],alpha=0.7,marker=styles[i],label="%s" %names[i])
        #axins.text(x[i-1], y[i-1],"%s"%i)
    # sub region of the original image
    x1, x2, y1, y2 = np.min(x)-(1/50)*np.min(x), np.max(x)+(1/50)*np.max(x),\
                     np.min(y)-(1)*np.min(y), np.max(y)+(1)*np.max(y)
    axins.set_xlim(x1,x2)
    axins.set_ylim(y1,y2)
    axins.set_xticks([])
    axins.set_yticks([])
    axins.set_xticklabels('')
    axins.set_yticklabels('')'''
    plt.legend(bbox_to_anchor=(1.5, 1),prop=dict(size='small'),loc='best')

def AnDA_stdev(a):
    """ Compute the Correlation between 2 n-dimensional vectors. """
    if (a.ndim==1):
        a = a[np.newaxis]
    if (a.ndim>2):
        a = a.reshape(a.shape[0],-1)
    abar = np.nanmean(a)
    return np.sqrt(np.nanmean((a-abar)**2,1))
   

def normalise(M):
    """ Normalize the entries of a multidimensional array sum to 1. """
    c = np.sum(M)
    # Set any zeros to one before dividing
    d = c + 1*(c==0)
    M = M/d
    return M

def mk_stochastic(T):
    """ Ensure the matrix is stochastic, i.e., the sum over the last dimension is 1. """

    if len(T.shape) == 1:
        T = normalise(T)
    else:
        n = len(T.shape)
        # Copy the normaliser plane for each i.
        normaliser = np.sum(T,n-1);
        normaliser = np.dstack([normaliser]*T.shape[n-1])[0]
        # Set zeros to 1 before dividing
        # This is valid since normaliser(i) = 0 iff T(i) = 0

        normaliser = normaliser + 1*(normaliser==0)
        T = T/normaliser.astype(float)
    return T

def sample_discrete(prob, r, c):
    """ Sampling from a non-uniform distribution. """

    cumprob = np.cumsum(prob)
    n = len(cumprob)
    R = np.random.rand(r,c)
    M = np.zeros([r,c])
    for i in range(0,n-1):
        M = M+1*(R>cumprob[i])    
    return int(M)

def resampleMultinomial(w):
    """ Multinomial resampler. """

    M = np.max(w.shape);
    Q = np.cumsum(w,0);
    Q[M-1] = 1; # Just in case...
    i = 0;
    indx = [];
    while (i<=(M-1)):
        sampl = np.random.rand(1,1);
        j = 0;
        while (Q[j]<sampl):
            j = j+1;
        indx.append(j);
        i = i+1
    return indx

def inv_using_SVD(Mat, eigvalMax):
    """ SVD decomposition of Matrix. """
    
    U,S,V = np.linalg.svd(Mat, full_matrices=True);
    eigval = np.cumsum(S)/np.sum(S);
    # search the optimal number of eigen values
    i_cut_tmp = np.where(eigval>=eigvalMax)[0];
    S = np.diag(S);
    V = V.T;
    i_cut = np.min(i_cut_tmp)+1
    U_1 = U[0:i_cut,0:i_cut]
    U_2 = U[0:i_cut,i_cut:]
    U_3 = U[i_cut:,0:i_cut]
    U_4 = U[i_cut:,i_cut:]
    S_1 = S[0:i_cut,0:i_cut]
    S_2 = S[0:i_cut,i_cut:]
    S_3 = S[i_cut:,0:i_cut]
    S_4 = S[i_cut:,i_cut:]
    V_1 = V[0:i_cut,0:i_cut]
    V_2 = V[0:i_cut,i_cut:]
    V_3 = V[i_cut:,0:i_cut]
    V_4 = V[i_cut:,i_cut:]
    tmp1 = np.dot(np.dot(V_1,np.linalg.inv(S_1)),U_1.T);
    tmp2 = np.dot(np.dot(V_1,np.linalg.inv(S_1)),U_3.T);
    tmp3 = np.dot(np.dot(V_3,np.linalg.inv(S_1)),U_1.T);
    tmp4 = np.dot(np.dot(V_3,np.linalg.inv(S_1)),U_3.T);
    inv_Mat = np.concatenate((np.concatenate((tmp1,tmp2),axis=1),np.concatenate((tmp3,tmp4),axis=1)),axis=0);
    tmp1 = np.dot(np.dot(U_1,S_1),V_1.T);
    tmp2 = np.dot(np.dot(U_1,S_1),V_3.T);
    tmp3 = np.dot(np.dot(U_3,S_1),V_1.T);
    tmp4 = np.dot(np.dot(U_3,S_1),V_3.T);
    hat_Mat = np.concatenate((np.concatenate((tmp1,tmp2),axis=1),np.concatenate((tmp3,tmp4),axis=1)),axis=0);
    det_inv_Mat = np.prod(np.diag(S[0:i_cut,0:i_cut]));   
    return inv_Mat;
 
def inv_using_Woodbury(ainv,u,cinv,v,rinv):
    """ inv using Woodbury equation """
    
    tmp = inv_using_SVD(cinv+np.dot(v,u)*rinv,0.9999)
    tmp_inv = -rinv*rinv*np.dot(np.dot(u,tmp),v)
    np.fill_diagonal(tmp_inv,tmp_inv.diagonal()+ainv)
    #return ainv-rinv*rinv*np.dot(np.dot(u,tmp),v)
    return tmp_inv
    
def hanning2d(M, N):
    """
    A 2D hanning window, as per IDL's hanning function.  See numpy.hanning for the 1d description
    """
    
    if N <= 1:
        return np.hanning(M)
    elif M <= 1:
        return np.hanning(N) # scalar unity; don't window if dims are too small
    else:
        return np.outer(np.hanning(M),np.hanning(N))

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(phi, rho)

def avg_raPsd2dv1(img3d,res,hanning):
    """ Computes and plots radially averaged power spectral density mean (power
     spectrum) of an image set img3d along the first dimension.
    """
    N = img3d.shape[0]
    for i in range(N):
        img=img3d[i,:,:]
        f_, Pf_ = raPsd2dv1(img,res,hanning)
        if i==0:
            f, Pf = f_, Pf_
        else:
            f = np.vstack((f,f_))
            Pf= np.vstack((Pf,Pf_))
    Pf = np.mean(Pf,axis=0)
    return f_, Pf

def avg_err_raPsd2dv1(img3d,img3dref,res,hanning):
    """ Computes and plots radially averaged power spectral density error mean (power
     spectrum) of an image set img3d along the first dimension.
    """
    N = img3d.shape[0]
    for i in range(N):
        img1 = img3d[i,:,:]
        img2 = img3dref[i,:,:]
        f_, Pf_ = raPsd2dv1(img1-img2,res,hanning)
        Pf_     = (Pf_/raPsd2dv1(img2,res,hanning)[1])
        if i==0:
            f, Pf = f_, Pf_
        else:
            f = np.vstack((f,f_))
            Pf= np.vstack((Pf,Pf_))
    Pf = np.mean(Pf,axis=0)
    return f_, Pf

def err_raPsd2dv1(img,imgref,res,hanning):
    """ Computes and plots radially averaged power spectral density error (power
     spectrum).
    """
    f_, Pf_ = raPsd2dv1(img-imgref,res,hanning)
    Pf_     = (Pf_/raPsd2dv1(imgref,res,hanning)[1])
    return f_, Pf_
    
def raPsd2dv1(img,res,hanning):
    """ Computes and plots radially averaged power spectral density (power
     spectrum) of image IMG with spatial resolution RES.
    """
    img = img.copy()
    N, M = img.shape
    if hanning:
        img = hanning2d(*img.shape) * img       
    img =  Imputing_NaN(img)     
    imgf = np.fft.fftshift(np.fft.fft2(img))
    imgfp = np.power(np.abs(imgf)/(N*M),2)    
    # Adjust PSD size
    dimDiff = np.abs(N-M)
    dimMax = max(N,M)
    if (N>M):
        if ((dimDiff%2)==0):
            imgfp = np.pad(imgfp,((0,0),(int(dimDiff/2),int(dimDiff/2))),'constant',constant_values=np.nan)
        else:
            imgfp = np.pad(imgfp,((0,0),(int(dimDiff/2),1+int(dimDiff/2))),'constant',constant_values=np.nan)
            
    elif (N<M):
        if ((dimDiff%2)==0):
            imgfp = np.pad(imgfp,((int(dimDiff/2),int(dimDiff/2)),(0,0)),'constant',constant_values=np.nan)
        else:
            imgfp = np.pad(imgfp,((int(dimDiff/2),1+int(dimDiff/2)),(0,0)),'constant',constant_values=np.nan)
    halfDim = int(np.ceil(dimMax/2.))
    X, Y = np.meshgrid(np.arange(-dimMax/2.,dimMax/2.-1+0.00001),np.arange(-dimMax/2.,dimMax/2.-1+0.00001))           
    theta, rho = cart2pol(X, Y)                                              
    rho = np.round(rho+0.5)   
    Pf = np.zeros(halfDim)
    f1 = np.zeros(halfDim)
    for r in range(halfDim):
      Pf[r] = np.nansum(imgfp[rho == (r+1)])
      f1[r] = float(r+1)/dimMax
    f1 = f1/res
    return f1, Pf

def build_LR(HR,GT,pct_var_init=.6,HPF=150):
# HR: the T*2D map
# GT: the T*2D ground truth map
# pct_var_init: pct of variance explained by PCA
# HPF: value (in km) to satisfy spectral value=0
    stop = False
    pct_var = pct_var_init
    while not stop:
        # compute LR with N_eof
        lr = np.copy(HR).reshape(HR.shape[0],-1)
        tmp = lr[0,:]
        sea_v2 = np.where(~np.isnan(tmp))[0]
        lr_no_land = lr[:,sea_v2]
        pca = PCA(n_components=pct_var_init)
        score_global = pca.fit_transform(lr_no_land)
        coeff_global = pca.components_.T
        mu_global = pca.mean_
        DataReconstructed_global = np.dot(score_global, coeff_global.T) +mu_global
        lr[:,sea_v2] = DataReconstructed_global
        lr = lr.reshape(HR.shape)
        # test if HPF is satisfied
        resssh=4
        f, Pf = avg_err_raPsd2dv1(lr,GT,resssh,True)
        index = ((1./f)-HPF).argmin()
        if np.abs(Pf[index]-1.)<1e-2:
            stop=True
        else:
            pct_var=pct_var+0.05
    return lr
