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
sns.set_style("whitegrid")
from skimage.morphology import disk
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
import image_toolkit as imkit

# This is to be run after cell_staining_timepoint_EDADA.py on 250610_bFB66_tun_EDADA to combine replicates. We also add
# a replicate number to each other expt.

path = '/Volumes/data_ssd2/Rojas_Lab/data/'
output_dir = './outputs/compiled_data/staining_plots/'


# Note: we only run this part once!
if not os.path.exists(output_dir+'EDADA_reformatting.txt'):

    expt_ids = ['/250610_bFB66_tun_EDADA']
    group_id = 'WT_EDADA_click'
    label = 'AF-AF488-azide'
    norm_cond = 'LB'  # Setting this here since this is the standard normalization condition
    thresh=0
    plotting_conds=['LB_1', 'LB_2', 'tun_1', 'tun_2']

    ind = 0
    df = None
    temp_df1 = pd.DataFrame()
    expt_id = expt_ids[ind]
    data_dir = "./outputs" + expt_id
    # Reading input data
    df = pd.read_pickle(data_dir + expt_id)
    df.index = np.arange(len(df))
    df.insert(7, 'Replicate', np.nan * np.ones(len(df)))
    for ind in range(len(df)):
        df.loc[ind, 'Replicate'] = df.loc[ind, 'Condition'][-1]
        df.loc[ind, 'Condition'] = df.loc[ind, 'Condition'][:-2]
    out_dir="./outputs"+expt_id
    df.to_pickle(out_dir+expt_id)
    with open(output_dir+'EDADA_reformatting.txt', "w") as f:
        print('I have run cell_staining_EDADA_reformatting.py already',file=f)

# This part doesn't matter if it's run multiple times.
expt_ids = ['/250612_bFB66_EDADA_tun_full', '/250613_bFB66_EDADA_tun_full','/250613_bFB66_EDADA_tun_full_rep2','/250616_bFB66_EDADA']
for ind in range(len(expt_ids)):
    temp_df1 = pd.DataFrame()
    expt_id =expt_ids[ind]
    out_dir = "./outputs" + expt_id
    data_dir = "./outputs" + expt_id

    df = pd.read_pickle(data_dir + expt_id)
    df['Replicate']=1
    df.to_pickle(out_dir+expt_id)
    df.head()