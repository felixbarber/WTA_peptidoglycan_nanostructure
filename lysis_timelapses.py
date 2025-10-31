import scipy
import skimage
import sys
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from numpy import matlib
import seaborn as sns
import math
import os
import scipy.optimize
import scipy.io as sio
from scipy import stats
import scipy.ndimage
# import h5py
sns.set(font_scale=1.5)
sns.set_style("white")
from skimage.morphology import disk
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
import image_toolkit as imkit

base_path = '/Users/felixbarber/Documents/Rojas_Lab/data/'

expt_id, date = '/230321_bFB7_Tun_lysis', '03/21/23'
num_scenes = 7
num_timepoints = 28  # number of timesteps
timestep = 300 # timestep in seconds.
channels = [2]
HADA_channel = 2  # the channel for integrating fluorescence
thresh_int = 2000
strain = 'cwlO'
condition = 'Tunicamycin'

out_dir = "./outputs" + expt_id
pval = 0.01
im_shape = [1500,1500]

if not os.path.exists(out_dir):
    os.mkdir(out_dir)
    os.mkdir(out_dir + '/images')

if not os.path.exists(out_dir + expt_id):  # if this experiment hasn't been analyzed in part before now
    expt_vals = {'expt_id': expt_id, 'channels': channels, 'im_shape': im_shape, 'base_path': base_path,
                 'num_scenes': num_scenes, 'FDAA_channel': HADA_channel, 'date': date, 'num_scenes': num_scenes,
                 'num_timepoints': num_timepoints, 'timestep': timestep, 'strain': strain, 'condition':condition}
    df = imkit.hydrolysis_outline_smart_bkgd(expt_vals, redo=True, thresh_int=thresh_int, timelapse_file_storage=True)
        # This gives the dataframe for this experiment

        # df['Condition'] = expt_vals['condition']
        # if conds.index(condition) == 0:
        #     df1 = df.copy()
        # else:
        #     df1 = pd.concat([df1, df])
    df1 = df.rename(columns={'Average F{0}'.format(expt_vals['FDAA_channel']): 'Average FDAA',
                            'Integrated F{0}'.format(expt_vals['FDAA_channel']): 'Integrated FDAA',
                            'Average outline F{0}'.format(expt_vals['FDAA_channel']): 'Average outline FDAA',
                            'Integrated outline F{0}'.format(expt_vals['FDAA_channel']): 'Integrated outline FDAA',
                            'CV outline F{0}'.format(expt_vals['FDAA_channel']): 'CV outline FDAA',
                            'SD outline F{0}'.format(expt_vals['FDAA_channel']): 'SD outline FDAA'})
    df1.to_pickle(out_dir + expt_id)
else:
    df = pd.read_pickle(out_dir + expt_id)

# df.to_pickle(out_dir + expt_id)
