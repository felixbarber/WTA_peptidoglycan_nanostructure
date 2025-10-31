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

#base_path = '/mnt/d/Documents_D/Rojas_lab/data/'
# base_path = '/Users/felixbarber/Documents/Rojas_lab/data/'
# base_path = '/Volumes/data_ssd1/Rojas_Lab/data/'
base_path = '/Volumes/data_ssd2/Rojas_Lab/data/'
thresh_peak=900
rescale=False  # Means that we rescale according to mean rather than minimum value. Accounts for things being lower intensity in HADa vs EDADA staining
min_thresh=0.0

# Note: Scenes_remove starts counting from 1.

# expt_id, date = '/221012_bFB69_Tun_gr_HADA', '10/12/22'
# conds=['120min']
# conditions = ['120 min, 0.5ug/mL Tun']
# time_labels = ['120 min']
# num_scenes = [5]
# scenes_remove = [[]]  # scenes to remove from consideration
# channels, HADA_channel, im_shape = [3], 3, [1500, 1500]
# label = 'HADA'
# thresh = 0  # threshold average outline fluorescence to filter out debris

# expt_id, date = '/220309_bFB69_Tun_gr_HADA', '03/09/22'
# conds=['60min']
# conditions = ['60 min, 0.5ug/mL Tun']
# time_labels = ['60 min']
# num_scenes = [6]
# scenes_remove = [[]]  # scenes to remove from consideration
# channels, HADA_channel, im_shape = [3], 3, [1500, 1500]
# label = 'HADA'
# thresh = 0  # threshold average outline fluorescence to filter out debris
# thresh_peak=450

# expt_id, date = '/221214_bFB7_HADA_Tun', '12/05/22'
# conds=['LB', '0min', '5min','10min']
# conditions=['LB', '0 min, 0.5ug/mL Tun', '5 min, 0.5ug/mL Tun', '10 min, 0.5ug/mL Tun', '5 min v2, 0.5ug/mL Tun']
# time_labels=['LB', '0 min', '5 min', '10 min']
# num_scenes=[6,7,8,9]
# scenes_remove=[[1,2,3,4,5],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6,7]] # scenes to remove from consideration — this is
# # because these scenes were in rows 3 & 4 so had poor growth conditions.
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'
# thresh = 0 # threshold average outline fluorescence to filter out debris

# expt_id, date = '/220120_bFB7_HADA_Tun', '01/20/21'
# conds=['LB','5min', '10min','15min']
# conditions=['LB','5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# time_labels=['LB', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# num_scenes=[8,7,7,7]
# scenes_remove=[[],[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'
# thresh=0

# expt_id, date = '/220121_bFB66_Tun_gr_HADA', '01/21/22'
# conds=['45min']
# conditions = ['45 min, 0.5ug/mL Tun']
# time_labels = ['45 min']
# num_scenes = [6]
# scenes_remove = [[]]  # scenes to remove from consideration
# channels, HADA_channel, im_shape = [3], 3, [1500, 1500]
# label = 'HADA'
# thresh = 0  # threshold average outline fluorescence to filter out debris
# thresh_peak=0.1 # adjusted the threshold peak for half exposure time.

# expt_id, date = '/220204_bFB69_Tun_gr_HADA', '02/04/22'
# conds=['45min']
# conditions = ['45 min, 0.5ug/mL Tun']
# time_labels = ['45 min']
# num_scenes = [6]
# scenes_remove = [[]]  # scenes to remove from consideration
# channels, HADA_channel, im_shape = [3], 3, [1500, 1500]
# label = 'HADA'
# thresh = 0  # threshold average outline fluorescence to filter out debris
# thresh_peak=0.1

# expt_id, date = '/240202_bFB205_Tun_HADA', '01/31/24'
# conds=['LB', '5min', '15min']
# conditions = ['LB', '5 min, 0.5ug/mL Tun', '15 min, 0.5ug/mL Tun']
# time_labels = ['LB', '5 min', '15 min']
# num_scenes = [5,6,6]
# scenes_remove = [[], [],[]]  # scenes to remove from consideration
# channels, HADA_channel, im_shape = [2], 2, [1500, 1500]
# label = 'HADA'
# thresh = 0  # threshold average outline fluorescence to filter out debris

# expt_id, date = '/240131_bFB205_Tun_HADA', '01/31/24'
# conds=['LB', '0min', '5min', '10min']
# conditions = ['LB', '0 min, 0.5ug/mL Tun', '5 min, 0.5ug/mL Tun', '10 min, 0.5ug/mL Tun']
# time_labels = ['LB', '0 min', '5 min', '10 min']
# num_scenes = [5, 5,5,6]
# scenes_remove = [[], [],[],[]]  # scenes to remove from consideration
# channels, HADA_channel, im_shape = [2], 2, [1500, 1500]
# label = 'HADA'
# thresh = 0  # threshold average outline fluorescence to filter out debris

# expt_id, date = '/220111_bFB79_HADA_Tun', '01/11/22'
# conds=['LB','0min', '5min','10min']
# conditions=['LB', '0 mins, 0.5ug/mL Tun', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun']
# time_labels=['LB', '0 mins, 0.5ug/mL Tun', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun']
# num_scenes=[4,4,6,6]
# scenes_remove=[[],[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'
# thresh=0   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/220104_bFB79_Tun_HADA', '01/04/22'
# conds=['LB','0min', '5min','10min']
# conditions=['LB', '0 mins, 0.5ug/mL Tun', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun']
# time_labels=['LB', '0 mins, 0.5ug/mL Tun', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun']
# num_scenes=[6,6,6,6]
# scenes_remove=[[],[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'
# thresh=0   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/220113_bFB79_HADA_Tun', '01/04/21'
# conds=['LB','5min', '10min','15min']
# conditions=['LB','5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# time_labels=['LB', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# num_scenes=[8,7,7,7]
# scenes_remove=[[],[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'
# thresh=0   # threshold average outline fluorescence to filter out debris
# thresh_peak=2000

# expt_id, date = '/241113_bFB69_Tun_HADA', '11/13/24'
# conds=["LB", "0min", "5min", "10min"]
# conditions=['LB', '0 mins, 0.5ug/mL Tun','5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun']
# time_labels=['-5 min','0 mins, 0.5ug/mL Tun','5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun']
# num_scenes=[7,7,7,7]
# scenes_remove=[[], [], [], []] # scenes to remove from consideration-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'
# thresh=0   # threshold average outline fluorescence to filter out debris
# thresh_peak=0.2

# expt_id, date = '/240202_bFB69_Tun_HADA', '02/02/24'
# conds=['LB', '5min', '15min', '25min']
# conditions = ['LB', '5 min, 0.5ug/mL Tun', '15 min, 0.5ug/mL Tun', '25 min, 0.5ug/mL Tun']
# time_labels = ['LB', '5 min', '15 min', '25 min']
# num_scenes = [6,6,6, 5]
# scenes_remove = [[], [],[], []]  # scenes to remove from consideration
# channels, HADA_channel, im_shape = [2], 2, [1500, 1500]
# label = 'HADA'
# thresh = 0  # threshold average outline fluorescence to filter out debris
# thresh_peak=0.2

# expt_id, date = '/220207_bFB69_Tun_HADA', '02/02/22'
# conds=['LB','5min', '10min','15min']
# conditions=['LB','5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# time_labels=['LB', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# num_scenes=[10,10,10,10]
# scenes_remove=[[],[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'
# thresh = 0  # threshold average outline fluorescence to filter out debris
# thresh_peak=450

# expt_id, date = '/240126_bFB66_Tun_HADA', '01/26/24'
# conds=['LB', '0min', '5min', '10min']
# conditions = ['LB', '0 min, 0.5ug/mL Tun', '5 min, 0.5ug/mL Tun', '10 min, 0.5ug/mL Tun']
# time_labels = ['LB', '0 min', '5 min', '10 min']
# num_scenes = [4, 5,5,5]
# scenes_remove = [[], [],[],[]]  # scenes to remove from consideration
# channels, HADA_channel, im_shape = [2], 2, [1500, 1500]
# label = 'HADA'
# thresh = 0  # threshold average outline fluorescence to filter out debris
# thresh_peak=0.2

# expt_id, date = '/210416_FB2_HADA_Staining', '04/16/21'
# conds=['LB', '5min','10min','15min','25min']
# conditions=['LB', '5 min 0.5ug/mL Tun', '5 min 0.5ug/mL Tun v2', '10 min 0.5ug/mL Tun', '15 min 0.5ug/mL Tun',
#             '25 min 0.5ug/mL Tun']
# time_labels=['LB', '5 min', '5 min v2', '10 min', '15 min', '25 min']
# num_scenes=[10,10,5,10,10,10]
# scenes_remove=[[],[],[],[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'
# thresh = 0  # threshold average outline fluorescence to filter out debris

# expt_id, date = '/210416_FB2_HADA_Staining', '04/16/21' # This one is the version to run for the paper
# conds=['LB', '5min','10min','15min','25min']
# conditions=['LB', '5 min 0.5ug/mL Tun', '10 min 0.5ug/mL Tun', '15 min 0.5ug/mL Tun',
#             '25 min 0.5ug/mL Tun']
# time_labels=['LB', '5 min', '10 min', '15 min', '25 min']
# num_scenes=[10,10,10,10,10]
# scenes_remove=[[],[],[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'
# thresh = 0  # threshold average outline fluorescence to filter out debris
# thresh_peak=0.2


# expt_id, date = '/220104_bFB66_Tun_HADA', '01/04/21'
# conds=['LB','0min', '5min','10min']
# conditions=['LB', '0 mins, 0.5ug/mL Tun', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun']
# time_labels=['LB', '0 mins', '5 min', '10 min']
# num_scenes=[7,7,7,7]
# scenes_remove=[[],[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'
# thresh=0   # threshold average outline fluorescence to filter out debris
# thresh_peak=0.2

expt_id, date = '/250616_bFB6_xylose_depletion_HADA', '06/16/25'
conds=['0min', '15min', '30min','60min']
conditions=['0 min depletion', '10 min depletion', '25 min depletion', '60 min depletion']
time_labels=['0 min', '10 min', '25 min', '60 min']
num_scenes=[2,2,2,2]
scenes_remove=[[],[],[],[]] # scenes to remove from considerarion-
channels, HADA_channel, im_shape=[2], 2, [1500,1500]
label = 'HADA'
thresh=0   # threshold average outline fluorescence to filter out debris
thresh_peak=0.1

# expt_id, date = '/250612_bFB66_EDADA_tun_full', '6/12/25'
# conds=["LB", "tun_hi", "fos", "untreated"]
# conditions=["LB", "Tun", "fos", "untreated"]
# time_labels=['-5 min', '5 min', '10 min', '15 min']
# num_scenes=[20,20,10,6]
# scenes_remove=[[], [7], [5],[3]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'AF-AF488-azide'
# thresh=0   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/250613_bFB66_EDADA_tun_full', '6/13/25'
# conds=["LB", "tun", "fos", "unstained"]
# conditions=["LB", "Tun", "fos", "untreated"]
# time_labels=['-5 min', '5 min', '10 min', '15 min']
# num_scenes=[20,20,10,6]
# scenes_remove=[[], [7], [5],[3]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'AF-AF488-azide'
# thresh=0   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/250613_bFB66_EDADA_tun_full_rep2', '6/13/25 v2'
# conds=["LB", "tun", "fos", "unstained"]
# conditions=["LB", "Tun", "fos", "untreated"]
# time_labels=['-5 min', '5 min', '10 min', '15 min']
# num_scenes=[20,20,10,6]
# scenes_remove=[[], [2,3,4], [],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'AF-AF488-azide'
# thresh=0   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/250616_bFB66_EDADA', '6/16/25'
# conds=["LB", "Tun", "fos", "tun_van","van", "untreated"]
# conditions=["LB", "Tun", "fos", "tun_van","van", "untreated"]
# time_labels=['-5 min', '5 min', '10 min', '15 min', '20 min', '25 min']
# num_scenes=[20,20,12,15,15,10]
# scenes_remove=[[], [8,9], [],[14],[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'AF-AF488-azide'
# thresh=0   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/250610_bFB66_tun_EDADA', '6/10/25'
# conds=["LB_1", "LB_2", "tun_1", "tun_2","LB_1_PI_day2", "LB_2_PI_day2", "tun_1_PI_day2", "tun_2_PI_day2"]
# conditions=["LB_1", "LB_2", "tun_1", "tun_2","LB_1_PI_day2", "LB_2_PI_day2", "tun_1_PI_day2", "tun_2_PI_day2"]
# time_labels=['-5 min', '5 min', '10 min', '15 min', '20 min', '25 min', '30 min', '35 min']
# num_scenes=[10,10,18,10,10,10,10,10]
# scenes_remove=[[7], [], [7,11],[4,5],[],[],[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'AF-AF488-azide'
# thresh=0   # threshold average outline fluorescence to filter out debris


# expt_id, date = '/241130_bFB69_GlpQ_antibody_pads', '11/30/24'
# conds=["Buffer", "GlpQ", "Control"]
# conditions=['Buffer', 'GlpQ', 'Control']
# time_labels=['-5 min', '5 min', '10 min']
# num_scenes=[5,5, 5]
# scenes_remove=[[], [], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'anti-His-AF488'
# thresh=0   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241129_bFB69_GlpQ_antibody_staining_pads', '11/29/24'
# conds=["Buffer", "GlpQ", "Control"]
# conditions=['Buffer', 'GlpQ', 'Control']
# time_labels=['-5 min', '5 min', '10 min']
# num_scenes=[5,5, 5]
# scenes_remove=[[], [], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'anti-His-AF488'
# thresh=20   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241126_bFB69_GlpQ_antibody_staining_pads', '11/26/24'
# conds=["Buffer", "GlpQ"]
# conditions=['Buffer', 'GlpQ']
# time_labels=['-5 min', '5 min']
# num_scenes=[5,5]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'anti-His-AF488'
# thresh=50   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241121_bFB69_GlpQ_antibody_staining', '11/21/24'
# conds=["Buffer", "GlpQ"]
# conditions=['Buffer', 'GlpQ']
# time_labels=['-5 min', '5 min']
# num_scenes=[6,6]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'anti-His-AF488'
# thresh=0   # threshold average outline fluorescence to filter out debris


# expt_id, date = '/241117_bFB69_LB_WGA_control', '11/17/24'
# conds=["LB", "10min"]
# conditions=['LB', '10min']
# time_labels=['-5 min', '5 min']
# num_scenes=[1,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-AF488'
# thresh=200   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241115_bFB69_LB_Van_control', '11/15/24'
# conds=["LB", "10min"]
# conditions=['LB', '10min']
# time_labels=['-5 min', '5 min']
# num_scenes=[1,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin-Bodipy'
# thresh=100   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241114_bFB69_Tun_Van_pads', '11/14/24'
# conds=["Tun", "LB", "LB_v2"]
# conditions=['Tun', 'LB', 'LB_v2']
# time_labels=['-5 min', '5 min', '10 min']
# num_scenes=[10,10, 10]
# # scenes_remove=[[6,7,8,9,10], [6,7,8,9,10],[]] # scenes to remove from considerarion-
# scenes_remove=[[], [],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin-Bodipy'
# thresh=100   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241114_bFB66_GlpQ_Van_pads', '11/14/24'
# conds=["GlpQ", "Buffer"]
# conditions=['GlpQ', 'Buffer']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin-Bodipy'
# thresh=100   # threshold average outline fluorescence to filter out debris





# expt_id, date = '/241113_bFB69_Tun_Van_pads_v2', '11/13/24 v2'
# conds=["Tun", "LB"]
# conditions=['Tun', 'LB']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin-Bodipy'
# thresh=100   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241113_bFB69_Tun_Van_pads_v1', '11/13/24'
# conds=["Tun", "LB"]
# conditions=['Tun', 'LB']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin-Bodipy'
# thresh=100   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241113_bFB66_GlpQ_Van_pads_v1', '11/13/24'
# conds=["GlpQ", "Buffer"]
# conditions=['GlpQ', 'Buffer']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin-Bodipy'
# thresh=100   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241112_bFB66_Tun_Van_pads', '11/12/24'
# conds=["Tun", "LB"]
# conditions=['Tun', 'LB']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin-Bodipy'
# thresh=100   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241112_bFB66_Tun_WGA_pads', '11/12/24'
# conds=["Tun", "LB"]
# conditions=['Tun', 'LB']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-AF488'
# thresh=100   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241112_bFB66_GlpQ_Van_pads', '11/12/24'
# conds=["GlpQ", "Buffer"]
# conditions=['GlpQ', 'Buffer']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin-Bodipy'
# thresh=100   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241108_bFB66_Tun_Van', '11/08/24'
# conds=["Tun", "LB"]
# conditions=['Tun', 'LB']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin-Bodipy'
# thresh=200   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241108_bFB69_GlpQ_WGA_pads_azide', '11/08/24'
# conds=["WGA", "Buffer"]
# conditions=['GlpQ', 'Buffer']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-488'
# thresh=200   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241105_bFB69_GlpQ_WGA_pads', '11/05/24'
# conds=["GlpQ", "Buffer"]
# conditions=['GlpQ', 'Buffer']
# conditions=['GlpQ', 'Buffer']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-488'
# thresh=200   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241105_bFB66_Tun_van', '11/05/24'
# conds=["LB", "Tun"]
# conditions=['LB', 'Tun']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,10]
# scenes_remove=[[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin-Bodipy'
# thresh=100   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241025_bFB66_Tun_WGA_pads', '10/25/24'
# conds=["LB", "Tun", "Tun_v1"]
# conditions=['LB', 'Tun', "Tun rep"]
# time_labels=['-5 min', '5 min', '10 min']
# num_scenes=[10,11,10]
# scenes_remove=[[],[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-AF488'
# thresh=200   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241024_bFB69_GlpQ_WGA_pads', '10/24/24'
# conds=["GlpQ", "GlpQ_v1", "Buffer"]
# conditions=['GlpQ', 'GlpQ rep', "Buffer"]
# time_labels=['-5 min', '5 min', '10 min']
# num_scenes=[12,10,10]
# scenes_remove=[[],[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-AF488'
# thresh=200   # threshold average outline fluorescence to filter out debris


#
# expt_id, date = '/241024_bFB66_Tun_WGA_pads', '10/18/24'
# conds=["Tun", "LB"]
# conditions=['Tun', 'LB']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,12]
# scenes_remove=[[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-AF488'
# thresh=100   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241023_bFB69_Tun_WGA_pads', '10/23/24'
# conds=["Tun", "LB", "LB_v2"]
# conditions=['Tun', 'LB', 'LB repeat']
# time_labels=['-5 min', '5 min', '15 min']
# num_scenes=[10,10, 10]
# scenes_remove=[[],[], []] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-AF488'
# thresh=500   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241022_bFB69_Tun_WGA_pads_LB', '10/22/24'
# conds=["Tun", "LB"]
# conditions=['Tun', 'LB']
# time_labels=['-5 min', '5 min']
# num_scenes=[10,10]
# scenes_remove=[[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-AF488'
# thresh=500   # threshold average outline fluorescence to filter out debris
# #
# expt_id, date = '/241018_bFB69_WGA_LB_pads', '10/18/24'
# conds=["Tun", "LB"]
# conditions=['Tun', 'LB']
# time_labels=['-5 min', '5 min']
# num_scenes=[11,8]
# scenes_remove=[[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-AF488'
# thresh=500   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241015_bFB69_Tun_WGA', '10/15/24'
# conds=["Tun", "LB"]
# conditions=['Tun', 'LB']
# time_labels=['-5 min', '5 min']
# num_scenes=[6,6]
# scenes_remove=[[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-AF488'
# thresh=300   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241011_bFB69_Tun_WGA', '10/11/24'
# conds=["Tun", "LB"]
# conditions=['Tun', 'LB']
# time_labels=['-5 min', '5 min']
# num_scenes=[5,5]
# scenes_remove=[[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-AF488'
# thresh=300   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/241008_bFB69_Tun_WGA', '10/08/24'
# conds=["Tun", "LB"]
# conditions=['Tun', 'LB']
# time_labels=['-5 min', '5 min']
# num_scenes=[7,7]
# scenes_remove=[[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-AF488'
# thresh=300   # threshold average outline fluorescence to filter out debris


# expt_id, date = '/241007_bFB69_GlpQ_WGA', '10/07/24'
# conds=["GlpQ", "buffer"]
# conditions=['GlpQ', 'PBS']
# time_labels=['-5 min', '5 min']
# num_scenes=[7,7]
# scenes_remove=[[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'WGA-AF488'
# thresh=300   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/240913_bFB66_GlpQ_FLVan', '09/13/24'
# conds=["GlpQ", "PBS"]
# conditions=['GlpQ', 'PBS']
# time_labels=['-5 min', '5 min']
# num_scenes=[7,7]
# scenes_remove=[[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin'
# thresh=300   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/240912_bFB66_GlpQ_FLVan', '09/12/24'
# conds=["GlpQ", "PBS"]
# conditions=['GlpQ', 'PBS']
# time_labels=['-5 min', '5 min']
# num_scenes=[5,5]
# scenes_remove=[[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin'
# thresh=300   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/240911_bFB66_Tun_FLVan', '09/11/24'
# conds=["Tun", "LB"]
# conditions=['Tun', 'LB']
# time_labels=['-5 min', '5 min']
# num_scenes=[5,5]
# scenes_remove=[[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin-Bopidy'
# thresh=300   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/240911_bFB66_FLVan', '09/11/24'
# conds=["GlpQ", "PBS"]
# conditions=['GlpQ', 'PBS']
# time_labels=['-5 min', '5 min']
# num_scenes=[6,5]
# scenes_remove=[[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Vancomycin-Bodipy'
# thresh=300   # threshold average outline fluorescence to filter out debris

# expt_id, date = '/210506_FB6_inducer_loss', '05/06/21'
# conds=['Xylose_induced', '10min', '25min','60min']
# conditions=['Xylose induced', '10 min depletion', '25 min depletion', '60 min depletion']
# time_labels=['-5 min', '10 min', '25 min', '60 min']
# num_scenes=[7,6,7,6]
# scenes_remove=[[],[],[],[]] # scenes to remove from considerarion-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'
# thresh=0   # threshold average outline fluorescence to filter out debris
# thresh_peak=0.1





# expt_id, date = '/210401_BS168_LB_HADA', '04/01/21'
# conds=['LB']
# conditions=['LB']
# num_scenes=[8]
# channels, HADA_channel, im_shape=[2], 2, [1192,1192]

# expt_id, date = '/210401_BS168_Tun_HADA_expt4', '04/01/21'
# conds=['0_5ug_Tun']
# conditions=['25 min 0.5ug/mL Tun']
# num_scenes=[5]
# channels, HADA_channel, im_shape=[2], 2, [1192,1192]

# expt_id, date = '/210429_FB1_HADA_staining_cellasic', '04/29/21'
# conds=['LB', '15min_0_5ugTun', '25min_0_5ugTun']
# conditions=['LB', '15 min 0.5ug/mL Tun', '25 min 0.5ug/mL Tun']
# num_scenes=[5,6,9]
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]

# expt_id, date = '/211012_ponA_tun_HADA', '10/12/21'
# conds=['bFB1_0_5uM', 'bFB1_0_25uM', 'bFB1_0_125uM','bFB1_LB','bFB45_0_5uM', 'bFB45_0_25uM', 'bFB45_0_125uM','bFB45_LB']
# conditions=['WT, 0.5uM Tun', 'WT, 0.25uM Tun', 'WT, 0.125uM Tun', 'WT, LB', 'ponA, 0.5uM Tun',\
            # 'ponA, 0.25uM Tun', 'ponA, 0.125uM Tun', 'ponA, LB']
# time_labels=['WT, 0.5uM Tun', 'WT, 0.25uM Tun', 'WT, 0.125uM Tun', 'WT, LB', 'ponA, 0.5uM Tun',\
            # 'ponA, 0.25uM Tun', 'ponA, 0.125uM Tun', 'ponA, LB']
# num_scenes=[10,10,10,10,10,10,10,10]
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]


# expt_id, date = '/211104_ConA_labeling', '11/04/21'
# conds=['bER18_GlpQPhoD', 'bER18_PBS', 'bFB46_GlpQPhoD','bFB46_PBS','bER18_unlabeled']
# conditions=['WT PY79, GlpQ & PhoD', 'WT PY79, PBS', 'tagE PY79, GlpQ & PhoD', 'tagE PY79, PBS', 'WT PY79, unlabeled']
# time_labels=['WT PY79, GlpQ & PhoD', 'WT PY79, PBS', 'tagE PY79, GlpQ & PhoD', 'tagE PY79, PBS', 'WT PY79, unlabeled']
# num_scenes=[11,10,10,10,10]
# scenes_remove=[[2,7],[1,10],[3,4,9],[2,3,4],[3,4,9,10]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'ConA'

# expt_id, date = '/211111_bFB10_ConA_Tun', '11/11/21'
# conds=['0min', '0min_v2', '5min','10min','15min','20min','25min']
# conditions=['LB', 'LB repeat', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun', '15 mins, 0.5ug/mL Tun', '20 mins, 0.5ug/mL Tun', '25 mins, 0.5ug/mL Tun']
# time_labels=['LB', 'LB repeat', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun', '15 mins, 0.5ug/mL Tun', '20 mins, 0.5ug/mL Tun', '25 mins, 0.5ug/mL Tun']
# num_scenes=[9,10,10,11,11,12,12]
# scenes_remove=[[3,7],[2,6,7,8],[4,10],[4,5,8],[2,4,5,6,8],[5,8],[2]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'ConA'

# expt_id, date = '/220107_bFB66_ConA_primed', '01/07/22'
# conds=['LB','LB_v2', '60min_Tun','60min_Tun_v2']
# conditions=['LB', 'LB v2', '60 mins, 0.5ug/mL Tun', '60 mins, 0.5ug/mL Tun v2']
# time_labels=['LB', 'LB v2', '60 mins, 0.5ug/mL Tun', '60 mins, 0.5ug/mL Tun v2']
# num_scenes=[6,6,6,5]
# scenes_remove=[[],[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'ConA'




# expt_id, date = '/220121_bFB66_ConA_pads', '01/25/21'
# conds=['LB','LB_v2', '5h_Tun']
# conditions=['LB','LB_v2', '5 hours, 0.5ug/mL Tun']
# time_labels=['LB','LB_v2', '5 hours, 0.5ug/mL Tun']
# num_scenes=[10,10,10]
# scenes_remove=[[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'

# expt_id, date = '/220202_bFB8_Tun_HADA', '02/02/22'
# conds=['LB','5min', '10min','15min']
# conditions=['LB','5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# time_labels=['LB', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# num_scenes=[8,9,10,6]
# scenes_remove=[[],[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'HADA'





# expt_id, date = '/221205_bFB69_Bocillin_Tun', '12/05/22'
# conds=['LB', '0min', '5min','10min']
# conditions=['LB', '0 min, 0.5ug/mL Tun', '5 min, 0.5ug/mL Tun', '10 min, 0.5ug/mL Tun']
# time_labels=['LB', '0 min', '5 min', '10 min']
# num_scenes=[6,6,6,7]
# scenes_remove=[[],[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Bocillin-FL'

# expt_id, date = '/221212_bFB69_Bocillin_Tun', '12/05/22'
# conds=['LB', '0min', '5min','10min', '5min_v2']
# conditions=['LB', '0 min, 0.5ug/mL Tun', '5 min, 0.5ug/mL Tun', '10 min, 0.5ug/mL Tun', '5 min v2, 0.5ug/mL Tun']
# time_labels=['LB', '0 min', '5 min', '10 min', '5 min v2']
# num_scenes=[6,6,5,6,5]
# scenes_remove=[[],[],[],[],[]] # scenes to remove from considerarion
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'Bocillin-FL'
# thresh = 300 # threshold average outline fluorescence to filter out debris



# expt_id, date = '/230206_bFB1_HADA_Tun', '02/06/23'
# conds=['LB', '5min']
# conditions = ['LB', '5 min, 0.5ug/mL Tun']
# time_labels = ['LB', '5 min']
# num_scenes = [7, 8]
# scenes_remove = [[], []]  # scenes to remove from consideration
# channels, HADA_channel, im_shape = [2], 2, [1500, 1500]
# label = 'HADA'
# thresh = 300  # threshold average outline fluorescence to filter out debris

# expt_id, date = '/230203_bFB108_HADA_Tun', '02/06/23'
# conds=['LB', '5min']
# conditions = ['LB', '5 min, 0.5ug/mL Tun']
# time_labels = ['LB', '5 min']
# num_scenes = [4, 4]
# scenes_remove = [[], []]  # scenes to remove from consideration
# channels, HADA_channel, im_shape = [2], 2, [1500, 1500]
# label = 'HADA'
# thresh = 300  # threshold average outline fluorescence to filter out debris

# expt_id, date = '/230203_bFB107_HADA_Tun', '02/06/23'
# conds=['LB', '5min']
# conditions = ['LB', '5 min, 0.5ug/mL Tun']
# time_labels = ['LB', '5 min']
# num_scenes = [6, 7]
# scenes_remove = [[], []]  # scenes to remove from consideration
# channels, HADA_channel, im_shape = [2], 2, [1500, 1500]
# label = 'HADA'
# thresh = 300  # threshold average outline fluorescence to filter out debris


out_dir="./outputs"+expt_id
pval=0.01

if not os.path.exists(out_dir):
    os.mkdir(out_dir)
    os.mkdir(out_dir+'/images')

expt_vals_ls=[]
for i0 in range(len(conds)):
    expt_vals_ls.append({'expt_id':expt_id, 'channels':channels,'im_shape':im_shape,
           'base_path':base_path, 'num_scenes':num_scenes[i0], 'cond':conds[i0], 'HADA_channel':HADA_channel, 'date':date,
           'excl_scenes':scenes_remove[i0],'thresh_peak':thresh_peak, 'min_thresh':min_thresh, 'rescale':rescale})

if not os.path.exists(out_dir+expt_id):
    dfs=[]
    for i0 in range(len(expt_vals_ls)):
        print(i0)
        # expt_vals_ls[i0]['median_vals']=imkit.timepoint_bkgd_fluorescence_calculation(expt_vals_ls[i0])
        # dfs.append(imkit.timepoint_import_data_outline(expt_vals_ls[i0]))
        temp_out,temp_ims=imkit.timepoint_import_data_outline_smart_bkgd(expt_vals_ls[i0])
        for i1 in range(len(temp_ims)):
            fig=plt.figure(figsize=[8,8])
            plt.imshow(temp_ims[i1])
            plt.axis('off')
            fig.savefig(out_dir+'/images'+expt_vals_ls[i0]['expt_id']+'_'+expt_vals_ls[i0]['cond']+'_s{0}.png'.format(i1),dpi=300,bbox_inches='tight')
            plt.clf()
        dfs.append(temp_out)
        del temp_ims, temp_out
        dfs[i0]['Condition']=conditions[i0]
        dfs[i0]['Date']=expt_vals_ls[i0]['date']
        
    for i0 in range(len(dfs)):  
        temp_df=dfs[i0].rename(columns={'Average F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'Average '+label,
                            'Integrated F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'Integrated '+label,
                                       'Average outline F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'Average outline '+label,
                            'Integrated outline F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'Integrated outline '+label,
                            'CV outline F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'CV outline '+label,
                            'SD outline F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'SD outline '+label,
                            'Skew outline F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'Skew outline '+label})
        if i0==0:
            df=temp_df.copy()
        else:
            df = df.append(temp_df[[obj for obj in df.columns]])
    df.to_pickle(out_dir+expt_id)
else:
    df=pd.read_pickle(out_dir+expt_id)

df = df[df['Average outline '+label] > thresh]  # filtering out debris that isn't fluorescent.


def iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,plot_points=True,showfliers=True, temp_hue=None):
    # fig=plt.figure(figsize=[6,4])
    fig = plt.figure()
    ax=plt.subplot(1,1,1)
    if temp_hue is None:
        plot=sns.boxplot(x=temp_iter,y=temp_var,data=df,fliersize=0,showfliers=showfliers)
        if plot_points:
            plot=sns.stripplot(x=temp_iter,y=temp_var,dodge=True,data=df,color='k',edgecolor='black',linewidth=1,alpha=0.1)
    else:
        plot = sns.boxplot(x=temp_iter, y=temp_var, data=df, fliersize=0, showfliers=showfliers, hue=temp_hue)
        if plot_points:
            plot = sns.stripplot(x=temp_iter, y=temp_var, dodge=True, data=df, color='k', edgecolor='black',
                                 linewidth=1, alpha=0.1, hue=temp_hue)
    plot.set(xlabel=temp_xlabel,ylabel=temp_ylab)
    plt.xticks(rotation = 90)
    
    print('Statistical significances for ', temp_var)
    temp_iter_vals=df[temp_iter].unique()
    print(temp_iter_vals)
    for i0 in range(len(temp_iter_vals)):
        cond1=temp_iter_vals[i0]
        for cond2 in temp_iter_vals[i0:]:
            if cond1!=cond2:
                x1=df[df[temp_iter]==cond1][temp_var]
                x2=df[df[temp_iter]==cond2][temp_var]
                print('Condition 1: '+cond1+',','Condition 2: '+cond2+':', scipy.stats.ttest_ind(x2, x1, axis=0, equal_var=False, nan_policy='propagate')[1] < pval)

    return fig,ax
print(df.Scene[:10])
# Now we plot the results and save the figures

sys.stdout = open(out_dir+expt_id+'_outputs.txt', "w")

# HADA average length density of puncta
temp_var, temp_out_name, temp_ylab='Cell spots/length', 'cell_spots_length', r'Cellular puncta/$\mu$m'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA average length density of wall puncta
temp_var, temp_out_name, temp_ylab='Wall spots/length', 'wall_spots_length', r'Peripheral puncta/$\mu$m'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()



# HADA average number of puncta
temp_var, temp_out_name, temp_ylab='Cell spots', 'cell_spots', 'Cellular puncta'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA average number of puncta
temp_var, temp_out_name, temp_ylab='Wall spots', 'wall_spots', 'Peripheral puncta'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline average values
temp_var, temp_out_name, temp_ylab='Average outline '+label, 'av_outline_fl', 'Average outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline average values
temp_var, temp_out_name, temp_ylab='Average '+label, 'av_area_fl', 'Average area fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline average values
temp_var, temp_out_name, temp_ylab='Average outline '+label, 'av_outline_fl', 'Average outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,plot_points=False,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'_no_data.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline average values
temp_var, temp_out_name, temp_ylab='Average outline '+label, 'av_outline_fl', 'FDAA Fluorescence'
temp_iter,temp_xlabel='Condition',''
excl='5 min 0.5ug/mL Tun v2'
sns.set(font_scale=1.5)
sns.set_style("whitegrid")
fig,ax=iter_plotting(df[df.Condition!=excl], temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,plot_points=False)
# print(df[df.Condition!='5 min 0.5ug/mL Tun v2'].Condition.unique())
ax.set_xticklabels(time_labels)
# ax.set_ylim(top=4000)
# ax.set_ylim(top=2000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'_excl_repeat.eps',dpi=300,bbox_inches='tight')
plt.clf()


# HADA area average values
temp_var, temp_out_name, temp_ylab='Average '+label, 'av_area_fl', 'Average area fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,plot_points=False,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'_no_data.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline integrated values
temp_var, temp_out_name, temp_ylab='Integrated outline '+label, 'int_outline_fl', 'Integrated outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline integrated values
temp_var, temp_out_name, temp_ylab='Average outline '+label, 'av_outline_fl', 'Average outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,temp_hue='Scene')
plt.legend(loc=[1.05,0.0])
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'_by_scene.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline integrated values
temp_var, temp_out_name, temp_ylab='Integrated outline '+label, 'int_outline_fl', 'Integrated outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,temp_hue='Scene')
plt.legend(loc=[1.05,0.0])
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'_by_scene.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA area integrated values
temp_var, temp_out_name, temp_ylab='Integrated '+label, 'int_area_fl', 'Integrated area fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline CV values
temp_var, temp_out_name, temp_ylab='CV outline '+label, 'cv_outline_fl', 'CV outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline SD values
temp_var, temp_out_name, temp_ylab='SD outline '+label, 'sd_outline_fl', 'SD outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline CV values
temp_var, temp_out_name, temp_ylab='CV outline '+label, 'cv_outline_fl', 'CV outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,plot_points=False,showfliers=False)
plt.ylim(ymax=2.5)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'_nopoints.png',dpi=300,bbox_inches='tight')
plt.clf()
sys.stdout.close()
