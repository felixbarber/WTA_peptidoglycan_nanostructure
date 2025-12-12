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

expt_ids = ['/241024_bFB66_Tun_WGA_pads', '/241025_bFB66_Tun_WGA_pads','/241112_bFB66_Tun_WGA_pads','/241018_bFB69_WGA_LB_pads', '/241022_bFB69_Tun_WGA_pads_LB', '/241023_bFB69_Tun_WGA_pads']
group_id = 'WGA_bulk_Tun_compiled'
label = 'WGA-AF488'
norm_cond = 'LB'  # Setting this here since this is the standard normalization condition
thresh=100
plotting_conds=['LB', 'Tun']
hue='Condition'
plot_points=False
scene_plotting=11 # number of scenes +1 that we will plot for each replicate, to avoid photobleaching


output_dir = './outputs/compiled_data/staining_plots/'
# path = '/mnt/d/Documents_D/Rojas_lab/data/'
# path = '/Users/felixbarber/Documents/Rojas_Lab/data'
# path = '/Volumes/easystore_hdd/Rojas_Lab/data'
# path = '/Users/felixbarber/Documents/GitHub/Rojas_lab_drafts/outputs'
path = '/Volumes/data_ssd2/Rojas_Lab/data/'

# This assumes that cell_staining_timepoint.py has already been run
# df = pd.DataFrame()
for ind in range(len(expt_ids)):
    temp_df1 = pd.DataFrame()
    expt_id =expt_ids[ind]
    temp_path = path + expt_id + expt_id + '_condition_parameters.pkl'
    with open(temp_path, 'rb') as input:
        expt_vals = pickle.load(input)
    data_dir = "./outputs" + expt_id
    temp_df = pd.read_pickle(data_dir + expt_id)
    temp_df['Celltype'] = expt_vals['Celltype']
    temp_df['expt'] = expt_vals['expt']
    temp_df['Date'] = expt_vals['Date']
    temp_df['Plot'] = [obj in plotting_conds for obj in temp_df.Condition]
    temp_df = temp_df[temp_df.Plot == 1]
    temp_df = temp_df[temp_df['Average outline ' + label] > thresh]  # filtering out debris that isn't fluorescent.
    temp_df['Normalized Average outline ' + label] = temp_df['Average outline ' + label] / \
                                                     temp_df[temp_df.Condition == norm_cond][
                                                         'Average outline ' + label].mean()
    # temp_df['Conditions']=expt_vals['Conditions']
    if ind == 0:
        df = pd.DataFrame(columns=temp_df.columns)
    df = df.append(temp_df)


# Now we plot the results and save the figures
# These are iterable
temp_vars = ['Average outline ' + label, 'Average ' + label, 'Normalized Average outline ' + label]
# temp_vars=['Average outline '+label, 'Average outline '+label, 'Average '+label, 'Normalized Average outline '+label]
temp_out_names = ['av_outline_fl', 'av_area_fl', 'normed_av_outline_fl']
temp_ylabs = ['Fluorescence', 'Area fluorescence', 'Staining (norm)']


# Now we generate paper quality figures

def iter_plotting(df, temp_var, temp_out_name, temp_ylab, temp_iter, temp_xlabel, temp_hue=None, plot_points=True):
    fig = plt.figure(figsize=[2.5, 2])
    temp_df=df[df.Scene<scene_plotting]
    sns.set(font_scale=0.9)
    sns.set_style("whitegrid")
    ax = plt.subplot(1, 1, 1)
    if not temp_hue is None:
        plot = sns.barplot(x=temp_iter, y=temp_var, data=temp_df, estimator=np.mean,capsize=0.4, hue=temp_hue)
    else:
        plot = sns.barplot(x=temp_iter, y=temp_var, data=temp_df, estimator=np.mean, capsize=0.4)
    plot.set(xlabel=temp_xlabel, ylabel=temp_ylab)
    return fig, ax

def iter_plotting_boxplot(df, temp_var, temp_out_name, temp_ylab, temp_iter, temp_xlabel, temp_hue=None, plot_points=True):
    fig = plt.figure(figsize=[2.5, 2])
    temp_df = df[df.Scene < scene_plotting]
    sns.set(font_scale=0.9)
    sns.set_style("whitegrid")
    ax = plt.subplot(1, 1, 1)
    if not temp_hue is None:
        plot = sns.boxplot(x=temp_iter, y=temp_var, data=temp_df, showfliers=False, hue=temp_hue)
        if plot_points:
            temp_ymin,temp_ymax=plt.gca().get_ylim()
            plot = sns.stripplot(x=temp_iter, y=temp_var, jitter=True,dodge=True, data=df, edgecolor='black', linewidth=0.5,
                                 alpha=0.1, hue=temp_hue,label=None)
            ax.set_ylim(bottom=temp_ymin, top=temp_ymax)
    else:
        plot = sns.boxplot(x=temp_iter, y=temp_var, data=temp_df, showfliers=False)

    plot.set(xlabel=temp_xlabel, ylabel=temp_ylab)
    return fig, ax
# # print([temp in plotting_conds for temp in df.Condition])
# print(df.Condition.unique())
# df=df[np.nonzero([temp in plotting_conds for temp in df.Condition])[0]]
print(df.head())
temp_xlabel = ''
temp_iter = 'Celltype'
pval = 0.01
print('I got here')
for i0 in range(len(temp_vars)):
    temp_var, temp_out_name, temp_ylab = temp_vars[i0], temp_out_names[i0], temp_ylabs[i0]
    fig, ax = iter_plotting(df, temp_var, temp_out_name, temp_ylab, temp_iter, temp_xlabel, temp_hue=hue)
    plt.legend(loc=[0.92,0.7])
    fig.savefig(output_dir + group_id + '_' + temp_out_name + '_barplot_compact.eps', dpi=300, bbox_inches='tight')
    fig.savefig(output_dir + group_id + '_' + temp_out_name + '_barplot_compact.png', dpi=300, bbox_inches='tight')
    plt.clf()
    print('Finished plot {0}'.format(i0))
for i0 in range(len(temp_vars)):
    temp_var, temp_out_name, temp_ylab = temp_vars[i0], temp_out_names[i0], temp_ylabs[i0]
    fig, ax = iter_plotting_boxplot(df, temp_var, temp_out_name, temp_ylab, temp_iter, temp_xlabel, temp_hue=hue,plot_points=plot_points)
    plt.legend(loc=[0.75, 0.7])
    fig.savefig(output_dir + group_id + '_' + temp_out_name + '_boxplot_compact.eps', dpi=300, bbox_inches='tight')
    fig.savefig(output_dir + group_id + '_' + temp_out_name + '_boxplot_compact.png', dpi=300, bbox_inches='tight')
    plt.clf()
    print('Finished plot {0}'.format(i0))



with open(output_dir + group_id + '_' + temp_out_name + '.txt', 'w') as f:
    print(df.groupby(['Celltype', 'Condition']).describe(), file=f)
    for celltype in df.Celltype.unique():
        print('For celltype =',celltype, file=f)
        temp_df=df[df.Celltype==celltype]
        temp_df=temp_df[temp_df.Scene<scene_plotting]
        # print(temp_df.groupby(['Condition', 'Date']).describe(), file=f)  # Python 3.x
        conds=temp_df.Condition.unique()
        # print(temp_df.groupby(['Condition']).describe(), file=f)  # Python 3.x
        conds = temp_df.Condition.unique()
        print('Conditions = ', conds, file=f)
        for temp_var in temp_vars:
            temp_v1=temp_df[temp_df.Condition==conds[0]][temp_var]
            temp_v2 = temp_df[temp_df.Condition == conds[1]][temp_var]
            out=scipy.stats.ttest_ind(temp_v1, temp_v2)
            print(temp_var, file=f)
            print(out, file=f)
            print('Vector lengths', len(temp_v1), len(temp_v2), file=f)
        print('Testing by dates:',file=f)
        for date in temp_df.Date.unique():
            print('Date', date, file=f)
            for temp_var in temp_vars:
                temp_bool=(temp_df.Condition==conds[0])*(temp_df.Date==date)
                temp_v1=temp_df[temp_bool][temp_var]
                temp_bool1 = (temp_df.Condition == conds[1]) * (temp_df.Date == date)
                temp_v2 = temp_df[temp_bool1][temp_var]
                out=scipy.stats.ttest_ind(temp_v1, temp_v2)
                print(temp_var, file=f)
                print(out, file=f)
                print('Conditions', conds,file=f)
                print('Vector lengths', len(temp_v1), len(temp_v2), file=f)
