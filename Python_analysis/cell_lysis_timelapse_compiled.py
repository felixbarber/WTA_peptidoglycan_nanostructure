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
import csv
# import h5py
sns.set(font_scale=1.5)
sns.set_style("white")


expts = [["/230323_bFB66_Tun_lysis", "/250626_bFB66_tun_lysis"],["/230317_bFB69_Tun_Lysis", "/230322_bFB69_Tun_lysis", "/240729_bFB69_Tun_lysis"]]
scene_nums = [[6,3],[3, 6, 3]]
len_times = [[26,26],[19, 26, 26]]
tperts = [[5.0],[5.0]]
starting_points = [[np.array([11, 11, 9, 11, 12, 11]), np.array([6,10,6])],[np.array([2,6,1]), np.array([6,3,2,1,1,1]), np.array([1,1,1])]]
strain_id = ['WT', r'$\Delta ponA$']
tstep = 5.0
out_name='ponA_lim'
pos=[0.1,0.6]

path = '/Volumes/data_ssd1/Rojas_Lab/data'
out_path = '/Users/barber.527/Documents/GitHub/Rojas_lab_drafts/outputs'

total_cells = []
lysed_cells = []
# Importing the data.

for ind in range(len(expts)):
    expt_ids=expts[ind]
    total_cells.append(np.nan * np.ones([np.sum(scene_nums[ind]), np.amax(len_times[ind])]))
    lysed_cells.append(np.nan * np.ones([np.sum(scene_nums[ind]), np.amax(len_times[ind])]))
    scene_tracker=0
    for expt_num in range(len(expt_ids)):
        for scene in range(scene_nums[ind][expt_num]):
            for timepoint in range(starting_points[ind][expt_num][scene],
                                   len_times[ind][expt_num] + 1):  # Note that in the filenames, time counts from 1, not zero
                #         print(timepoint)
                # Finding out the number of cells in each scene
                with open(path + expt_ids[expt_num] + '/annotated_images/s{0}'.format(
                        str(scene + 1).zfill(3)) + expt_ids[expt_num] + '_s{0}_t{1}_all_cells.csv'.format(str(scene + 1).zfill(3),
                                                                                               str(timepoint).zfill(
                                                                                                       4))) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        #                 temp_out.append(row) # Data should be saved in UTF-8 format
                        line_count += 1
                    total_cells[ind][scene_tracker+scene, timepoint - 1] = line_count - 1
                # number of lysed cells
                with open(path + expt_ids[expt_num] + '/annotated_images/s{0}'.format(
                        str(scene + 1).zfill(3)) + expt_ids[expt_num]+ '_s{0}_t{1}_lysed_cells.csv'.format(str(scene + 1).zfill(3),
                                                                                                 str(timepoint).zfill(
                                                                                                         4))) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        #                 temp_out.append(row) # Data should be saved in UTF-8 format
                        line_count += 1
                    lysed_cells[ind][scene_tracker+scene, timepoint - 1] = line_count - 1
        scene_tracker+=scene_nums[ind][expt_num]
# Next, we plot the average traces for all experiments.
frac_lysed=[]
for ind in range(len(expts)):
    frac_lysed.append(lysed_cells[ind]*100.0 / total_cells[ind])
    for row in range(lysed_cells[ind].shape[0]):
        frac_lysed[ind][row,:np.nonzero(~np.isnan(frac_lysed[ind][row,:]))[0][0]]=0

# print(frac_lysed)
# exit()

fig = plt.figure(figsize=[8, 6])
for expt_num in range(len(expts)):
    temp_vals = np.nanmean(frac_lysed[expt_num], axis=0)
    temp_std = np.nanstd(frac_lysed[expt_num], axis=0)
    time = np.arange(np.amax(len_times[expt_num])) * tstep - tperts[expt_num]
    plt.fill_between(time,temp_vals-temp_std,temp_vals+temp_std,alpha=0.4)
ax=plt.gca()
ymin,ymax=ax.get_ylim()
plt.vlines(0.0, ymin=0.0, ymax=0.6*ymax, color='k', linestyle='-.', label='Tunicamycin added')
# plt.legend(loc=[1.05, 0.2])
plt.legend(loc=2)
plt.ylabel('Percentage of lysed cells')
plt.xlabel('Time (mins)')
fig.savefig(out_path+'/compiled_data/lysis_plots/'+out_name+'_mean.png', dpi=300, bbox_inches='tight')
plt.clf()

# Next, we plot the average traces for all experiments.
fig = plt.figure(figsize=[8, 6])
for expt_num in range(len(expts)):
    temp_vals = np.nanmean(frac_lysed[expt_num], axis=0)
    temp_std = np.nanstd(frac_lysed[expt_num], axis=0)
    time = np.arange(np.amax(len_times[expt_num])) * tstep - tperts[expt_num]
    plt.fill_between(time,temp_vals-temp_std,temp_vals+temp_std,alpha=0.4)
    plt.plot(time, temp_vals, label=strain_id[expt_num]+ ", mean")
ax=plt.gca()
ymin,ymax=ax.get_ylim()
plt.vlines(0.0, ymin=0.0, ymax=0.6*ymax, color='k', linestyle='-.', label='Tunicamycin added')
plt.legend(loc=2)
plt.ylabel('Percentage of lysed cells')
plt.xlabel('Time (mins)')
fig.savefig(out_path+'/compiled_data/lysis_plots/'+out_name+'_mean.png', dpi=300, bbox_inches='tight')
plt.clf()

# Next, we plot the average traces for all experiments.
fig = plt.figure(figsize=[8, 6])
for expt_num in range(len(expts)):
    temp_vals = np.nanmedian(frac_lysed[expt_num], axis=0)
    temp_std = scipy.stats.iqr(frac_lysed[expt_num],axis=0)
    time = np.arange(np.amax(len_times[expt_num])) * tstep - tperts[expt_num]
    plt.fill_between(time, temp_vals-temp_std, temp_vals+temp_std, alpha=0.4)
    plt.plot(time, temp_vals, label=strain_id[expt_num] + ", median")
ax = plt.gca()
ymin,ymax = ax.get_ylim()
plt.vlines(0.0, ymin=0.0, ymax=0.6*ymax, color='k', linestyle='-.', label='Tunicamycin added')
plt.legend(loc=2)
plt.ylabel('Percentage of lysed cells')
plt.xlabel('Time (mins)')
fig.savefig(out_path+'/compiled_data/lysis_plots/'+out_name+'_median.png', dpi=300, bbox_inches='tight')
plt.clf()

# Now we generate paper-quality figures

# Next, we plot the average traces for all experiments.
fig = plt.figure(figsize=[2.5, 2])
sns.set(font_scale=1.0)
sns.set_style("ticks")
for expt_num in range(len(expts)):
    temp_vals = np.nanmean(frac_lysed[expt_num], axis=0)
    temp_std = np.nanstd(frac_lysed[expt_num], axis=0)
    time = np.arange(np.amax(len_times[expt_num])) * tstep - tperts[expt_num]
    plt.fill_between(time, temp_vals-temp_std, temp_vals+temp_std, alpha=0.4)
    plt.plot(time, temp_vals, label=strain_id[expt_num])
ax = plt.gca()
plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle='-', colors='k', lw=0.5)
plt.legend(loc=pos)
plt.ylabel('Lysis (%)')
plt.xlabel('Time (min)')
fig.savefig(out_path+'/compiled_data/lysis_plots/'+out_name+'_mean_paper.pdf', bbox_inches='tight')
plt.clf()

fig = plt.figure(figsize=[2.5, 2])
sns.set(font_scale=1.0)
sns.set_style("whitegrid")
for expt_num in range(len(expts)):
    temp_vals = np.nanmedian(frac_lysed[expt_num], axis=0)
    temp_std = np.nanstd(frac_lysed[expt_num], axis=0)
    time = np.arange(np.amax(len_times[expt_num])) * tstep - tperts[expt_num]
    plt.fill_between(time, temp_vals-temp_std, temp_vals+temp_std, alpha=0.4)
    plt.plot(time, temp_vals, label=strain_id[expt_num])
ax = plt.gca()
plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle='-', colors='k', lw=0.5)
plt.legend(loc=2)
plt.ylabel('Lysis (%)')
plt.xlabel('Time (min)')
fig.savefig(out_path+'/compiled_data/lysis_plots/'+out_name+'_med_paper.pdf', bbox_inches='tight')
plt.clf()

fig = plt.figure(figsize=[2.5, 2])
sns.set(font_scale=1.0)
sns.set_style("whitegrid")
for expt_num in range(len(expts)):
    temp_vals = np.nanmedian(frac_lysed[expt_num], axis=0)
    temp_std = np.nanstd(frac_lysed[expt_num], axis=0)/np.sqrt(np.sum(~np.isnan(frac_lysed[expt_num]),axis=0))
    time = np.arange(np.amax(len_times[expt_num])) * tstep - tperts[expt_num]
    plt.fill_between(time, temp_vals-temp_std, temp_vals+temp_std, alpha=0.4)
    plt.plot(time, temp_vals, label=strain_id[expt_num])

# print(frac_lysed)
ax = plt.gca()
plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle='-', colors='k', lw=0.5)
plt.legend(loc=2)
plt.ylabel('Lysis (%)')
plt.xlabel('Time (min)')
fig.savefig(out_path+'/compiled_data/lysis_plots/'+out_name+'_med_paper_SEM.pdf', bbox_inches='tight')
plt.legend(loc=[1.05, 0.0])
fig.savefig(out_path+'/compiled_data/lysis_plots/'+out_name+'_med_paper_SEM_diff_legend.pdf', bbox_inches='tight')
plt.clf()

with open('/Users/barber.527/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/lysis_plots/' + out_name+'.txt', 'w') as f:
    for expt in range(len(expts)):
        print(strain_id[expt], file=f)
        print('Total cells:', np.sum(np.nanmax(total_cells[expt],axis=1)), file=f)  # Python 3.x
