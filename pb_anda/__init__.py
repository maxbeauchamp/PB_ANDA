"""
PB_ANDA (new modifications by mbeaucha) 
"""

__author		= "Maxime Beauchamp"
__version__ 		= "0.0.1"
__last_modification__	= "2019-12-10"

##################################
# Standard lib
##################################
import sys
import os
import shutil
import time as timer
from os.path import join as join_paths
from datetime import date, datetime, timedelta
import itertools
import warnings
import traceback
import re
import functools
import configparser
import builtins
import time
from time import sleep
import multiprocessing
import mkl
import cv2
from tqdm import tqdm
from collections import OrderedDict
import pickle

assert sys.version_info >= (3,6), "Need Python>=3.6"

##################################
# Config
##################################
dirs = {}

# Define paths
datapath="/home3/datawork/mbeaucha"
basepath="/home3/datahome/mbeaucha/algo/PB_ANDA"

print("Initializing PB-AnDA libraries...",flush=True)

##################################
# Scientific and mapping
##################################
import matplotlib.pyplot as plt
import pandas as pd
import shapely
from shapely import wkt
#import geopandas as gpd
from cartopy import crs as ccrs
import cartopy.feature as cfeature
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.sparse import diags
from scipy.stats import multivariate_normal
from scipy.ndimage.morphology import distance_transform_edt as bwdist
from scipy.interpolate import RegularGridInterpolator
import skill_metrics as sm
import xarray as xr
import netCDF4
from pyflann import *
import xesmf as xe

##################################
# Tools
##################################
from .mods.tools import *
from .mods.AnDA_variables import PR, VAR, General_AF, AnDA_result
from .mods.AnDA_stat_functions import raPsd2dv1, err_raPsd2dv1, avg_raPsd2dv1, avg_err_raPsd2dv1, fit_Rvar, plotFit_Rvar
from .mods.AnDA_transform_functions import Load_data, Gradient, Post_process, LR_perform, VE_Dineof, MS_VE_Dineof, Imputing_NaN, PCA_perform
from .mods.AnDA_stat_functions import AnDA_RMSE, AnDA_CRMSE, AnDA_correlate, AnDA_stdev, Taylor_diag
from .mods.AnDA_Multiscale_Assimilation import Multiscale_Assimilation as MS_AnDA

print("...Done") # ... initializing Libraries



