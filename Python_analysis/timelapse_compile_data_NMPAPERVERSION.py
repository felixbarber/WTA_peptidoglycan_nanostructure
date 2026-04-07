# import scipy
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

# out_path='/Users/felixbarber/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/'
# in_path='/Users/felixbarber/Documents/GitHub/Rojas_lab_drafts/outputs'
out_path='/Users/barber.527/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/'
in_path='/Users/barber.527/Documents/GitHub/Rojas_lab_drafts/outputs'

##################### Experiment specifics
tstep=20.0

# expt_ids = ['/220121_bFB66_Tun_gr', '/211216_bFB66_Tun_gr', '/211215_bFB66_Tun_gr']
# expt_label = 'bFB66_Tun_gr'
# Celltype = 'WT'
# t_pert = [5*60.0,5*60.0,5*60.0]

# expt_ids = ['/220204_bFB69_Tun_gr', '/220309_bFB69_Tun_gr', '/221012_bFB69_Tun_gr', '/240927_bFB69_Tun_gr', '/241126_bFB69_Tun_gr']
# expt_label = 'bFB69_Tun_gr'
# t_pert = [5*60.0,5*60.0, 5*60.0, 10*60.0, 5.0*60.0]
# Celltype = r'$\Delta ponA$'
# t_pert1 = []

# expt_ids = ['/211020_bFB8_Tun', '/211216_bFB8_Tun_gr', '/210723_FB8_Tun_Response'] # Note not to use 7/23 data for this since there was an air bubble
# expt_label = 'bFB8_Tun_gr'
# t_pert = [10*60.0,5*60.0, 10*60.0]
# Celltype = r'$\Delta lytE$'
# t_pert1 = []

# expt_ids = ['/240925_bFB7_Tun_gr','/240926_bFB7_Tun_gr', '/250519_bFB7_tun_gr']
# expt_label = 'bFB7_Tun_gr'
# t_pert = [10*60.0,10*60.0,10*60.0]
# Celltype = r'$\Delta cwlO$'
# t_pert1 = []

# expt_ids = ['/250613_bFB66_s750_tun_gr', '/250612_bFB66_s750_tun_gr']
# expt_label = 'bFB66_s750_tun'
# Celltype = r'WT s750'
# t_pert = [20.0*60.0, 20.0*60.0]
# t_pert1 = []
# tstep=60.0

# expt_ids = ['/210429_FB6_inducer_loss', '/210506_FB6_inducer_loss_timelapse', '/231110_bFB6_Xylose_depletion']
# expt_label = 'bFB6_Xylose_depletion'
# t_pert = [5*60.0, 2*60.0, 10*60.0]
# Celltype = r'$P_{Xylose}-TagO$'
# t_pert1 = []

# expt_ids = ['/250508_bFB69_pad_LB', '/250514_bFB69_LB_pad_rep2', '/250514_bFB69_LB_pad']
# expt_label = 'bFB69_LB_pad'
# Celltype = r'$\Delta ponA$'
# t_pert = [-200.0, -200.0,-200.0]
# t_pert1 = []

# expt_ids = ['/250508_bFB66_pad_LB', '/250509_bFB66_pad_LB', '/250515_bFB66_LB_pad', '/250512_bFB66_LB_pad']
# expt_label = 'bFB66_LB_pad'
# Celltype = 'WT'
# t_pert = [-200.0, -200.0, -200.0,-200.0]
# t_pert1 = []

# expt_ids = ['/250507_bFB66_pad_tun_v2', '/250512_bFB66_tun_pad', '/250515_bFB66_tun_pad']
# expt_label = 'bFB66_tun_pad'
# Celltype = 'WT Tunicamycin'
# t_pert = [-500.0,-300.0, -200.0]
# t_pert1 = []

# expt_ids = ['/220303_bFB87_Tun_gr','/220311_bFB87_Tun_gr']
# expt_label = 'bFB87_Tun_gr'
# t_pert = [5*60.0,5*60.0]
# Celltype = r'$\Delta ponA$, $\Delta cwlO$'
# t_pert1 = []

# expt_ids = ['/220304_bFB93_Tun_gr', '/220310_bFB93_Tun_gr']
# expt_label = 'bFB93_Tun_gr'
# t_pert = [5*60.0, 5*60.0]
# Celltype = r'$\Delta ponA$, $\Delta lytE$'
# t_pert1 = []

# expt_ids = ['/231105_bFB69_PBS_BufferA_500mMSorbitol_recovery_15min',
#             '/231119_bFB69_PBS_BufferA_500mMSorbitol_recovery_15min_ZPBS',
#             '/240528_bFB69_BufferA_500mMSorbitol',
#             '/231129_bFB69_PBS_BufferA_500mMSorbitol_15min_recovery']
# expt_label = 'bFB69_PBS_bufferA_500mMSorb_rec'
# Celltype = 'Buffer, Sorbitol treated'
# t_pert = [10*60.0, 10*60.0, 10*60.0, 10*60.0]
# t_pert1 = [25*60.0, 25*60.0, 25*60.0, 25*60.0]

# expt_ids = ['/230921_bFB66_PBS_BufferA_recovery_15min', '/230926_bFB66_PBS_GlpQdenat_recovery_15min',
#             '/231103_bFB66_PBS_denatGlpQ_recovery_15min']
# expt_label = 'bFB66_PBS_GlpQdenat_rec'
# Celltype = 'Buffer treated'
# t_pert = [10*60.0,10*60.0, 10*60.0]
# t_pert1 = [25*60.0, 25*60.0, 25*60.0]

# expt_ids = ['/231004_bFB69_PBS_BufferA_recovery_15min', '/231027_bFB69_PBS_BufferA_recovery_15min',
#             '/231115_bFB69_PBS_BufferA_recovery_15min_ZPBS']
# expt_label = 'bFB69_PBS_Buffer_rec'
# Celltype = r'$\Delta ponA$ Buffer treated'
# t_pert = [10*60.0, 10*60.0, 10*60.0]
# t_pert1 = [25*60.0, 25*60.0, 25*60.0]

# expt_ids = ['/230921_bFB66_PBS_GlpQ_recovery_15min', '/230926_bFB66_PBS_GlpQ_recovery_15min',
#             '/231004_bFB66_PBS_GlpQ_recovery_15min', '/231011_bFB66_PBS_GlpQ_recovery_15min']
# expt_label = 'bFB66_PBS_GlpQ_rec'
# Celltype = 'GlpQ treated'
# t_pert = [10*60.0, 10*60.0, 10*60.0, 10*60.0]
# t_pert1 = [25*60.0, 25*60.0, 25*60.0, 25*60.0]

# expt_ids = ['/231012_bFB69_PBS_GlpQ_recovery_15min', '/231018_bFB69_PBS_GlpQ_recovery_15min', '/231108_bFB69_PBS_GlpQ_recovery_15min_ZPBS']
# expt_label = 'bFB69_PBS_GlpQ_rec'
# Celltype = 'GlpQ treated'
# t_pert = [10*60.0, 10*60, 10*60.0]
# t_pert1 = [25*60.0, 25*60.0, 25*60.0]

expt_ids = ['/231110_bFB69_PBS_GlpQ_500mMSorbitol_recovery_15min_ZPBS', '/231103_bFB69_PBS_GlpQ_500mMSorbitol_recovery_15min',
            '/231117_bFB69_PBS_GlpQ_500mMSorbitol_recovery_15min_ZPBS']
expt_label = 'bFB69_PBS_GlpQ_500mMSorb_rec'
Celltype = 'GlpQ, Sorbitol treated'
t_pert = [10*60.0, 10*60.0, 10*60.0]
t_pert1 = [25*60.0, 25*60.0, 25*60.0]


var_ls=['sgr_l', 'sgr_sa', 'width']
yscale = [60*60.0, 60*60.0, 1.0]
# saving the experimental parameters
temp = {'expt_label':expt_label, 't_pert':t_pert, 'expt_ids':expt_ids, 'tstep':tstep,'vars':var_ls, 'Celltype':Celltype}
if 't_pert1' in locals():
    temp['t_pert1']=t_pert1
temp_path = out_path+expt_label+'_condition_parameters.pkl'
with open(temp_path, 'wb') as output:  # Overwrites any existing file.
    pickle.dump(temp, output, pickle.HIGHEST_PROTOCOL)

def compile_values_v1(temp_yvs, temp_xvs, show_out=False):
    # This function takes lists of arrays for each experiment and aligns them
    # this gives the maximal range for each data set around the perturbation timepoint.
    # Assumes the same timestep in each case
    temp1=[temp[0] for temp in temp_xvs]
    temp2=[temp[-1] for temp in temp_xvs]
    temp_xv=np.linspace(np.amin(temp1), np.amax(temp2), int((np.amax(temp2)-np.amin(temp1))/tstep+1))
    temp_out=np.empty([np.sum([int(temp.shape[0]) for temp in temp_yvs]), len(temp_xv)])
    temp_out[:]=np.nan
    num_points=0
    for i0 in range(len(temp_yvs)):
        start_ind = np.nonzero(temp_xv==temp_xvs[i0][0])[0][0]
        end_ind = np.nonzero(temp_xv==temp_xvs[i0][-1])[0][0]
        if show_out:
            print(start_ind, end_ind)
            print(temp_out.shape)
            print(temp_yvs[i0].shape)
            print(num_points)
        temp_out[num_points:num_points+temp_yvs[i0].shape[0], start_ind:end_ind+1]=temp_yvs[i0][:,:]
        num_points+=temp_yvs[i0].shape[0]
    return(temp_out, temp_xv)


def compile_values_v2(temp_yvs, temp_xvs, show_out=False):
    # This function takes lists of arrays for each experiment and aligns them conservatively, excluding timepoints with
    # incomplete coverage
    # Assumes the same timestep in each case
    temp1=[temp[0] for temp in temp_xvs]
    temp2=[temp[-1] for temp in temp_xvs]
    temp_xv = np.linspace(np.amax(temp1), np.amin(temp2), int((np.amin(temp2) - np.amax(temp1)) / tstep + 1))
    temp_out=np.empty([np.sum([int(temp.shape[0]) for temp in temp_yvs]), len(temp_xv)])
    temp_out[:]=np.nan
    num_points=0
    for i0 in range(len(temp_yvs)):
        start_ind = np.nonzero(temp_xvs[i0]>=temp_xv[0])[0][0]
        end_ind = np.nonzero(temp_xvs[i0]>=temp_xv[-1])[0][0]
        if show_out:
            print(start_ind, end_ind)
            print(temp_out.shape)
            print(temp_yvs[i0].shape)
            print(num_points)
        temp_out[num_points:num_points+temp_yvs[i0].shape[0], :] = temp_yvs[i0][:, start_ind:end_ind+1]
        num_points += temp_yvs[i0].shape[0]
    return(temp_out, temp_xv)

# Code
for var in var_ls:
    xvs,yvs=[],[]
    for expt_id in expt_ids:
        temp=np.load(in_path+expt_id+expt_id+'_time.npy')
        temp -=t_pert[expt_ids.index(expt_id)]
        xvs.append(temp)
        temp1=np.load(in_path+expt_id+expt_id+'_'+var+'.npy')*yscale[var_ls.index(var)]
        if not(t_pert[expt_ids.index(expt_id)]<0): # if the normalization time is not less than zero
            temp1*=1.0/np.nanmedian(temp1[:,np.nonzero(temp==0)[0][0]]) # Normalization step for each timelapse separately
        else:
            temp1 *= 1.0 / np.nanmedian(
                temp1[:, 0])  # Normalization step for each timelapse separately
        yvs.append(temp1)
    yv, xv=compile_values_v1(yvs,xvs)
    np.save(out_path+expt_label+'_'+var+'_normed.npy', yv)
    del(xv, yv, xvs, yvs)

# Repeating the above but without the normalization step
for var in var_ls:
    xvs,yvs=[],[]
    for expt_id in expt_ids:
        temp=np.load(in_path+expt_id+expt_id+'_time.npy')
        temp -=t_pert[expt_ids.index(expt_id)]
        xvs.append(temp)
        temp1=np.load(in_path+expt_id+expt_id+'_'+var+'.npy')*yscale[var_ls.index(var)]
        yvs.append(temp1)
    yv, xv=compile_values_v1(yvs,xvs)
    np.save(out_path+expt_label+'_'+var+'.npy', yv)
np.save(out_path+expt_label+'_time.npy', xv)

# Generating conservative datasets
for var in var_ls:
    xvs,yvs=[],[]
    for expt_id in expt_ids:
        temp=np.load(in_path+expt_id+expt_id+'_time.npy')
        temp -=t_pert[expt_ids.index(expt_id)]
        xvs.append(temp)
        temp1=np.load(in_path+expt_id+expt_id+'_'+var+'.npy')*yscale[var_ls.index(var)]
        if not(t_pert[expt_ids.index(expt_id)] < 0):  # if the normalization time is not less than zero
            temp1 *= 1.0 / np.nanmedian(
                temp1[:, np.nonzero(temp == 0)[0][0]])  # Normalization step for each timelapse separately
        else:
            temp1 *= 1.0 / np.nanmedian(
                temp1[:, 0])  # Normalization step for each timelapse separately
        yvs.append(temp1)
    yv, xv=compile_values_v2(yvs,xvs)
    # Filtering out rows that were only tracked in the timepoints we have now removed.
    # temp_yv=np.sum(np.isnan(yv),axis=1)
    # yv1=yv[np.nonzero(temp_yv!=yv.shape[1])[0],:]
    # # print(yv1)
    # print(yv[np.nonzero(temp_yv==yv.shape[1])[0],:])
    # print(yv.shape, yv1.shape, xv.shape)
    np.save(out_path+expt_label+'_'+var+'_normed_conservative.npy', yv)

for var in var_ls:
    xvs,yvs=[],[]
    for expt_id in expt_ids:
        temp=np.load(in_path+expt_id+expt_id+'_time.npy')
        temp -=t_pert[expt_ids.index(expt_id)]
        xvs.append(temp)
        temp1=np.load(in_path+expt_id+expt_id+'_'+var+'.npy')*yscale[var_ls.index(var)]
        yvs.append(temp1)
    yv, xv=compile_values_v2(yvs,xvs)
    # Filtering out rows that were only tracked in the timepoints we have now removed.
    # temp_yv=np.sum(np.isnan(yv),axis=1)
    # yv1=yv[np.nonzero(temp_yv!=yv.shape[1])[0],:]
    # print(yv1)
    # print(yv[np.nonzero(temp_yv==yv.shape[1])[0],:])
    # print(yv.shape, yv1.shape, xv.shape)
    np.save(out_path+expt_label+'_'+var+'_conservative.npy', yv)
np.save(out_path+expt_label+'_time_conservative.npy', xv)