import scipy
import sys
from scipy import io
import numpy as np
import numpy.matlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle
import seaborn as sns
import pandas as pd
from numpy import matlib
import seaborn as sns
import math
import os
import scipy.optimize
import scipy.io as sio
from scipy import stats
import scipy.ndimage

sns.set(font_scale=1.5)
sns.set_style("whitegrid")

# base_path = '/mnt/d/Documents_D/Rojas_lab/data/'
# base_path = '/Users/felixbarber/Documents/Rojas_lab/data/'
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path = '/Volumes/easystore_hdd/Rojas_Lab/data/'
# data_path='/Users/felixbarber/Documents/Rojas_lab/data/'
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'

# This script can be applied to generate a set of basic plots for an experiment with two, sequential antibiotic shocks.
# It is specifically designed so that it allows for different timesteps in different parts of the experiment.

# Should we remove the non-growing cells? This likely depends on the experiment, but in theory the segmented cells
remove_non_growing_cells = True
remove_fliers = True

expt_id = '/250612_bFB66_s750_tun_gr'
tsteps = 151
dt = 60.0*np.ones(tsteps-1) # time interval between timepoints in seconds
labels = ['Tunicamycin added']
t_pert = [20*60.0]
max_time_truncation = 160*60.0
scene_nums = 1
max_width = 3.0
min_width = 0.5
min_length = 2.0
perform_ttest=False
base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250613_bFB66_s750_tun_gr'
# tsteps = 151
# dt = 60.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [20*60.0]
# max_time_truncation = 160*60.0
# scene_nums = 1
# max_width = 3.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250522_bFB66_s750_tun_gr'
# tsteps = 151
# dt = 60.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [20*60.0]
# max_time_truncation = 160*60.0
# scene_nums = 1
# max_width = 3.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250520_bFB66_s750_tun_gr'
# tsteps = 151
# dt = 60.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [20*60.0]
# max_time_truncation = 160*60.0
# scene_nums = 1
# max_width = 3.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250519_bFB7_tun_gr'
# tsteps = 166
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 2
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250515_bFB66_tun_pad'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [-190.0]
# max_time_truncation = 140*60.0
# scene_nums = 1
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250515_bFB66_LB_pad'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [-200.0]
# max_time_truncation = 140*60.0
# scene_nums = 1
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250514_bFB69_LB_pad_rep2'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [-200.0]
# max_time_truncation = 140*60.0
# scene_nums = 1
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250514_bFB69_LB_pad'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [-200]
# max_time_truncation = 140*60.0
# scene_nums = 1
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250513_bFB66_s750_tun_gr_p2'
# tsteps = 71
# dt = 60.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [-38*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width = 2.0
# min_width = 0.5
# min_length = 1.5
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250513_bFB66_s750_tun_gr'
# tsteps = 53
# dt = 60.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [20.0*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width = 2.0
# min_width = 0.5
# min_length = 1.5
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250512_bFB66_tun_pad'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [-300.0]
# max_time_truncation = 140*60.0
# scene_nums = 1
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250507_bFB66_pad_tun_v2'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [-500.0]
# max_time_truncation = 140*60.0
# scene_nums = 1
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250512_bFB66_LB_pad'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [-200.0]
# max_time_truncation = 140*60.0
# scene_nums = 1
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'
#
# expt_id = '/250509_bFB66_pad_LB'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [-200.0]
# max_time_truncation = 140*60.0
# scene_nums = 1
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'
#
# expt_id = '/250508_bFB69_pad_LB'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [-200.0]
# max_time_truncation = 140*60.0
# scene_nums = 1
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250402_bFB66_LB'
# tsteps = 361
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['LB Switched']
# t_pert = [60*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 2
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250508_bFB66_pad_LB'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [-200.0]
# max_time_truncation = 140*60.0
# scene_nums = 1
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'




# expt_id = '/250506_bFB66_pad_tun'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [0.0]
# max_time_truncation = 140*60.0
# scene_nums = 1
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250505_bFB66_pad_LB'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Spotted on pad']
# t_pert = [0.0]
# max_time_truncation = 140*60.0
# scene_nums = 1
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'



# expt_id = '/250408_bFB291_IPTG_induction'
# tsteps = 361
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['1mM IPTG added']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250402_bFB66_LB'
# tsteps = 361
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['LB well switch']
# t_pert = [60*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250403_bFB292_IPTG_induction'
# tsteps = 361
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['1mM IPTG added']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 2  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250326_bFB295_IPTG_induction'
# tsteps = 361
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['1mM IPTG added']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 3  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'


# expt_id = '/250325_bFB293_IPTG_induction'
# tsteps = 361
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['1mM IPTG added']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'


# expt_id = '/250324_bFB291_IPTG_induction'
# tsteps = 361
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['1mM IPTG added']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250227_bFB87_Tun_PBS_long_incubation_45min'
# tsteps = 345
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added', 'PBS added']
# t_pert = [10*60.0, 55*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250226_bFB66_Tun_PBS_long_incubation_45min'
# tsteps = 345
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added', 'PBS added']
# t_pert = [10*60.0, 55*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 3  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250225_bFB66_Tun_PBS_long_incubation_30min'
# tsteps = 301
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added', 'PBS added']
# t_pert = [10*60.0, 40*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 2  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250224_bFB66_Tun_BufferA_long_incubation'
# tsteps = 271
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added', 'PBS added']
# t_pert = [10*60.0, 30*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250219_bFB66_Spp1_300ug_LB'
# tsteps = 91
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = [r'300$\mu$g/mL Spp1 added']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'


# expt_id = '/250221_bFB69_Tun_PBS_long_incubation'
# tsteps = 271
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added', 'PBS added']
# t_pert = [10*60.0, 30*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250220_bFB66_Tun_PBS_long_incubation'
# tsteps = 271
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added', 'PBS added']
# t_pert = [10*60.0, 30*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250218_bFB66_PBS_long_incubation'
# tsteps = 361
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS added','LB restored']
# t_pert = [10*60.0, 70*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250213_bFB8_PBS_BufferA_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+BufferA added','PBS+BufferA removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/250213_bFB8_25uMGlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/241202_bFB7_25uMGlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 3  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/241201_bFB93_40uMGlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/241201_bFB93_25uMGlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/241130_bFB93_25uMGlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/241129_bFB87_25uMGlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/241126_bFB69_Tun_gr'
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'


# expt_id = '/241115_bFB87_GlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/241007_bFB69_GlpQ_LB'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['40uM GlpQ added']
# t_pert = [10*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240927_bFB69_Tun_gr'
# tsteps = 166
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [10*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 4
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240926_bFB7_Tun_gr' # Run 3/10
# tsteps = 166
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [10*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 4
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240925_bFB93_40uMGlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240925_bFB93_40uMGlpQ_recovery_v2'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'


# expt_id = '/240925_bFB7_Tun_gr' # Run 3/10
# tsteps = 166
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [10*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240920_bFB93_40uMGlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240920_bFB93_PBS_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Buffer added','PBS+BufferA removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240920_bFB93_GlpQ_Recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240918_bFB87_PBS_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+BufferA added','PBS+BufferA removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240918_bFB87_GlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240901_bFB66_30minPBS_recovery_run2'
# tsteps = 316
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Buffer added','PBS+Buffer removed']
# t_pert = [10*60.0, 40*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'


# expt_id = '/240901_bFB66_30minPBS_recovery'
# tsteps = 316
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Buffer added','PBS+Buffer removed']
# t_pert = [10*60.0, 40*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240807_bF66_40uMGlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS +40uM new GlpQ added', 'LB added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240725_bFB66_40uM_GlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS +25uM new GlpQ added', 'LB added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240724_bFB69_25uM_GlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS +25uM new GlpQ added', 'LB added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/240724_bFB66_25uM_GlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS +25uM new GlpQ added', 'LB added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'


# expt_id = '/240724_bFB66_29uM_GlpQ_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS +29uM new GlpQ added', 'LB added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False


# expt_id = '/240612_bFB260_degron_tester_500uMIPTG002'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['5uM Rapamycin added']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 2  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/240528_bFB69_BufferA_500mMSorbitol'
# tsteps = 391
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS + BufferA added', 'LB+Sorbitol added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/240528_bFB69_GlpQ_500mMSorbitol'
# tsteps = 391
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS + GlpQ added', 'LB+Sorbitol added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/240527_bFB66_BufferA_tester'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS + BufferA added', 'LB added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/240527_bFB66_GlpQ_tester'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS +40uM new GlpQ added', 'LB added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'

# expt_id = '/240527_bFB66_GlpQ_tester'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS +40uM new GlpQ added', 'LB added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False


# expt_id = '/240523_bFB69_BufferA_tester'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS +40uM new GlpQ added', 'LB added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/240523_bFB69_GlpQ_tester'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS +40uM new GlpQ added', 'LB added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False


# expt_id = '/240503_bFB69_GlpQ_tester'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS +20uM new GlpQ added', 'LB added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/240311_bFB69_PBS_GlpQ_conc_recovery'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS +30uM new GlpQ added', 'LB added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 2  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/231129_bFB69_PBS_BufferA_500mMSorbitol_15min_recovery'
# tsteps = 391
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS added', 'LB + 500mM Sorbitol added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/240111_bFB66_Tun_500mMSorbitol_test'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added', '500mM Sorbitol added']
# t_pert = [5*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/231119_bFB69_PBS_BufferA_500mMSorbitol_recovery_15min_ZPBS'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS added', 'PBS removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/231117_bFB69_PBS_GlpQ_500mMSorbitol_recovery_15min_ZPBS'
# tsteps = 391
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS added', 'PBS removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'


# expt_id = '/231115_bFB69_PBS_BufferA_recovery_15min_ZPBS'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS added', 'PBS removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'


# expt_id = '/231110_bFB6_Xylose_depletion'
# tsteps = 361
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Xylose removed']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/231110_bFB69_PBS_GlpQ_500mMSorbitol_recovery_15min_ZPBS'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','LB+500mM Sorbitol added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'


# expt_id = '/231108_bFB69_PBS_GlpQ_recovery_15min_ZPBS'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'


# expt_id = '/231105_bFB69_PBS_BufferA_500mMSorbitol_recovery_15min'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Buffer added','Sorbitol added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/231103_bFB66_PBS_denatGlpQ_recovery_15min'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Buffer added','Sorbitol added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/231103_bFB69_PBS_GlpQ_500mMSorbitol_recovery_15min'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added','Sorbitol added']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'



# expt_id = '/231030_bFB66_PBS_BufferA_recovery_30min'
# tsteps = 316
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Buffer added','PBS+Buffer removed']
# t_pert = [10*60.0, 40*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'

# expt_id = '/231030_bFB69_PBS_BufferA_recovery_30min'
# tsteps = 361
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Buffer added','PBS+Buffer removed']
# t_pert = [10*60.0, 40*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/231027_bFB69_PBS_BufferA_recovery_15min'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Buffer added','PBS+Buffer removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'


# expt_id = '/210929_bFB2_teichoicase_recovery'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Teichoicase added','PBS+Teichoicase removed']
# t_pert = [10*60.0, 30*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 6  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False


# expt_id = '/211006_bFB1_teichoicase_recovery'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Teichoicase removed']
# t_pert = [6.5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 6  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/210731_FB2_GlpQ_Response_10uM'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Teichoicase added']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 7  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/210916_bFB1_PBS_teichoicase_recovery' # Run 3/10
# tsteps = 271
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Buffer added', 'PBS+Buffer removed']
# t_pert = [2*60.0, 22*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 6  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/210916_bFB1_PBS_recovery' # Run 3/10
# tsteps = 211
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Buffer added', 'PBS+Buffer removed']
# t_pert = [10*60.0, 30*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 8  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width = 4.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=False

# expt_id = '/231018_bFB69_PBS_BufferA_recovery_15min' # Run 3/10
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Buffer added', 'PBS+Buffer removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/231018_bFB69_PBS_GlpQ_recovery_15min' # Run 3/10
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added', 'PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'


# expt_id = '/231012_bFB69_PBS_GlpQ_recovery_15min' # Run 3/10
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added', 'PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4  # Note that this timelapse had some growth in scene 5 but that these cells were very far away from the
# # inlet and likely received a lower dose of GlpQ based on CY5 channel
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'


# expt_id = '/231011_bFB66_PBS_GlpQ_recovery_15min' # Run 3/10
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added', 'PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False



# expt_id = '/231005_bFB66_PBS_GlpQconst_recovery' # Run 3/10
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added', 'PBS removed, GlpQ retained']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
#

# expt_id = '/231004_bFB69_PBS_BufferA_recovery_15min' # Run 3/10
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+BufferA added', 'PBS+BufferA removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'

#
#
# expt_id = '/231004_bFB66_PBS_GlpQ_recovery_15min' # Run 3/10
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added', 'PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
#
# expt_id = '/230926_bFB66_PBS_GlpQdenat_recovery_15min' # Run 3/10
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+denatured GlpQ added', 'PBS+denatured GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
#
# expt_id = '/230926_bFB66_PBS_GlpQ_recovery_15min' # Run 3/10
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added', 'PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
#
# expt_id = '/230921_bFB66_PBS_BufferA_recovery_15min' # Run 3/10
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+Buffer A added', 'PBS+Buffer A removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/230921_bFB66_PBS_GlpQ_recovery_15min' # Run 3/10
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS+GlpQ added', 'PBS+GlpQ removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5  # Note we actually have 6 scenes here but scene 6 has a very low initial growth rate so we'll cut it.
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/230825_bFB66_PBS_recovery_15min' # Run 3/10
# tsteps = 256
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS added', 'PBS removed']
# t_pert = [10*60.0, 25*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 6
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False


# expt_id = '/230825_bFB66_PBS_recovery' # Run 3/10
# tsteps = 270
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS added', 'Buffer added', 'Buffer removed']
# t_pert = [10*60.0, 25*60.0, 40*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 6
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/230404_bER47_Tun' # Run 3/10
# tsteps = 271
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/230331_bER47_Mecillinam_Tun_LB' # Run 3/10
# tsteps = 271
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added', 'Mecillinam added']
# t_pert = [10*60.0, 30*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/230331_bER47_Mecillinam_LB' # Run 3/10
# tsteps = 211
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Mecillinam added']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False


# expt_id = '/200928_BS_tun_test'
# tsteps = 271
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [20*60.0]
# scene_nums = 5
# max_width=1.5
# min_width=0.5
# min_length=2.0
# perform_ttest=True
# max_time_truncation = tsteps*dt[0]

# expt_id = '/210108_BS_tun'
# tsteps = 533
# labels = ['Tunicamycin added', 'Tunicamycin removed']
# dt = np.concatenate([20.0*np.ones(10*60/20),10.0*np.ones(30*60/10),30.0*np.ones(160*60/30)])
# # time interval between each successive timepoint in seconds
# print(dt.shape)
# t_pert = [20*60.0, 100*60.0]
# # max_time_truncation = 90*60.0
# scene_nums = 3
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=True

# expt_id = '/210128_FB2_Tun_response'
# tsteps = 271
# labels = ['Tunicamycin added']
# dt = 20.0*np.ones(tsteps-1)
# # time interval between each successive timepoint in seconds
# print(dt.shape)
# t_pert = [20*60.0]
# # max_time_truncation = 90*60.0
# scene_nums = 5
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=True
#
# expt_id = '/210212_FB1_LB_Tun_response'
# tsteps = 199
# labels = ['0.5 ug/mL Tunicamycin added']
# dt = 20.0*np.ones(tsteps-1)
# # time interval between each successive timepoint in seconds
# print(dt.shape)
# t_pert = [10*60.0]
# max_time_truncation = 90*60.0
# scene_nums = 5
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=True

# expt_id="/210228_FB1_LB_Tun_response_HADA_0_25_ug"
# tsteps = 124
# labels = ['0.5 ug/mL Tunicamycin added']
# dt = 20.0*np.ones(tsteps-1)
# # time interval between each successive timepoint in seconds
# t_pert = [10*60.0]
# # max_time_truncation = 90*60.0
# scene_nums = 4
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=True

# expt_id="/210228_FB1_LB_Tun_response_HADA_0_5_ug"
# tsteps = 124
# labels = ['0.5 ug/mL Tunicamycin added']
# dt = 20.0*np.ones(tsteps-1)
# # time interval between each successive timepoint in seconds
# t_pert = [10*60.0]
# # max_time_truncation = 90*60.0
# scene_nums = 4
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=True

# expt_id="/210228_FB1_LB_Tun_response_HADA_1_ug"
# tsteps = 124
# labels = ['0.5 ug/mL Tunicamycin added']
# dt = 20.0*np.ones(tsteps-1)
# # time interval between each successive timepoint in seconds
# t_pert = [10*60.0]
# # max_time_truncation = 90*60.0
# scene_nums = 4
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=True

# expt_id="/191216_Paola_CRISPRi_TagO"
# tsteps = 120
# labels = ['CRISPRi TagO inhibition']
# dt = 60.0*np.ones(tsteps-1)
# # time interval between each successive timepoint in seconds
# t_pert = [10*60.0]
# max_time_truncation = 90*60.0
# scene_nums = 4
# max_width = 2.0
# min_width = 0.5
# min_length = 2.0
# perform_ttest=True

# expt_id = '/201112_BS_tun_fos_simult'
# tsteps = 271
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin + Fosfomycin']
# t_pert = [20*60.0]
# max_time_truncation = 75*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True

# expt_id = '/210304_FB1_LB_Tun_response_HADA'
# tsteps = 199
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin']
# t_pert = [10*60.0]
# max_time_truncation = 75*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True

# expt_id = '/210429_FB6_inducer_loss'
# tsteps = 277
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Xylose depleted']
# t_pert = [5*60.0]
# max_time_truncation = 80*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True

# expt_id = '/210416_FB2_Tun_response'
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin']
# t_pert = [10*60.0]
# max_time_truncation = 50*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True

# expt_id = '/210506_FB6_inducer_loss_timelapse'
# tsteps = 295
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Xylose depleted']
# t_pert = [2*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True

# expt_id = '/210507_FB1_Tun_Mg'
# tsteps = 196
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin and MgCl2 added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 7
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True

# expt_id = '/210718_FB1_Tun_Response'
# tsteps = 136
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 2
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True


# expt_id = '/210718_FB7_Tun_Response'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True

# expt_id = '/210718_FB8_Tun_Response'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'

# expt_id = '/210723_FB8_Tun_Response' # Note - This experiment had an air bubble so the data is not very good.
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [10*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 8
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'

# expt_id = '/210723_FB7_Tun_Response'# Run 3/10
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [10*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 7
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True

# expt_id = '/210723_FB1_Tun_Response'
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [10*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 7
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True

# expt_id = '/210916_bFB1_PBS_recovery'
# tsteps = 211
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS added', 'PBS removed']
# t_pert = [10*60.0, 30*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 8
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True

# expt_id = '/210916_bFB1_PBS_teichoicase_recovery'
# tsteps = 271
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS + teichoicase added', 'PBS removed']
# t_pert = [2*60.0, 22*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=True

# expt_id = '/210929_bFB2_teichoicase_recovery'
# tsteps = 271
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS + teichoicase added', 'PBS removed']
# t_pert = [10*60.0, 30*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/211006_bFB2_teichoicase_recovery'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS removed']
# t_pert = [11*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/211006_bFB1_teichoicase_recovery'
# tsteps = 181
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS removed']
# t_pert = [6.5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/211014_bFB1_teichoicase_tunicamycin_recovery'
# tsteps = 271
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS, 0.5ug/mL Tun & teichoicases added', 'PBS removed']
# t_pert = [2*60.0, 22*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 7
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/211019_bFB1_PBS_buffer_recov'
# tsteps = 271    
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['PBS & enzyme buffer added', 'PBS removed']
# t_pert = [10*60.0, 30*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 7
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/211020_bFB7_Tun'# Run 3/10
# tsteps = 166
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [10*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'

# expt_id = '/211020_bFB8_Tun'# Run 3/10
# tsteps = 166
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [10*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd2/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd2/Rojas_Lab/data/'


# expt_id = '/211215_bFB66_Tun_gr'# Run 3/10 # Run back to here for different timepoint numbers
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/211215_bFB7_Tun_gr' # Run 3/10
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'

# expt_id = '/211216_bFB8_Tun_gr'# Run 3/10
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'

# expt_id = '/211216_bFB66_Tun_gr'# Run 3/10
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/220105_bFB79_Tun_response'
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 7
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
#
# expt_id = '/220121_bFB66_Tun_gr'# Run 3/10
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 7
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/220202_bFB66_Tun_Mg_gr'
# tsteps = 226
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin and 25mM Mg2+ added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
#
# expt_id = '/220204_bFB69_Tun_gr' # Run 3/10
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False


# expt_id = '/220218_bFB66_Tun_gr_Mg'
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/220223_bFB87_Tun_Mg_gr'
# tsteps = 195
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/220224_bFB69_Tun_Mg_gr'
# tsteps = 195
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/220303_bFB87_Tun_gr' # Run 3/10
# tsteps = 196
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5 # actually 7 but stop at 5 to ensure good growth.
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'

# expt_id = '/220304_bFB93_Tun_gr' # Run 3/10
# tsteps = 196
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5 # stop here to ensure good growth
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'

# expt_id = '/220309_bFB69_Tun_gr' # Run 3/10
# tsteps = 196
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/220310_bFB93_Tun_gr' # Run 3/10
# tsteps = 196
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5 # Actually 8 but stop at 5 to ensure good growth.
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'

# expt_id = '/220311_bFB87_Tun_gr' # Run 3/10 # Needs update scene nums
# tsteps = 196
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['0.5ug/mL Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False
# base_path='/Volumes/data_ssd1/Rojas_Lab/data/'
# data_path='/Volumes/data_ssd1/Rojas_Lab/data/'

# expt_id = '/210429_FB6_inducer_loss' # Run 3/10
# tsteps = 277
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Xylose depleted']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/210506_FB6_inducer_loss_timelapse' # Run 3/10
# tsteps = 277
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Xylose depleted']
# t_pert = [2*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 6
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/220831_bFB145_Tun_gr' # Run 3/10
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 4
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/220902_bFB149_Tun_gr' # Run 3/10
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 4
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/220909_bFB145_Tun_gr' # Run 3/10
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 4
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/220916_bFB145_Tun_gr' # Run 3/10
# tsteps = 196
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 99*60.0
# scene_nums = 5
# max_width=2.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/221004_bFB145_Tun_gr' # Run 3/10
# tsteps = 376
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/221005_bFB149_Tun_gr' # Run 3/10
# tsteps = 376
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/221012_bFB69_Tun_gr' # Run 3/10
# tsteps = 376
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added']
# t_pert = [5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/221014_bFB154_Xyl_depl_gr' # Run 3/10
# tsteps = 376
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Xylose depleted']
# t_pert = [5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/221021_bFB113_Tun_gr' # Run 3/10
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tun added']
# t_pert = [5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/221021_bFB109_Tun_gr' # Run 3/10
# tsteps = 151
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tun added']
# t_pert = [5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 4
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/221025_bFB109_Tun_gr' # Run 3/10
# tsteps = 286
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tun added']
# t_pert = [5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/221025_bFB113_Tun_gr' # Run 3/10
# tsteps = 286
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tun added']
# t_pert = [5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/221025_bFB118_Tun_gr' # Run 3/10
# tsteps = 286
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tun added']
# t_pert = [5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/221110_bFB66_Amp_gr' # Run 3/10
# tsteps = 196
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Amp added']
# t_pert = [5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False


# expt_id = '/221110_bFB66_Tun_Amp_gr' # Run 3/10
# tsteps = 196
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tun and Amp added']
# t_pert = [5*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 5
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False


# expt_id = '/230314_bFB169_Mecillinam' # Run 3/10
# tsteps = 211
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Mecillinam added']
# t_pert = [10*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 6
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False

# expt_id = '/230314_bFB169_Mecillinam_Tun' # Run 3/10
# tsteps = 241
# dt = 20.0*np.ones(tsteps-1) # time interval between timepoints in seconds
# labels = ['Tunicamycin added', 'Mecillinam added']
# t_pert = [10*60.0, 20*60.0]
# max_time_truncation = 140*60.0
# scene_nums = 6
# max_width=4.0
# min_width=0.5
# min_length=2.0
# perform_ttest=False



# Generic code to be run.
initial_time_plotting = 8  # number of minutes for which to plot the growth rate values of each scene
thresh = 0.00001  # threshold for the average growth rate below which we preclude cells from analysis. This is set very
# low to make sure that cells are actually not growing at all.
window = 2 # number of time points on either side with which to calculate the local slope
flier_thresh = 2.0 # threshold for number of iqrs away from median growth rate beyond which we preclude cells from analysis.
tvec=np.cumsum(dt)
tvec=np.insert(tvec,0,0.0)
max_tstep_truncation = len(tvec) # this is the point at which the analysis truncates if you want it to be before the
# end of the dataset

# making file structures
if not os.path.exists('./outputs'+expt_id):
    os.mkdir('./outputs'+expt_id)
linestyles = ['-','-.','--']
sys.stdout = open('./outputs'+expt_id+expt_id+'_outputs.txt', "w")
# Loading the data (same as antibiotic_growth_inhibition_tester_combined_shock_v2.py)
temp = []
temp1 = []
temp2 = []
temp3 = []
for i0 in range(1, scene_nums+1):
    temp_name = expt_id+'_s{:03d}'.format(i0)
    temp_path = data_path+expt_id+temp_name+'_1_a'+temp_name+'_BT_felix.mat'
    data=scipy.io.loadmat(temp_path)
    temp.append(np.asarray(data['lcell']))
    temp1.append(np.asarray(data['wcell']))
    temp2.append(np.asarray(data['sacell']))
    temp3.append(i0*np.ones(data['lcell'].shape[0]))
lcell = np.concatenate(temp,axis=0)
wcell = np.concatenate(temp1,axis=0)
sacell = np.concatenate(temp2,axis=0)
scene_num_tracker = np.concatenate(temp3,axis=0)
# filtering the data based on dimensions
sacell=sacell[:, :max_tstep_truncation]
lcell=lcell[:, :max_tstep_truncation]
wcell=wcell[:, :max_tstep_truncation]
sacell[np.isnan(lcell)]=np.nan # making sure that the surface area doesn't include fixed objects that have been
# filtered successfully within lcell and wcell.
print(lcell.shape,wcell.shape,sacell.shape, max_tstep_truncation)
time=tvec[:max_tstep_truncation]


###################################################################
# Updated 7/5/23
# We now use a cutoff time that is based on when cells start to fatten, since our tracking becomes very bad after this
# point.
wmed = np.nanmedian(wcell,axis=0)
wmed_gr = []
w_window = 20
for i0 in range(len(wmed)):
    ind1, ind2 = np.amax([i0-w_window, 0]), np.amin([i0+w_window, len(time)])
    wmed_gr.append(scipy.stats.linregress(20.0*np.arange(ind1, ind2), wmed[ind1:ind2])[0])
wmed_gr = np.asarray(wmed_gr)
thresh_w_gr = 0.00008
if np.sum(wmed_gr>thresh_w_gr)>0:
    cutoff_time = np.nonzero(wmed_gr > thresh_w_gr)[0][0]
else:
    cutoff_time = len(time)-1
time_truncated = time[:cutoff_time]
print("cutoff time = ", cutoff_time)
# exit()
# filtering to only include contigs of 5 timepoints or more.

cutoff=5
for i0 in range(lcell.shape[0]): # for each cell trace
    temp=(~np.isnan(lcell[i0,:])).astype(int) # 1 for cell, 0 for nan
    inds1=np.nonzero(np.diff(np.concatenate([[0],temp, [0]]))==1) # beginning of each trace
    inds2=np.nonzero(np.diff(np.concatenate([[0],temp, [0]]))==-1) # end point of each trace
    lens=(inds2[0]-inds1[0]).tolist() # gives the length of each contig
    for i1 in range(len(lens)):
        if lens[i1]<cutoff:
            lcell[i0,inds1[0][i1]:inds1[0][i1]+lens[i1]]=np.nan
            wcell[i0,inds1[0][i1]:inds1[0][i1]+lens[i1]]=np.nan
            sacell[i0,inds1[0][i1]:inds1[0][i1]+lens[i1]]=np.nan

# fitting to find the surface area growth rate at each point.

sgr_sa = np.zeros(sacell.shape)
sgr_sa[:, :] = np.nan
sgr_l = np.zeros(lcell.shape)
sgr_l[:, :] = np.nan
window = 5
window_sa = 15 # note that the larger window here all but ensures that the measured SA growth rate will be less
# time-sensitive to changes in growth rate.
for i0 in range(sacell.shape[0]):  # number of cells
    for i1 in range(sacell.shape[1]):  # timepoints
        if ~np.isnan(lcell[i0, i1]):  # if this timepoint is not a nan value
            # for specific length growth rate
            temp_x = time[max([i1 - window, 0]):min([i1 + window, len(time)])] # window of length 5 for all regions poss
            temp_y = lcell[i0, max([i1 - window, 0]):min([i1 + window, len(time)])]
            temp_x = temp_x[~np.isnan(temp_y)] # select only points that have actual data
            temp_y = temp_y[~np.isnan(temp_y)]
            temp_vals = scipy.stats.linregress(temp_x, temp_y)
            sgr_l[i0, i1] = temp_vals[0] / np.nanmean(temp_y)

            # for specific SA growth rate
            temp_x = time[max([i1 - window_sa, 0]):min([i1 + window_sa, len(time)])]
            temp_y = sacell[i0, max([i1 - window_sa, 0]):min([i1 + window_sa, len(time)])]
            temp_x = temp_x[~np.isnan(temp_y)]
            temp_y = temp_y[~np.isnan(temp_y)]
            temp_vals = scipy.stats.linregress(temp_x, temp_y)
            sgr_sa[i0, i1] = temp_vals[0] / np.nanmean(temp_y)

###################################################################
# plotting the cell length growth rate traces
fig=plt.figure(figsize=[8, 5])
xv=time
for i0 in range(lcell.shape[0]):
    yv = lcell[i0, :]
    print(yv)
    plt.plot(xv,yv,alpha=0.4)
ax=plt.gca()
for i0 in range(len(t_pert)):
    plt.vlines(t_pert[i0],ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0])
plt.legend(loc=[1.02,0.2])
plt.ylabel(r'Length ($\mu m$)')
plt.xlabel('Time (s)')
fig.savefig('./outputs'+expt_id+expt_id+'_cell_lengths.png',dpi=150,bbox_inches='tight')
plt.clf()



###################################################################
# Plotting the sgr on a nice time axis
sgr=np.zeros(sgr_l.shape)
sgr[:,:]=sgr_l[:,:]

# Filtering to remove cells that simply don't grow throughout the whole timelapse
if remove_non_growing_cells:
    filt_inds=np.nonzero(np.nanmean(sgr,axis=1)<thresh)
    sgr[filt_inds,:]=np.nan
    wcell[filt_inds,:]=np.nan
    sgr_sa[filt_inds,:]=np.nan

sgrmed = np.nanmedian(sgr,axis=0)
sgrstd = scipy.stats.iqr(sgr,axis=0,nan_policy='omit')
fliers = np.absolute(sgr-np.tile(sgrmed,[sgr.shape[0],1]))/np.tile(sgrstd,[sgr.shape[0],1])>flier_thresh
sgr[np.nonzero(fliers)]=np.nan
sgr*=3600.0
xv=time/60.0
fig=plt.figure(figsize=[8,5])
for i0 in range(sgr.shape[0]):
    temp=(~np.isnan(sgr[i0,:])).astype(int)
    inds1=np.nonzero(np.diff(np.concatenate([[0],temp, [0]]))==1)[0] # beginning of each trace
    inds2=np.nonzero(np.diff(np.concatenate([[0],temp, [0]]))==-1)[0] # end point of each trace
    for ind in range(len(inds1)):
        yv=sgr[i0,inds1[ind]:inds2[ind]]
        xv1 = xv[inds1[ind]:inds2[ind]]
        plt.xlim(left=0.0,right=np.amax(xv))
        plt.plot(xv1,yv,alpha=0.2,color='b')
yv=np.nanmedian(sgr,axis=0)
err=np.nanstd(sgr,axis=0)/np.sqrt(np.sum(~np.isnan(sgr),axis=0))
plt.fill_between(xv,yv-err,yv+err,alpha=0.5,color='r')
plt.plot(xv,yv,label= 'Smoothed median',color='k',lw=3.0)
# plt.ylim(ymin=0)
ax=plt.gca()
for i0 in range(len(t_pert)):
    plt.vlines(t_pert[i0]/60.0,ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0])
plt.legend()
plt.xlabel('Time (min)')
plt.ylabel(r'$\frac{1}{l}\frac{dl}{dt}$ ($h^{-1}$)')
fig.savefig('./outputs/'+expt_id+expt_id+'_sgr_not_truncated.png',bbox_inches='tight',dpi=150)
plt.xlim(xmax=xv[cutoff_time])
fig.savefig('./outputs/'+expt_id+expt_id+'_sgr_truncated.png',bbox_inches='tight',dpi=150)
plt.clf()



# Plotting the sgr on its original axis
sgr=np.zeros(sgr_l.shape)
sgr[:,:]=sgr_l[:,:]

# Filtering to remove cells that simply don't grow throughout the whole timelapse
if remove_non_growing_cells:
    filt_inds=np.nonzero(np.nanmean(sgr,axis=1)<thresh)
    sgr[filt_inds, :] = np.nan

sgrmed = np.nanmedian(sgr,axis=0)
sgrstd = scipy.stats.iqr(sgr,axis=0,nan_policy='omit')
fliers = np.absolute(sgr-np.tile(sgrmed,[sgr.shape[0],1]))/np.tile(sgrstd,[sgr.shape[0],1])>flier_thresh
if remove_fliers:
    sgr[np.nonzero(fliers)]=np.nan
xv=time
fig=plt.figure(figsize=[8,5])
for i0 in range(sgr.shape[0]):
    temp=(~np.isnan(sgr[i0,:])).astype(int)
    inds1=np.nonzero(np.diff(np.concatenate([[0],temp, [0]]))==1)[0] # beginning of each trace
    inds2=np.nonzero(np.diff(np.concatenate([[0],temp, [0]]))==-1)[0] # end point of each trace
    for ind in range(len(inds1)):
        yv=sgr[i0,inds1[ind]:inds2[ind]]
        xv1 = xv[inds1[ind]:inds2[ind]]
        plt.xlim(left=0.0,right=np.amax(xv))
        plt.plot(xv1,yv,alpha=0.2,color='b')
yv=np.nanmedian(sgr,axis=0)
err=np.nanstd(sgr,axis=0)/np.sqrt(np.sum(~np.isnan(sgr),axis=0))
plt.fill_between(xv,yv-err,yv+err,alpha=0.5,color='r')
plt.plot(xv,yv,label= 'Smoothed median',color='k',lw=3.0)
plt.ylim(ymin=0)
ax=plt.gca()
for i0 in range(len(t_pert)):
    plt.vlines(t_pert[i0],ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0])
plt.legend(loc=[1.02,0.2])
plt.xlabel('Time (s)')
plt.ylabel(r'$\frac{1}{l}\frac{dl}{dt}$ ($s^{-1}$)')
# plt.title('Growth rate response to antibiotic perturbation')
fig.savefig('./outputs/'+expt_id+expt_id+'_sgr.png',bbox_inches='tight',dpi=150)
plt.xlim(xmax=xv[cutoff_time])
fig.savefig('./outputs/'+expt_id+expt_id+'_sgr_original_truncated.png',bbox_inches='tight',dpi=150)
plt.show()
plt.clf()

np.save('./outputs/'+expt_id+expt_id+'_sgr_l.npy',sgr)
print("DIMENSIONS", sgr.shape, scene_num_tracker.shape)
np.save('./outputs/'+expt_id+expt_id+'_scene_nums.npy',scene_num_tracker)
np.save('./outputs/'+expt_id+expt_id+'_time.npy',time)
np.save('./outputs/'+expt_id+expt_id+'_width.npy',wcell)

# Now we just briefly plot the initial growth rate by chamber number for the first 10 mins
temp_cols=["Scene","Initial Growth Rate"]
temp_df=pd.DataFrame(columns=temp_cols)
temp_cutoff = np.nonzero(time > initial_time_plotting * 60)[0][0]
temp_lcutoff=np.nonzero(time>2*60)[0][0]
print(temp_cutoff)
for cell in range(sgr.shape[0]):
    temp_gr=np.nanmean(sgr[cell,temp_lcutoff:temp_cutoff])
    temp_df1=pd.DataFrame(columns=temp_cols, data=[[str(int(scene_num_tracker[cell])),temp_gr]])
    temp_df=pd.concat([temp_df,temp_df1])
print(temp_df.Scene.unique())
fig=plt.figure(figsize=[8,5])
temp_df=temp_df[[~np.isnan(obj) for obj in temp_df["Initial Growth Rate"]]]
sns.boxplot(data=temp_df,x="Scene",y="Initial Growth Rate")
fig.savefig('./outputs/'+expt_id+expt_id+'sgr_initial_by_scene.png',bbox_inches='tight',dpi=150)
plt.clf()


# Plotting a hexbin version of specific cell growth rates

xv=time
fig=plt.figure(figsize=[8,5])
yv_out = np.array([])
for i0 in range(sgr.shape[0]):
    yv=sgr[i0,:]
    xv1 = xv[:]
    if i0 ==0:
        yv_out=yv
        xv_out=xv1
    else:
        yv_out=np.concatenate([yv,yv_out])
        xv_out = np.concatenate([xv1, xv_out])
plt.xlim(left=0.0,right=np.amax(xv_out))
plt.hexbin(xv_out,yv_out,cmap ='plasma')
yv=scipy.ndimage.gaussian_filter(np.nanmedian(sgr,axis=0),sigma=1)
plt.plot(xv,yv,label= 'Smoothed median',color='g',lw=3.0)
# plt.ylim(ymin=np.nanmedian(sgrmed)-4*np.nanmedian(sgrstd),ymax=np.nanmedian(sgrmed)+6*np.nanmedian(sgrstd))
ax=plt.gca()
for i0 in range(len(t_pert)):
    plt.vlines(t_pert[i0],ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0],color='y')
plt.legend(loc=[0.5,0.6])
plt.xlabel('Time (s)')
plt.ylabel(r'$\frac{1}{l}\frac{dl}{dt}$ ($s^{-1}$)')
fig.savefig('./outputs/'+expt_id+expt_id+'_sgr_hexbin.png',bbox_inches='tight',dpi=150)
plt.clf()

###################################################################
# plotting the traces of cell widths

fig=plt.figure(figsize=[8,5])
xv=time
for i0 in range(lcell.shape[0]):
    yv=wcell[i0,:]
    plt.plot(xv,yv,alpha=0.4)
ax=plt.gca()
for i0 in range(len(t_pert)):
    plt.vlines(t_pert[i0],ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0])
plt.legend(loc=[1.02,0.2])
plt.ylabel(r'Width ($\mu m$)')
plt.xlabel('Time (s)')
fig.savefig('./outputs'+expt_id+expt_id+'_cell_widths.png',dpi=150,bbox_inches='tight')
plt.clf()

# plotting the heatmap of cell widths

wmed = np.nanmedian(wcell,axis=0)
wstd = np.nanstd(wcell,axis=0)

xv=time[:]
fig=plt.figure(figsize=[8,5])
for i0 in range(sgr.shape[0]):
    yv=wcell[i0,:]
    # print np.isnan(yv)
    xv1 = xv[~np.isnan(yv)]
    yv=yv[~np.isnan(yv)]
    plt.xlim(left=0.0,right=np.amax(xv))
    plt.plot(xv1,yv,'.',alpha=0.2,color='b')
plt.plot(xv,wmed,label= 'Median',color='k',lw=3.0)
# plt.ylim(ymin=np.nanmedian(sgrmed)-0.5*np.nanmedian(sgrstd),ymax=np.nanmedian(sgrmed)+1.0*np.nanmedian(sgrstd))
ax=plt.gca()
for i0 in range(len(t_pert)):
    plt.vlines(t_pert[i0],ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0])
plt.legend(loc=[1.02,0.2])
plt.xlabel('Time (s)')
plt.ylabel(r'Cell width ($\mu m$)')
# plt.title('Cell width in response to antibiotic perturbation')
fig.savefig('./outputs/'+expt_id+expt_id+'_widths_dist.png',bbox_inches='tight',dpi=150)
plt.clf()

# plotting a nicer set of traces of cell widths

wmed = np.nanmedian(wcell,axis=0)
wstd = np.nanstd(wcell,axis=0)

xv=time[:]
fig=plt.figure(figsize=[8,5])
for i0 in range(wcell.shape[0]):
    temp=(~np.isnan(wcell[i0,:])).astype(int)
    inds1=np.nonzero(np.diff(np.concatenate([[0],temp, [0]]))==1)[0] # beginning of each trace
    inds2=np.nonzero(np.diff(np.concatenate([[0],temp, [0]]))==-1)[0] # end point of each trace
    for ind in range(len(inds1)):
        yv=wcell[i0,inds1[ind]:inds2[ind]]
        xv1 = xv[inds1[ind]:inds2[ind]]
        plt.xlim(left=0.0,right=np.amax(xv))
        plt.plot((xv1-t_pert[0])/60.0,yv,alpha=0.1,color='b')
plt.xlim(left=-t_pert[0]/60.0,right=np.amax(xv)/60.0)
plt.plot((xv-t_pert[0])/60.0,wmed,label= 'median',color='r',lw=3.0)
plt.fill_between((xv-t_pert[0])/60.0,wmed-wstd,wmed+wstd,alpha=0.2,color='r',lw=3.0)
# plt.ylim(ymin=np.nanmedian(sgrmed)-0.5*np.nanmedian(sgrstd),ymax=np.nanmedian(sgrmed)+1.0*np.nanmedian(sgrstd))
ax=plt.gca()
for i0 in range(len(t_pert)):
    plt.vlines((t_pert[i0]-t_pert[0])/60.0,ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0])
plt.legend(loc=[1.02,0.2])
plt.xlabel('Time (min)')
plt.ylabel(r'Cell width ($\mu m$)')
# plt.title('Cell width in response to antibiotic perturbation')
fig.savefig('./outputs/'+expt_id+expt_id+'_widths_dist_v2.png',bbox_inches='tight',dpi=150)
plt.clf()


###################################################################
# plotting the traces of cell SA

fig=plt.figure(figsize=[8,5])
xv=time
for i0 in range(lcell.shape[0]):
    yv=sacell[i0,:]
    plt.plot(xv,yv,alpha=0.4)
ax=plt.gca()
for i0 in range(len(t_pert)):
    plt.vlines(t_pert[i0],ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0])
plt.legend(loc=[1.02,0.2])
# plt.ylim(ymin=0.0,ymax=np.nanmedian(sacell.flatten())+4*np.nanmedian(sacell.flatten()))
plt.ylabel(r'Surface Area ($\mu m^2$)')
plt.xlabel('Time (s)')
fig.savefig('./outputs'+expt_id+expt_id+'_cell_sa.png',dpi=150,bbox_inches='tight')
plt.clf()

###################################################################
sgrmed = np.nanmedian(sgr,axis=0)
sgrstd = np.nanstd(sgr,axis=0)
nfliers = np.absolute(sgr-np.tile(sgrmed,[sgr.shape[0],1]))/np.tile(sgrstd,[sgr.shape[0],1])<4.0
print('Perturbation index', int(t_pert[0]/dt[0]))
print('Cell length growth rate values')
temp=np.nanmean(sgr[:,:int(t_pert[0]/dt[0])],axis=1)*60**2
max_trunc=int(t_pert[0]/dt[0])+int(30*60.0/dt[0]) # gives the required time delay before calculating the final growth rate
print('Pre shock growth rate median cell average', np.around(np.nanmedian(temp),4))
print('Pre shock growth rate SD cell average', np.around(np.nanstd(temp),4))
print('Pre shock growth rate SEM', np.around(np.nanstd(temp)/np.sqrt(np.sum(~np.isnan(temp))),4))
temp=np.nanmean(sgr[:,max_trunc:],axis=1)*60**2
print('Post shock growth rate median cell average', np.around(np.nanmedian(temp),4))
print('Post shock growth rate SD cell average', np.around(np.nanstd(temp),4))
print('Post shock growth rate SEM', np.around(np.nanstd(temp)/np.sqrt(np.sum(~np.isnan(temp))),4))

###################################################################
# Plotting the SA SGR
flier_thresh=2.0
cutoff_thresh=0.0001
sgr=np.zeros(sgr_sa.shape)
sgr[:,:]=sgr_sa[:,:]

# Filtering to remove cells that simply don't grow throughout the whole timelapse
if remove_non_growing_cells:
    filt_inds=np.nonzero(np.nanmean(sgr,axis=1)<thresh)
    sgr[filt_inds,:]=np.nan
sgrmed = np.nanmedian(sgr,axis=0)
sgrstd = scipy.stats.iqr(sgr,axis=0,nan_policy='omit')
fliers = np.absolute(sgr-np.tile(sgrmed,[sgr.shape[0],1]))/np.tile(sgrstd,[sgr.shape[0],1])>flier_thresh # filtering 
if remove_fliers:
    sgr[np.nonzero(fliers)]=np.nan
xv=time
fig=plt.figure(figsize=[8,5])
for i0 in range(sgr.shape[0]):
    temp=(~np.isnan(sgr[i0,:])).astype(int)
    inds1=np.nonzero(np.diff(np.concatenate([[0],temp, [0]]))==1)[0] # beginning of each trace
    inds2=np.nonzero(np.diff(np.concatenate([[0],temp, [0]]))==-1)[0] # end point of each trace
    for ind in range(len(inds1)):
        yv=sgr[i0,inds1[ind]:inds2[ind]]
        xv1 = xv[inds1[ind]:inds2[ind]]
        plt.xlim(left=0.0,right=np.amax(xv))
        plt.plot(xv1,yv,alpha=0.2,color='b')
yv=np.nanmedian(sgr,axis=0)
err=np.nanstd(sgr,axis=0)/np.sqrt(np.sum(~np.isnan(sgr),axis=0))
plt.ylim(ymin=0)
plt.fill_between(xv,yv-err,yv+err,alpha=0.5,color='r')
plt.plot(xv,yv,label= 'Median',color='k',lw=3.0)

# plt.ylim(ymin=np.nanmedian(sgrmed)-4*np.nanmedian(sgrstd),ymax=np.nanmedian(sgrmed)+6*np.nanmedian(sgrstd))
ax=plt.gca()
for i0 in range(len(t_pert)):
    plt.vlines(t_pert[i0],ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0])
plt.legend(loc=[1.02,0.2])
plt.xlabel('Time (s)')
plt.ylabel(r'$\frac{1}{S}\frac{dS}{dt}$ ($s^{-1}$)')
# plt.title('Growth rate response to antibiotic perturbation')
fig.savefig('./outputs/'+expt_id+expt_id+'_sgr_SA.png',bbox_inches='tight',dpi=300)
plt.show()
np.save('./outputs/'+expt_id+expt_id+'_sgr_sa.npy',sgr)
plt.clf()

# Plotting a streamlined version of the data
fig=plt.figure(figsize=[8,5])
sgr_sa_smoothed=np.nanmedian(sgr_sa,axis=0)
sgr_sa_iqr_smoothed=scipy.stats.iqr(sgr_sa,axis=0,nan_policy='omit')
plt.plot(time,sgr_sa_smoothed,label='Smoothed Median',lw=3.0)
plt.fill_between(time,sgr_sa_smoothed-sgr_sa_iqr_smoothed,
                 sgr_sa_smoothed+sgr_sa_iqr_smoothed,alpha=0.2)
plt.ylim(ymin=-0.0005,ymax=0.0015)
ax=plt.gca()
for i0 in range(len(t_pert)):
    plt.vlines(t_pert[i0],ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0])
plt.legend()
plt.xlabel('Time (s)')
plt.ylabel(r'$\frac{1}{S}\frac{dS}{dt}$ ($s^{-1}$)')
# plt.title('Growth rate response to antibiotic perturbation')
fig.savefig('./outputs/'+expt_id+expt_id+'_sgr_SA_iqr.png',bbox_inches='tight',dpi=300)
plt.clf()

# Plotting growth rate on better axis
trunc_time=time[np.nonzero(time<=max_time_truncation)[0]]
trunc_sgr_sa = sgr_sa[:,np.nonzero(time<=max_time_truncation)[0]]*60*60
fig=plt.figure(figsize=[8,5])
sgr_sa_smoothed=np.nanmedian(trunc_sgr_sa,axis=0)
err=np.nanstd(trunc_sgr_sa,axis=0)/np.sqrt(np.sum(~np.isnan(trunc_sgr_sa),axis=0))
plt.plot(trunc_time/60,sgr_sa_smoothed,label='Median',lw=3.0)
plt.fill_between(trunc_time/60,sgr_sa_smoothed-err,
                 sgr_sa_smoothed+err,alpha=0.2)
plt.ylim(ymin=0.0,ymax=3)
ax=plt.gca()
for i0 in range(len(t_pert)):
    plt.vlines(t_pert[i0]/60,ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0])
plt.legend()
plt.xlabel('Time (min)')
plt.ylabel(r'$\frac{1}{S}\frac{dS}{dt}$ ($h^{-1}$)')
# plt.title('Growth rate response to antibiotic perturbation')
fig.savefig('./outputs/'+expt_id+expt_id+'_sgr_SA_sem.png',bbox_inches='tight',dpi=300)
fig.savefig('./outputs/'+expt_id+expt_id+'_sgr_SA_sem.pdf',bbox_inches='tight',dpi=300,format='pdf')
print('SA growth rate')
max_trunc=int(t_pert[0]/dt[0])+int(30*60.0/dt[0]) # gives the required time delay before calculating the final growth rate
temp=np.nanmean(trunc_sgr_sa[:,:int(t_pert[0]/dt[0])],axis=1)
print('Pre shock growth rate median cell average', np.around(np.nanmedian(temp),4))
print('Pre shock growth rate SD cell average', np.around(np.nanstd(temp),4))
print('Pre shock growth rate SEM', np.around(np.nanstd(temp)/np.sqrt(np.sum(~np.isnan(temp))),4))
temp=np.nanmean(trunc_sgr_sa[:,max_trunc:],axis=1)
print('Post shock growth rate median cell average', np.around(np.nanmedian(temp),4))
print('Post shock growth rate SD cell average', np.around(np.nanstd(temp),4))
print('Post shock growth rate SEM', np.around(np.nanstd(temp)/np.sqrt(np.sum(~np.isnan(temp))),4))
sys.stdout.close()
plt.clf()

# if perform_ttest:
#
    # fig=plt.figure(figsize=[8,5])
    # tpert=np.nonzero(time[:-1]>=t_pert[0])[0][0]
    # plt.plot(time[:tpert+1],np.nanmedian(sgr,axis=0)[:tpert+1],label='Unperturbed growth')
    # # One sample T-test to check the delay period for each shock
    # print(sgr.shape)
    # yv=scipy.ndimage.gaussian_filter(np.nanmedian(sgr,axis=0),sigma=2)
    # yvar = np.nanstd(sgr, axis=0)
    # yv1 = np.nanmedian(sgr, axis=0)
    # for i0 in range(len(t_pert)):
        # tpert = np.nonzero(time[:-1] >= t_pert[i0])[0][0]
        # temp1 = np.nanmean(sgr[:,tpert-20:tpert].flatten())
        # same = []
        # pvals=[]
        #
        # for i1 in range(len(yv)-tpert-1):
            # temp2 = sgr[np.nonzero(nfliers[:,tpert+i1])[0], tpert+i1]
            #
        # #     print(temp1.shape)
            # vals=scipy.stats.ttest_1samp(temp2,temp1,nan_policy='omit')
            # same.append(vals[1]<0.01)
            # pvals.append(vals[1])
        # same=np.asarray(same)
        # print(same)
        # print(np.nonzero(~same))
        # temp_val = np.nonzero(~same)[0][-1]
        # plt.plot(time[tpert:tpert + temp_val + 1], yv.flatten()[tpert:tpert + temp_val + 1],
                 # label='Delay period {0}= {1} s'.format(i0+1,np.sum(dt[tpert:tpert+temp_val])))
        # # Note we have the +1 here since temp_val is the last point at which we saw agreement in means. The time until we see a difference
        # # is the relevant value for the delay period
        # if i0<len(t_pert)-1:
            # max_range=tpert + np.nonzero(time[:-1] >= t_pert[i0+1])[0][0]
            # print(max_range)
        # else:
            # max_range=len(time)-2
            #
        # plt.plot(time[tpert+temp_val:max_range],yv.flatten()[tpert+temp_val:max_range],label='Decay period {0}'.format(i0+1))
        # # plt.hlines(temp1,xmin=(tpert[0][0]-20)*dt, xmax=tpert[0][0]*dt,label='Mean val',linestyle=linestyles[i0])
        #
    # plt.ylim(ymin=np.nanmedian(sgrmed)-4*np.nanmedian(sgrstd),ymax=np.nanmedian(sgrmed)+6*np.nanmedian(sgrstd))
    #
    # plt.fill_between(time,yv1.flatten()-yvar.flatten(),yv1.flatten()+yvar.flatten(),alpha=0.3,color='grey')
    # ax=plt.gca()
    # for i0 in range(len(t_pert)):
        # plt.vlines(t_pert[i0],ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0])
    # plt.legend(loc=[1.02,0.2])
    # plt.xlim(left=0,right=time[-2])
    # plt.ylabel(r'$\frac{1}{l}\frac{dl}{dt}$ ($s^{-1}$)')
    # plt.xlabel('Time (s)')
    # print("Delay period = {0} s".format((temp_val+1)*20.0))
    # plt.title('Growth rate response to antibiotic perturbation')
    # fig.savefig('./outputs'+expt_id+expt_id+'_sgr_labeled.png',bbox_inches='tight',dpi=150)
    # plt.clf()


